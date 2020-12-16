import logging

from marshmallow import pre_load, fields

from config import db, ma
from tb_houston_service.tools import ModelTools

logger = logging.getLogger("tb_houston_service.models")


class SystemSettings(db.Model):
    __tablename__ = "systemsettings"
    __table_args__ = {'schema': 'eagle_db'}
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer)
    username = db.Column(db.String(255))
    token = db.Column(db.String(255))
    lastUpdated = db.Column(db.String(20))

    def __repr__(self):
        return f"<SystemSettings(id={self.id!r}, username={self.username!r}, token={self.token!r})>"


class SystemSettingsSchema(ma.ModelSchema):
    class Meta:
        model = SystemSettings
        include_fk = True
        load_instance = True

    @pre_load()
    def serialize_pre_load(self, data, **kwargs):
        logger.debug(
            "SystemSettingsSchema::pre_load::serialize_pre_load: %s", data)
        data["lastUpdated"] = ModelTools.get_utc_timestamp()
        if "id" in data:
            del data["id"]
        return data


class SystemSettingsResultSchema(ma.ModelSchema):
    username = fields.Str()
    token = fields.Str()
    lastUpdated = fields.Str()
