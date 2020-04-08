# System modules

# 3rd party modules
from flask import make_response, abort
from config import db
from models import Activator
from marshmallow import pprint


def read_one():
    """
    This function responds to a request for /api/activator_meta/

    :param activator:
    :return:              count of activators
    """

    count = Activator.query.count()
    data = { 'count': count }
    return data, 200
