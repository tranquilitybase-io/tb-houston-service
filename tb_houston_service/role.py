"""
deployments module
supports all the ReST actions for the
role collection
"""

# 3rd party modules
from pprint import pformat
from flask import make_response, abort
from config import db, app
from tb_houston_service.models import Role, RoleSchema


def read_all():
    """
    Responds to a request for /api/role.
    with the complete lists of roles
    :return:        json string of list of roles.
    """

    # Create the list of roles from our data
    role = db.session.query(Role).order_by(Role.id).all()
    app.logger.debug(pformat(role))
    # Serialize the data for the response
    role_schema = RoleSchema(many=True)
    data = role_schema.dump(role)
    return data


def read_one(id):
    """
    Responds to a request for /api/role/{id}.
    with one matching role from roles
    :param application:   id of role to find
    :return:              role matching id.
    """

    role = db.session.query(Role).filter(Role.id == id).one_or_none()

    if role is not None:
        # Serialize the data for the response
        role_schema = RoleSchema()
        data = role_schema.dump(role)
        return data
    else:
        abort(404, "Role with id {id} not found".format(id=id))


def create(roleDetails):
    """
    Creates a new role in the role list.
    based on the passed in role data
    :param role:  role to create in role structure
    :return:        201 on success, 406 on role exists.
    """

   # Remove id as it's created automatically
    if 'id' in roleDetails:
        del roleDetails['id']    

    schema = RoleSchema()
    new_role = schema.load(roleDetails, session=db.session)
    db.session.add(new_role)
    db.session.commit()

    data = schema.dump(new_role)
    return data, 201



def update(id, roleDetails):
    """
    Updates an existing role in the role list.
    :param id:    id of the role to update in the role list
    :param role:   role to update
    :return:       updated role.
    """

    app.logger.debug(pformat(roleDetails))

    if roleDetails["id"] != id:
        abort(400, f"Id mismatch in path and body")

    # Does the role exist in role list?
    existing_role = db.session.query(Role).filter(Role.id == id).one_or_none()

    # Does role exist?

    if existing_role is not None:
        schema = RoleSchema()
        update_role = schema.load(roleDetails, session=db.session)
        update_role.id = roleDetails["id"]

        db.session.merge(update_role)
        db.session.commit()

        # return the updted role in the response
        data = schema.dump(update_role)
        return data, 200

    # otherwise, nope, deployment doesn't exist, so that's an error
    else:
        abort(404, f"Role {id} not found")


def delete(id):
    """
    Deletes a role from the roles list.
    :param id: id of the role to delete
    :return:    200 on successful delete, 404 if not found.
    """
    # Does the role to delete exist?
    existing_role = db.session.query(Role).filter(Role.id == id).one_or_none()

    # if found?
    if existing_role is not None:
        db.session.delete(existing_role)
        db.session.commit()

        return make_response(f"Role {id} successfully deleted", 200)

    # Otherwise, nope, role to delete not found
    else:
        abort(404, f"Role {id} not found")