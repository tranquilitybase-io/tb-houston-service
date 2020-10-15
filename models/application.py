import logging
import json

from sqlalchemy.ext.declarative import declarative_base
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import pre_load

from config import db
from tb_houston_service.tools import ModelTools

logger = logging.getLogger("tb_houston_service.models")
Base = declarative_base()

class Application(Base):
    __tablename__ = "application"
    id = db.Column(db.Integer, primary_key=True)
    isActive = db.Column(db.Boolean)
    lastUpdated = db.Column(db.String(20))
    isFavourite = db.Column(db.Boolean)
    solutionId = db.Column(db.Integer, db.ForeignKey("solution.id"))
    activatorId = db.Column(db.Integer, db.ForeignKey("activator.id"))
    name = db.Column(db.String(255))
    env = db.Column(db.String(64))
    status = db.Column(db.String(64))
    description = db.Column(db.String(255))
    resources = db.Column(db.String(255))

    def __repr__(self):
        return "<Application(id={self.id!r}, name={self.name!r})>".format(self=self)

class ApplicationSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Application
        include_fk = True
        load_instance = True

    @pre_load()
    def serialize_pre_load(self, data):
        logger.debug("ApplicationSchema::pre_load::serialize_pre_load: %s", data)
        data["lastUpdated"] = ModelTools.get_utc_timestamp()
        if "isActive" not in data:
            data["isActive"] = True
        if "isFavourite" not in data:
            data["isFavourite"] = False
        if "resources" in data:
            data["resources"] = json.dumps(data["resources"])
        else:
            data["resources"] = "[]"
        return data
