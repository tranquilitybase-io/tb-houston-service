import json
import logging

from marshmallow import pre_load

from config import db, ma
from tb_houston_service.tools import ModelTools

logger = logging.getLogger("tb_houston_service.models")


class Application(db.Model):
    __tablename__ = "application"
    __table_args__ = {"schema": "eagle_db"}
    id = db.Column(db.Integer, primary_key=True)
    isActive = db.Column(db.Boolean)
    lastUpdated = db.Column(db.String(20))
    isFavourite = db.Column(db.Boolean)
    solutionId = db.Column(db.Integer, db.ForeignKey("eagle_db.solution.id"))
    activatorId = db.Column(db.Integer, db.ForeignKey("eagle_db.activator.id"))
    name = db.Column(db.String(255))
    env = db.Column(db.String(64))
    status = db.Column(db.String(64))
    description = db.Column(db.String(255))
    resources = db.Column(db.String(255))

    def __repr__(self):
        return "<Application(id={self.id!r}, name={self.name!r})>".format(self=self)


class ApplicationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Application
        include_fk = True
        load_instance = True

    @pre_load()
    def serialize_pre_load(self, data, **kwargs):
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
