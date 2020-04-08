# System modules

# 3rd party modules
from flask import make_response, abort
from config import db
from models import Application
from marshmallow import pprint


def read_one(activatorId):
    """
    This function responds to a request for /api/application_meta/{activatorId}

    :param application:   activatorId
    :return:              count of applications that match the acivatorId
    """

    acount = Application.query.filter(Application.activatorId == activatorId).count()
    data = { 'count': acount }
    return data, 200
