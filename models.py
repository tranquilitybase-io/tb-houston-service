from datetime import datetime
from marshmallow import fields, pre_load, post_dump
from config import db, ma, app
import json

class ModelTools():

    def get_utc_epoch(self):
        return datetime.utcnow().strftime('%s')

    def get_utc_timestamp(self):
        return datetime.utcnow().strftime(("%Y-%m-%d %H:%M:%S"))

    def get_timestamp(self):
        return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))

    def datetime_as_string(dt):
        if dt is None:
            return datetime.utcnow().strftime(("%Y-%m-%d %H:%M:%S"))
        else:
            return dt.strftime("%Y-%m-%d %H:%M:%S")

    def load_json_array(s):
        try:
            return json.loads(s)
        except Exception as e:
            return []

    def json_dump(obj):
        #return json.dumps(obj, indent=2, sort_keys=True)
        return json.dumps(obj)

    # simple redact function, used prior to logging
    def redact_dict(my_dict):
        new_dict = my_dict.copy()
        new_dict['username'] = "XXXXX"
        new_dict['password'] = "XXXXX"
        return new_dict

# Activator
class Activator(db.Model):
    __tablename__ = "activator"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    type = db.Column(db.String(255))
    available = db.Column(db.Boolean)
    sensitivity = db.Column(db.String(255))
    category = db.Column(db.String(255))
    envs = db.Column(db.String(255))
    platforms = db.Column(db.String(255))
    lastUpdated = db.Column(db.String(255))
    userCapacity = db.Column(db.Integer)
    serverCapacity = db.Column(db.Integer)
    regions = db.Column(db.String(255))
    hosting = db.Column(db.String(255))
    apiManagement = db.Column(db.String(255))
    ci = db.Column(db.String(255))
    cd = db.Column(db.String(255))
    sourceControl = db.Column(db.String(255))
    businessUnit = db.Column(db.String(255))
    technologyOwner = db.Column(db.String(255))
    technologyOwnerEmail  = db.Column(db.String(255))
    billing = db.Column(db.String(255))
    activator = db.Column(db.String(255))
    resources = db.Column(db.String(255))
    status = db.Column(db.String(255))
    description = db.Column(db.String(255))


class ActivatorSchema(ma.ModelSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = Activator
        sqla_session = db.session

    @pre_load
    def serialize_arrays(self, in_data, **kwargs):
        try:
            in_data["ci"] = json.dumps(in_data["ci"])
        except Exception as e:
            app.logger.warning(e)
        try:
            in_data["cd"] = json.dumps(in_data["cd"])
        except Exception as e:
            app.logger.warning(e)
        try:
            in_data["resources"] = json.dumps(in_data["resources"])
        except Exception as e:
            app.logger.warning(e)
        try:
            in_data["hosting"] = json.dumps(in_data["hosting"])
        except Exception as e:
            app.logger.warning(e)
        try:
            in_data["envs"] = json.dumps(in_data["envs"])
        except Exception as e:
            app.logger.warning(e)
        try:
            in_data["sourceControl"] = json.dumps(in_data["sourceControl"])
        except Exception as e:
            app.logger.warning(e)
        try:
            in_data["regions"] = json.dumps(in_data["regions"])
        except Exception as e:
            app.logger.warning(e)
        try:
            in_data["apiManagement"] = json.dumps(in_data["apiManagement"])
        except Exception as e:
            app.logger.warning(e)
        try:
            in_data["platforms"] = json.dumps(in_data["platforms"])
        except Exception as e:
            app.logger.warning(e)
        return in_data

    @post_dump
    def deserialize_arrays(self, out_data, many, **kwargs):
        try:
            out_data["ci"] = json.loads(out_data["ci"])
        except Exception as e:
            app.logger.warning(e)
        try:
            out_data["cd"] = json.loads(out_data["cd"])
        except Exception as e:
            app.logger.warning(e)
        try:
            out_data["resources"] = json.loads(out_data["resources"])
        except Exception as e:
            app.logger.warning(e)
        try:
            out_data["hosting"] = json.loads(out_data["hosting"])
        except Exception as e:
            app.logger.warning(e)
        try:
            out_data["envs"] = json.loads(out_data["envs"])
        except Exception as e: 
            app.logger.warning(e)
        try:
            out_data["sourceControl"] = json.loads(out_data["sourceControl"])
        except Exception as e: 
            app.logger.warning(e)
        try:
            out_data["regions"] = json.loads(out_data["regions"])
        except Exception as e: 
            app.logger.warning(e)
        try:
            out_data["apiManagement"] = json.loads(out_data["apiManagement"])
        except Exception as e: 
            app.logger.warning(e)
        try:
            out_data["platforms"] = json.loads(out_data["platforms"])
        except Exception as e: 
            app.logger.warning(e)
        return out_data

# Application
class Application(db.Model):
    __tablename__ = "application"
    id = db.Column(db.Integer, primary_key=True)
    solutionId = db.Column(db.Integer, db.ForeignKey('solution.id'))
    activatorId = db.Column(db.Integer, db.ForeignKey('activator.id'))
    name = db.Column(db.String(255))
    env = db.Column(db.String(64))
    status = db.Column(db.String(64))
    description = db.Column(db.String(255))

class ApplicationSchema(ma.ModelSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = Application
        sqla_session = db.session

# Solutions
class Solution(db.Model):
    __tablename__ = "solution"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.String(255))
    businessUnit = db.Column(db.String(255))
    costCentre = db.Column(db.String(255))
    ci = db.Column(db.String(255))
    cd = db.Column(db.String(255))
    sourceControl = db.Column(db.String(255))
    environments = db.Column(db.String(255))
    active = db.Column(db.Boolean)
    favourite = db.Column(db.Boolean)
    teams = db.Column(db.Integer())
    lastUpdated = db.Column(db.String(255))

    applications = db.relationship('Application')

class SolutionSchema(ma.ModelSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = Solution
        sqla_session = db.session

    @pre_load
    def serialize_arrays(self, in_data, **kwargs):
        try:
            in_data["environments"] = json.dumps(in_data["environments"])
        except Exception as e:
            app.logger.warning(e)
        return in_data

    @post_dump
    def deserialize_arrays(self, out_data, many, **kwargs):
        try:
            out_data["environments"] = json.loads(out_data["environments"])
        except Exception as e:
            app.logger.warning(e)
        return out_data

# class ApplicationActivatorSchema(ma.ModelSchema):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#
#     class Meta:
#         model = Application
#         sqla_session = db.session
#
#     id = fields.Int()
#     name = fields.Str()
#     activators = fields.Nested('ActivatorSchema')

# Team
class Team(db.Model):
    __tablename__ = "team"
    key = db.Column(db.String(255), primary_key=True)
    value = db.Column(db.String(255))


class TeamSchema(ma.ModelSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = Team
        sqla_session = db.session

# Environment
class Environment(db.Model):
    __tablename__ = "environment"
    key = db.Column(db.String(255), primary_key=True)
    value = db.Column(db.String(255))

class EnvironmentSchema(ma.ModelSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = Environment
        sqla_session = db.session

# CI
class CI(db.Model):
    __tablename__ = "ci"
    key = db.Column(db.String(255), primary_key=True)
    value = db.Column(db.String(255))


class CISchema(ma.ModelSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = CI
        sqla_session = db.session
# CD
class CD(db.Model):
    __tablename__ = "cd"
    key = db.Column(db.String(255), primary_key=True)
    value = db.Column(db.String(255))


class CDSchema(ma.ModelSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = CD
        sqla_session = db.session

# SourceControl
class SourceControl(db.Model):
    __tablename__ = "sourcecontrol"
    key = db.Column(db.String(255), primary_key=True)
    value = db.Column(db.String(255))

class SourceControlSchema(ma.ModelSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = SourceControl
        sqla_session = db.session

# BusinessUnit
class BusinessUnit(db.Model):
    __tablename__ = "businessunit"
    key = db.Column(db.String(255), primary_key=True)
    value = db.Column(db.String(255))


class BusinessUnitSchema(ma.ModelSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = BusinessUnit
        sqla_session = db.session
# LandingZoneProgressItem
class LandingZoneProgressItem(db.Model):
    __tablename__ = "landingzoneprogressitem"
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String)
    completed = db.Column(db.Boolean)

class LandingZoneProgressItemSchema(ma.ModelSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = LandingZoneProgressItem
        sqla_session = db.session

# LandingZoneAction
class LandingZoneAction(db.Model):
    __tablename__ = "landingzoneaction"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    categoryName = db.Column(db.String)
    categoryClass= db.Column(db.String)
    completionRate = db.Column(db.Integer)
    locked = db.Column(db.Boolean)

class LandingZoneActionSchema(ma.ModelSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = LandingZoneAction
        sqla_session = db.session


# class SolutionEnhancedSchema(ma.ModelSchema):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#
#     class Meta:
#         model = Solution
#         sqla_session = db.session
#
#     # applications = fields.Nested('ApplicationActivatorSchema')
#
#     @pre_load
#     def serialize_arrays(self, in_data, **kwargs):
#         try:
#             in_data["environments"] = json.dumps(in_data["environments"])
#         except Exception as e:
#             app.logger.warning(e)
#         return in_data
#
#     @post_dump
#     def deserialize_arrays(self, out_data, many, **kwargs):
#         try:
#             out_data["environments"] = json.loads(out_data["environments"])
#         except Exception as e:
#             app.logger.warning(e)
#         return out_data

