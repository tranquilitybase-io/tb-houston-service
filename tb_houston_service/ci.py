"""
This is the deployments module and supports all the ReST actions for the
ci collection
"""
from pprint import pformat

from flask import abort, make_response

from config import app, db
from models import CI, CISchema


def read_all():
    """
    This function responds to a request for /api/ci
    with the complete lists of CIs

    :return:        json string of list of CIs
    """
    # Create the list of CIs from our data
    ci = db.session.query(CI).order_by(CI.id).all()
    app.logger.debug(pformat(ci))
    # Serialize the data for the response
    ci_schema = CISchema(many=True)
    data = ci_schema.dump(ci)
    return data


def read_one(id):
    """
    This function responds to a request for /ci/{id}
    with one matching ci from CIs

    :param application:   id of ci to find
    :return:              ci matching id
    """
    ci = db.session.query(CI).filter(CI.id == id).one_or_none()

    if ci is not None:
        # Serialize the data for the response
        ci_schema = CISchema()
        data = ci_schema.dump(ci)
        return data
    else:
        abort(404, "CI with id {id} not found".format(id=id))


def read_keyValues():
    """
    This function responds to a request for /keyValues/ci
    with the complete lists of CIs

    :return:        json string of list of CIs
    """
    # Create the list of CIs from our data
    ci = db.session.query(CI).order_by(CI.id).all()
    app.logger.debug(pformat(ci))
    # Serialize the data for the response
    ci_schema = CISchema(many=True)
    data = ci_schema.dump(ci)
    keyValues = []
    for d in data:
        keyValuePair = {}
        keyValuePair["key"] = d.get("id")
        keyValuePair["value"] = d.get("value")
        keyValues.append(keyValuePair)
    print(keyValues)
    return keyValues


def create(ciDetails):
    """
    This function creates a new ci in the ci list
    based on the passed in ci data

    :param ci: ci to create in ci structure
    :return:        201 on success, 406 on ci exists
    """
    # Remove id as it's created automatically
    if "id" in ciDetails:
        del ciDetails["id"]
    # Does the ci exist already?
    existing_ci = (
        db.session.query(CI).filter(CI.value == ciDetails["value"]).one_or_none()
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
        abort(406, "CI already exists")


def update(id, ciDetails):
    """
    This function updates an existing ci in the ci list

    :param id:    id of the ci to update in the ci list
    :param ci:   ci to update
    :return:       updated ci
    """
    app.logger.debug(pformat(ciDetails))

    if ciDetails["id"] != id:
        abort(400, "Key mismatch in path and body")

    # Does the ci exist in ci list?
    existing_ci = db.session.query(CI).filter(CI.id == id).one_or_none()

    # Does ci exist?

    if existing_ci is not None:
        schema = CISchema()
        update_ci = schema.load(ciDetails, session=db.session)
        update_ci.id = ciDetails["id"]

        db.session.merge(update_ci)
        db.session.commit()

        # return the updted ci in the response
        data = schema.dump(update_ci)
        return data, 200

    # otherwise, nope, deployment doesn't exist, so that's an error
    else:
        abort(404, "CI not found")


def delete(id):
    """
    This function deletes a CI from the CI list

    :param id: id of the CI to delete
    :return:    200 on successful delete, 404 if not found
    """
    # Does the ci to delete exist?
    existing_ci = db.session.query(CI).filter(CI.id == id).one_or_none()

    # if found?
    if existing_ci is not None:
        db.session.delete(existing_ci)
        db.session.commit()

        return make_response(f"CI {id} successfully deleted", 200)

    # Otherwise, nope, ci to delete not found
    else:
        abort(404, f"CI {id} not found")
