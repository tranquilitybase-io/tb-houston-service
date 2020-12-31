"""
This is the deployments module and supports all the ReST actions for the
solutions collection
"""
import logging

from flask import abort, make_response
from sqlalchemy import literal_column
from sqlalchemy.exc import SQLAlchemyError

from config.db_lib import db_session
from models import Solution, SolutionSchema
from tb_houston_service import security, solution_extension
from tb_houston_service.extendedSchemas import (
    ExtendedSolutionSchema,
    SolutionNamesOnlySchema,
)
from tb_houston_service.tools import ModelTools

logger = logging.getLogger("tb_houston_service.solution")


def read_all(
    isActive=None,
    isFavourite=None,
    isSandbox=None,
    namesonly=None,
    page=None,
    page_size=None,
    sort=None,
):
    """
    This function responds to a request for /api/solutions
    with the complete lists of solutions

    :return:        json string of list of solutions
    """
    logger.debug("solution.read_all")
    logger.debug(
        "Parameters: isActive: %s, isFavourite: %s, isSandbox: %s, namesonly: %s, page: %s, page_size: %s, sort: %s",
        isActive,
        isFavourite,
        isSandbox,
        namesonly,
        page,
        page_size,
        sort,
    )
    with db_session() as dbs:
        # pre-process sort instructions
        if sort == None:
            solution_query = dbs.query(Solution).order_by(Solution.id)
        else:
            try:
                sort_inst = [si.split(":") for si in sort]
                orderby_arr = []
                for si in sort_inst:
                    si1 = si[0]
                    if len(si) > 1:
                        si2 = si[1]
                    else:
                        si2 = "asc"
                    orderby_arr.append(f"{si1} {si2}")
                # print("orderby: {}".format(orderby_arr))
                solution_query = dbs.query(Solution).order_by(
                    literal_column(", ".join(orderby_arr))
                )
            except SQLAlchemyError as e:
                logger.warning("Exception: %s", e)
                solution_query = dbs.query(Solution).order_by(Solution.id)

        # filter solutions by logged in user id
        business_unit_ids = security.get_business_units_ids_for_user(dbsession=dbs)

        # Create the list of solutions from our data
        solution_query = solution_query.filter(
            (isActive == None or Solution.isActive == isActive),
            (isFavourite == None or Solution.isFavourite == isFavourite),
            (isSandbox == None or Solution.isSandbox == isSandbox),
            (
                business_unit_ids == None
                or Solution.businessUnitId.in_(business_unit_ids)
            ),
        )

        # do limit and offset last
        if page == None or page_size == None:
            solutions = solution_query.all()
        else:
            solutions = solution_query.limit(page_size).offset(page * page_size)

        if namesonly == True:
            # Serialize the data for the response
            schema = SolutionNamesOnlySchema(many=True)
            data = schema.dump(solutions)
        else:
            for sol in solutions:
                sol = solution_extension.expand_solution(sol, dbsession=dbs)
            schema = ExtendedSolutionSchema(many=True)
            data = schema.dump(solutions)

        logger.debug("read_all: %s", data)
        return data, 200


def read_one(oid):
    """
    This function responds to a request for /api/solution/{oid}
    with one matching solution from solutions

    :param application:   id of solution to find
    :return:              solution matching id
    """
    with db_session() as dbs:
        # filter solutions by logged in user
        business_unit_ids = security.get_business_units_ids_for_user(dbsession=dbs)
        sol = (
            dbs.query(Solution)
            .filter(
                Solution.id == oid,
                (
                    business_unit_ids == None
                    or Solution.businessUnitId.in_(business_unit_ids)
                ),
            )
            .one_or_none()
        )

        if sol is not None:
            solution = solution_extension.expand_solution(sol, dbsession=dbs)
            # Serialize the data for the response
            solution_schema = ExtendedSolutionSchema()
            data = solution_schema.dump(solution)
            return data, 200
        else:
            abort(404, f"Solution with id {oid} not found".format(id=oid))


def create(solutionDetails):
    """
    This function creates a new solution in the solutions list
    based on the passed in solutions data

    :param solution:  solution to create in solutions list
    :return:        201 on success, 406 on solutions exists
    """
    data = None
    with db_session() as dbs:
        # Defaults
        if solutionDetails.get("isActive") == None:
            solutionDetails["isActive"] = True

        if solutionDetails.get("isFavourite") == None:
            solutionDetails["isFavourite"] = False

        if solutionDetails.get("deployed") == None:
            solutionDetails["deployed"] = False

        if solutionDetails.get("deploymentState") == None:
            solutionDetails["deploymentState"] = ""

        if solutionDetails.get("statusId") == None:
            solutionDetails["statusId"] = 0

        if solutionDetails.get("statusCode") == None:
            solutionDetails["statusCode"] = ""

        if solutionDetails.get("statusMessage") == None:
            solutionDetails["statusMessage"] = ""

        if solutionDetails.get("isSandbox") == None:
            solutionDetails["isSandbox"] = False

        # Remove applications because Solutions don't have
        # any applications when they are first created
        if "applications" in solutionDetails:
            del solutionDetails["applications"]

        # we don't need the id, the is generated automatically on the database
        if "id" in solutionDetails:
            del solutionDetails["id"]

        solutionDetails["lastUpdated"] = ModelTools.get_utc_timestamp()
        envs = solutionDetails.get("environments")

        # Validate the business unit
        business_unit_ids = security.get_business_units_ids_for_user(dbsession=dbs)
        if business_unit_ids:
            business_unit = solutionDetails.get("businessUnitId")
            if business_unit not in business_unit_ids:
                abort(
                    400,
                    f"Unauthorized to create solutions for business unit {business_unit}",
                )
        else:
            # initially will let this pass, but in future we could abort if user is not a member of any business units
            pass

        # Removing this as the below schema is not expecting this field.
        if "environments" in solutionDetails:
            del solutionDetails["environments"]

        schema = SolutionSchema(many=False)

        new_solution = schema.load(solutionDetails, session=dbs)
        new_solution.lastUpdated = ModelTools.get_utc_timestamp()
        dbs.add(new_solution)
        dbs.flush()
        if envs:
            solution_extension.create_solution_environments(
                new_solution.id, envs, dbsession=dbs
            )
        new_solution = solution_extension.expand_solution(new_solution, dbsession=dbs)
        schema = ExtendedSolutionSchema()
        data = schema.dump(new_solution)

    # Serialize and return the newly created solution
    # in the response

    return data, 201


def update(oid, solutionDetails):
    """
    Updates an existing solutions in the solutions list.

    :param key:    key of the solutions to update in the solutions list
    :param solutions:   solutions to update
    :return:       updated solutions
    """
    logger.debug("update::solutionDetails: %s", solutionDetails)
    with db_session() as dbs:
        # Does the solutions exist in solutions list?
        existing_solution = dbs.query(Solution).filter(Solution.id == oid).one_or_none()

        # Does solutions exist?

        if existing_solution is not None:
            solutionDetails["id"] = oid

            # Validate the business unit
            business_unit_ids = security.get_business_units_ids_for_user(dbsession=dbs)
            if business_unit_ids:
                business_unit = solutionDetails.get("businessUnitId")
                if business_unit and business_unit not in business_unit_ids:
                    abort(
                        400,
                        f"Unauthorized to update solutions for business unit {business_unit}",
                    )
                business_unit = existing_solution.businessUnitId
                if business_unit and business_unit not in business_unit_ids:
                    abort(
                        400,
                        f"Unauthorized to update solutions for business unit {business_unit}",
                    )
            else:
                # initially will let this pass, but in future we could abort if user is not a member of any business units
                pass

            envs = solutionDetails.get("environments")
            # Remove envs as it's processed separately, but in the same transaction.
            if "environments" in solutionDetails:
                del solutionDetails["environments"]
                solution_extension.create_solution_environments(
                    oid, envs, dbsession=dbs
                )
            schema = SolutionSchema(many=False)
            new_solution = schema.load(solutionDetails, session=dbs)
            new_solution.lastUpdated = ModelTools.get_utc_timestamp()
            dbs.merge(new_solution)
            dbs.commit()

            new_solution = solution_extension.expand_solution(
                new_solution, dbsession=dbs
            )
            # return the updted solutions in the response
            schema = ExtendedSolutionSchema(many=False)
            data = schema.dump(new_solution)
            logger.debug("data: %s", data)
            return data, 200
            # otherwise, nope, deployment doesn't exist, so that's an error
        else:
            abort(404, f"Solution {oid} not found")


def delete(oid):
    """
    This function deletes a solution from the solutions list

    :param key: id of the solutions to delete
    :return:    200 on successful delete, 404 if not found
    """
    with db_session() as dbs:
        # Does the solution to delete exist?
        existing_solution = dbs.query(Solution).filter(Solution.id == oid).one_or_none()

        # Validate the business unit
        business_unit_ids = security.get_business_units_ids_for_user(dbsession=dbs)
        if business_unit_ids:
            business_unit = existing_solution.businessUnitId
            if business_unit and business_unit not in business_unit_ids:
                abort(
                    400,
                    f"Unauthorized to delete solutions for business unit {business_unit}",
                )
        else:
            pass

        # if found?
        if existing_solution is not None:
            existing_solution.isActive = False
            dbs.merge(existing_solution)
            dbs.commit()
            return make_response(f"Solution {oid} successfully deleted", 200)

        # Otherwise, nope, solution to delete not found
        else:
            abort(404, f"Solution {oid} not found")
