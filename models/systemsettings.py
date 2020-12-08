import logging

from marshmallow import pre_load

from config import db, ma
from tb_houston_service.tools import ModelTools

logger = logging.getLogger("tb_houston_service.models")


class Systemsettings(db.Model):
    __tablename__ = "systemsettings"
    __table_args__ = {'schema': 'eagle_db'}
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer)
    username = db.Column(db.String(255))
    token = db.Column(db.Bytes(255))

    def __repr__(self):
        return "<Systemsettings(id={self.id!r}, user={self.user!r})>".format(
            self=self
        )


class SystemsettingsSchema(ma.ModelSchema):
    class Meta:
        model = Systemsettings
        include_fk = True
        load_instance = True

    @pre_load()
    def serialize_pre_load(self, data, **kwargs):
        logger.debug("SystemsettingsSchema::pre_load::serialize_pre_load: %s", data)
        data["lastUpdated"] = ModelTools.get_utc_timestamp()
        return data
