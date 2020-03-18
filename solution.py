"""
This is the deployments module and supports all the ReST actions for the
solutions collection
"""

# System modules
from datetime import datetime

# 3rd party modules
from flask import make_response, abort, jsonify
from config import db, app
from models import Application, Activator
from models import Solution, SolutionSchema
from models import ModelTools
from extendedSchemas import ExtendedSolutionSchema
from pprint import pformat


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
    app_dict = {}
    for ap in apps:
      app_dict = {
        'id': ap.id,
        'name': ap.name,
        'env': ap.env,
        'status': ap.status,
        'description': ap.description
      }
      acts = Activator.query.filter(Activator.id == ap.activatorId).all()
      act_dict = {}
      for act in acts:
        act_dict = { 
          'name': act.name,
          'type': act.type,
          'available': act.available,
          'sensitivity': act.sensitivity,
          'category': act.category,
          'envs': ModelTools.load_json_array(act.envs),
          'platforms': ModelTools.load_json_array(act.platforms),
          'lastUpdated': ModelTools.datetime_as_string(act.lastUpdated),
          'userCapacity': act.userCapacity,
          'serverCapacity': act.serverCapacity,
          'regions': ModelTools.load_json_array(act.regions),
          'hosting': ModelTools.load_json_array(act.hosting),
          'apiManagement': ModelTools.load_json_array(act.apiManagement),
          'ci': ModelTools.load_json_array(act.ci),
          'cd': ModelTools.load_json_array(act.cd),
          'sourceControl': ModelTools.load_json_array(act.sourceControl),
          'businessUnit': act.businessUnit,
          'technologyOwner': act.technologyOwner,
          'technologyOwnerEmail': act.technologyOwnerEmail,
          'billing': act.billing,
          'activator': act.activator,
          'resources': ModelTools.load_json_array(act.resources),
          'status': act.status,
          'description': act.description
        }
      app_dict['activator'] = act_dict
      app_arr.append(app_dict)

  sol_dict['applications'] = app_arr
  return sol_dict


def read_all():
    """
    This function responds to a request for /api/solutions
    with the complete lists of solutions

    :return:        json string of list of solutions
    """

    # Create the list of solutions from our data
    solutions = Solution.query.order_by(Solution.id).all()
    app.logger.debug("solution.read_all")

    solutions_arr = []
    for sol in solutions:
        solutions_arr.append(build_solution(sol))

    app.logger.debug("solutions array:")
    app.logger.debug(pformat(solutions_arr))

    # Serialize the data for the response
    schema = ExtendedSolutionSchema(many=True)
    data = schema.dump(solutions_arr)
    app.logger.debug("solutions data:")
    app.logger.debug(data)
    return data


def read_one(id):
    """
    This function responds to a request for /api/solution/{id}
    with one matching solution from solutions

    :param application:   id of solution to find
    :return:              solution matching id
    """

    sol = (Solution.query.filter(Solution.id == id).one_or_none())

    if sol is not None:
        solution = build_solution(sol)
        # Serialize the data for the response
        solution_schema = ExtendedSolutionSchema()
        data = solution_schema.dump(solution)
        return data
    else:
        abort(
            404, "Solution with id {id} not found".format(id=id)
        )


def create(solution):
    """
    This function creates a new solution in the solutions list
    based on the passed in solutions data

    :param solution:  solution to create in solutions list
    :return:        201 on success, 406 on solutions exists
    """

    app.logger.debug("Before")
    app.logger.debug(pformat(solution))

    lastUpdated = ModelTools.get_utc_timestamp()

    # Defaults
    if (solution.get('active') == None):
      solution['active'] = True

    if (solution.get('favourite') == None):
      solution['favourite'] = True

    if (solution.get('teams') == None):
      solution['teams'] = 0

    # Remove applications because Solutions don't have 
    # any applications when they are first created
    if ('applications' in solution):
      del solution['applications']

    # we don't need the id, the is generated automatically on the database
    if ('id' in solution):
      del solution["id"]

    solution['lastUpdated'] = ModelTools.get_utc_timestamp()
      
    app.logger.debug("After")
    app.logger.debug(pformat(solution))

    schema = SolutionSchema()
    new_solution = schema.load(solution, session=db.session)
    db.session.add(new_solution)
    db.session.commit()

    # Serialize and return the newly created solution
    # in the response
    data = schema.dump(new_solution)
    return data, 201


def update(id, solution):
    """
    This function updates an existing solutions in the solutions list

    :param key:    key of the solutions to update in the solutions list
    :param solutions:   solutions to update
    :return:       updated solutions
    """

    app.logger.debug(solution)

    # Does the solutions exist in solutions list?
    existing_solution = Solution.query.filter(
            Solution.id == id
    ).one_or_none()

    # Does solutions exist?

    if existing_solution is not None:
        schema = SolutionSchema()
        update_solution = schema.load(solution, session=db.session)
        update_solution.key = solution['id']
        update_solution.lastUpdated = ModelTools.get_utc_timestamp()

        db.session.merge(update_solution)
        db.session.commit()

        # return the updted solutions in the response
        data = schema.dump(update_solution)
        return data, 200

    # otherwise, nope, deployment doesn't exist, so that's an error
    else:
        abort(404, f"Solution not found")


def delete(id):
    """
    This function deletes a solution from the solutions list

    :param key: id of the solutions to delete
    :return:    200 on successful delete, 404 if not found
    """
    # Does the solution to delete exist?
    existing_solution = Solution.query.filter(Solution.id == id).one_or_none()

    # if found?
    if existing_solution is not None:
        db.session.delete(existing_solution)
        db.session.commit()

        return make_response(f"Solution {id} successfully deleted", 200)

    # Otherwise, nope, solution to delete not found
    else:
        abort(404, f"Solution {id} not found")


