import logging
import json

from marshmallow import pre_load

from config import db, ma
from tb_houston_service.tools import ModelTools

logger = logging.getLogger("tb_houston_service.models")

class Activator(db.Model):
    __tablename__ = "activator"
    __table_args__ = {'schema': 'eagle_db'}
    id = db.Column(db.Integer, primary_key=True)
    isActive = db.Column(db.Boolean)
    lastUpdated = db.Column(db.String(20))
    isFavourite = db.Column(db.Boolean)
    name = db.Column(db.String(255))
    available = db.Column(db.Boolean())
    sensitivity = db.Column(db.String(255))
    userCapacity = db.Column(db.Integer)
    serverCapacity = db.Column(db.Integer)
    regions = db.Column(db.String(255))
    hosting = db.Column(db.String(255))
    apiManagement = db.Column(db.String(255))
    sourceControlId = db.Column(db.Integer, db.ForeignKey("eagle_db.sourcecontrol.id"))
    businessUnitId = db.Column(db.Integer)
    technologyOwner = db.Column(db.String(255))
    technologyOwnerEmail = db.Column(db.String(255))
    billing = db.Column(db.String(255))
    activator = db.Column(db.String(255))
    status = db.Column(db.String(255))
    accessRequestedById = db.Column(db.Integer, db.ForeignKey("eagle_db.user.id"))
    source = db.Column(db.String(100))
    gitRepoUrl = db.Column(db.String(255))
    gitSnapshotJson = db.Column(db.String(2048))

    @staticmethod
    def get_git_clone_url() -> str:
        try:
            return Activator.gitSnapshotJson["git_clone_url"]
        except Exception as ex:
            logger.exception(ex)

    def __repr__(self):
        return "<Activator(id={self.id!r}, name={self.name!r})>".format(self=self)


class ActivatorSchema(ma.ModelSchema):
    class Meta:
        model = Activator
        include_fk = True
        load_instance = True

    @pre_load()
    def serialize_pre_load(self, data, **kwargs):
        logger.debug("ActivatorSchema::pre_load::serialize_pre_load: %s", data)
        data["lastUpdated"] = ModelTools.get_utc_timestamp()
        if "isActive" not in data:
            data["isActive"] = True
        if "isFavourite" not in data:
            data["isFavourite"] = False
        if "envs" in data:
            data["envs"] = json.dumps(data["envs"])
        if "regions" in data:
            data["regions"] = json.dumps(data["regions"])
        if "hosting" in data:
            data["hosting"] = json.dumps(data["hosting"])
        if "apiManagement" in data:
            data["apiManagement"] = json.dumps(data["apiManagement"])
        if data.get("accessRequestedById") == 0:
            data["accessRequestedById"] = None
        return data
