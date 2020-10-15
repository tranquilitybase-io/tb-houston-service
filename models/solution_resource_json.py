from sqlalchemy.ext.declarative import declarative_base
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from config import db

Base = declarative_base()

class SolutionResourceJSON(Base):
    __tablename__ = "solutionresourcejson"
    solutionId = db.Column(db.Integer(), primary_key=True)
    json = db.Column(db.String(30000))

class SolutionResourceJSONSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = SolutionResourceJSON
        include_fk = True
        load_instance = True
