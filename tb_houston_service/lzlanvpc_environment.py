"""
A helper module to create the lzlanvpc environment relationship.
"""
# 3rd party modules
import logging
from config import db
from tb_houston_service.models import LZLanVpcEnvironment, LZLanVpcEnvironmentSchema
from tb_houston_service.models import LZLanVpc

logger = logging.getLogger("tb_houston_service.lzlanvpc_environment")


def create(lzLanVpcEnvironmentListDetail):
    logger.debug("create: %s", lzLanVpcEnvironmentListDetail)
    # Remove the id
    lzLanVpcEnvironmentListDetail.pop("id", None)
    # Does the LZ Lanvpc environment exist?
    existing_lzlanvpc_env = (
        db.session.query(LZLanVpcEnvironment)
        .filter(
            LZLanVpcEnvironment.lzlanvpcId
            == lzLanVpcEnvironmentListDetail["lzlanvpcId"],
            LZLanVpcEnvironment.environmentId
            == lzLanVpcEnvironmentListDetail["environmentId"],
        )
        .one_or_none()
    )
    schema = LZLanVpcEnvironmentSchema()

    # Does sol_env exist?
    if existing_lzlanvpc_env is not None:
        logger.debug("update: %s", existing_lzlanvpc_env)
        existing_lzlanvpc_env.isActive = lzLanVpcEnvironmentListDetail.get(
            "isActive", True
        )
        db.session.merge(existing_lzlanvpc_env)
    else:
        logger.debug("create: %s", lzLanVpcEnvironmentListDetail)
        lzlanvpc_env_change = schema.load(
            lzLanVpcEnvironmentListDetail, session=db.session
        )
        db.session.add(lzlanvpc_env_change)


def logical_delete_all_active():
    objs = db.session.query(LZLanVpc).filter(LZLanVpc.isActive == True).all()
    for o in objs:
        o.isActive = False
    db.session.add(o)
