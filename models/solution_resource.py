from sqlalchemy.ext.declarative import declarative_base
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from config import db

Base = declarative_base()

class SolutionResource(Base):
    __tablename__ = "solutionresource"
    solutionId = db.Column(db.Integer(), primary_key=True)
    key = db.Column(db.String(50), primary_key=True)
    value = db.Column(db.String(255))

class SolutionResourceSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = SolutionResource
        include_fk = True
        load_instance = True
