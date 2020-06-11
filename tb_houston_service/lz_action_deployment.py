import logging
from tb_houston_service.models import LandingZoneAction
from tb_houston_service.models import LandingZoneProgressItem
from config import db


logger = logging.getLogger("tb_houston_service.lz_action_deployment")


def environment_deployment():
    """
    Deployment Steps:
    sets eagle_db.landingzoneaction.title='Environment' row completionRate col to 100%
    sets eagle_db.landingzoneaction.title='Wan' row locked col to false
    sets eagle_db.landingzoneprogressitem.label='Environment' row completed col to true

    Before state:
    LandingZoneAction.title == "Environment", completionRate == 0
    LandingZoneAction.title == "WAN", locked == 1
    LandingZoneProgressItem.label == "Environment", completed = False

    After state:
    LandingZoneAction.title == "Environment", completionRate == 100
    LandingZoneAction.title == "WAN", locked == 0
    LandingZoneProgressItem.label == "Environment", completed = True    
    """

    data = {"deployment": False}
    return_code = 500

    try:
        lza_environment = (
            db.session.query(LandingZoneAction)
            .filter(LandingZoneAction.title == "Environment")
            .one()
        )
        logger.debug(lza_environment)
        lza_environment.completionRate = 100
        lza_wan = (
            db.session.query(LandingZoneAction)
            .filter(LandingZoneAction.title == "WAN")
            .one()
        )
        logger.debug(lza_wan)
        lza_wan.locked = False
        lzpi_environment = (
            db.session.query(LandingZoneProgressItem)
            .filter(LandingZoneProgressItem.label == "Environment")
            .one()
        )
        logger.debug(lzpi_environment)
        lzpi_environment.completed = True
        db.session.add(lza_environment)
        db.session.add(lza_wan)
        db.session.add(lzpi_environment)
        db.session.commit()
        data = {"deployment": True}
        return_code = 200
    except:
        db.session.rollback()
        raise
    finally:
        db.session.close()

    return data, return_code


if __name__ == "__main__":
    resp = environment_deployment()
    logger.debug(resp)
