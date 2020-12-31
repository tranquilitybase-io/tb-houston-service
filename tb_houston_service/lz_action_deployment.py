import logging

from flask import abort

from config.db_lib import db_session
from models import (
    LandingZoneAction,
    LandingZoneProgressItem,
    LZEnvironment,
    LZLanVpc,
    LZLanVpcEnvironment,
)
from tb_houston_service import lzlanvpc

logger = logging.getLogger("tb_houston_service.lz_action_deployment")


def is_valid_lzlanvpc(dbsession):
    logger.debug("is_valid_lzlanvpc")
    count = (
        dbsession.query(LZLanVpc)
        .filter(LZLanVpc.isActive, LZLanVpc.sharedVPCProjectId == None)
        .count()
    )
    return count == 0


# LZLanVpcEnvironment validation
# Validate all active environments are associated with active lzlanvpc
def is_valid_lzlanvpc_environment(dbsession):
    logger.debug("is_valid_lzlanvpc_environment")
    # env_id checks
    active_env_ids = set(
        [
            obj.id
            for obj in dbsession.query(LZEnvironment)
            .filter(LZEnvironment.isActive)
            .all()
        ]
    )
    active_vpc_env_ids = set(
        [
            obj.environmentId
            for obj in dbsession.query(LZLanVpcEnvironment)
            .filter(LZLanVpcEnvironment.isActive)
            .all()
        ]
    )
    env_sym_diff = active_env_ids.symmetric_difference(active_vpc_env_ids)
    if len(env_sym_diff) > 0:
        logger.debug("env sym_diff: %s", env_sym_diff)
        return False

    # vpc_id checks
    active_vpc_ids = set(
        [obj.id for obj in dbsession.query(LZLanVpc).filter(LZLanVpc.isActive).all()]
    )
    active_vpc_env_ids = set(
        [
            obj.lzlanvpcId
            for obj in dbsession.query(LZLanVpcEnvironment)
            .filter(LZLanVpcEnvironment.isActive)
            .all()
        ]
    )
    vpc_sym_diff = active_vpc_ids.symmetric_difference(active_vpc_env_ids)
    if len(env_sym_diff) > 0:
        logger.debug("vpc sym_diff: %s", vpc_sym_diff)
        return False
    return True


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
    logger.debug("environment_deployment")

    data = {"deployment": False}
    return_code = 500

    with db_session() as dbs:

        lzlanvpc.set_shared_vpc_project_id(dbsession=dbs)

        if not is_valid_lzlanvpc(dbsession=dbs):
            abort(400, "Invalid LAN VPC found.")

        if not is_valid_lzlanvpc_environment(dbsession=dbs):
            abort(
                400, "All active environments must be connected to an active LAN VPC."
            )

        lza_environment = (
            dbs.query(LandingZoneAction)
            .filter(LandingZoneAction.title == "Environment")
            .one()
        )
        logger.debug(lza_environment)
        lza_environment.completionRate = 100
        lza_wan = (
            dbs.query(LandingZoneAction).filter(LandingZoneAction.title == "WAN").one()
        )
        logger.debug(lza_wan)
        lza_wan.locked = False
        lzpi_environment = (
            dbs.query(LandingZoneProgressItem)
            .filter(LandingZoneProgressItem.label == "Environment")
            .one()
        )
        logger.debug(lzpi_environment)
        lzpi_environment.completed = True
        dbs.add(lza_environment)
        dbs.add(lza_wan)
        dbs.add(lzpi_environment)
        dbs.commit()
        data = {"deployment": True}
        return_code = 200
    return data, return_code


if __name__ == "__main__":
    resp = environment_deployment()
    logger.debug(resp)
