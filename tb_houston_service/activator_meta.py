from config import db
from models import Activator

def read_one():
    """
    Responds to a request for /api/activator_meta/.

    :param activator:
    :return:              count of activators
    """
    count = db.session.query(Activator).count()
    data = {"count": count}
    return data, 200
