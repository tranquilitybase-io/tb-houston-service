"""
This is the deployments module and supports all the ReST actions for the
ci collection
"""

# 3rd party modules
from flask import make_response, abort
from config import db, app
from models import CI, CISchema
from pprint import pformat


def read_all():
    """
    This function responds to a request for /api/ci
    with the complete lists of CIs 

    :return:        json string of list of CIs 
    """

    # Create the list of CIs from our data
    ci = CI.query.order_by(CI.key).all()
    app.logger.debug(pformat(ci))
    # Serialize the data for the response
    ci_schema = CISchema(many=True)
    data = ci_schema.dump(ci)
    return data


def read_one(key):
    """
    This function responds to a request for /api/ci/{key}
    with one matching ci from CIs 

    :param application:   key of ci to find
    :return:              ci matching key
    """

    ci = (CI.query.filter(CI.key == key).one_or_none())

    if ci is not None:
        # Serialize the data for the response
        ci_schema = CISchema()
        data = ci_schema.dump(ci)
        return data
    else:
        abort(
            404, "CI with key {key} not found".format(key=key)
        )


def create(ciDetails):
    """
    This function creates a new ci in the ci list
    based on the passed in ci data

    :param ci: ci to create in ci structure
    :return:        201 on success, 406 on ci exists
    """
    key = ciDetails.get("key", None)
    value = ciDetails.get("value", None)

    # Does the ci exist already?
    existing_ci = (
        CI.query.filter(CI.key == key).one_or_none()
    )

    if existing_ci is None:
        schema = CISchema()
        new_ci = schema.load(ciDetails, session=db.session)
        db.session.add(new_ci)
        db.session.commit()

        # Serialize and return the newly created deployment
        # in the response
        data = schema.dump(new_ci)

        return data, 201

    # Otherwise, it already exists, that's an error
    else:
        abort(406, f"CI already exists")


def update(key, ciDetails):
    """
    This function updates an existing ci in the ci list

    :param key:    key of the ci to update in the ci list
    :param ci:   ci to update
    :return:       updated ci
    """

    app.logger.debug(pformat(ciDetails))

    if ciDetails["key"] != key:
           abort(400, f"Key mismatch in path and body")

    # Does the ci exist in ci list?
    existing_ci = CI.query.filter(
            CI.key == key
    ).one_or_none()

    # Does ci exist?

    if existing_ci is not None:
        schema = CISchema()
        update_ci = schema.load(ciDetails, session=db.session)
        update_ci.key = ciDetails['key']

        db.session.merge(update_ci)
        db.session.commit()

        # return the updted ci in the response
        data = schema.dump(update_ci)
        return data, 200

    # otherwise, nope, deployment doesn't exist, so that's an error
    else:
        abort(404, f"CI not found")


def delete(key):
    """
    This function deletes a CI from the CI list

    :param key: key of the CI to delete
    :return:    200 on successful delete, 404 if not found
    """
    # Does the ci to delete exist?
    existing_ci = CI.query.filter(CI.key == key).one_or_none()

    # if found?
    if existing_ci is not None:
        db.session.delete(existing_ci)
        db.session.commit()

        return make_response(f"CI {key} successfully deleted", 200)

    # Otherwise, nope, ci to delete not found
    else:
        abort(404, f"CI {key} not found")


