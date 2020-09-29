import logging
from tb_houston_service.models import Application
from tb_houston_service.models import Team
from tb_houston_service.models import BusinessUnit
from tb_houston_service.models import LZEnvironment
from tb_houston_service.models import LZLanVpc
from tb_houston_service.models import LZLanVpcEnvironment
from tb_houston_service.models import SolutionEnvironment
from tb_houston_service.models import CI,CD,SourceControl
from tb_houston_service.tools import ModelTools
from tb_houston_service import application_extension
from tb_houston_service import team_extension
from tb_houston_service import security

logger = logging.getLogger('tb_houston_service.solution_extension')


def expand_solution(sol, dbsession):
    logger.debug("dbs: %s", dbsession)    
    environments = (
        dbsession.query(LZEnvironment)
        .filter(
            SolutionEnvironment.solutionId == sol.id,
            SolutionEnvironment.environmentId == LZEnvironment.id,
            SolutionEnvironment.isActive
        )
        .all()
    )
    sol.environments = environments

    a_team = dbsession.query(Team).filter(Team.id == sol.teamId).one_or_none()
    sol.team = team_extension.expand_team(a_team)

    sol.applications = dbsession.query(Application).filter(
        Application.solutionId == sol.id,
        Application.isActive
    ).all()

    for ap in sol.applications:
        ap = application_extension.expand_application(ap, dbsession = dbsession)

    if sol.businessUnitId:
        sol.businessUnit = dbsession.query(BusinessUnit).filter(BusinessUnit.id == sol.businessUnitId, BusinessUnit.isActive).one_or_none()

    if sol.ciId:
        sol.ci = dbsession.query(CI).filter(CI.id == sol.ciId).one_or_none()
    
    if sol.cdId:
        sol.cd = dbsession.query(CD).filter(CD.id == sol.cdId).one_or_none()
    
    if sol.sourceControlId:
        sol.sourceControl = dbsession.query(SourceControl).filter(SourceControl.id == sol.sourceControlId).one_or_none()
    
    return sol


def expand_solution_for_dac(sol, dbsession):
    environments = (
        dbsession.query(LZEnvironment)
        .filter(
            SolutionEnvironment.solutionId == sol.id,
            SolutionEnvironment.environmentId == LZEnvironment.id,
        )
        .all()
    )
    logger.debug("expand_solution_for_dac::environments: %s", environments)
    # 20200730 - Expand environments + lzvpc name
    sol.environments = environments
    for se in sol.environments:
        lzlanvpc = dbsession.query(LZLanVpc).filter(
            LZLanVpcEnvironment.environmentId == se.id,
            LZLanVpcEnvironment.lzlanvpcId == LZLanVpc.id,
            LZLanVpcEnvironment.isActive,
            LZLanVpc.isActive
        ).one_or_none()
        if lzlanvpc:
            se.sharedVPCProjectId = lzlanvpc.sharedVPCProjectId

    a_team = dbsession.query(Team).filter(Team.id == sol.teamId).one_or_none()
    sol.team = team_extension.expand_team_with_users(a_team)

    if sol.businessUnitId:
        businessUnit = dbsession.query(BusinessUnit).filter(BusinessUnit.id == sol.businessUnitId, BusinessUnit.isActive).one_or_none()
        if businessUnit:
            sol.businessUnit = businessUnit.name
        else:
            sol.businessUnit = ""
        
    if sol.ciId:
        ci = dbsession.query(CI).filter(CI.id == sol.ciId).one_or_none()
        if ci:
            sol.ci = ci.value
            
    if sol.cdId:
        cd = dbsession.query(CD).filter(CD.id == sol.cdId).one_or_none()
        if cd:
            sol.cd = cd.value

    if sol.sourceControlId:
        sourceControl = dbsession.query(SourceControl).filter(SourceControl.id == sol.sourceControlId).one_or_none()
        if sourceControl:
            sol.sourceControl = sourceControl.value 
    
    # set createdBy field
    logged_in_user = security.get_valid_user_from_token(dbsession = dbsession)
    logger.debug("logged_in_user: %s", logged_in_user)
    if logged_in_user:
        sol.createdBy = f"{logged_in_user.firstName} {logged_in_user.lastName}"
    else:
        sol.createdBy = ""
    return sol


def create_solution_environments(solutionId, list_of_env_ids, dbsession):
    """
    Args:
        solutionId ([int]): [The Solution id]
        list_of_env_ids ([list]): [A list of LZEnvironment ids]

        1. Logically delete all active solution environments for this solution
        2. Reactivate the solution env relationship that are in this list: list_of_env_ids
        3. Create the solution env that are not in this list.

    """

    # Inactivates the active solution environments for this Solution (solutionId)
    envs = dbsession.query(SolutionEnvironment).filter(
        SolutionEnvironment.solutionId == solutionId,
        SolutionEnvironment.isActive
    ).all()
    for env in envs:
        env.isActive = False
    dbsession.flush()

    for env in list_of_env_ids:
        existing_sol_env = dbsession.query(SolutionEnvironment).filter(
            SolutionEnvironment.solutionId == solutionId,
            SolutionEnvironment.environmentId == env
        ).one_or_none()

        if existing_sol_env:
            existing_sol_env.isActive = True
            dbsession.merge(existing_sol_env)
        else:
            new_env_solution = SolutionEnvironment(
                solutionId = solutionId, 
                environmentId = env,
                lastUpdated = ModelTools.get_utc_timestamp(),
                isActive = True
            )
            dbsession.add(new_env_solution)
        logger.debug("Added solution environment: {new_env_solution} to transaction.")
