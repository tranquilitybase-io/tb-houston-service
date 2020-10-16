"""
Deployments module, supports all the ReST actions for the
cd collection
"""
from pprint import pformat
from flask import make_response, abort

from config import db, app
from models import CD, CDSchema

def read_all():
    """
    Responds to a request for /api/cd
    with the complete lists of CDs

    :return:        json string of list of CDs
    """
    # Create the list of CDs from our data
    cd = db.session.query(CD).order_by(CD.id).all()
    app.logger.debug(pformat(cd))
    # Serialize the data for the response
    cd_schema = CDSchema(many=True)
    data = cd_schema.dump(cd)
    return data

def read_keyValues():
    """
    This function responds to a request for /keyValues/cd
    with the complete lists of CDs 

    :return:        json string of list of CDs 
    """
    # Create the list of CDs from our data
    cd = db.session.query(CD).order_by(CD.id).all()
    app.logger.debug(pformat(cd))
    # Serialize the data for the response
    cd_schema = CDSchema(many=True)
    data = cd_schema.dump(cd)
    keyValues = []
    for d in data:
        keyValuePair = {}
        keyValuePair["key"] = d.get("id")
        keyValuePair["value"] = d.get("value")
        keyValues.append(keyValuePair)
    print(keyValues)
    return keyValues

def read_one(id):
    """
    This function responds to a request for /api/cd/{id}
    with one matching cd from CDs 

    :param application:   id of cd to find
    :return:              cd matching id
    """
    cd = db.session.query(CD).filter(CD.id == id).one_or_none()

    if cd is not None:
        # Serialize the data for the response
        cd_schema = CDSchema()
        data = cd_schema.dump(cd)
        return data
    else:
        abort(404, "CD with id {id} not found".format(id=id))

def create(cdDetails):
    """
    This function creates a new cd in the cd list
    based on the passed in cd data

    :param cd: cd to create in cd structure
    :return:        201 on success, 406 on cd exists
    """
    # Remove id as it's created automatically
    if 'id' in cdDetails:
        del cdDetails['id']
    # Does the cd exist already?
    existing_cd = db.session.query(CD).filter(CD.value == cdDetails["value"]).one_or_none()

    if existing_cd is None:
        schema = CDSchema()
        new_cd = schema.load(cdDetails, session=db.session)
        db.session.add(new_cd)
        db.session.commit()

        # Serialize and return the newly created deployment
        # in the response
        data = schema.dump(new_cd)

        return data, 201

    # Otherwise, it already exists, that's an error
    else:
        abort(406, f"CD already exists")

def update(id, cdDetails):
    """
    This function updates an existing cd in the cd list

    :param key:    id of the cd to update in the cd list
    :param cd:   cd to update
    :return:       updated cd
    """
    app.logger.debug(pformat(cdDetails))

    if cdDetails["id"] != id:
        abort(400, f"Id mismatch in path and body")

    # Does the cd exist in cd list?
    existing_cd = db.session.query(CD).filter(CD.id == id).one_or_none()

    # Does cd exist?

    if existing_cd is not None:
        schema = CDSchema()
        update_cd = schema.load(cdDetails, session=db.session)
        update_cd.id = cdDetails["id"]

        db.session.merge(update_cd)
        db.session.commit()

        # return the updted cd in the response
        data = schema.dump(update_cd)
        return data, 200

    # otherwise, nope, deployment doesn't exist, so that's an error
    else:
        abort(404, f"CD not found")

def delete(id):
    """
    This function deletes a CD from the CD list

    :param key: id of the CD to delete
    :return:    200 on successful delete, 404 if not found
    """
    # Does the cd to delete exist?
    existing_cd = db.session.query(CD).filter(CD.id == id).one_or_none()

    # if found?
    if existing_cd is not None:
        db.session.delete(existing_cd)
        db.session.commit()

        return make_response(f"CD {id} successfully deleted", 200)

    # Otherwise, nope, cd to delete not found
    else:
        abort(404, f"CD {id} not found")
