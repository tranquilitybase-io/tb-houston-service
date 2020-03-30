from models import ModelTools
from models import Application
from models import Activator
import application_extension


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
    'environments': ModelTools.load_json_array(sol.environments),
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
