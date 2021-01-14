"""
The sharedServicesAction module and supports all the ReST actions for the
sharedServicesAction collection
"""
from pprint import pformat

from config import app, db
from models import SharedServicesAction, SharedServicesActionSchema


def read_all():
    """
    Responds to a request for /api/sharedServicesActions
    with the complete lists of sharedServicesActions

    :return:        json string of list of sharedServicesActions
    """
    # Create the list of people from our data
    sharedServicesActions = db.session.query(SharedServicesAction).all()

    # Serialize the data for the response
    sharedServicesAction_schema = SharedServicesActionSchema(many=True)
    data = sharedServicesAction_schema.dump(sharedServicesActions)
    app.logger.debug("sharedServicesAction data:")
    app.logger.debug(pformat(data))
    return data
