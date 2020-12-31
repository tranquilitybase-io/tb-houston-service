import logging

from flask import abort
from sqlalchemy import literal_column
from sqlalchemy.exc import SQLAlchemyError

from config.db_lib import db_session
from models import (
    Activator,
    Application,
    Notification,
    NotificationActivator,
    NotificationActivatorSchema,
    NotificationApplicationDeployment,
    NotificationApplicationDeploymentSchema,
    NotificationSchema,
    NotificationSolutionDeployment,
    NotificationSolutionDeploymentSchema,
    NotificationTeam,
    NotificationTeamSchema,
    NotificationType,
    Solution,
    Team,
)
from tb_houston_service import security
from tb_houston_service.extendedSchemas import ExtendedNotificationSchema
from tb_houston_service.tools import ModelTools

logger = logging.getLogger("tb_houston_service.notification")


def read_all(
    typeId=None, isRead=None, isActive=None, page=None, page_size=None, sort=None
):
    logger.debug("read_all: %s", typeId)
    with db_session() as dbs:
        # pre-process sort instructions
        if sort == None:
            notifications_query = dbs.query(Notification).order_by(
                Notification.lastUpdated + " desc"
            )
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
                notifications_query = dbs.query(Notification).order_by(
                    Notification.lastUpdated + " desc"
                )

        user = security.get_valid_user_from_token(dbsession=dbs)
        if not user:
            abort(404, "No valid user found!")
        toUserId = user.id
        notifications_query = notifications_query.filter(
            (typeId == None or Notification.typeId == typeId),
            (toUserId == None or Notification.toUserId == toUserId),
            (isRead == None or Notification.isRead == isRead),
            (isActive == None or Notification.isActive == isActive),
        )

        # do limit and offset last
        if page == None or page_size == None:
            notifications = notifications_query.all()
        else:
            notifications = notifications_query.limit(page_size).offset(
                page * page_size
            )

        for n in notifications:
            n.type = (
                dbs.query(NotificationType)
                .filter(NotificationType.id == n.typeId)
                .one_or_none()
            )
            if n.typeId == 1:
                n.details = (
                    dbs.query(NotificationActivator)
                    .filter(
                        n.id == NotificationActivator.notificationId,
                        Activator.id == NotificationActivator.activatorId,
                    )
                    .one_or_none()
                )
            elif n.typeId == 2:
                n.details = (
                    dbs.query(NotificationTeam)
                    .filter(
                        n.id == NotificationTeam.notificationId,
                        Team.id == NotificationTeam.teamId,
                    )
                    .one_or_none()
                )
            elif n.typeId == 3:
                n.details = (
                    dbs.query(NotificationApplicationDeployment)
                    .filter(
                        n.id == NotificationApplicationDeployment.notificationId,
                        Application.id
                        == NotificationApplicationDeployment.applicationId,
                    )
                    .one_or_none()
                )
            elif n.typeId == 4:
                n.details = (
                    dbs.query(NotificationSolutionDeployment)
                    .filter(
                        n.id == NotificationSolutionDeployment.notificationId,
                        Solution.id == NotificationSolutionDeployment.solutionId,
                    )
                    .one_or_none()
                )
        schema = ExtendedNotificationSchema(many=True)
        data = schema.dump(notifications)
        return data, 200


def create(notification, typeId, dbsession):
    # if id is zero or None (null), we create a a new notification otherwise
    #  we update an existing notification.
    oid = notification.get("id", None)
    logger.debug("oid: %s", oid)
    notification["typeId"] = typeId
    notification["lastUpdated"] = ModelTools.get_utc_timestamp()
    logger.debug("create notification: %s", notification)

    if not oid:
        # Insert
        if notification.get("isActive", None) == None:
            notification["isActive"] = True
        if notification.get("isRead", None) == None:
            notification["isRead"] = False
        if notification.get("typeId") == 1:
            tmp_notification = {}
            tmp_notification["typeId"] = notification.get("typeId")
            tmp_notification["message"] = notification.get("message")
            tmp_notification["isActive"] = notification.get("isActive", True)
            tmp_notification["isRead"] = notification.get("isRead")
            tmp_notification["importance"] = notification.get("importance")
            tmp_notification["toUserId"] = notification.get("toUserId")
            tmp_notification["fromUserId"] = notification.get("fromUserId")
            tmp_notification["lastUpdated"] = ModelTools.get_utc_timestamp()
            aSchema = NotificationSchema()
            new_notification = aSchema.load(tmp_notification, session=dbsession)
            dbsession.add(new_notification)
            dbsession.flush()
            naSchema = NotificationActivatorSchema()
            notificationActivator = {}
            notificationActivator["notificationId"] = new_notification.id
            notificationActivator["activatorId"] = notification.get("activatorId")
            notificationActivator["lastUpdated"] = ModelTools.get_utc_timestamp()
            notificationActivator["isActive"] = notification.get("isActive", True)
            logger.debug("notificationActivator: %s", notificationActivator)
            new_na = naSchema.load(notificationActivator, session=dbsession)
            dbsession.add(new_na)
        elif notification.get("typeId") == 2:
            tmp_notification = {}
            tmp_notification["typeId"] = notification.get("typeId")
            tmp_notification["message"] = notification.get("message")
            tmp_notification["isActive"] = notification.get("isActive", True)
            tmp_notification["isRead"] = notification.get("isRead")
            tmp_notification["importance"] = notification.get("importance")
            tmp_notification["toUserId"] = notification.get("toUserId")
            tmp_notification["fromUserId"] = notification.get("fromUserId")
            tmp_notification["lastUpdated"] = ModelTools.get_utc_timestamp()
            aSchema = NotificationSchema()
            new_notification = aSchema.load(tmp_notification, session=dbsession)
            dbsession.add(new_notification)
            dbsession.flush()
            naSchema = NotificationTeamSchema()
            notificationTeam = {}
            notificationTeam["notificationId"] = new_notification.id
            notificationTeam["teamId"] = notification.get("teamId")
            notificationTeam["lastUpdated"] = ModelTools.get_utc_timestamp()
            notificationTeam["isActive"] = notification.get("isActive", True)
            new_na = naSchema.load(notificationTeam, session=dbsession)
            dbsession.add(new_na)
        elif notification.get("typeId") == 3:
            tmp_notification = {}
            tmp_notification["typeId"] = notification.get("typeId")
            tmp_notification["message"] = notification.get("message")
            tmp_notification["isActive"] = notification.get("isActive", True)
            tmp_notification["isRead"] = notification.get("isRead")
            tmp_notification["importance"] = notification.get("importance")
            tmp_notification["toUserId"] = notification.get("toUserId")
            tmp_notification["fromUserId"] = notification.get("fromUserId")
            tmp_notification["lastUpdated"] = ModelTools.get_utc_timestamp()
            aSchema = NotificationSchema()
            new_notification = aSchema.load(tmp_notification, session=dbsession)
            dbsession.add(new_notification)
            dbsession.flush()
            nadSchema = NotificationApplicationDeploymentSchema()
            notificationApplicationDeployment = {}
            notificationApplicationDeployment["notificationId"] = new_notification.id
            notificationApplicationDeployment["applicationId"] = notification.get(
                "applicationId"
            )
            notificationApplicationDeployment[
                "lastUpdated"
            ] = ModelTools.get_utc_timestamp()
            notificationApplicationDeployment["isActive"] = notification.get(
                "isActive", True
            )
            new_na = nadSchema.load(
                notificationApplicationDeployment, session=dbsession
            )
            dbsession.add(new_na)
        elif notification.get("typeId") == 4:
            tmp_notification = {}
            tmp_notification["typeId"] = notification.get("typeId")
            tmp_notification["message"] = notification.get("message")
            tmp_notification["isActive"] = notification.get("isActive", True)
            tmp_notification["isRead"] = notification.get("isRead")
            tmp_notification["importance"] = notification.get("importance")
            tmp_notification["toUserId"] = notification.get("toUserId")
            tmp_notification["fromUserId"] = notification.get("fromUserId")
            tmp_notification["lastUpdated"] = ModelTools.get_utc_timestamp()
            aSchema = NotificationSchema()
            new_notification = aSchema.load(tmp_notification, session=dbsession)
            dbsession.add(new_notification)
            dbsession.flush()
            nsdSchema = NotificationSolutionDeploymentSchema()
            notificationSolutionDeployment = {}
            notificationSolutionDeployment["notificationId"] = new_notification.id
            notificationSolutionDeployment["solutionId"] = notification.get(
                "solutionId"
            )
            notificationSolutionDeployment[
                "lastUpdated"
            ] = ModelTools.get_utc_timestamp()
            notificationSolutionDeployment["isActive"] = notification.get(
                "isActive", True
            )
            new_na = nsdSchema.load(notificationSolutionDeployment, session=dbsession)
            dbsession.add(new_na)
        else:
            logger.error(
                "Unknown notification type, the transaction will be rolled back for this notification!"
            )
            dbsession.rollback()
    else:
        # Update
        aSchema = NotificationSchema()
        if notification.get("typeId") == 1:
            notification.pop("typeId")
            updated_notification = aSchema.load(notification, session=dbsession)
            dbsession.merge(updated_notification)
            dbsession.flush()
            notificationActivator = (
                dbsession.query(NotificationActivator)
                .filter(NotificationActivator.notificationId == updated_notification.id)
                .one()
            )
            notificationActivator.lastUpdated = ModelTools.get_utc_timestamp()
            notificationActivator.isActive = notification.get(
                "isActive", notificationActivator.isActive
            )
            dbsession.merge(notificationActivator)
        elif notification.get("typeId") == 2:
            notification.pop("typeId")
            updated_notification = aSchema.load(notification, session=dbsession)
            dbsession.merge(updated_notification)
            dbsession.flush()
            notificationTeam = (
                dbsession.query(NotificationTeam)
                .filter(NotificationTeam.notificationId == updated_notification.id)
                .one()
            )
            notificationTeam.lastUpdated = ModelTools.get_utc_timestamp()
            notificationTeam.isActive = notification.get(
                "isActive", notificationTeam.isActive
            )
            dbsession.merge(notificationTeam)
        elif notification.get("typeId") == 3:
            notification.pop("typeId")
            updated_notification = aSchema.load(notification, session=dbsession)
            dbsession.merge(updated_notification)
            dbsession.flush()
            notificationApplicationDeployment = (
                dbsession.query(NotificationApplicationDeployment)
                .filter(
                    NotificationApplicationDeployment.notificationId
                    == updated_notification.id
                )
                .one()
            )
            notificationApplicationDeployment.lastUpdated = (
                ModelTools.get_utc_timestamp()
            )
            notificationApplicationDeployment.isActive = notification.get(
                "isActive", notificationApplicationDeployment.isActive
            )
            dbsession.merge(notificationApplicationDeployment)
        elif notification.get("typeId") == 4:
            notification.pop("typeId")
            updated_notification = aSchema.load(notification, session=dbsession)
            dbsession.merge(updated_notification)
            dbsession.flush()
            notificationSolutionDeployment = (
                dbsession.query(NotificationSolutionDeployment)
                .filter(
                    NotificationSolutionDeployment.notificationId
                    == updated_notification.id
                )
                .one()
            )
            notificationSolutionDeployment.lastUpdated = ModelTools.get_utc_timestamp()
            notificationSolutionDeployment.isActive = notification.get(
                "isActive", notificationSolutionDeployment.isActive
            )
            dbsession.merge(notificationSolutionDeployment)
        else:
            logger.error(
                "typeId is missing, the transaction will be rolled back for this notification!"
            )
            dbsession.rollback()
    logger.debug("processed: %s", notification)
    return notification


def create_all(
    notificationListDetails,
    typeId,
    isRead=None,
    isActive=None,
    page=None,
    page_size=None,
    sort=None,
):
    logger.debug("create_all: %s", notificationListDetails)
    with db_session() as dbs:
        for n in notificationListDetails:
            create(n, typeId, dbsession=dbs)

    (data, resp_code) = read_all(
        typeId=typeId,
        isRead=isRead,
        isActive=isActive,
        page=page,
        page_size=page_size,
        sort=sort,
    )
    logger.debug("data: %s, resp_code: %s", data, resp_code)
    return data, 201


def meta(typeId=None, isRead=None, isActive=None):
    """
    Responds to a request for /api/notificationsMeta/.

    :param activator:
    :return:              total count of notifications
    """
    with db_session() as dbs:
        user = security.get_valid_user_from_token(dbsession=dbs)
        if not user:
            abort(404, "No valid user found!")
        toUserId = user.id
        count = (
            dbs.query(Notification)
            .filter(
                (typeId == None or Notification.typeId == typeId),
                (toUserId == None or Notification.toUserId == toUserId),
                (isRead == None or Notification.isRead == isRead),
                (isActive == None or Notification.isActive == isActive),
            )
            .count()
        )
        data = {"count": count}
        return data, 200


# service functions
def delete(oid, dbsession):
    logger.debug("delete: %s", oid)
    na = (
        dbsession.query(NotificationActivator)
        .filter(
            NotificationActivator.notificationId == oid, NotificationActivator.isActive
        )
        .one_or_none()
    )
    if na:
        na.isActive = False
        na.lastUpdated = ModelTools.get_utc_timestamp()

    nt = (
        dbsession.query(NotificationTeam)
        .filter(NotificationTeam.notificationId == oid, NotificationTeam.isActive)
        .one_or_none()
    )
    if nt:
        nt.isActive = False
        nt.lastUpdated = ModelTools.get_utc_timestamp()

    nad = (
        dbsession.query(NotificationApplicationDeployment)
        .filter(
            NotificationApplicationDeployment.notificationId == oid,
            NotificationApplicationDeployment.isActive,
        )
        .one_or_none()
    )
    if nt:
        nad.isActive = False
        nad.lastUpdated = ModelTools.get_utc_timestamp()

    nsd = (
        dbsession.query(NotificationSolutionDeployment)
        .filter(
            NotificationSolutionDeployment.notificationId == oid,
            NotificationSolutionDeployment.isActive,
        )
        .one_or_none()
    )
    if nt:
        nsd.isActive = False
        nsd.lastUpdated = ModelTools.get_utc_timestamp()

    n = (
        dbsession.query(Notification)
        .filter(Notification.id == oid, Notification.isActive)
        .one_or_none()
    )
    if n:
        n.isActive = False
        n.lastUpdated = ModelTools.get_utc_timestamp()


def dismiss(
    fromUserId,
    dbsession,
    activatorId=None,
    teamId=None,
    applicationId=None,
    solutionId=None,
):
    if activatorId:
        ns = (
            dbsession.query(Notification)
            .filter(
                NotificationActivator.notificationId == Notification.id,
                NotificationActivator.isActive,
                Notification.isActive,
                Notification.fromUserId == fromUserId,
            )
            .all()
        )
        for n in ns:
            delete(n.id, dbsession)
    if teamId:
        n = (
            dbsession.query(Notification)
            .filter(
                NotificationTeam.teamId == Notification.id,
                NotificationTeam.isActive,
                Notification.isActive,
                Notification.fromUserId == fromUserId,
            )
            .all()
        )
        for n in ns:
            delete(n.id, dbsession)
    if applicationId:
        n = (
            dbsession.query(Notification)
            .filter(
                NotificationApplicationDeployment.teamId == Notification.id,
                NotificationApplicationDeployment.isActive,
                Notification.isActive,
                Notification.fromUserId == fromUserId,
            )
            .all()
        )
        for n in ns:
            delete(n.id, dbsession)
    if solutionId:
        n = (
            dbsession.query(Notification)
            .filter(
                NotificationSolutionDeployment.teamId == Notification.id,
                NotificationSolutionDeployment.isActive,
                Notification.isActive,
                Notification.fromUserId == fromUserId,
            )
            .all()
        )
        for n in ns:
            delete(n.id, dbsession)
