"""
This is the activator module and supports all the ReST actions for the
activators collection
"""

# 3rd party modules
from flask import make_response, abort
import logging
import json
from pprint import pformat
from sqlalchemy import literal_column


from config import db
from tb_houston_service.models import Activator, ActivatorSchema
from tb_houston_service.models import User
from tb_houston_service.tools import ModelTools
from tb_houston_service.extendedSchemas import ExtendedActivatorPatchedSchema
from tb_houston_service.extendedSchemas import ExtendedActivatorCategorySchema
from tb_houston_service.extendedSchemas import ExtendedUserSchema
from tb_houston_service import activator_extension


logger = logging.getLogger("tb_houston_service.activator")


def expand_access_requested_by_patch(act):
    # update accessRequestedBy, this need refactoring and done properly, see comment above.
    auser = db.session.query(User).filter(act['accessRequestedBy'] == User.id).one_or_none()
    logger.debug("auser: %s", auser)
    if auser:
        user_schema = ExtendedUserSchema()
        user_data = user_schema.dump(auser)
        act['accessRequestedBy'] = user_data
    else:
        act['accessRequestedBy'] = None
    return act


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

    logger.debug("Parameters: isActive: %s, isFavourite: %s, category: %s, status: %s, environment: %s, platform: %s, type: %s, source: %s, sensitivity: %s, page: %s, page_size: %s, sort: %s",
     isActive, isFavourite, category, status, environment, platform, type, source, sensitivity, page, page_size, sort)

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
        except Exception as e:
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


    # This is a better way of doing it, but doesn't work because we can't assign an object 
    #  to accessRequested because it's an integer 
    # for act in activators:
    #     act = activator_extension.expand_activator(act)
    # Serialize the data for the response

    activator_schema = ExtendedActivatorPatchedSchema(many=True)
    data = activator_schema.dump(activators)

    for act in data:
        act = expand_access_requested_by_patch(act)


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

    act = db.session.query(Activator).filter(
        Activator.id == oid
    ).one_or_none()

    if act is not None:
        # Should be expected here, but because we're changing the type of accessRequestedBy from integer to an object,
        # The SQLAlchemy complains with: "_mysql_connector.MySQLInterfaceError: Python type User cannot be converted"
        # act = activator_extension.expand_activator(act)
        # Serialize the data for the response
        schema = ExtendedActivatorPatchedSchema(many=False)
        data = schema.dump(act)
        data = expand_access_requested_by_patch(data)
                
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

    # Remove id as it's created automatically
    if "id" in activatorDetails:
        del activatorDetails["id"]

    schema = ActivatorSchema()
    new_activator = schema.load(activatorDetails, session=db.session)
    db.session.add(new_activator)
    db.session.commit()

    # Serialize and return the newly created deployment
    # in the response
    schema = ExtendedActivatorPatchedSchema(many=False)
    data = schema.dump(new_activator)
    data = expand_access_requested_by_patch(data)
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

    # Does the activators exist in activators list?
    existing_activator = (
        db.session.query(Activator).filter(Activator.id == oid).one_or_none()
    )

    # Does activator exist?

    if existing_activator is not None:
        # schema = ActivatorSchema()
        activatorDetails["id"] = oid
        logger.info("activatorDetails: %s", activatorDetails)
        schema = ActivatorSchema(many=False, session=db.session)
        updatedActivator = schema.load(activatorDetails)
        logger.info("updatedActivator: %s", updatedActivator)
        db.session.merge(updatedActivator)
        db.session.commit()
        # return the updated activator in the response
        schema = ExtendedActivatorPatchedSchema(many=False)
        data = schema.dump(updatedActivator)
        data = expand_access_requested_by_patch(data)
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
    # Does the activator to delete exist?
    existing_activator = (
        db.session.query(Activator).filter(Activator.id == oid).one_or_none()
    )

    # if found?
    if existing_activator is not None:
        existing_activator.isActive = False
        db.session.merge(existing_activator)
        db.session.commit()

        return make_response(f"Activator id {oid} successfully deleted", 200)

    # Otherwise, nope, activator to delete not found
    else:
        abort(404, f"Activator id {oid} not found")


def setActivatorStatus(activatorDetails):
    """
    Update the activator status.
    : return:      The activator that was changed
    """

    logger.info(pformat(activatorDetails))
    # Does the activator to delete exist?
    existing_activator = (
        db.session.query(Activator)
        .filter(Activator.id == activatorDetails["id"], Activator.isActive)
        .one_or_none()
    )

    # if found?
    if existing_activator is not None:
        existing_activator.status = activatorDetails.get(
            "status", existing_activator.status
        )
        existing_activator.accessRequestedBy = activatorDetails.get(
            "accessRequestedBy", existing_activator.accessRequestedBy
        )
        existing_activator.lastUpdated = ModelTools.get_utc_timestamp()

        db.session.merge(existing_activator)
        db.session.commit()

        activator = activator_extension.expand_activator(existing_activator)
        activator_schema = ExtendedActivatorPatchedSchema()
        data = activator_schema.dump(activator)
        data = expand_access_requested_by_patch(data)
        return data, 200

    # Otherwise, nope, activator to update was not found
    else:
        db.session.close()
        actid = activatorDetails["id"]
        abort(404, f"Activator id {actid} not found")


def categories():
    """
    :return:        distinct list of activator categories.
    """

    sql = "select category from activator group by category"
    rs = db.session.execute(sql)
    categories_arr = []
    for row in rs:
        categories_arr.append({"category": row["category"]})

    schema = ExtendedActivatorCategorySchema(many=True)
    data = schema.dump(categories_arr)
    db.session.close()
    return data, 200