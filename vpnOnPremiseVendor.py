"""
This is the deployments module and supports all the ReST actions for the
vpnOnPremiseVendor collection
"""

# System modules
from datetime import datetime

# 3rd party modules
from flask import make_response, abort
from config import db, app
from models import VPNOnPremiseVendor, VPNOnPremiseVendorSchema
from pprint import pformat


def read_all():
    """
    This function responds to a request for /api/vpnOnPremiseVendor
    with the complete lists of VPNOnPremiseVendors 

    :return:        json string of list of VPNOnPremiseVendors 
    """

    # Create the list of VPNOnPremiseVendors from our data
    vpnOnPremiseVendor = VPNOnPremiseVendor.query.order_by(VPNOnPremiseVendor.key).all()
    app.logger.debug(pformat(vpnOnPremiseVendor))
    # Serialize the data for the response
    vpnOnPremiseVendor_schema = VPNOnPremiseVendorSchema(many=True)
    data = vpnOnPremiseVendor_schema.dump(vpnOnPremiseVendor)
    return data


def read_one(key):
    """
    This function responds to a request for /api/vpnOnPremiseVendor/{key}
    with one matching vpnOnPremiseVendor from VPNOnPremiseVendors 

    :param application:   key of vpnOnPremiseVendor to find
    :return:              vpnOnPremiseVendor matching key
    """

    vpnOnPremiseVendor = (VPNOnPremiseVendor.query.filter(VPNOnPremiseVendor.key == key).one_or_none())

    if vpnOnPremiseVendor is not None:
        # Serialize the data for the response
        vpnOnPremiseVendor_schema = VPNOnPremiseVendorSchema()
        data = vpnOnPremiseVendor_schema.dump(vpnOnPremiseVendor)
        return data
    else:
        abort(
            404, "VPNOnPremiseVendor with key {key} not found".format(key=key)
        )


def create(vpnOnPremiseVendor):
    """
    This function creates a new vpnOnPremiseVendor in the vpnOnPremiseVendor list
    based on the passed in vpnOnPremiseVendor data

    :param vpnOnPremiseVendor: vpnOnPremiseVendor to create in vpnOnPremiseVendor structure
    :return:        201 on success, 406 on vpnOnPremiseVendor exists
    """
    key = vpnOnPremiseVendor.get("key", None)
    value = vpnOnPremiseVendor.get("value", None)

    # Does the vpnOnPremiseVendor exist already?
    existing_vpnOnPremiseVendor = (
        VPNOnPremiseVendor.query.filter(VPNOnPremiseVendor.key == key).one_or_none()
    )

    if existing_vpnOnPremiseVendor is None:
        schema = VPNOnPremiseVendorSchema()
        new_vpnOnPremiseVendor = schema.load(vpnOnPremiseVendor, session=db.session)
        db.session.add(new_vpnOnPremiseVendor)
        db.session.commit()

        # Serialize and return the newly created deployment
        # in the response
        data = schema.dump(new_vpnOnPremiseVendor)

        return data, 201

    # Otherwise, it already exists, that's an error
    else:
        abort(406, f"VPNOnPremiseVendor already exists")


def update(key, vpnOnPremiseVendor):
    """
    This function updates an existing vpnOnPremiseVendor in the vpnOnPremiseVendor list

    :param key:    key of the vpnOnPremiseVendor to update in the vpnOnPremiseVendor list
    :param vpnOnPremiseVendor:   vpnOnPremiseVendor to update
    :return:       updated vpnOnPremiseVendor
    """

    app.logger.debug(pformat(vpnOnPremiseVendor))

    if vpnOnPremiseVendor["key"] != key:
           abort(400, f"Key mismatch in path and body")

    # Does the vpnOnPremiseVendor exist in vpnOnPremiseVendor list?
    existing_vpnOnPremiseVendor = VPNOnPremiseVendor.query.filter(
            VPNOnPremiseVendor.key == key
    ).one_or_none()

    # Does vpnOnPremiseVendor exist?

    if existing_vpnOnPremiseVendor is not None:
        schema = VPNOnPremiseVendorSchema()
        update_vpnOnPremiseVendor = schema.load(vpnOnPremiseVendor, session=db.session)
        update_vpnOnPremiseVendor.key = vpnOnPremiseVendor['key']

        db.session.merge(update_vpnOnPremiseVendor)
        db.session.commit()

        # return the updted vpnOnPremiseVendor in the response
        data = schema.dump(update_vpnOnPremiseVendor)
        return data, 200

    # otherwise, nope, deployment doesn't exist, so that's an error
    else:
        abort(404, f"VPNOnPremiseVendor not found")


def delete(key):
    """
    This function deletes a VPNOnPremiseVendor from the VPNOnPremiseVendor list

    :param key: key of the VPNOnPremiseVendor to delete
    :return:    200 on successful delete, 404 if not found
    """
    # Does the vpnOnPremiseVendor to delete exist?
    existing_vpnOnPremiseVendor = VPNOnPremiseVendor.query.filter(VPNOnPremiseVendor.key == key).one_or_none()

    # if found?
    if existing_vpnOnPremiseVendor is not None:
        db.session.delete(existing_vpnOnPremiseVendor)
        db.session.commit()

        return make_response(f"VPNOnPremiseVendor {key} successfully deleted", 200)

    # Otherwise, nope, vpnOnPremiseVendor to delete not found
    else:
        abort(404, f"VPNOnPremiseVendor {key} not found")


