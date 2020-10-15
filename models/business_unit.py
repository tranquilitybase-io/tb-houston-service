from sqlalchemy.ext.declarative import declarative_base
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from config import db

Base = declarative_base()

class BusinessUnit(Base):
    __tablename__ = "businessunit"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(200))
    isActive = db.Column(db.Boolean())

    def __repr__(self):
        return "<BusinessUnit(id={self.id!r}, name={self.name!r})>".format(self=self)

class BusinessUnitSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = BusinessUnit
        include_fk = True
        load_instance = True
