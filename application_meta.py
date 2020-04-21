# System modules

# 3rd party modules
from models import Application


def read_one(activatorId):
    """
    Responds to a request for /api/application_meta/{activatorId}

    :param application:   activatorId
    :return:              count of applications that match the acivatorId
    """

    acount = Application.query.filter(Application.activatorId == activatorId).count()
    data = { 'count': acount }
    return data, 200
