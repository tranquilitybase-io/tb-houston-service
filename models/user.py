import logging

from sqlalchemy.ext.declarative import declarative_base
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import pre_load

from config import db
from tb_houston_service.tools import ModelTools

logger = logging.getLogger("tb_houston_service.models")
Base = declarative_base()

class User(Base):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    firstName = db.Column(db.String(100))
    lastName = db.Column(db.String(100))
    isAdmin = db.Column(db.Boolean(), default=False)
    isActive = db.Column(db.Boolean(), default=True)
    showWelcome = db.Column(db.Boolean(), default=True)
    lastUpdated = db.Column(db.String(20))

    def __repr__(self):
        return "<User(id={self.id!r}, email={self.email!r})>".format(
            self=self
        )


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_fk = True
        load_instance = True

    @pre_load()
    def serialize_pre_load(self, data):
        logger.debug("UserSchema::pre_load::serialize_pre_load: %s", data)
        data["lastUpdated"] = ModelTools.get_utc_timestamp()
        return data