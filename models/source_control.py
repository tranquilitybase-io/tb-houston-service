from sqlalchemy.ext.declarative import declarative_base
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from config import db

Base = declarative_base()

class SourceControl(Base):
    __tablename__ = "sourcecontrol"
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(255))

class SourceControlSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = SourceControl
        include_fk = True
        load_instance = True
