from sqlalchemy import ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from config import db

Base = declarative_base()

class ActivatorCD(Base):
    __tablename__ = "activatorCD"
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    activatorId = db.Column(db.Integer(), ForeignKey("activator.id"))
    cdId = db.Column(db.Integer(), ForeignKey("cd.id"))
    lastUpdated = db.Column(db.String(20))
    isActive = db.Column(db.Boolean())

    def __repr__(self):
        return "<Activator(id={self.id!r}, activatorId={self.activatorId!r}, activatorId={self.cdId!r})>".format(
            self=self
        )

class ActivatorCDSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ActivatorCD
        include_fk = True
        load_instance = True