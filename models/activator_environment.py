from sqlalchemy import ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from config import db

Base = declarative_base()

class ActivatorEnvironment(Base):
    __tablename__ = "activatorEnvironment"
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    activatorId = db.Column(db.Integer(), ForeignKey("activator.id"))
    envId = db.Column(db.Integer(), ForeignKey("lzenvironment.id"))
    lastUpdated = db.Column(db.String(20))
    isActive = db.Column(db.Boolean())

    def __repr__(self):
        return "<Activator(id={self.id!r}, activatorId={self.activatorId!r}, activatorId={self.envId!r})>".format(
            self=self
        )

class ActivatorEnvironmentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ActivatorEnvironment
        include_fk = True
        load_instance = True
