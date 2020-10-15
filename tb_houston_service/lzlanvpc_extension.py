import logging

from config import db
from models import LZEnvironment, LZLanVpcEnvironment

logger = logging.getLogger('tb_houston_service.lzlanvpc_extension')

def expand_lzlanvpc(lzlanvpc):
    environments = (
        db.session.query(LZEnvironment)
        .filter(
            LZLanVpcEnvironment.lzlanvpcId == lzlanvpc.id,
            LZLanVpcEnvironment.environmentId == LZEnvironment.id,
            LZLanVpcEnvironment.isActive
        )
        .all()
    )
    lzlanvpc.environments = environments
    return lzlanvpc

def create_lzlanvpc_environments(lzlanvpc_id, list_of_env_ids):
    for env in list_of_env_ids:
        lzlanvpc_env = db.session.query(LZLanVpcEnvironment).filter(
            LZLanVpcEnvironment.lzlanvpcId == lzlanvpc_id,
            LZLanVpcEnvironment.environmentId == env
        ).one_or_none()
        if lzlanvpc_env is None:
            new_lzlanvpc_env = LZLanVpcEnvironment(
                lzlanvpcId = lzlanvpc_id, 
                environmentId = env,
                isActive = True
                )
            db.session.add(new_lzlanvpc_env)
            logger.debug("Added lzlanvpc environment: %s to transaction.", new_lzlanvpc_env)
        else:
            lzlanvpc_env.isActive = True
            db.session.merge(lzlanvpc_env)
            logger.debug("Added lzlanvpc environment: %s to transaction.", lzlanvpc_env)
