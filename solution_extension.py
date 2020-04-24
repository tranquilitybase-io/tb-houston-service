from models import ModelTools
from models import Application
import application_extension
import json


def build_solution(sol):
  sol_dict = {
    'id': sol.id,
    'name': sol.name,
    'description': sol.description,
    'businessUnit': sol.businessUnit,
    'costCentre': sol.costCentre,
    'ci': sol.ci,
    'cd': sol.cd,
    'sourceControl': sol.sourceControl,
    'environments': json.loads(sol.environments or '[]'),
    'active': sol.active,
    'favourite': sol.favourite,
    'teams': sol.teams,
    'lastUpdated': ModelTools.datetime_as_string(sol.lastUpdated)
  }

  apps = Application.query.filter(Application.solutionId == sol.id).all()
  app_arr = []
  if apps is not None:
    for ap in apps:
      app_dict = application_extension.build_application(ap)
      app_arr.append(app_dict)

  sol_dict['applications'] = app_arr
  return sol_dict
