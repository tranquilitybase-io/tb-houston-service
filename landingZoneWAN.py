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

    flattened_landingZoneWAN = flatten(landingZoneWAN, delimiter)

    # Does landingZoneWAN exist?
    if existing_landingZoneWAN is not None:
        flattened_landingZoneWAN = flatten(flatten(landingZoneWAN, delimiter))
        existing_landingZoneWAN.googleSession__primaryGcpVpcSubnet = flattened_landingZoneWAN.get('googleSession__primaryGcpVpcSubnet', '')
        existing_landingZoneWAN.googleSession__primaryRegion = flattened_landingZoneWAN.get('googleSession__primaryRegion', '')
        existing_landingZoneWAN.googleSession__primarySubnetName = flattened_landingZoneWAN.get('googleSession__primarySubnetName', '')
        existing_landingZoneWAN.googleSession__secondaryGcpVpcSubnet = flattened_landingZoneWAN.get('googleSession__secondaryGcpVpcSubnet', '')
        existing_landingZoneWAN.googleSession__secondaryRegion = flattened_landingZoneWAN.get('googleSession__secondaryRegion', '')
        existing_landingZoneWAN.googleSession__secondarySubnetName = flattened_landingZoneWAN.get('googleSession__secondarySubnetName', '')
        existing_landingZoneWAN.onPremiseSession__primaryBgpPeer = flattened_landingZoneWAN.get('onPremiseSession__primaryBgpPeer', '')
        existing_landingZoneWAN.onPremiseSession__primaryPeerIp = flattened_landingZoneWAN.get('onPremiseSession__primaryPeerIp', '')
        existing_landingZoneWAN.onPremiseSession__primaryPeerIpSubnet = flattened_landingZoneWAN.get('onPremiseSession__primaryPeerIpSubnet', '')
        existing_landingZoneWAN.onPremiseSession__primarySharedSecret = flattened_landingZoneWAN.get('onPremiseSession__primarySharedSecret', '')
        existing_landingZoneWAN.onPremiseSession__primaryVpnTunnel = flattened_landingZoneWAN.get('onPremiseSession__primaryVpnTunnel', '')
        existing_landingZoneWAN.onPremiseSession__secondaryBgpPeer = flattened_landingZoneWAN.get('onPremiseSession__secondaryBgpPeer', '')
        existing_landingZoneWAN.onPremiseSession__secondaryPeerIp = flattened_landingZoneWAN.get('onPremiseSession__secondaryPeerIp', '')
        existing_landingZoneWAN.onPremiseSession__secondaryPeerIpSubnet = flattened_landingZoneWAN.get('onPremiseSession__secondaryPeerIpSubnet', '')
        existing_landingZoneWAN.onPremiseSession__secondarySharedSecret = flattened_landingZoneWAN.get('onPremiseSession__secondarySharedSecret', '')
        existing_landingZoneWAN.onPremiseSession__secondaryVpnTunnel = flattened_landingZoneWAN.get('onPremiseSession__secondaryVpnTunnel', '')
        existing_landingZoneWAN.onPremiseSession__vendor = flattened_landingZoneWAN.get('onPremiseSession__vendor', '')
        existing_landingZoneWAN.vpn__bgpInterfaceNetLength = flattened_landingZoneWAN.get('vpn__bgpInterfaceNetLength', '')
        existing_landingZoneWAN.vpn__bgpRoutingMode = flattened_landingZoneWAN.get('vpn__bgpRoutingMode', '')
        existing_landingZoneWAN.vpn__cloudRouterName = flattened_landingZoneWAN.get('vpn__cloudRouterName', '')
        existing_landingZoneWAN.vpn__description = flattened_landingZoneWAN.get('vpn__description', '')
        existing_landingZoneWAN.vpn__externalVpnGateway = flattened_landingZoneWAN.get('vpn__externalVpnGateway', '')
        existing_landingZoneWAN.vpn__googleASN = flattened_landingZoneWAN.get('vpn__googleASN', 0)
        existing_landingZoneWAN.vpn__haVpnGateway = flattened_landingZoneWAN.get('vpn__haVpnGateway', '')
        existing_landingZoneWAN.vpn__peerASN = flattened_landingZoneWAN.get('vpn__peerASN', 0)
        existing_landingZoneWAN.vpn__projectName = flattened_landingZoneWAN.get('vpn__projectName', '')
        existing_landingZoneWAN.vpn__subnetMode = flattened_landingZoneWAN.get('vpn__subnetMode', '')
        existing_landingZoneWAN.vpn__vpcName = flattened_landingZoneWAN.get('vpn__vpcName', '')

        schema = LandingZoneWANSchema()

        #if '_sa_instance_state' in existing_landingZoneWAN:
        #    del existing_landingZoneWAN['_sa_instance_state']

        # load into schema and save to db
        #update_landingZoneWAN = schema.load(existing_landingZoneWAN, session=db.session)

        db.session.merge(existing_landingZoneWAN)
        db.session.commit()

        # return the updated landingZoneWAN in the response
        data = schema.dump(existing_landingZoneWAN)
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


