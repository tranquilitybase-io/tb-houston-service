"""
deployments module
supports all the ReST actions for the
team collection
"""

# 3rd party modules
from pprint import pformat
from flask import make_response, abort
from sqlalchemy import literal_column

from config import db, app
from tb_houston_service.models import UserCloudRole, UserCloudRoleSchema
from tb_houston_service.extendedSchemas import ExtendedUserCloudRoleSchema
from tb_houston_service.userCloudRole_extension import expand_user_cloud_role


def read_all(
    userId=None, cloudRoleId=None, active=None, page=None, page_size=None, sort=None
):
    """
    Gets the complete lists of user roles
    Responds to a request for /api/userCloudRole

    :return:        json string of list of user roles
    """

    # Create the list of user roles from our data
    # pre-process sort instructions

    if sort == None:
        userCloudRole_query = db.session.query(UserCloudRole).order_by(UserCloudRole.id)

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
            userCloudRole_query = db.session.query(UserCloudRole).order_by(
                literal_column(", ".join(orderby_arr))
            )
        except Exception as e:
            print(e)
            userCloudRole_query = db.session.query(UserCloudRole).order_by(UserCloudRole.id)

    userCloudRole_query = userCloudRole_query.filter(
        (userId == None or UserCloudRole.userId == userId),
        (cloudRoleId == None or UserCloudRole.cloudRoleId == cloudRoleId),
        (active == None or UserCloudRole.isActive == active),
    )

    if page == None or page_size == None:
        userCloudRoles = userCloudRole_query.all()
    else:
        userCloudRoles = userCloudRole_query.limit(page_size).offset(page * page_size).all()

    # Serialize the data for the response
    for ur in userCloudRoles:
        expand_user_cloud_role(ur)
    userCloudRole_schema = ExtendedUserCloudRoleSchema(many=True)
    data = userCloudRole_schema.dump(userCloudRoles)
    app.logger.debug("user roles data:")
    app.logger.debug(pformat(data))
    return data


def read_one(oid):
    """
    Responds to a request for /api/userCloudRole/{oid}
    with one matching user-role from user-roles

    :param application:   key of user-role to find
    :return:              user-role matching key.
    """

    userCloudRole = db.session.query(UserCloudRole).filter(UserCloudRole.id == oid).one_or_none()

    if userCloudRole is not None:
        # Serialize the data for the response
        expand_user_cloud_role(userCloudRole)
        userCloudRole_schema = ExtendedUserCloudRoleSchema(many=False)
        data = userCloudRole_schema.dump(userCloudRole)
        return data
    else:
        abort(404, f"User Role with id {oid} not found")


def create(userCloudRoleDetails):
    """
    Creates a new user-role relationship 
    based on the passed in user and role data

    :param team:  team to create in team structure
    :return:        201 on success, 406 on user-role combination exists already.
    """
    # Remove id as it's created automatically
    if "id" in userCloudRoleDetails:
        del userCloudRoleDetails["id"]

    # Does the user role exist already?
    existing_user_role = (
        db.session.query(UserCloudRole)
        .filter(UserCloudRole.userId == userCloudRoleDetails["userId"])
        .filter(UserCloudRole.cloudRoleId == userCloudRoleDetails["cloudRoleId"])
        .one_or_none()
    )

    if existing_user_role is None:
        schema = UserCloudRoleSchema()
        new_user_role = schema.load(userCloudRoleDetails, session=db.session)
        db.session.add(new_user_role)
        db.session.commit()

        # Serialize and return the newly created deployment
        # in the response
        data = schema.dump(new_user_role)

        return data, 201

    # Otherwise, it already exists, that's an error
    else:
        userCloudRoleDetails["id"] = existing_user_role.id
        update(existing_user_role.id, userCloudRoleDetails)


def update(oid, userCloudRoleDetails):
    """
    Updates an existing user role in the user list

    :param id:    id of the role to update in the user list
    :param team:   team to update
    :return:       updated user role.
    """

    app.logger.debug(pformat(userCloudRoleDetails))

    if userCloudRoleDetails["id"] != int(oid):
        abort(400, f"Id mismatch in path and body")

    # Does the user role relationship exist in userCloudRoles list?
    existing_user_role = (
        db.session.query(UserCloudRole).filter(UserCloudRole.id == oid).one_or_none()
    )

    # Does user-role exist?

    if existing_user_role is not None:
        schema = UserCloudRoleSchema()
        update_user_role = schema.load(userCloudRoleDetails, session=db.session)
        update_user_role.id = userCloudRoleDetails["id"]

        db.session.merge(update_user_role)
        db.session.commit()

        # return the updted user role in the response
        data = schema.dump(update_user_role)
        return data, 200

    # otherwise, nope, deployment doesn't exist, so that's an error
    else:
        abort(404, f"User Role not found")


def delete(oid):
    """
    Logical deletes a user role from the user roles list

    :param id: id of the user role to delete
    :return:    200 on successful delete, 404 if not found.
    """
    # Does the user role to delete exist?
    existing_user_role = (
        db.session.query(UserCloudRole).filter(UserCloudRole.id == oid).one_or_none()
    )

    # if found?
    if existing_user_role is not None:
        existing_user_role.isActive = False
        db.session.merge(existing_user_role)
        db.session.commit()

        return make_response(f"User Role {oid} successfully deleted", 200)

    # Otherwise, nope, user role to delete not found
    else:
        abort(404, f"User Role {oid} not found")
