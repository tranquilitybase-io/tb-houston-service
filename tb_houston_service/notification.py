from pprint import pformat
import logging
from sqlalchemy import literal_column
from flask import abort
from sqlalchemy.exc import SQLAlchemyError
from tb_houston_service.models import Notification
from tb_houston_service.models import NotificationSchema
from tb_houston_service.models import NotificationActivator
from tb_houston_service.models import NotificationActivatorSchema
from tb_houston_service.extendedSchemas import ExtendedNotificationActivatorSchema
from config.db_lib import db_session
from tb_houston_service.tools import ModelTools


logger = logging.getLogger("tb_houston_service.notification")


def read_all(typeId, toUserId = None, isRead = None, isActive = None, sort = None):
    logger.debug("read_all: %s", typeId)    
    with db_session() as dbs:
        # pre-process sort instructions
        if sort == None:
            notifications_query = dbs.query(Notification).order_by(Notification.lastUpdated + " desc")
        else:
            try:
                sort_inst = [si.split(":") for si in sort]
                orderby_arr = []
                for si in sort_inst:
                    si1 = si[0]
                    if len(si) > 1:
                        si2 = si[1]
                    else:
                        si2 = "asc"
                    orderby_arr.append(f"{si1} {si2}")
                # print("orderby: {}".format(orderby_arr))
                notifications_query = dbs.query(Notification).order_by(
                    literal_column(", ".join(orderby_arr))
                )
            except SQLAlchemyError as e:
                logger.warning("Exception: %s", e)
                notifications_query = dbs.query(Notification).order_by(Notification.lastUodated + " desc")

        notifications_query = notifications_query.filter(
            (toUserId == None or Notification.toUserId == toUserId),
            (isRead == None or Notification.isRead == isRead),
            (isActive == None or Notification.isActive == isActive)
        )

        notifications = notifications_query.all()

        if typeId == 1:
            for notif in notifications:
                activator_notification = dbs.query(NotificationActivator).filter(NotificationActivator.notificationId == notif.id).one_or_none()
                if activator_notification:
                    notif.activatorId = activator_notification.activatorId
            schema = ExtendedNotificationActivatorSchema(many=True)
            data = schema.dump(notifications)
            return data, 200
        abort("Unknown typeId", 500)



def create(notification, typeId):
    logger.debug("create: %s", notification)
    with db_session() as dbs:
        # if id is zero or None (null), we create a a new notification otherwise
        #  we update an existing notification.
        oid = notification.get("id", None)
        activatorId = notification.pop("activatorId", None)
        notification['typeId'] = typeId        
        notification["lastUpdated"] = ModelTools.get_utc_timestamp()

        if not oid:
            # Insert
            notification.pop('id', None)
            if notification.get('isActive', None) == None:
              notification["isActive"] = True
            if notification.get('isRead', None) == None:
              notification["isRead"] = False            
            aSchema = NotificationSchema()
            new_notification = aSchema.load(notification, session=dbs)
            dbs.add(new_notification)
            dbs.flush()            
            if notification.get("typeId") == 1 and activatorId:
                naSchema = NotificationActivatorSchema()
                notificationActivator = {}
                notificationActivator["notificationId"] = new_notification.id
                notificationActivator["activatorId"] = activatorId   
                notificationActivator["lastUpdated"] = ModelTools.get_utc_timestamp()    
                notificationActivator["isActive"] = notification.get("isActive", True)                                            
                new_na = naSchema.load(notificationActivator, session=dbs)
                dbs.add(new_na)
            else:
                logger.error("typeId or activatorId is missing, the transaction will be rolled back for this notification!")
                dbs.rollback()
        else:
            # Update
            aSchema = NotificationSchema()
            updated_notification = aSchema.load(notification, session=dbs)
            dbs.merge(updated_notification)   
            dbs.flush()
            if notification.get("typeId") == 1:
                naSchema = NotificationActivatorSchema()
                notificationActivator = dbs.query(NotificationActivator).filter(NotificationActivator.notificationId == updated_notification.id).one()
                notificationActivator.lastUpdated = ModelTools.get_utc_timestamp()
                notificationActivator.isActive = notification.get('isActive', True)
                dbs.merge(notificationActivator)
            else:
                logger.error("typeId is missing, the transaction will be rolled back for this notification!")
                dbs.rollback()           
    logger.debug("processed: %s", notification)
    return notification


def create_all(notificationListDetails, typeId, toUserId = None, isRead = None, isActive = None, sort = None):
    logger.debug("create_all: %s", notificationListDetails)    
    for n in notificationListDetails:
        create(n, typeId)

    (data, resp_code) = read_all(typeId, toUserId = toUserId, isRead = isRead, isActive = isActive, sort = sort)
    logger.debug("data: %s, resp_code: %s", data, resp_code)
    return data, 201


