from config import db
from models import Application

def read_one(activatorId):
    """
    Responds to a request for /api/application_meta/{activatorId}

    :param application:   activatorId
    :return:              count of applications that match the acivatorId
    """
    acount = (
        db.session.query(Application)
        .filter(Application.activatorId == activatorId)
        .count()
    )
    db.session.close()
    data = {"count": acount}
    return data, 200
