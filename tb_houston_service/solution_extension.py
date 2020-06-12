import logging
from config import db
from tb_houston_service.models import Application
from tb_houston_service.models import Team
from tb_houston_service.models import LZEnvironment
from tb_houston_service.models import SolutionEnvironment
from tb_houston_service.tools import ModelTools
from tb_houston_service import application_extension
from tb_houston_service import team_extension

logger = logging.getLogger('tb_houston_service.solution_extension')


def expand_solution(sol):
    environments = (
        db.session.query(LZEnvironment)
        .filter(
            SolutionEnvironment.solutionId == sol.id,
            SolutionEnvironment.environmentId == LZEnvironment.id,
            SolutionEnvironment.isActive
        )
        .all()
    )
    sol.environments = environments

    a_team = db.session.query(Team).filter(Team.id == sol.teamId).one_or_none()
    sol.team = team_extension.expand_team(a_team)

    if sol.applications is None:
       sol.applications = db.session.query(Application).filter(Application.solutionId == sol.id).all()

    for ap in sol.applications:
        ap = application_extension.expand_application(ap)

    return sol


def expand_solution_for_dac(sol):
    environments = (
        db.session.query(LZEnvironment)
        .filter(
            SolutionEnvironment.solutionId == sol.id,
            SolutionEnvironment.environmentId == LZEnvironment.id,
        )
        .all()
    )
    sol.environments = environments
    a_team = db.session.query(Team).filter(Team.id == sol.teamId).one_or_none()
    sol.team = team_extension.expand_team_with_users(a_team)
    return sol


def create_solution_environments(solutionId, list_of_env_ids):
    """
    Args:
        solutionId ([int]): [The Solution id]
        list_of_env_ids ([list]): [A list of LZEnvironment ids]

        1. Logically delete all active solution environments for this solution
        2. Reactivate the solution env relationship that are in this list: list_of_env_ids
        3. Create the solution env that are not in this list.

    """

    # Inactivates the active solution environments for this Solution (solutionId)
    envs = db.session.query(SolutionEnvironment).filter(
        SolutionEnvironment.solutionId == solutionId,
        SolutionEnvironment.isActive
    ).all()
    for env in envs:
        env.isActive = False
    db.session.flush()

    for env in list_of_env_ids:
        existing_sol_env = db.session.query(SolutionEnvironment).filter(
            SolutionEnvironment.solutionId == solutionId,
            SolutionEnvironment.environmentId == env
        ).one_or_none()

        if existing_sol_env:
            existing_sol_env.isActive = True
            db.session.merge(existing_sol_env)
        else:
            new_env_solution = SolutionEnvironment(
                solutionId = solutionId, 
                environmentId = env,
                lastUpdated = ModelTools.get_utc_timestamp(),
                isActive = True
            )
            db.session.add(new_env_solution)
        logger.debug("Added solution environment: {new_env_solution} to transaction.")
