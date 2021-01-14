"""
This is the sharedServicesProgressItem module and supports all the ReST actions for the
sharedServicesProgressItem collection
"""
from pprint import pformat

from config import app, db
from models import SharedServicesProgressItem, SharedServicesProgressItemSchema


def read_all():
    """
    This function responds to a request for /api/sharedServicesProgressItems
    with the complete lists of sharedServicesProgressItems

    :return:        json string of list of sharedServicesProgressItems
    """
    # Create the list of people from our data
    sharedServicesProgressItems = db.session.query(SharedServicesProgressItem).all()

    # Serialize the data for the response
    sharedServicesProgressItem_schema = SharedServicesProgressItemSchema(many=True)
    data = sharedServicesProgressItem_schema.dump(sharedServicesProgressItems)
    app.logger.debug("sharedServicesProgressItem data:")
    app.logger.debug(pformat(data))
    return data
