"""
This is the landingZoneProgressItem module and supports all the ReST actions for the
landingZoneProgressItem collection
"""

# System modules
from datetime import datetime

# 3rd party modules
from flask import make_response, abort
from config import db, app
from models import LandingZoneProgressItem, LandingZoneProgressItemSchema
from pprint import pformat


def apply_state_transition(lz_progress_items):
    # If all action locked status are False, set WAN action locked status to True
    # labels: WAN, VPN, Interconnect, Peering, DNS, Directory Services, Internet, SSO, Logging, Billing, Security Centre, Example
    #if (lz_progress_items['label'] == "WAN" and lz_progress_items[':
    # TODO 

    return lz_progress_items

    

def read_all():
    """
    This function responds to a request for /api/landingZoneProgressItems
    with the complete lists of landingZoneProgressItems

    :return:        json string of list of landingZoneProgressItems
    """

    # Create the list of people from our data
    landingZoneProgressItems = LandingZoneProgressItem.query.all()
    modifiedLandingZoneProgressItems = apply_state_transition(landingZoneProgressItems)

    # Serialize the data for the response
    landingZoneProgressItem_schema = LandingZoneProgressItemSchema(many=True)
    data = landingZoneProgressItem_schema.dump(modifiedLandingZoneProgressItems)
    app.logger.debug("landingZoneProgressItem data:")
    app.logger.debug(pformat(data))
    return data


def read_one(id):
    """
    This function responds to a request for /api/landingZoneProgressItem/{id}
    with one matching landingZoneProgressItem from landingZoneProgressItems

    :param landingZoneProgressItem:   id of the landingZoneProgressItem to find
    :return:              landingZoneProgressItem matching the id
    """

    landingZoneProgressItem = (LandingZoneProgressItem.query.filter(LandingZoneProgressItem.id == id).one_or_none())

    if landingZoneProgressItem is not None:
        # Serialize the data for the response
        landingZoneProgressItem_schema = LandingZoneProgressItemSchema()
        data = landingZoneProgressItem_schema.dump(landingZoneProgressItem)
        app.logger.debug("landingZoneProgressItem data:")
        app.logger.debug(pformat(data))
        return data
    else:
        abort(
            404, "LandingZoneProgressItem with id {id} not found".format(id=id)
        )


def create(landingZoneProgressItem):
    """
    This function creates a new landingZoneProgressItem in the landingZoneProgressItem structure
    based on the passed in landingZoneProgressItem data

    :param landingZoneProgressItem:  landingZoneProgressItem to create in landingZoneProgressItem list
    :return:             201 on success, 406 on landingZoneProgressItem exists
    """
  
    # we don't need the id, the is generated automatically on the database
    if ('id' in landingZoneProgressItem):
      del landingZoneProgressItem["id"]

    schema = LandingZoneProgressItemSchema()
    new_landingZoneProgressItem = schema.load(landingZoneProgressItem, session=db.session)
    db.session.add(new_landingZoneProgressItem)
    db.session.commit()

    # Serialize and return the newly created landingZoneProgressItem
    # in the response
    data = schema.dump(new_landingZoneProgressItem)
    app.logger.debug("landingZoneProgressItem data:")
    app.logger.debug(pformat(data))

    return data, 201


def update(id, landingZoneProgressItem):
    """
    This function updates an existing landingZoneProgressItem in the landingZoneProgressItem list

    :param id: id of the landingZoneProgressItem to update in the landingZoneProgressItem list
    :param landingZoneProgressItem:   landingZoneProgressItem to update
    :return: updated landingZoneProgressItem
    """

    app.logger.debug("landingZoneProgressItem: ")
    app.logger.debug(pformat(landingZoneProgressItem))

    app.logger.debug(id)
    app.logger.debug(landingZoneProgressItem["id"])

    if landingZoneProgressItem["id"] != id:
      abort(400, f"Key mismatch in path and body")

    # Does the landingZoneProgressItem exist in landingZoneProgressItems?
    existing_landingZoneProgressItem = LandingZoneProgressItem.query.filter(LandingZoneProgressItem.id == id).one_or_none()

    # Does landingZoneProgressItem exist?
    if existing_landingZoneProgressItem is not None:
        schema = LandingZoneProgressItemSchema()
        update_landingZoneProgressItem = schema.load(landingZoneProgressItem, session=db.session)
        update_landingZoneProgressItem.id = id

        db.session.merge(update_landingZoneProgressItem)
        db.session.commit()

        # return the updated landingZoneProgressItem in the response
        data = schema.dump(update_landingZoneProgressItem)
        app.logger.debug("landingZoneProgressItem data:")
        app.logger.debug(pformat(data))
        return data, 200

    # otherwise, nope, landingZoneProgressItem doesn't exist, so that's an error
    else:
        abort(404, f"LandingZoneProgressItem not found")


def delete(id):
    """
    This function deletes an landingZoneProgressItem from the landingZoneProgressItem list

    :param id: id of the landingZoneProgressItem to delete
    :return:             200 on successful delete, 404 if not found
    """
    # Does the landingZoneProgressItem to delete exist?
    existing_landingZoneProgressItem = LandingZoneProgressItem.query.filter(LandingZoneProgressItem.id == id).one_or_none()

    # if found?
    if existing_landingZoneProgressItem is not None:
        db.session.delete(existing_landingZoneProgressItem)
        db.session.commit()

        return make_response(f"LandingZoneProgressItem id {id} successfully deleted", 200)

    # Otherwise, nope, landingZoneProgressItem to delete not found
    else:
        abort(404, f"LandingZoneProgressItem id {id} not found")


