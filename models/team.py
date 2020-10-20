import logging

from marshmallow import pre_load

from config import db, ma
from tb_houston_service.tools import ModelTools

logger = logging.getLogger("tb_houston_service.models")

class Team(db.Model):
    __tablename__ = "team"
    __table_args__ = {'schema': 'eagle_db'}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(200))
    cloudIdentityGroup = db.Column(db.String(200))
    businessUnitId = db.Column(db.Integer)
    lastUpdated = db.Column(db.String(20))
    isActive = db.Column(db.Boolean())
    accessRequestedById = db.Column(db.Integer, db.ForeignKey("eagle_db.user.id")) 

class TeamSchema(ma.ModelSchema):
    class Meta:
        model = Team
        include_fk = True
        load_instance = True

    @pre_load()
    def serialize_pre_load(self, data, **kwargs):
        logger.debug("TeamSchem::pre_load::serialize_pre_load: %s", data) 
        data["lastUpdated"] = ModelTools.get_utc_timestamp()        
        if 'isActive' not in data:
            data['isActive'] = True
        if data.get('accessRequestedById') == 0:
            data['accessRequestedById'] = None
        if data.get('cloudIdentityGroup') is None:
            data['cloudIdentityGroup'] = ''

        return data
