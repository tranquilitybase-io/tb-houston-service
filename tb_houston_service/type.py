"""
This is the deployments module and supports all the ReST actions for the
type collection
"""

# 3rd party modules
from flask import make_response, abort
from config import db, app
from tb_houston_service.models import Type, TypeSchema
from pprint import pformat


def read_all():
    """
    This function responds to a request for /api/type
    with the complete lists of Types 

    :return:        json string of list of Types 
    """

    # Create the list of Types from our data
    type = db.session.query(Type).order_by(Type.id).all()
    app.logger.debug(pformat(type))
    # Serialize the data for the response
    type_schema = TypeSchema(many=True)
    data = type_schema.dump(type)
    return data


def read_one(id):
    """
    This function responds to a request for /type/{id}
    with one matching type from Types

    :param application:   id of type to find
    :return:              type matching id
    """

    type = db.session.query(Type).filter(Type.id == id).one_or_none()

    if type is not None:
        # Serialize the data for the response
        type_schema = TypeSchema()
        data = type_schema.dump(type)
        return data
    else:
        abort(404, "Type with id {id} not found".format(id=id))

def read_keyValues():
    """
    This function responds to a request for /keyValues/type
    with the complete lists of Types 

    :return:        json string of list of Types 
    """

    # Create the list of Types from our data
    type = db.session.query(Type).order_by(Type.id).all()
    app.logger.debug(pformat(type))
    # Serialize the data for the response
    type_schema = TypeSchema(many=True)
    data = type_schema.dump(type)
    keyValues = []
    for d in data:
        keyValuePair = {}
        keyValuePair["key"] = d.get("id")
        keyValuePair["value"] = d.get("value")
        keyValues.append(keyValuePair)
    print(keyValues)
    return keyValues



def create(typeDetails):
    """
    This function creates a new type in the type list
    based on the passed in type data

    :param type: type to create in type structure
    :return:        201 on success, 406 on type exists
    """
    # Remove id as it's created automatically
    if 'id' in typeDetails:
        del typeDetails['id']
    # Does the type exist already?
    existing_type = db.session.query(Type).filter(Type.value == typeDetails["value"]).one_or_none()

    if existing_type is None:
        schema = TypeSchema()
        new_type = schema.load(typeDetails, session=db.session)
        db.session.add(new_type)
        db.session.commit()

        # Serialize and return the newly created deployment
        # in the response
        data = schema.dump(new_type)

        return data, 201

    # Otherwise, it already exists, that's an error
    else:
        abort(406, f"Type already exists")


def update(id, typeDetails):
    """
    This function updates an existing type in the type list

    :param id:    id of the type to update in the type list
    :param type:   type to update
    :return:       updated type
    """

    app.logger.debug(pformat(typeDetails))

    if typeDetails["id"] != id:
        abort(400, f"Key mismatch in path and body")

    # Does the type exist in type list?
    existing_type = db.session.query(Type).filter(Type.id == id).one_or_none()

    # Does type exist?

    if existing_type is not None:
        schema = TypeSchema()
        update_type = schema.load(typeDetails, session=db.session)
        update_type.id = typeDetails["id"]

        db.session.merge(update_type)
        db.session.commit()

        # return the updted type in the response
        data = schema.dump(update_type)
        return data, 200

    # otherwise, nope, deployment doesn't exist, so that's an error
    else:
        abort(404, f"Type not found")


def delete(id):
    """
    This function deletes a Type from the Type list

    :param id: id of the Type to delete
    :return:    200 on successful delete, 404 if not found
    """
    # Does the type to delete exist?
    existing_type = db.session.query(Type).filter(Type.id == id).one_or_none()

    # if found?
    if existing_type is not None:
        db.session.delete(existing_type)
        db.session.commit()

        return make_response(f"Type {id} successfully deleted", 200)

    # Otherwise, nope, type to delete not found
    else:
        abort(404, f"Type {id} not found")
