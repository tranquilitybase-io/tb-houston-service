from sqlalchemy import ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from config import db

Base = declarative_base()

class ActivatorMetadataVariable(Base):
    __tablename__ = "activatorMetadataVariables"
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    activatorMetadataId = db.Column(db.Integer(), ForeignKey("activatorMetadata.id"))
    name = db.Column(db.String(255))
    type = db.Column(db.String(255))
    value = db.Column(db.String(255))
    defaultValue = db.Column(db.String(255))   
    isOptional = db.Column(db.Boolean())

    def __repr__(self):
        return "<ActivatorMetadataVariable(id={self.id!r}, activatorMetadataId={self.activatorMetadataId!r})>".format(self=self)

class ActivatorMetadataVariableSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ActivatorMetadataVariable
        include_fk = True
        load_instance = True
