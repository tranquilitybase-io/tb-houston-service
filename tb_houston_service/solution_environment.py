"""
This is the deployments module and supports all the ReST actions for the
solution environment collection
"""
import logging
from pprint import pformat
from flask import make_response
from config import db
from models import SolutionEnvironment, SolutionEnvironmentSchema
from tb_houston_service.tools import ModelTools

logger = logging.getLogger("tb_houston_service.solutionEnvironment")

def read_all():
    """
    This function responds to a request for /api/solutionEnvironment
    with the complete lists of solution environment relationships

    :return:        json string of list of solutionEnvironments
    """
    # Create the list of solution environments from our data
    sol_env = (
        db.session.query(SolutionEnvironment).order_by(SolutionEnvironment.id).all()
    )
    logger.debug(pformat(sol_env))
    # Serialize the data for the response
    schema = SolutionEnvironmentSchema(many=True)
    data = schema.dump(sol_env)
    return data, 200

def create(solEnvDetails):
    logger.debug("solutionEnvironment::create: %s", solEnvDetails)
    # Remove the id
    solEnvDetails.pop("id", None)
    # Does the solution environment exist?
    existing_sol_env = (
        db.session.query(SolutionEnvironment)
        .filter(
            SolutionEnvironment.solutionId == solEnvDetails["solutionId"],
            SolutionEnvironment.environmentId == solEnvDetails["environmentId"],
        )
        .one_or_none()
    )
    schema = SolutionEnvironmentSchema()

    # Does sol_env exist?
    if existing_sol_env is not None:
        logger.debug("solutionEnvironment::update: %s", existing_sol_env)
        existing_sol_env.isActive = solEnvDetails.get("isActive", True)
        existing_sol_env.lastUpdated = ModelTools.get_utc_timestamp()
        db.session.merge(existing_sol_env)
        db.session.commit()
        data = schema.dump(existing_sol_env)
        return data, 201
    else:
        logger.debug("solutionEnvironment::create: %s", solEnvDetails)
        sol_env_change = schema.load(solEnvDetails, session=db.session)
        sol_env_change.isActive = solEnvDetails.get("isActive", True)
        sol_env_change.lastUpdated = ModelTools.get_utc_timestamp()
        db.session.add(sol_env_change)
        db.session.commit()
        data = schema.dump(sol_env_change)
        return data, 201

def create_all(solutionEnvironmentListDetails):
    """
    This function updates solution environments relationships.

    :param solution environment:  solution environment to update
    :return:       updated solution environment
    """
    logger.debug("create_all: %s", pformat(solutionEnvironmentListDetails))
    for lze in solutionEnvironmentListDetails:
        create(lze)
    return make_response("Solution environments successfully created/updated", 201)
