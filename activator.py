"""
This is the activator module and supports all the ReST actions for the
activators collection
"""

# 3rd party modules
from flask import make_response, abort
from config import db, app
from models import Activator
from models import ActivatorSchema
from models import ModelTools
from extendedSchemas import ExtendedActivatorSchema
from extendedSchemas import ExtendedActivatorCategorySchema
import activator_extension
import json
from pprint import pformat
from sqlalchemy import literal_column


def read_all(category=None, status=None, environment=None,
        platform=None, type=None, source=None,
        sensitivity=None, page=None, page_size=None, sort=None):
    """
    This function responds to a request for /api/activators
    with the complete lists of activators

    :return:        json string of list of activators
    """

    # Create the list of activators from our data

    # pre-process sort instructions
    if (sort==None):
        activator_query = Activator.query.order_by(Activator.id)
    else:
        try:
            sort_inst = [ si.split(":") for si in sort ]
            orderby_arr = []
            for si in sort_inst:
                si1 = si[0]
                if len(si) > 1:
                    si2 = si[1]
                else:
                    si2 = "asc"
                orderby_arr.append(f"{si1} {si2}")
            #print("orderby: {}".format(orderby_arr))
            activator_query = Activator.query.order_by(literal_column(", ".join(orderby_arr)))
        except Exception as e:
            print(e)
            activator_query = Activator.query.order_by(Activator.id)

    activator_query = activator_query.filter(
      (category==None or Activator.category==category),
      (status==None or Activator.status==status),
      (environment==None or Activator.envs.like("%\"{}\"%".format(environment))),
      (platform==None or Activator.platforms.like("%\"{}\"%".format(platform))),
      (type==None or Activator.type==type),
      (source==None or Activator.sourceControl.like("%\"{}\"%".format(source))),
      (sensitivity==None or Activator.sensitivity==sensitivity)
    )

    if (page==None or page_size==None):
      activators = activator_query.all()
    else:
      activators = activator_query.limit(page_size).offset(page * page_size).all()

    activators_arr = []
    for act in activators:
        activators_arr.append(activator_extension.build_activator(act))

    # Serialize the data for the response
    activator_schema = ExtendedActivatorSchema(many=True)
    data = activator_schema.dump(activators_arr)
    app.logger.debug("read_all")
    app.logger.debug(pformat(data))
    return data, 200


def read_one(oid):
    """
    This function responds to a request for /api/activator/{key}
    with one matching activator from activatorss

    :param application:   key of activator to find
    :return:              activator matching key
    """

    act = (Activator.query.filter(Activator.id == oid).one_or_none())

    if act is not None:
        # Serialize the data for the response
        activator = activator_extension.build_activator(act)
        activator_schema = ExtendedActivatorSchema(many=False)
        data = activator_schema.dump(activator)
        return data, 200
    else:
        abort(
            404, f"Activator with id {oid} not found".format(id=oid)
        )


def create(activatorDetails):
    """
    This function creates a new activator in the activator list
    based on the passed in activator data

    :param activator:  activator to create in activator list
    :return:        201 on success, 406 on activator exists
    """

    # Remove id as it's created automatically
    if 'id' in activatorDetails:
        del activatorDetails['id']

    activatorDetails['accessRequestedBy'] = activatorDetails.get('accessRequestedBy', 0)
    activatorDetails['ci'] = json.dumps(activatorDetails.get('ci', []))
    activatorDetails['cd'] = json.dumps(activatorDetails.get('cd', []))
    activatorDetails['hosting'] = json.dumps(activatorDetails.get('hosting', []))
    activatorDetails['envs'] = json.dumps(activatorDetails.get('envs', []))
    activatorDetails['sourceControl'] = json.dumps(activatorDetails.get('sourceControl', []))
    activatorDetails['regions'] = json.dumps(activatorDetails.get('regions', []))
    activatorDetails['apiManagement'] = json.dumps(activatorDetails.get('apiManagement', []))
    activatorDetails['platforms'] = json.dumps(activatorDetails.get('platforms', []))

    schema = ActivatorSchema()
    new_activator = schema.load(activatorDetails, session=db.session)
    new_activator.lastUpdated = ModelTools.get_utc_timestamp()

    db.session.add(new_activator)
    db.session.commit()

    # Serialize and return the newly created deployment
    # in the response

    new_activator.ci = json.loads(new_activator.ci or '[]')
    new_activator.cd = json.loads(new_activator.cd or '[]')
    new_activator.hosting = json.loads(new_activator.hosting or '[]')
    new_activator.envs = json.loads(new_activator.envs or '[]')
    new_activator.sourceControl = json.loads(new_activator.sourceControl or '[]')
    new_activator.regions = json.loads(new_activator.regions or '[]')
    new_activator.apiManagement = json.loads(new_activator.apiManagement or '[]')
    new_activator.platforms = json.loads(new_activator.platforms or '[]')

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

    app.logger.debug("update")
    app.logger.debug("id")
    app.logger.debug(oid)
    app.logger.debug("activator")
    app.logger.debug(pformat(activatorDetails))

    if 'id' in activatorDetails and activatorDetails['id'] != oid:
      abort(400, f"Key mismatch in path and body")

    # Does the activators exist in activators list?
    existing_activator = Activator.query.filter(Activator.id == oid).one_or_none()

    # Does activator exist?

    if existing_activator is not None:
        #schema = ActivatorSchema()
        activatorDetails['lastUpdated'] = ModelTools.get_utc_timestamp()
        activatorDetails['accessRequestedBy'] = activatorDetails.get('accessRequestedBy', existing_activator.accessRequestedBy)
        activatorDetails["ci"] = json.dumps(activatorDetails.get("ci", existing_activator.ci))
        activatorDetails["cd"] = json.dumps(activatorDetails.get("cd", existing_activator.cd))
        activatorDetails["hosting"] = json.dumps(activatorDetails.get("hosting", existing_activator.hosting))
        activatorDetails["envs"] = json.dumps(activatorDetails.get("envs", existing_activator.envs))
        activatorDetails["sourceControl"] = json.dumps(activatorDetails.get("sourceControl", existing_activator.sourceControl))
        activatorDetails["regions"] = json.dumps(activatorDetails.get("regions", existing_activator.regions))
        activatorDetails["apiManagement"] = json.dumps(activatorDetails.get("apiManagement", existing_activator.apiManagement))
        activatorDetails["platforms"] = json.dumps(activatorDetails.get("platforms", existing_activator.platforms))
        Activator.query.filter(Activator.id == oid).update(activatorDetails)
        db.session.commit()
        # return the updated activator in the response
        return read_one(oid)
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
    existing_activator = Activator.query.filter(Activator.id == oid).one_or_none()

    # if found?
    if existing_activator is not None:
        db.session.delete(existing_activator)
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

    app.logger.info(pformat(activatorDetails))
    # Does the activator to delete exist?
    existing_activator = Activator.query.filter(Activator.id == activatorDetails['id']).one_or_none()

    # if found?
    if existing_activator is not None:
        existing_activator.status = activatorDetails.get('status', existing_activator.status)
        existing_activator.accessRequestedBy = activatorDetails.get('accessRequestedBy', existing_activator.accessRequestedBy)
        existing_activator.lastUpdated = ModelTools.get_utc_timestamp()

        db.session.merge(existing_activator)
        db.session.commit()

        activator = activator_extension.build_activator(existing_activator)
        activator_schema = ExtendedActivatorSchema()
        data = activator_schema.dump(activator)
        return data, 200

    # Otherwise, nope, activator to update was not found
    else:
        actid = activatorDetails['id']
        abort(404, f"Activator id {actid} not found")


def categories():
    """
    :return:        distinct list of activator categories.
    """

    sql = "select category from activator group by category"
    rs = db.session.execute(sql)
    categories_arr = []
    for row in rs:
        categories_arr.append({ "category": row['category'] })

    schema = ExtendedActivatorCategorySchema(many=True)
    data = schema.dump(categories_arr)
    return data, 200
