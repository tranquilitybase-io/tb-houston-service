import logging

from sqlalchemy.ext.declarative import declarative_base
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import pre_load

from config import db
from tb_houston_service.tools import ModelTools

logger = logging.getLogger("tb_houston_service.models")
Base = declarative_base()

class Solution(Base):
    __tablename__ = "solution"
    id = db.Column(db.Integer(), primary_key=True)
    isActive = db.Column(db.Boolean)
    lastUpdated = db.Column(db.String(20))
    isFavourite = db.Column(db.Boolean)
    name = db.Column(db.String(30))
    description = db.Column(db.String(255))
    businessUnitId = db.Column(db.Integer())
    costCentre = db.Column(db.String(255))
    ciId = db.Column(db.Integer())
    cdId = db.Column(db.Integer())
    sourceControlId = db.Column(db.Integer())
    teamId = db.Column(db.Integer())
    deployed = db.Column(db.Boolean())
    deploymentState = db.Column(db.String(45))
    statusId = db.Column(db.Integer())
    statusCode = db.Column(db.String(45))
    statusMessage = db.Column(db.String(255))
    taskId = db.Column(db.String(100))
    deploymentFolderId = db.Column(db.String(50))

    def __repr__(self):
        return "<Solution(id={self.id!r}, name={self.name!r})>".format(self=self)


class SolutionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Solution
        include_fk = True
        load_instance = True

    @pre_load()
    def serialize_pre_load(self, data):
        logger.debug("SolutionSchema::pre_load::serialize_pre_load: %s", data)
        data["lastUpdated"] = ModelTools.get_utc_timestamp()
        if "isActive" not in data:
            data["isActive"] = True
        if "isFavourite" not in data:
            data["isFavourite"] = False
        if "name" in data:
            data["name"] = data["name"][: Solution.name.type.length]
        return data