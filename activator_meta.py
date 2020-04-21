# System modules

# 3rd party modules
from models import Activator


def read_one():
    """
    Responds to a request for /api/activator_meta/.

    :param activator:
    :return:              count of activators
    """

    count = Activator.query.count()
    data = { 'count': count }
    return data, 200
