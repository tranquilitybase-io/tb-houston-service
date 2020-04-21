"""
This is the deployments module and supports all the ReST actions for the
environment collection
"""

# 3rd party modules
from flask import make_response, abort
from config import db, app
from models import Environment, EnvironmentSchema
from pprint import pformat


def read_all():
    """
    This function responds to a request for /api/environment
    with the complete lists of environments

    :return:        json string of list of environments
    """

    # Create the list of environments from our data
    environment = Environment.query.order_by(Environment.key).all()
    app.logger.debug(pformat(environment))
    # Serialize the data for the response
    environment_schema = EnvironmentSchema(many=True)
    data = environment_schema.dump(environment)
    return data


def read_one(key):
    """
    This function responds to a request for /api/environment/{key}
    with one matching environment from environments

    :param application:   key of environment to find
    :return:              environment matching key
    """

    environment = (Environment.query.filter(Environment.key == key).one_or_none())

    if environment is not None:
        # Serialize the data for the response
        environment_schema = EnvironmentSchema()
        data = environment_schema.dump(environment)
        return data
    else:
        abort(
            404, "Environment with key {key} not found".format(key=key)
        )


def create(environmentDetails):
    """
    This function creates a new environment in the environment list
    based on the passed in environment data

    :param environment:  environment to create in environment structure
    :return:        201 on success, 406 on environment exists
    """
    key = environmentDetails.get("key", None)

    # Does the environment exist already?
    existing_environment = (
        Environment.query.filter(Environment.key == key).one_or_none()
    )

    if existing_environment is None:
        schema = EnvironmentSchema()
        new_environment = schema.load(environmentDetails, session=db.session)
        db.session.add(new_environment)
        db.session.commit()

        # Serialize and return the newly created deployment
        # in the response
        data = schema.dump(new_environment)

        return data, 201

    # Otherwise, it already exists, that's an error
    else:
        abort(406, f"Environment already exists")


def update(key, environmentDetails):
    """
    This function updates an existing environment in the environment list

    :param key:    key of the environment to update in the environment list
    :param environment:   environment to update
    :return:       updated environment
    """

    app.logger.debug(pformat(environmentDetails))

    if environmentDetails["key"] != key:
           abort(400, f"Key mismatch in path and body")
 
    # Does the environment exist in environment list?
    existing_environment = Environment.query.filter(
            Environment.key == key
    ).one_or_none()

    # Does environment exist?

    if existing_environment is not None:
        schema = EnvironmentSchema()
        update_environment = schema.load(environmentDetails, session=db.session)
        update_environment.key = environmentDetails['key']

        db.session.merge(update_environment)
        db.session.commit()

        # return the updted environment in the response
        data = schema.dump(update_environment)
        return data, 200

    # otherwise, nope, deployment doesn't exist, so that's an error
    else:
        abort(404, f"Environment not found")


def delete(key):
    """
    Deletes an environment from the environments list.

    :param key: key of the environment to delete
    :return:    200 on successful delete, 404 if not found
    """
    # Does the environment to delete exist?
    existing_environment = Environment.query.filter(Environment.key == key).one_or_none()

    # if found?
    if existing_environment is not None:
        db.session.delete(existing_environment)
        db.session.commit()

        return make_response(f"Environment {key} successfully deleted", 200)

    # Otherwise, nope, environment to delete not found
    else:
        abort(404, f"Environment {key} not found")


