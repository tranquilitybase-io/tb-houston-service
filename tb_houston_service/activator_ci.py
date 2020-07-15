from tb_houston_service.models import ActivatorCI
from config.db_lib import db_session

def create_activator_ci(activatorId, list_of_ci,dbs):
    """
    Args:
        activatorId ([int]): [The Activator id]
        list_of_ci ([list]): [A list of CI ids]

        1. Logically delete all active CI ids for this activator
        2. Reactivate the activator ci relaionship that are in this list: list_of_ci
        3. Create the activator-ci rows that are not in this list.

    """

    # Inactivates the active solution environments for this Solution (activatorId)
    ci_list = db.session.query(ActivatorCI).filter(
        ActivatorCI.activatorId == activatorId,
        ActivatorCI.isActive
    ).all()
    for ci in ci_list:
        ci.isActive = False
    db.session.flush()

    for ci in list_of_ci:
        existing_act_ci = db.session.query(ActivatorCI).filter(
            ActivatorCI.activatorId == activatorId,
            ActivatorCI.ciId == ci
        ).one_or_none()

        if existing_act_ci:
            existing_act_ci.isActive = True
            dbs.merge(existing_act_ci)
        else:
            new_act_ci = ActivatorCI(
                activatorId = activatorId, 
                ciId = ci,
                lastUpdated = ModelTools.get_utc_timestamp(),
                isActive = True
            )
            dbs.add(new_act_ci)
        logger.debug("Added Activator CI: {new_act_ci} to transaction.")
    
    return dbs

