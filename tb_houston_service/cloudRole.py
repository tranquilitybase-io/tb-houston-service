"""
deployments module
supports all the ReST actions for the
cloudRole collection
"""
from pprint import pformat
from flask import make_response, abort

from config import db, app
from models import CloudRole, CloudRoleSchema

def read_all():
    """
    Responds to a request for /api/cloudRole.
    with the complete lists of cloudRoles
    :return:        json string of list of cloudRoles.
    """
    # Create the list of cloudRoles from our data
    cloudRole = db.session.query(CloudRole).order_by(CloudRole.id).all()
    app.logger.debug(pformat(cloudRole))
    # Serialize the data for the response
    cloud_role_schema = CloudRoleSchema(many=True)
    data = cloud_role_schema.dump(cloudRole)
    return data

def read_one(id):
    """
    Responds to a request for /api/cloudRole/{id}.
    with one matching cloudRole from cloudRoles
    :param application:   id of cloudRole to find
    :return:              cloudRole matching id.
    """
    cloudRole = db.session.query(CloudRole).filter(CloudRole.id == id).one_or_none()

    if cloudRole is not None:
        # Serialize the data for the response
        cloud_role_schema = CloudRoleSchema()
        data = cloud_role_schema.dump(cloudRole)
        return data
    else:
        abort(404, "Role with id {id} not found".format(id=id))

def create(cloudRoleDetails):
    """
    Creates a new cloudRole in the cloudRole list.
    based on the passed in cloudRole data
    :param cloudRole:  cloudRole to create in cloudRole structure
    :return:        201 on success, 406 on cloudRole exists.
    """
   # Remove id as it's created automatically
    if 'id' in cloudRoleDetails:
        del cloudRoleDetails['id']    

    schema = CloudRoleSchema()
    new_cloud_role = schema.load(cloudRoleDetails, session=db.session)
    db.session.add(new_cloud_role)
    db.session.commit()

    data = schema.dump(new_cloud_role)
    return data, 201

def update(id, cloudRoleDetails):
    """
    Updates an existing cloudRole in the cloudRole list.
    :param id:    id of the cloudRole to update in the cloudRole list
    :param cloudRole:   cloudRole to update
    :return:       updated cloudRole.
    """
    app.logger.debug(pformat(cloudRoleDetails))

    if cloudRoleDetails["id"] != id:
        abort(400, "id mismatch in path and body")

    # Does the cloudRole exist in cloudRole list?
    existing_cloud_role = db.session.query(CloudRole).filter(CloudRole.id == id).one_or_none()

    # Does cloudRole exist?

    if existing_cloud_role is not None:
        schema = CloudRoleSchema()
        update_cloud_role = schema.load(cloudRoleDetails, session=db.session)
        update_cloud_role.id = cloudRoleDetails["id"]

        db.session.merge(update_cloud_role)
        db.session.commit()

        # return the updted cloudRole in the response
        data = schema.dump(update_cloud_role)
        return data, 200

    # otherwise, nope, deployment doesn't exist, so that's an error
    else:
        abort(404, f"CloudRole {id} not found")

def delete(id):
    """
    Deletes a cloudRole from the cloudRoles list.
    :param id: id of the cloudRole to delete
    :return:    200 on successful delete, 404 if not found.
    """
    # Does the cloudRole to delete exist?
    existing_cloud_role = db.session.query(CloudRole).filter(CloudRole.id == id).one_or_none()

    # if found?
    if existing_cloud_role is not None:
        db.session.delete(existing_cloud_role)
        db.session.commit()

        return make_response(f"CloudRole {id} successfully deleted", 200)

    # Otherwise, nope, cloudRole to delete not found
    else:
        abort(404, f"CloudRole {id} not found")
