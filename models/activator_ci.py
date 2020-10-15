from sqlalchemy import ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from config import db

Base = declarative_base()

class ActivatorCI(Base):
    __tablename__ = "activatorCI"
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    activatorId = db.Column(db.Integer(), ForeignKey("activator.id"))
    ciId = db.Column(db.Integer(), ForeignKey("ci.id"))
    lastUpdated = db.Column(db.String(20))
    isActive = db.Column(db.Boolean())

    def __repr__(self):
        return "<Activator(id={self.id!r}, activatorId={self.activatorId!r}, activatorId={self.ciId!r})>".format(
            self=self
        )

class ActivatorCISchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ActivatorCI
        include_fk = True
        load_instance = True