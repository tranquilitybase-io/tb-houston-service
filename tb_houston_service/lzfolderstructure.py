"""
This is the deployments module and supports all the ReST actions for the
Landing Zone folder structure collection
"""
import json
import logging
from pprint import pformat

from config import db
from models import LZFolderStructure, LZFolderStructureChild
from tb_houston_service.extendedSchemas import ExtendedLZMetadataFSApplicationSchema

logger = logging.getLogger("tb_houston_service.lzFolderStructure")

# At time of writing max number of levels is ten
max_levels = 10


def add_folders(folders):
    for folder in folders:
        children = folder.get("children")
        if children:
            for child in children:
                fs = (
                    db.session.query(LZFolderStructure)
                    .filter(LZFolderStructure.id == folder["id"])
                    .one_or_none()
                )
                if fs:
                    fs.name = folder["name"]
                    fs.isActive = folder["isActive"]
                    db.session.merge(fs)
                else:
                    fs = LZFolderStructure(
                        id=folder["id"],
                        name=folder["name"],
                        isActive=folder["isActive"],
                    )
                    db.session.add(fs)

                fsc = (
                    db.session.query(LZFolderStructureChild)
                    .filter(
                        LZFolderStructureChild.folderId == folder["id"],
                        LZFolderStructureChild.childId == child["id"],
                    )
                    .one_or_none()
                )
                if fsc:
                    fsc.folderId = folder["id"]
                    fsc.childId = child["id"]
                    db.session.merge(fsc)
                else:
                    fsc = LZFolderStructureChild(
                        folderId=folder["id"], childId=child["id"]
                    )
                    db.session.add(fsc)
            add_folders(children)
        else:
            fs = (
                db.session.query(LZFolderStructure)
                .filter(LZFolderStructure.id == folder["id"])
                .one_or_none()
            )
            if fs:
                fs.name = folder["name"]
                fs.isActive = folder["isActive"]
                db.session.merge(fs)
            else:
                fs = LZFolderStructure(
                    id=folder["id"], name=folder["name"], isActive=folder["isActive"]
                )
                db.session.add(fs)

            fsc = (
                db.session.query(LZFolderStructureChild)
                .filter(
                    LZFolderStructureChild.folderId == folder["id"],
                    LZFolderStructureChild.childId == None,
                )
                .one_or_none()
            )
            if fsc:
                fsc.folderId = folder["id"]
                fsc.childId = None
                db.session.merge(fsc)
            else:
                fsc = LZFolderStructureChild(folderId=folder["id"], childId=None)
                db.session.add(fsc)


def read():
    """
    This function responds to a request for /api/lzfolderstructure
    with the complete lists of Folder Structure relationships

    :return:        json string of list of Folder Structure
    """
    schema = ExtendedLZMetadataFSApplicationSchema(many=True)
    fss = (
        db.session.query(LZFolderStructure).order_by(LZFolderStructure.id.desc()).all()
    )

    children = None
    fs = None
    for fs in fss:
        print(f"Processing {fs.name} *****")
        for fs_1 in (
            db.session.query(LZFolderStructure)
            .filter(
                LZFolderStructureChild.folderId == fs.id,
                LZFolderStructure.id == LZFolderStructureChild.childId,
            )
            .order_by(LZFolderStructure.id.desc())
            .all()
        ):
            if children:
                children = [
                    {
                        "id": fs_1.id,
                        "name": fs_1.name,
                        "isActive": fs_1.isActive,
                        "children": children,
                    }
                ]
            else:
                children = [
                    {"id": fs_1.id, "name": fs_1.name, "isActive": fs_1.isActive}
                ]

            print(f"children: {children}")

    folder_structure = [
        {"id": fs.id, "name": fs.name, "isActive": fs.isActive, "children": children}
    ]
    data = schema.dump(folder_structure)
    print(f"fs: {json.dumps(data, indent=4)}")
    return data, 200


def create(lzFolderStructureDetails):
    """
    This function updates folder structure relationships.

    :param folder structure details:  folder structure to update
    :return:       updated folder structure
    """
    logger.debug("create_all: %s", pformat(lzFolderStructureDetails))

    try:
        add_folders(lzFolderStructureDetails)
        db.session.commit()
    except:
        db.session.rollback()
        raise
    finally:
        db.session.close()
    resp = read()
    return resp[0], 201
