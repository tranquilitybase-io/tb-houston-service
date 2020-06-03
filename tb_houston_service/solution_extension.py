import json
from config import db
from tb_houston_service.tools import ModelTools
from tb_houston_service.models import Application
from tb_houston_service.models import Team
from tb_houston_service import application_extension


def build_solution(sol):
    sol_dict = {
        "id": sol.id,
        "name": sol.name,
        "description": sol.description,
        "businessUnit": sol.businessUnit,
        "costCentre": sol.costCentre,
        "ci": sol.ci,
        "cd": sol.cd,
        "sourceControl": sol.sourceControl,
        "environments": json.loads(sol.environments or "[]"),
        "active": sol.active,
        "favourite": sol.favourite,
        "teamId": sol.teamId,
        "lastUpdated": ModelTools.datetime_as_string(sol.lastUpdated),
        "deploymentFolderId": sol.deploymentFolderId,
    }

    apps = db.session.query(Application).filter(Application.solutionId == sol.id).all()
    app_arr = []
    if apps is not None:
        for ap in apps:
            app_dict = application_extension.build_application(ap)
            app_arr.append(app_dict)

    sol_dict["applications"] = app_arr

    team = db.session.query(Team).filter(Team.id == sol.teamId).one_or_none()
    sol_dict["team"] = team

    return sol_dict
