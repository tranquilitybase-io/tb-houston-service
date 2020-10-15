from sqlalchemy.ext.declarative import declarative_base
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from config import db

Base = declarative_base()

class UserCloudRole(Base):
    __tablename__ = "userCloudRole"
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer)
    cloudRoleId = db.Column(db.Integer)
    isActive = db.Column(db.Boolean())

class UserCloudRoleSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = UserCloudRole
        include_fk = True
        load_instance = True
