from marshmallow import Schema, fields, pre_load, post_load, pre_dump, post_dump, pprint
#from flask import Flask

#from flask_sqlalchemy import SQLAlchemy
#from flask_marshmallow import Marshmallow
#import json

#app = Flask(__name__)
#db = SQLAlchemy(app)
#ma = Marshmallow(app)

class HealthSchema(Schema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    status = fields.Str()


class ExtendedActivatorSchema(Schema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    id = fields.Int()
    name = fields.Str()
    type = fields.Str()
    available = fields.Str()
    sensitivity = fields.Str()
    category = fields.Str()
    envs = fields.List(fields.Str())
    platforms = fields.List(fields.Str())
    lastUpdated = fields.Str()
    userCapacity = fields.Str()
    serverCapacity = fields.Str()
    regions = fields.List(fields.Str())
    hosting = fields.List(fields.Str())
    apiManagement = fields.List(fields.Str())
    ci = fields.List(fields.Str())
    cd = fields.List(fields.Str())
    sourceControl = fields.List(fields.Str())
    businessUnit = fields.Str()
    technologyOwner = fields.Str()
    technologyOwnerEmail  = fields.Str()
    billing = fields.Str()
    activator = fields.Str()
    resources = fields.List(fields.Dict())
    status = fields.Str()
    description = fields.Str()


class ExtendedApplicationSchema(Schema):
    solutionId = fields.Int()
    activatorId = fields.Int()
    name = fields.Str()
    env = fields.Str()
    status = fields.Str()
    description = fields.Str()
    activator = fields.Nested(ExtendedActivatorSchema(many=False))



class ExtendedSolutionSchema(Schema):
    __envelope__ = {"single": "solution", "many": "solutions"}

    id = fields.Int()
    name = fields.Str()
    description = fields.Str()
    buinessUnit = fields.Str()
    costCentre = fields.Str()
    ci = fields.Str()
    cd = fields.Str()
    sourceControl = fields.Str()
    environments = fields.List(fields.Str())
    active = fields.Boolean()
    favourite = fields.Boolean()
    teams = fields.Str()
    lastUpdated = fields.Str()
    applications = fields.Nested(ExtendedApplicationSchema(many=True))
