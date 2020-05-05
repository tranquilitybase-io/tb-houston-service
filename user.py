"""
deployments module
supports all the ReST actions for the
user collection
"""

# 3rd party modules
from flask import make_response, abort
from config import db, app
from models import User, UserSchema
from pprint import pformat


def read_all():
    """
    Gets the complete lists of users

    :return:        json string of list of users
    """

    # Create the list of users from our data
    user = User.query.order_by(User.id).all()
    app.logger.debug(pformat(user))
    # Serialize the data for the response
    user_schema = UserSchema(many=True)
    data = user_schema.dump(user)
    return data


def read_one(id):
    """
    This function responds to a request for /api/user/{id}
    with one matching user from users

    :param application:   id of user to find
    :return:              user matching id
    """

    user = (User.query.filter(User.id == id).one_or_none())


    if user is not None:
        # Serialize the data for the response
        user_schema = UserSchema()
        data = user_schema.dump(user)
        return data
    else:
        abort(
            404, "User with id {id} not found".format(id=id)
        )


def create(userDetails):
    """
    This function creates a new user in the user list
    based on the passed in user data

    :param user:  user to create in user structure
    :return:        201 on success, 406 on user exists
    """
    # Remove id as it's created automatically
    if 'id' in userDetails:
        del userDetails['id']
    # Does the user exist already?
    existing_user = (
        User.query.filter(User.firstName == userDetails['firstName']).filter(User.lastName == userDetails['lastName']).one_or_none()
    )

    if existing_user is None:
        schema = UserSchema()
        new_user = schema.load(userDetails, session=db.session)
        db.session.add(new_user)
        db.session.commit()

        # Serialize and return the newly created deployment
        # in the response
        data = schema.dump(new_user)

        return data, 201

    # Otherwise, it already exists, that's an error
    else:
        abort(406, f"User already exists")


def update(id, userDetails):
    """
    This function updates an existing user in the user list

    :param id:    id of the user to update in the user list
    :param user:   user to update
    :return:       updated user
    """

    app.logger.debug(pformat(userDetails))

    if userDetails["id"] != int(id):
           abort(400, f"Id mismatch in path and body")

    # Does the user exist in user list?
    existing_user = User.query.filter(
            User.id == id
    ).one_or_none()

    # Does user exist?

    if existing_user is not None:
        schema = UserSchema()
        update_user = schema.load(userDetails, session=db.session)
        update_user.id = userDetails['id']

        db.session.merge(update_user)
        db.session.commit()

        # return the updted user in the response
        data = schema.dump(update_user)
        return data, 200

    # otherwise, nope, deployment doesn't exist, so that's an error
    else:
        abort(404, f"User not found")


def delete(id):
    """
    This function deletes a user from the users list

    :param id: id of the user to delete
    :return:    200 on successful delete, 404 if not found
    """
    # Does the user to delete exist?
    existing_user = User.query.filter(User.id == id).one_or_none()

    # if found?
    if existing_user is not None:
        db.session.delete(existing_user)
        db.session.commit()

        return make_response(f"User {id} successfully deleted", 200)

    # Otherwise, nope, user to delete not found
    else:
        abort(404, f"User {id} not found")


