from sqlalchemy import ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from config import db

Base = declarative_base()

class SolutionEnvironment(Base):
    __tablename__ = "solutionenvironment"
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    solutionId = db.Column(db.Integer(), ForeignKey("solution.id"))
    environmentId = db.Column(db.Integer(), ForeignKey("lzenvironment.id"))
    lastUpdated = db.Column(db.String(20))
    isActive = db.Column(db.Boolean())

    def __repr__(self):
        return "<Solution(id={self.id!r}, solutionId={self.solutionId!r}, solutionId={self.environmentId!r})>".format(
            self=self
        )

class SolutionEnvironmentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = SolutionEnvironment
        include_fk = True
        load_instance = True
