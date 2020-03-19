"""
This is the landingZoneProgressitem module and supports all the ReST actions for the
landingZoneProgressitem collection
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
    This function responds to a request for /api/landingZoneProgressitems
    with the complete lists of landingZoneProgressitems

    :return:        json string of list of landingZoneProgressitems
    """

    # Create the list of people from our data
    landingZoneProgressitems = LandingZoneProgressItem.query.all()
    modifiedLandingZoneProgressItems = apply_state_transition(landingZoneProgressitems)

    # Serialize the data for the response
    landingZoneProgressitem_schema = LandingZoneProgressItemSchema(many=True)
    data = landingZoneProgressitem_schema.dump(modifiedLandingZoneProgressItems)
    app.logger.debug("landingZoneProgressitem data:")
    app.logger.debug(pformat(data))
    return data


def read_one(id):
    """
    This function responds to a request for /api/landingZoneProgressitem/{id}
    with one matching landingZoneProgressitem from landingZoneProgressitems

    :param landingZoneProgressitem:   id of the landingZoneProgressitem to find
    :return:              landingZoneProgressitem matching the id
    """

    landingZoneProgressitem = (LandingZoneProgressItem.query.filter(LandingZoneProgressItem.id == id).one_or_none())

    if landingZoneProgressitem is not None:
        # Serialize the data for the response
        landingZoneProgressitem_schema = LandingZoneProgressItemSchema()
        data = landingZoneProgressitem_schema.dump(landingZoneProgressitem)
        app.logger.debug("landingZoneProgressitem data:")
        app.logger.debug(pformat(data))
        return data
    else:
        abort(
            404, "LandingZoneProgressItem with id {id} not found".format(id=id)
        )


def create(landingZoneProgressitem):
    """
    This function creates a new landingZoneProgressitem in the landingZoneProgressitem structure
    based on the passed in landingZoneProgressitem data

    :param landingZoneProgressitem:  landingZoneProgressitem to create in landingZoneProgressitem list
    :return:             201 on success, 406 on landingZoneProgressitem exists
    """

    schema = LandingZoneProgressItemSchema()
    new_landingZoneProgressitem = schema.load(landingZoneProgressitem, session=db.session)
    db.session.add(new_landingZoneProgressitem)
    db.session.commit()

    # Serialize and return the newly created landingZoneProgressitem
    # in the response
    data = schema.dump(new_landingZoneProgressitem)
    app.logger.debug("landingZoneProgressitem data:")
    app.logger.debug(pformat(data))

    return data, 201


def update(id, landingZoneProgressitem):
    """
    This function updates an existing landingZoneProgressitem in the landingZoneProgressitem list

    :param id: id of the landingZoneProgressitem to update in the landingZoneProgressitem list
    :param landingZoneProgressitem:   landingZoneProgressitem to update
    :return: updated landingZoneProgressitem
    """

    app.logger.debug("landingZoneProgressitem: ")
    app.logger.debug(pformat(landingZoneProgressitem))

    # Does the landingZoneProgressitem exist in landingZoneProgressitems?
    existing_landingZoneProgressitem = LandingZoneProgressItem.query.filter(LandingZoneProgressItem.id == id).one_or_none()

    # Does landingZoneProgressitem exist?
    if existing_landingZoneProgressitem is not None:
        schema = LandingZoneProgressItemSchema()
        update_landingZoneProgressitem = schema.load(landingZoneProgressitem, session=db.session)
        update_landingZoneProgressitem.id = id

        db.session.merge(update_landingZoneProgressitem)
        db.session.commit()

        # return the updated landingZoneProgressitem in the response
        data = schema.dump(update_landingZoneProgressitem)
        app.logger.debug("landingZoneProgressitem data:")
        app.logger.debug(pformat(data))
        return data, 200

    # otherwise, nope, landingZoneProgressitem doesn't exist, so that's an error
    else:
        abort(404, f"LandingZoneProgressItem not found")


def delete(id):
    """
    This function deletes an landingZoneProgressitem from the landingZoneProgressitem list

    :param id: id of the landingZoneProgressitem to delete
    :return:             200 on successful delete, 404 if not found
    """
    # Does the landingZoneProgressitem to delete exist?
    existing_landingZoneProgressitem = LandingZoneProgressItem.query.filter(LandingZoneProgressItem.id == id).one_or_none()

    # if found?
    if existing_landingZoneProgressitem is not None:
        db.session.delete(existing_landingZoneProgressitem)
        db.session.commit()

        return make_response(f"LandingZoneProgressItem id {id} successfully deleted", 200)

    # Otherwise, nope, landingZoneProgressitem to delete not found
    else:
        abort(404, f"LandingZoneProgressItem id {id} not found")


