"""
Deployments module, supports all the ReST actions for the
cd collection
"""

# 3rd party modules
from pprint import pformat
from flask import make_response, abort
from config import db, app
from tb_houston_service.models import CD, CDSchema


def read_all():
    """
    Responds to a request for /api/cd
    with the complete lists of CDs

    :return:        json string of list of CDs
    """

    # Create the list of CDs from our data
    cd = db.session.query(CD).order_by(CD.key).all()
    app.logger.debug(pformat(cd))
    # Serialize the data for the response
    cd_schema = CDSchema(many=True)
    data = cd_schema.dump(cd)
    return data


def read_one(key):
    """
    This function responds to a request for /api/cd/{key}
    with one matching cd from CDs 

    :param application:   key of cd to find
    :return:              cd matching key
    """

    cd = db.session.query(CD).filter(CD.key == key).one_or_none()

    if cd is not None:
        # Serialize the data for the response
        cd_schema = CDSchema()
        data = cd_schema.dump(cd)
        return data
    else:
        abort(404, "CD with key {key} not found".format(key=key))


def create(cdDetails):
    """
    This function creates a new cd in the cd list
    based on the passed in cd data

    :param cd: cd to create in cd structure
    :return:        201 on success, 406 on cd exists
    """
    key = cdDetails.get("key", None)

    # Does the cd exist already?
    existing_cd = db.session.query(CD).filter(CD.key == key).one_or_none()

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


def update(key, cdDetails):
    """
    This function updates an existing cd in the cd list

    :param key:    key of the cd to update in the cd list
    :param cd:   cd to update
    :return:       updated cd
    """

    app.logger.debug(pformat(cdDetails))

    if cdDetails["key"] != key:
        abort(400, f"Key mismatch in path and body")

    # Does the cd exist in cd list?
    existing_cd = db.session.query(CD).filter(CD.key == key).one_or_none()

    # Does cd exist?

    if existing_cd is not None:
        schema = CDSchema()
        update_cd = schema.load(cdDetails, session=db.session)
        update_cd.key = cdDetails["key"]

        db.session.merge(update_cd)
        db.session.commit()

        # return the updted cd in the response
        data = schema.dump(update_cd)
        return data, 200

    # otherwise, nope, deployment doesn't exist, so that's an error
    else:
        abort(404, f"CD not found")


def delete(key):
    """
    This function deletes a CD from the CD list

    :param key: key of the CD to delete
    :return:    200 on successful delete, 404 if not found
    """
    # Does the cd to delete exist?
    existing_cd = db.session.query(CD).filter(CD.key == key).one_or_none()

    # if found?
    if existing_cd is not None:
        db.session.delete(existing_cd)
        db.session.commit()

        return make_response(f"CD {key} successfully deleted", 200)

    # Otherwise, nope, cd to delete not found
    else:
        abort(404, f"CD {key} not found")
