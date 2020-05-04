"""
deployments module
supports all the ReST actions for the
cloudaccount collection
"""

# 3rd party modules
from flask import make_response, abort
from config import db, app
from models import CloudAccount, CloudAccountSchema
from pprint import pformat


def read_all():
    """
    This function responds to a request for /api/cloudaccount
    with the complete lists of cloudaccounts

    :return:        json string of list of cloudaccounts
    """

    # Create the list of cloudaccounts from our data
    cloudaccount = CloudAccount.query.order_by(CloudAccount.id).all()
    app.logger.debug(pformat(cloudaccount))
    # Serialize the data for the response
    cloudaccount_schema = CloudAccountSchema(many=True)
    data = cloudaccount_schema.dump(cloudaccount)
    return data


def read_one(id):
    """
    This function responds to a request for /api/cloudaccount/{key}
    with one matching cloudaccount from cloudaccounts

    :param application:   key of cloudaccount to find
    :return:              cloudaccount matching key
    """

    cloudaccount = (CloudAccount.query.filter(CloudAccount.id == id).one_or_none())


    if cloudaccount is not None:
        # Serialize the data for the response
        cloudaccount_schema = CloudAccountSchema()
        data = cloudaccount_schema.dump(cloudaccount)
        return data
    else:
        abort(
            404, "CloudAccount with id {id} not found".format(id=id)
        )


def create(cloudAccountDetails):
    """
    This function creates a new cloudaccount in the cloudaccount list
    based on the passed in cloudaccount data

    :param cloudaccount:  cloudaccount to create in cloudaccount structure
    :return:        201 on success, 406 on cloudaccount exists
    """
    
    # Does the cloudaccount exist already?
    existing_cloudaccount = (
        CloudAccount.query.filter(CloudAccount.id == cloudAccountDetails['id']).one_or_none()
    )

    if existing_cloudaccount is None:
        schema = CloudAccountSchema()
        new_cloudaccount = schema.load(cloudAccountDetails, session=db.session)
        db.session.add(new_cloudaccount)
        db.session.commit()

        # Serialize and return the newly created deployment
        # in the response
        data = schema.dump(new_cloudaccount)

        return data, 201

    # Otherwise, it already exists, that's an error
    else:
        abort(406, f"CloudAccount already exists")


def update(id, cloudAccountDetails):
    """
    This function updates an existing cloudaccount in the cloudaccount list

    :param id:    id of the cloudaccount to update in the cloudaccount list
    :param cloudaccount:   cloudaccount to update
    :return:       updated cloudaccount
    """

    app.logger.debug(pformat(cloudAccountDetails))

    if cloudAccountDetails["id"] != int(id):
           abort(400, f"Id mismatch in path and body")

    # Does the cloudaccount exist in cloudaccount list?
    existing_cloudaccount = CloudAccount.query.filter(
            CloudAccount.id == id
    ).one_or_none()

    # Does cloudaccount exist?

    if existing_cloudaccount is not None:
        schema = CloudAccountSchema()
        update_cloudaccount = schema.load(cloudAccountDetails, session=db.session)
        update_cloudaccount.id = cloudAccountDetails['id']

        db.session.merge(update_cloudaccount)
        db.session.commit()

        # return the updted cloudaccount in the response
        data = schema.dump(update_cloudaccount)
        return data, 200

    # otherwise, nope, deployment doesn't exist, so that's an error
    else:
        abort(404, f"CloudAccount not found")


def delete(id):
    """
    This function deletes a cloudaccount from the cloudaccounts list

    :param id: id of the cloudaccount to delete
    :return:    200 on successful delete, 404 if not found
    """
    # Does the cloudaccount to delete exist?
    existing_cloudaccount = CloudAccount.query.filter(CloudAccount.id == id).one_or_none()

    # if found?
    if existing_cloudaccount is not None:
        db.session.delete(existing_cloudaccount)
        db.session.commit()

        return make_response(f"CloudAccount {id} successfully deleted", 200)

    # Otherwise, nope, cloudaccount to delete not found
    else:
        abort(404, f"CloudAccount {id} not found")


