import logging
from config import db
from tb_houston_service.models import User
from tb_houston_service.models import CI
import json


logger = logging.getLogger("tb_houston_service.activator_extension")

def expand_activator(act):
    """
    Expand accessRequestedBy from an integer to an object. 
    Do not use, fails with:
    '_mysql_connector.MySQLInterfaceError: Python type User cannot be converted'
    Need to fix the data model later. 
    """
    logger.debug("expand_activator: %s", act)
    act.accessRequestedBy = (
        db.session.query(User).filter(User.id == act.accessRequestedById).one_or_none()
    )
    return act

def expand_ci(act):
    ciList = json.loads(act.ci)
    newList =[]
    for id in ciList:
        name = db.session.query(CI).filter(CI.id == int(id) ).one_or_none()
        newList.append(name.value)
    act.ci = json.dumps(newList)
    print(act.ci)
    return act


