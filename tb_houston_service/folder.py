"""
This is the deployments module and supports all the ReST actions for the
folder collection
"""

# 3rd party modules
from pprint import pformat
from flask import make_response, abort
from config import db, app
from tb_houston_service.models import Folder, FolderSchema
from tb_houston_service.DeploymentStatus import DeploymentStatus
from tb_houston_service import lzfolderstructure


APPLICATIONS = "Applications"
BUSINESS_UNIT = "Business Unit"
TEAM = "Team"
SOLUTION = "Solutions"


def read_all():
    """
    Responds to a request for /api/folder
    with the complete lists of Folders

    :return: json string of list of Folders
    """

    # Create the list of Folders from our data
    fdr = db.session.query(Folder).order_by(Folder.id).all()
    app.logger.debug(pformat(fdr))
    # Serialize the data for the response
    folder_schema = FolderSchema(many=True)
    data = folder_schema.dump(fdr)
    app.logger.debug(data)
    return data, 200


def read_one(oid):
    """
    Responds to a request for /api/folder/{id}
    with one matching folder from Folders 

    :param application:   id of folder to find
    :return:              folder matching id
    """

    fdr = db.session.query(Folder).filter(Folder.id == oid).one_or_none()

    if fdr is not None:
        # Serialize the data for the response
        folder_schema = FolderSchema()
        data = folder_schema.dump(fdr)
        app.logger.debug(data)
        return data, 200
    else:
        abort(404, "Folder with id {id} not found".format(id=oid))


def create(folderDetails):
    """
    Creates a new folder in the folder list
    based on the passed in folder data

    :param folder: folder to create in folder structure
    :return:        201 on success, 406 on folder exists
    """
    # Remove id as it's created automatically
    if "id" in folderDetails:
        del folderDetails["id"]

    schema = FolderSchema()
    new_folder = schema.load(folderDetails, session=db.session)
    db.session.add(new_folder)
    db.session.commit()

    # Serialize and return the newly created deployment
    # in the response
    data = schema.dump(new_folder)
    app.logger.debug(data)
    return data, 201


def update(oid, folderDetails):
    """
    Updates an existing folder in the folder list

    :param key:    id of the folder to update in the folder list
    :param folder:   folder to update
    :return:       updated folder.
    """

    app.logger.debug(f"folder::update: oid: {oid} folderDetails: {folderDetails}")

    if folderDetails.get(id, oid) != oid:
        abort(400, f"id mismatch in path and body")

    # Does the folder exist in folder list?
    existing_folder = db.session.query(Folder).filter(Folder.id == oid).one_or_none()

    # Does folder exist?

    if existing_folder is not None:

        schema = FolderSchema()
        update_folder = schema.load(folderDetails, session=db.session)
        update_folder.id = existing_folder.id

        db.session.merge(update_folder)
        db.session.commit()

        # return the updted deployment in the response
        data = schema.dump(update_folder)
        app.logger.debug(data)
        return data, 200

    # otherwise, nope, folder doesn't exist, so that's an error
    else:
        abort(404, f"Folder with id {oid} not found")


def delete(oid):
    """
    Deletes a Folder from the Folder list.

    :param id: id of the Folder to delete
    :return:    200 on successful delete, 404 if not found
    """
    # Does the folder to delete exist?
    existing_folder = db.session.query(Folder).filter(Folder.id == oid).one_or_none()

    # if found?
    if existing_folder is not None:
        db.session.delete(existing_folder)
        db.session.commit()

        return make_response(f"Folder {oid} successfully deleted", 200)

    # Otherwise, nope, folder to delete not found
    else:
        abort(404, f"Folder with id {oid} not found")


def get_folder_meta():
    resp = lzfolderstructure.read()
    app.logger.debug(f"get_folder_meta::resp: {resp}")

    data = {}
    jso = resp[0][0]
    data[jso["name"]] = jso["isActive"]
    jso = jso["children"][0]
    data[jso["name"]] = jso["isActive"]
    jso = jso["children"][0]
    data[jso["name"]] = jso["isActive"]
    jso = jso["children"][0]
    data[jso["name"]] = jso["isActive"]
    folder_meta = [k for k in data if data[k] == True]
    print(f"folder::get_folder_meta: {folder_meta}")
    return folder_meta


def read_or_create_by_parent_folder_id_and_folder_name(parentFolderId, folderName):
    """
    Called by solution_deployment.

    :param application:   solutionId and the folderName
    :return:              parentFolderId, status, taskId
    """

    app.logger.debug(f"parentFolderId: {parentFolderId}, folderName: {folderName}")
    fdr = (
        db.session.query(Folder)
        .filter(
            Folder.parentFolderId == parentFolderId, Folder.folderName == folderName
        )
        .one_or_none()
    )

    if fdr is not None:
        # Serialize the data for the response
        folder_schema = FolderSchema()
        data = folder_schema.dump(fdr)
        app.logger.debug(
            f"folder::read_or_create_by_parent_folder_id_and_folder_name: {data}"
        )
        return data, 200
    else:
        folderDetails = {
            "parentFolderId": parentFolderId,
            "folderId": None,
            "folderName": folderName,
            "status": DeploymentStatus.PENDING,
            "taskId": None,
        }
        return create(folderDetails)
