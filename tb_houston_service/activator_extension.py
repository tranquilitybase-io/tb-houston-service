import logging
from config import db
from tb_houston_service.models import User
from tb_houston_service.models import CI, ActivatorCI
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
    act_ci_list = (db.session.query(ActivatorCI).filter(ActivatorCI.activatorId == act.id).all())
    print(act_ci_list)
    newList =[]
    for act_ci in act_ci_list:
        name = db.session.query(CI).filter(CI.id == act_ci.ciId).one_or_none()
        newList.append(name.value)
    print(newList)
    act.ci = json.dumps(newList)
    print(act.ci)
    return act


