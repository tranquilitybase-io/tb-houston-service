from sqlalchemy.ext.declarative import declarative_base
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from config import db

Base = declarative_base()

class CloudRole(Base):
    __tablename__ = "cloudRole"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    cloudIdentityGroup = db.Column(db.String(200))
    description = db.Column(db.String(200))

class CloudRoleSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = CloudRole
        include_fk = True
        load_instance = True
