"""
This is the activator module and supports all the ReST actions for the
activators collection
"""

# 3rd party modules
from flask import make_response, abort
import logging
from pprint import pformat
from sqlalchemy import literal_column
from sqlalchemy.exc import SQLAlchemyError


from config import db
from config.db_lib import db_session
from tb_houston_service.models import Activator, ActivatorSchema
from tb_houston_service.models import User
from tb_houston_service.models import Notification
from tb_houston_service import notification
from tb_houston_service.tools import ModelTools
from tb_houston_service.extendedSchemas import ExtendedActivatorSchema
from tb_houston_service.extendedSchemas import ExtendedActivatorCategorySchema
from tb_houston_service import activator_extension

logger = logging.getLogger("tb_houston_service.activator")


def read_all(
    isActive=None,
    isFavourite=None,
    category=None,
    status=None,
    environment=None,
    platform=None,
    type=None,
    source=None,
    sensitivity=None,
    page=None,
    page_size=None,
    sort=None,
):
    """
    This function responds to a request for /api/activators
    with the complete lists of activators

    :return:        json string of list of activators
    """

    # Create the list of activators from our data

    logger.debug(
        "Parameters: isActive: %s, isFavourite: %s, category: %s, status: %s, environment: %s, platform: %s, type: %s, source: %s, sensitivity: %s, page: %s, page_size: %s, sort: %s",
        isActive,
        isFavourite,
        category,
        status,
        environment,
        platform,
        type,
        source,
        sensitivity,
        page,
        page_size,
        sort,
    )

    with db_session() as dbs:
        # pre-process sort instructions
        if sort == None:
            activator_query = db.session.query(Activator).order_by(Activator.id)
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
                activator_query = db.session.query(Activator).order_by(
                    literal_column(", ".join(orderby_arr))
                )
            except SQLAlchemyError as e:
                logger.warning(e)
                activator_query = db.session.query(Activator).order_by(Activator.id)

    activator_query = activator_query.filter(
        (category == None or Activator.category == category),
        (status == None or Activator.status == status),
        (environment == None or Activator.envs.like('%"{}"%'.format(environment))),
        (platform == None or Activator.platforms.like('%"{}"%'.format(platform))),
        (type == None or Activator.type == type),
        (source == None or Activator.sourceControl.like('%"{}"%'.format(source))),
        (sensitivity == None or Activator.sensitivity == sensitivity),
        (isActive == None or Activator.isActive == isActive),
        (isFavourite == None or Activator.isFavourite == isFavourite),
    )

    if page == None or page_size == None:
        activators = activator_query.all()
    else:
        activators = activator_query.limit(page_size).offset(page * page_size).all()
    # Expand all Activators
    for act in activators:
        act = activator_extension.expand_activator(act, dbs)

    activator_schema = ExtendedActivatorSchema(many=True)
    data = activator_schema.dump(activators)

    logger.debug("read_all")
    logger.debug(pformat(data))
    return data, 200


def read_one(oid):
    """
    This function responds to a request for /api/activator/{key}
    with one matching activator from activatorss

    :param application:   key of activator to find
    :return:              activator matching key
    """
    with db_session() as dbs:

        act = dbs.query(Activator).filter(Activator.id == oid).one_or_none()

        if act is not None:
            # Expand Activator
            act = activator_extension.expand_activator(act, dbs)
            schema = ExtendedActivatorSchema(many=False)
            data = schema.dump(act)
            return data, 200
        else:
            abort(404, f"Activator with id {oid} not found".format(id=oid))


def create(activatorDetails):
    """
    This function creates a new activator in the activator list
    based on the passed in activator data

    :param activator:  activator to create in activator list
    :return:        201 on success, 406 on activator exists
    """
    with db_session() as dbs:
        # Remove id as it's created automatically
        if "id" in activatorDetails:
            del activatorDetails["id"]

        extraFields = activator_extension.refine_activator_details(
            activatorDetails
        )

        schema = ActivatorSchema()
        new_activator = schema.load(activatorDetails, session=dbs)
        dbs.add(new_activator)
        dbs.flush()
        # Create entries into all tables where activator has association
        activator_extension.create_activator_associations(
            extraFields, new_activator, dbs
        )
        # Expand Activator
        new_activator = activator_extension.expand_activator(new_activator, dbs)
        schema = ExtendedActivatorSchema(many=False)
        data = schema.dump(new_activator)
        return data, 201


def update(oid, activatorDetails):
    """
    This function updates an existing activator in the activators list

    :param key:    key of the activator to update in the activators list
    :param activator:   activator to update
    :return:       updated activator
    """

    logger.debug("update")
    logger.debug("id")
    logger.debug(oid)
    logger.debug("activator")
    logger.debug(pformat(activatorDetails))

    if "id" in activatorDetails and activatorDetails["id"] != oid:
        abort(400, "Key mismatch in path and body")

    with db_session() as dbs:
        # Does the activators exist in activators list?
        existing_activator = (
            dbs.query(Activator).filter(Activator.id == oid).one_or_none()
        )

        # Does activator exist?

        if existing_activator is not None:
            # schema = ActivatorSchema()
            activatorDetails["id"] = oid
            logger.info("activatorDetails: %s", activatorDetails)

            extraFields = activator_extension.refine_activator_details(
                activatorDetails
            )

            schema = ActivatorSchema(many=False, session=dbs)
            updatedActivator = schema.load(activatorDetails)
            logger.info("updatedActivator: %s", updatedActivator)
            dbs.merge(updatedActivator)
            # Update CI list in activatorCI table
            # return the updated activator in the response
            dbs.flush()

            activator_extension.create_activator_associations(
                extraFields, updatedActivator, dbs
            )
            # Expand activator
            updatedActivator = activator_extension.expand_activator(updatedActivator, dbs)

            schema = ExtendedActivatorSchema(many=False)
            data = schema.dump(updatedActivator)
            return data, 200
        # otherwise, nope, deployment doesn't exist, so that's an error
        else:
            abort(404, f"Activator id {oid} not found")


def delete(oid):
    """
    This function deletes an activator from the activators list

    :param key: key of the activator to delete
    :return:    200 on successful delete, 404 if not found
    """
    with db_session() as dbs:
        # Does the activator to delete exist?
        existing_activator = (
            dbs.query(Activator).filter(Activator.id == oid).one_or_none()
        )

        # if found?
        if existing_activator is not None:
            existing_activator.isActive = False
            dbs.merge(existing_activator)
            dbs.flush()

            # Delete entires Activator-CI relationship table
            activator_extension.delete_activator_associations(
                existing_activator.id, dbs
            )

            return make_response(f"Activator id {oid} successfully deleted", 200)

            # Otherwise, nope, activator to delete not found
        else:
            abort(404, f"Activator id {oid} not found")


def notify_user(message, activatorId, toUserId, importance=1):
    logger.debug(
        "notify_users fromUserId: %s message: %s activatorId: %s",
        toUserId,
        message,
        activatorId,
    )
    # Notify all user
    with db_session() as dbs:
        # To avoid sending duplicate notifications, send only if no previous active message.
        existing_notifications = (
            dbs.query(Notification)
            .filter(
                Notification.message == message,
                Notification.toUserId == toUserId,
                Notification.isActive,
            )
            .count()
        )
        logger.debug("existing_notifications: %s", existing_notifications)
        if existing_notifications == 0:
            notification_payload = {
                "activatorId": activatorId,
                "message": message,
                "toUserId": toUserId,
                "importance": importance,
            }
            notification.create(notification_payload, typeId=1, dbsession=dbs)
            # Auto-dismiss the previous notification from the user
            notification.dismiss(
                fromUserId=toUserId, activatorId=activatorId, dbsession=dbs
            )


def notify_admins(message, activatorId, fromUserId, importance=1):
    logger.debug(
        "notify_admins fromUserId: %s message: %s activatorId: %s",
        fromUserId,
        message,
        activatorId,
    )
    # Notify all admins
    notification_payload = {
        "activatorId": activatorId,
        "message": message,
        "fromUserId": fromUserId,
        "toUserId": 0,
        "importance": importance,
    }

    # TODO: Send admin notifications to teammember.isTeamAdmin,
    # joining with activator.businessUnitId when that become available.
    with db_session() as dbs:
        admins = dbs.query(User).filter(User.isAdmin, User.isActive).all()
        for admin in admins:
            # To avoid sending duplicate notifications, send only if no previous active message.
            existing_notifications = (
                dbs.query(Notification)
                .filter(
                    Notification.message == message,
                    Notification.toUserId == admin.id,
                    Notification.isActive,
                )
                .count()
            )
            logger.debug("existing_notifications: %s", existing_notifications)
            if existing_notifications == 0:
                notification_payload["toUserId"] = admin.id
                notification.create(notification_payload, typeId=1, dbsession=dbs)
                # Auto-dismiss the previous notification from the user
                # notification.dismiss(fromUserId = fromUserId, activatorId = activatorId, dbsession = dbs)


def setActivatorStatus(activatorDetails):
    """
    Update the activator status.
    : return:      The activator that was changed
    """

    logger.info(pformat(activatorDetails))

    with db_session() as dbs:
        # Does the activator to delete exist?
        existing_activator = (
            dbs.query(Activator)
            .filter(Activator.id == activatorDetails["id"], Activator.isActive)
            .one_or_none()
        )

        # if found?
        if existing_activator is not None:
            schema = ActivatorSchema()
            updated_activator = schema.load(activatorDetails, session=dbs)
            updated_activator.lastUpdated = ModelTools.get_utc_timestamp()
            dbs.merge(updated_activator)
            
            # Expand Activator
            updated_activator = activator_extension.expand_activator(updated_activator, dbs)

            activator_schema = ExtendedActivatorSchema()
            data = activator_schema.dump(updated_activator)

            # Create notifications
            if (
                updated_activator.status != "Available"
                and updated_activator.accessRequestedById
            ):
                full_name = (
                    (updated_activator.accessRequestedBy.firstName or "")
                    + " "
                    + (updated_activator.accessRequestedBy.lastName or "")
                )
                activator_name = (
                    f"Activator {updated_activator.id} ({updated_activator.name})"
                )
                message = f"{full_name} has requested access to {activator_name}"
                notify_admins(
                    message=message,
                    activatorId=updated_activator.id,
                    fromUserId=updated_activator.accessRequestedById,
                )
            elif (
                updated_activator.status == "Available"
                and updated_activator.accessRequestedById
            ):
                activator_name = (
                    f"Activator {updated_activator.id} ({updated_activator.name})"
                )
                message = f"Access to {activator_name} has been granted."
                notify_user(
                    message,
                    activatorId=updated_activator.id,
                    toUserId=updated_activator.accessRequestedById,
                )

            return data, 200

        # Otherwise, nope, activator to update was not found
        else:
            actid = activatorDetails["id"]
            abort(404, f"Activator id {actid} not found")


def categories():
    """
    :return:        distinct list of activator categories.
    """

    with db_session() as dbs:
        sql = "select category from activator group by category"
        rs = dbs.execute(sql)
        categories_arr = []
        for row in rs:
            categories_arr.append({"category": row["category"]})

        schema = ExtendedActivatorCategorySchema(many=True)
        data = schema.dump(categories_arr)
        return data, 200
