"""
This is the landingZoneWAN module and supports all the ReST actions for the
landingZoneWAN collection
"""

# System modules
from datetime import datetime

# 3rd party modules
from flask import make_response, abort, jsonify
from config import db, app
from models import LandingZoneWAN, LandingZoneWANSchema
from extendedSchemas import ExtendedLandingZoneWANSchema
from extendedSchemas import IdSchema
from pprint import pformat
from pprint import pprint
from flatten_json import flatten, unflatten
import json

delimiter = '__'

def read_all():
    """
    This function responds to a request for /api/landingZoneWANs
    with the complete lists of landingZoneWANs

    :return:        json string of list of landingZoneWANs
    """

    # Create the list of people from our data
    landingZoneWANs = LandingZoneWAN.query.all()
    landingZoneWANArr = []
    for lzw in landingZoneWANs:
        landingZoneWANArr.append(unflatten(lzw.__dict__, delimiter))

    # Serialize the data for the response
    eschema = ExtendedLandingZoneWANSchema(many=True)
    data = eschema.dump(landingZoneWANArr)
    app.logger.debug("landingZoneWAN data:")
    app.logger.debug(pformat(data))
    return data


def read_one(id):
    """
    This function responds to a request for /api/landingZoneWAN/{id}
    with one matching landingZoneWAN from landingZoneWANs

    :param landingZoneWAN:   id of the landingZoneWAN to find
    :return:              landingZoneWAN matching the id
    """

    landingZoneWAN = (LandingZoneWAN.query.filter(LandingZoneWAN.id == id).one_or_none())

    if landingZoneWAN is not None:
        # Serialize the data for the response
        landingZoneWAN_schema = ExtendedLandingZoneWANSchema(many=False)
        unflattened_landingZoneWAN = unflatten(landingZoneWAN.__dict__, delimiter)
        data = landingZoneWAN_schema.dump(unflattened_landingZoneWAN)
        app.logger.debug("landingZoneWAN data:")
        app.logger.debug(pformat(data))
        return data
    else:
        abort(
            404, "LandingZoneWAN with id {id} not found".format(id=id)
        )


def create(landingZoneWAN):
    """
    This function creates a new landingZoneWAN in the landingZoneWAN structure
    based on the passed in landingZoneWAN data

    :param landingZoneWAN:  landingZoneWAN to create in landingZoneWAN list
    :return:             201 on success, 406 on landingZoneWAN exists
    """

    # we don't need the id, the is generated automatically on the database
    if ('id' in landingZoneWAN):
      del landingZoneWAN["id"]

    # flatten the python object into a python dictionary
    flattened_landingZoneWAN = flatten(landingZoneWAN, delimiter)
    schema = LandingZoneWANSchema(many=False)
    new_landingZoneWAN = schema.load(flattened_landingZoneWAN, session=db.session)
    # Save python object to the database
    db.session.add(new_landingZoneWAN)
    db.session.commit()

    idSchema = IdSchema(many=False)
    data = idSchema.dump(new_landingZoneWAN)

    app.logger.debug("landingZoneWAN data:")
    app.logger.debug(pformat(data))

    return data, 201


def update(id, landingZoneWAN):
    """
    This function updates an existing landingZoneWAN in the landingZoneWAN list

    :param id: id of the landingZoneWAN to update in the landingZoneWAN list
    :param landingZoneWAN:   landingZoneWAN to update
    :return: updated landingZoneWAN
    """

    app.logger.debug("landingZoneWAN: ")
    app.logger.debug(pformat(landingZoneWAN))

    if landingZoneWAN['id'] != id:
        abort(400, f"Key mismatch in path and body")

    # Does the landingZoneWAN exist in landingZoneWANs?
    existing_landingZoneWAN = LandingZoneWAN.query.filter(LandingZoneWAN.id == id).one_or_none()

    # Does landingZoneWAN exist?
    if existing_landingZoneWAN is not None:
        flattened_landingZoneWAN = flatten(flatten(landingZoneWAN, delimiter))
        existing_landingZoneWAN.googleSession__primaryGcpVpcSubnet = landingZoneWAN.get('googleSession__primaryGcpVpcSubnet', '')
        existing_landingZoneWAN.googleSession__primaryRegion = landingZoneWAN.get('googleSession__primaryRegion', '')
        existing_landingZoneWAN.googleSession__primarySubnetName = landingZoneWAN.get('googleSession__primarySubnetName', '')
        existing_landingZoneWAN.googleSession__secondaryGcpVpcSubnet = landingZoneWAN('googleSession__secondaryGcpVpcSubnet', '')
        existing_landingZoneWAN.googleSession__secondaryRegion = landingZoneWAN('googleSession__secondaryRegion', '')
        existing_landingZoneWAN.googleSession__secondarySubnetName = landingZoneWAN('googleSession__secondarySubnetName', '')
        existing_landingZoneWAN.onPremiseSession__primaryBgpPeer = landingZoneWAN('onPremiseSession__primaryBgpPeer', '')
        existing_landingZoneWAN.onPremiseSession__primaryPeerIp = landingZoneWAN('onPremiseSession__primaryPeerIp', '')
        existing_landingZoneWAN.onPremiseSession__primaryPeerIpSubnet = landingZoneWAN('onPremiseSession__primaryPeerIpSubnet', '')
        existing_landingZoneWAN.onPremiseSession__primarySharedSecret = landingZoneWAN('onPremiseSession__primarySharedSecret', '')
        existing_landingZoneWAN.onPremiseSession__primaryVpnTunnel = landingZoneWAN('onPremiseSession__primaryVpnTunnel', '')
        existing_landingZoneWAN.onPremiseSession__secondaryBgpPeer = landingZoneWAN('onPremiseSession__secondaryBgpPeer', '')
        existing_landingZoneWAN.onPremiseSession__secondaryPeerIp = landingZoneWAN('onPremiseSession__secondaryPeerIp', '')
        existing_landingZoneWAN.onPremiseSession__secondaryPeerIpSubnet = landingZoneWAN('onPremiseSession__secondaryPeerIpSubnet', '')
        existing_landingZoneWAN.onPremiseSession__secondarySharedSecret = landingZoneWAN('onPremiseSession__secondarySharedSecret', '')
        existing_landingZoneWAN.onPremiseSession__secondaryVpnTunnel = landingZoneWAN('onPremiseSession__secondaryVpnTunnel', '')
        existing_landingZoneWAN.onPremiseSession__vendor = landingZoneWAN('onPremiseSession__vendor', '')
        existing_landingZoneWAN.vpn__bgpInterfaceNetLength = landingZoneWAN('vpn__bgpInterfaceNetLength', '')
        existing_landingZoneWAN.vpn__bgpRoutingMode = landingZoneWAN('vpn__bgpRoutingMode', '')
        existing_landingZoneWAN.vpn__cloudRouterName = landingZoneWAN('vpn__cloudRouterName', '')
        existing_landingZoneWAN.vpn__description = landingZoneWAN('vpn__description', '')
        existing_landingZoneWAN.vpn__externalVpnGateway = landingZoneWAN('vpn__externalVpnGateway', '')
        existing_landingZoneWAN.vpn__googleASN = landingZoneWAN('vpn__googleASN', 0)
        existing_landingZoneWAN.vpn__haVpnGateway = landingZoneWAN('vpn__haVpnGateway', '')
        existing_landingZoneWAN.vpn__peerASN = landingZoneWAN('vpn__peerASN', 0)
        existing_landingZoneWAN.vpn__projectName = landingZoneWAN('vpn__projectName', '')
        existing_landingZoneWAN.vpn__subnetMode = landingZoneWAN('vpn__subnetMode', '')
        existing_landingZoneWAN.vpn__vpcName = landingZoneWAN('vpn__vpcName', '')

        schema = LandingZoneWANSchema()
        # flatten the landingZoneWAN object into a python dictionary
        flatten_landingZoneWAN = flatten(existing_landingZoneWAN, delimiter)
        # load into schema and save to db
        update_landingZoneWAN = schema.load(flatten_landingZoneWAN, session=db.session)

        db.session.merge(flatten_landingZoneWAN)
        db.session.commit()

        # return the updated landingZoneWAN in the response
        data = schema.dump(update_landingZoneWAN)
        app.logger.debug("landingZoneWAN data:")
        app.logger.debug(pformat(data))
        return data, 200

    # otherwise, nope, landingZoneWAN doesn't exist, so that's an error
    else:
        abort(404, f"LandingZoneWAN not found")


def delete(id):
    """
    This function deletes an landingZoneWAN from the landingZoneWAN list

    :param id: id of the landingZoneWAN to delete
    :return:             200 on successful delete, 404 if not found
    """
    # Does the landingZoneWAN to delete exist?
    existing_landingZoneWAN = LandingZoneWAN.query.filter(LandingZoneWAN.id == id).one_or_none()

    # if found?
    if existing_landingZoneWAN is not None:
        db.session.delete(existing_landingZoneWAN)
        db.session.commit()

        return make_response(f"LandingZoneWAN id {id} successfully deleted", 200)

    # Otherwise, nope, landingZoneWAN to delete not found
    else:
        abort(404, f"LandingZoneWAN id {id} not found")


