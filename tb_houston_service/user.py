"""
deployments module
supports all the ReST actions for the
user collection
"""

# 3rd party modules
from pprint import pformat
from flask import make_response, abort

from config import db, app
from tb_houston_service.models import User, UserSchema


def read_all():
    """
    Gets the complete lists of users

    :return:        json string of list of users
    """

    # Create the list of users from our data
    user = db.session.query(User).order_by(User.id).all()
    app.logger.debug(pformat(user))
    # Serialize the data for the response
    user_schema = UserSchema(many=True)
    data = user_schema.dump(user)
    return data, 200


def read_one(oid):
    """
    Responds to a request for /api/user/{oid}.
    with one matching user from users

    :param application:   oid of user to find
    :return:              user matching oid
    """

    user = db.session.query(User).filter(User.id == oid).one_or_none()

    if user is not None:
        # Serialize the data for the response
        user_schema = UserSchema()
        data = user_schema.dump(user)
        return data, 200
    return abort(404, f"User with id {oid} not found")


def create(userDetails):
    """
    Creates a new user in the user list.
    based on the passed in user data

    :param user:  user to create in user structure
    :return:        201 on success, 406 on user exists
    """
    # Remove id as it's created automatically
    if "id" in userDetails:
        del userDetails["id"]
    # Does the user exist already?
    existing_user = (
        db.session.query(User)
        .filter(User.firstName == userDetails["firstName"])
        .filter(User.lastName == userDetails["lastName"])
        .one_or_none()
    )

    if existing_user is None:
        schema = UserSchema()
        if "IsActive" not in userDetails:
            userDetails["isActive"] = 1
        new_user = schema.load(userDetails, session=db.session)
        db.session.add(new_user)
        db.session.commit()

        # Serialize and return the newly created deployment
        # in the response
        data = schema.dump(new_user)

        return data, 201

    # Otherwise, it already exists, that's an error
    return abort(406, "User already exists")


def update(oid, userDetails):
    """
    Updates an existing user in the user list.

    :param id:    oid of the user to update in the user list
    :param user:   user to update
    :return:       updated user
    """

    app.logger.debug(pformat(userDetails))

    if userDetails.get("id") and userDetails.get("id") != oid:
        abort(400, f"Id {oid} mismatch in path and body")

    # Does the user exist in user list?
    existing_user = db.session.query(User).filter(User.id == oid).one_or_none()

    # Does user exist?

    if existing_user is not None:
        schema = UserSchema()
        update_user = schema.load(userDetails, session=db.session)
        update_user.email = userDetails.get('email', existing_user.email)
        update_user.firstName = userDetails.get('firstName', existing_user.firstName)
        update_user.lastName = userDetails.get('lastName', existing_user.lastName)
        update_user.isAdmin = userDetails.get('isAdmin', existing_user.isAdmin)
        update_user.isActive = userDetails.get('isActive', existing_user.isActive)
        update_user.showWelcome = userDetails.get('showWelcome', existing_user.showWelcome)
        db.session.merge(update_user)
        db.session.commit()

        # return the updted user in the response
        data = schema.dump(update_user)
        return data, 200

    # otherwise, nope, deployment doesn't exist, so that's an error
    return abort(404, f"User {oid} not found")


def delete(oid):
    """
    Deletes a user from the users list.

    :param id: oid of the user to delete
    :return:    200 on successful delete, 404 if not found
    """
    # Does the user to delete exist?
    existing_user = db.session.query(User).filter(User.id == oid).one_or_none()

    # if found?
    if existing_user is not None:
        existing_user.isActive = False
        db.session.merge(existing_user)
        db.session.commit()

        return make_response(f"User {oid} successfully deleted", 200)

    # Otherwise, nope, user to delete not found
    return abort(404, f"User {oid} not found")
