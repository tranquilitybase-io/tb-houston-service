"""
This is the landingZoneWAN module and supports all the ReST actions for the
landingZoneWAN collection
"""
from pprint import pformat

from flask import abort, make_response
from flatten_json import flatten, unflatten

from config import app, db
from models import LandingZoneWAN, LandingZoneWANSchema
from tb_houston_service.extendedSchemas import ExtendedLandingZoneWANSchema, IdSchema

delimiter = "__"


def read_all():
    """
    This function responds to a request for /api/landingZoneWANs
    with the complete lists of landingZoneWANs

    :return:        json string of list of landingZoneWANs
    """
    # Create the list of people from our data
    landingZoneWANs = db.session.query(LandingZoneWAN).all()
    landingZoneWANArr = []
    for lzw in landingZoneWANs:
        landingZoneWANArr.append(unflatten(lzw.__dict__, delimiter))

    # Serialize the data for the response
    eschema = ExtendedLandingZoneWANSchema(many=True)
    data = eschema.dump(landingZoneWANArr)
    app.logger.debug("landingZoneWAN data:")
    app.logger.debug(pformat(data))
    return data


def read_one(oid):
    """
    This function responds to a request for /api/landingZoneWAN/{oid}
    with one matching landingZoneWAN from landingZoneWANs

    :param landingZoneWAN:   id of the landingZoneWAN to find
    :return:              landingZoneWAN matching the id
    """
    landingZoneWAN = (
        db.session.query(LandingZoneWAN).filter(LandingZoneWAN.id == oid).one_or_none()
    )

    if landingZoneWAN is not None:
        # Serialize the data for the response
        landingZoneWAN_schema = ExtendedLandingZoneWANSchema(many=False)
        unflattened_landingZoneWAN = unflatten(landingZoneWAN.__dict__, delimiter)
        data = landingZoneWAN_schema.dump(unflattened_landingZoneWAN)
        app.logger.debug("landingZoneWAN data:")
        app.logger.debug(pformat(data))
        return data
    else:
        abort(404, f"LandingZoneWAN with id {oid} not found".format(id=oid))


def create(landingZoneWANDetails):
    """
    This function creates a new landingZoneWAN in the landingZoneWAN structure
    based on the passed in landingZoneWAN data

    :param landingZoneWAN:  landingZoneWAN to create in landingZoneWAN list
    :return:             201 on success, 406 on landingZoneWAN exists
    """
    # we don't need the id, the is generated automatically on the database
    if "id" in landingZoneWANDetails:
        del landingZoneWANDetails["id"]

    # flatten the python object into a python dictionary
    flattened_landingZoneWAN = flatten(landingZoneWANDetails, delimiter)
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


def update(oid, landingZoneWANDetails):
    """
    This function updates an existing landingZoneWAN in the landingZoneWAN list

    :param id: id of the landingZoneWAN to update in the landingZoneWAN list
    :param landingZoneWAN:   landingZoneWAN to update
    :return: updated landingZoneWAN
    """
    app.logger.debug("landingZoneWAN: ")
    app.logger.debug(pformat(landingZoneWANDetails))

    if landingZoneWANDetails["id"] != oid:
        abort(400, f"Key mismatch in path and body")

    # Does the landingZoneWAN exist in landingZoneWANs?
    existing_landingZoneWAN = (
        db.session.query(LandingZoneWAN).filter(LandingZoneWAN.id == oid).one_or_none()
    )

    flattened_landingZoneWAN = flatten(landingZoneWANDetails, delimiter)

    # Does landingZoneWAN exist?
    if existing_landingZoneWAN is not None:
        flattened_landingZoneWAN = flatten(flatten(landingZoneWANDetails, delimiter))
        existing_landingZoneWAN.googleEndpoint__primaryGcpVpcSubnet = (
            flattened_landingZoneWAN.get("googleEndpoint__primaryGcpVpcSubnet", "")
        )
        existing_landingZoneWAN.googleEndpoint__primaryRegion = (
            flattened_landingZoneWAN.get("googleEndpoint__primaryRegion", "")
        )
        existing_landingZoneWAN.googleEndpoint__primarySubnetName = (
            flattened_landingZoneWAN.get("googleEndpoint__primarySubnetName", "")
        )
        existing_landingZoneWAN.googleEndpoint__secondaryGcpVpcSubnet = (
            flattened_landingZoneWAN.get("googleEndpoint__secondaryGcpVpcSubnet", "")
        )
        existing_landingZoneWAN.googleEndpoint__secondaryRegion = (
            flattened_landingZoneWAN.get("googleEndpoint__secondaryRegion", "")
        )
        existing_landingZoneWAN.googleEndpoint__secondarySubnetName = (
            flattened_landingZoneWAN.get("googleEndpoint__secondarySubnetName", "")
        )
        existing_landingZoneWAN.remoteEndpoint__primaryBgpPeer = (
            flattened_landingZoneWAN.get("remoteEndpoint__primaryBgpPeer", "")
        )
        existing_landingZoneWAN.remoteEndpoint__primaryPeerIp = (
            flattened_landingZoneWAN.get("remoteEndpoint__primaryPeerIp", "")
        )
        existing_landingZoneWAN.remoteEndpoint__primaryPeerIpSubnet = (
            flattened_landingZoneWAN.get("remoteEndpoint__primaryPeerIpSubnet", "")
        )
        existing_landingZoneWAN.remoteEndpoint__primarySharedSecret = (
            flattened_landingZoneWAN.get("remoteEndpoint__primarySharedSecret", "")
        )
        existing_landingZoneWAN.remoteEndpoint__primaryVpnTunnel = (
            flattened_landingZoneWAN.get("remoteEndpoint__primaryVpnTunnel", "")
        )
        existing_landingZoneWAN.remoteEndpoint__secondaryBgpPeer = (
            flattened_landingZoneWAN.get("remoteEndpoint__secondaryBgpPeer", "")
        )
        existing_landingZoneWAN.remoteEndpoint__secondaryPeerIp = (
            flattened_landingZoneWAN.get("remoteEndpoint__secondaryPeerIp", "")
        )
        existing_landingZoneWAN.remoteEndpoint__secondaryPeerIpSubnet = (
            flattened_landingZoneWAN.get("remoteEndpoint__secondaryPeerIpSubnet", "")
        )
        existing_landingZoneWAN.remoteEndpoint__secondarySharedSecret = (
            flattened_landingZoneWAN.get("remoteEndpoint__secondarySharedSecret", "")
        )
        existing_landingZoneWAN.remoteEndpoint__secondaryVpnTunnel = (
            flattened_landingZoneWAN.get("remoteEndpoint__secondaryVpnTunnel", "")
        )
        existing_landingZoneWAN.remoteEndpoint__vendor = flattened_landingZoneWAN.get(
            "remoteEndpoint__vendor", ""
        )
        existing_landingZoneWAN.vpn__bgpInterfaceNetLength = (
            flattened_landingZoneWAN.get("vpn__bgpInterfaceNetLength", "")
        )
        existing_landingZoneWAN.vpn__bgpRoutingMode = flattened_landingZoneWAN.get(
            "vpn__bgpRoutingMode", ""
        )
        existing_landingZoneWAN.vpn__cloudRouterName = flattened_landingZoneWAN.get(
            "vpn__cloudRouterName", ""
        )
        existing_landingZoneWAN.vpn__description = flattened_landingZoneWAN.get(
            "vpn__description", ""
        )
        existing_landingZoneWAN.vpn__externalVpnGateway = flattened_landingZoneWAN.get(
            "vpn__externalVpnGateway", ""
        )
        existing_landingZoneWAN.vpn__googleASN = flattened_landingZoneWAN.get(
            "vpn__googleASN", 0
        )
        existing_landingZoneWAN.vpn__haVpnGateway = flattened_landingZoneWAN.get(
            "vpn__haVpnGateway", ""
        )
        existing_landingZoneWAN.vpn__peerASN = flattened_landingZoneWAN.get(
            "vpn__peerASN", 0
        )
        existing_landingZoneWAN.vpn__projectName = flattened_landingZoneWAN.get(
            "vpn__projectName", ""
        )
        existing_landingZoneWAN.vpn__subnetMode = flattened_landingZoneWAN.get(
            "vpn__subnetMode", ""
        )
        existing_landingZoneWAN.vpn__vpcName = flattened_landingZoneWAN.get(
            "vpn__vpcName", ""
        )

        schema = LandingZoneWANSchema()

        # if '_sa_instance_state' in existing_landingZoneWAN:
        #    del existing_landingZoneWAN['_sa_instance_state']

        # load into schema and save to db
        # update_landingZoneWAN = schema.load(existing_landingZoneWAN, session=db.session)

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


def delete(oid):
    """
    This function deletes an landingZoneWAN from the landingZoneWAN list

    :param id: id of the landingZoneWAN to delete
    :return:             200 on successful delete, 404 if not found
    """
    # Does the landingZoneWAN to delete exist?
    existing_landingZoneWAN = (
        db.session.query(LandingZoneWAN).filter(LandingZoneWAN.id == oid).one_or_none()
    )

    # if found?
    if existing_landingZoneWAN is not None:
        db.session.delete(existing_landingZoneWAN)
        db.session.commit()

        return make_response(f"LandingZoneWAN id {oid} successfully deleted", 200)

    # Otherwise, nope, landingZoneWAN to delete not found
    else:
        abort(404, f"LandingZoneWAN id {oid} not found")
