from sqlalchemy.ext.declarative import declarative_base
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from config import db

Base = declarative_base()

class SubnetMode(Base):
    __tablename__ = "subnetmode"
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String)
    value = db.Column(db.String)

class SubnetModeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = SubnetMode
        include_fk = True
        load_instance = True
