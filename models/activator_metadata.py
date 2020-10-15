from sqlalchemy import ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from config import db

Base = declarative_base()

class ActivatorMetadata(Base):
    __tablename__ = "activatorMetadata"
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    activatorId = db.Column(db.Integer(), ForeignKey("activator.id"))
    name = db.Column(db.String(255))
    description = db.Column(db.String(255))
    category = db.Column(db.String(255))
    typeId = db.Column(db.Integer(), ForeignKey("type.id"))
    activatorLink = db.Column(db.String(255))
    lastUpdated = db.Column(db.String(20))
    latestVersion = db.Column(db.String(30))
   
    def __repr__(self):
        return "<ActivatorMetadata(id={self.id!r}, name={self.name!r})>".format(self=self)

class ActivatorMetadataSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ActivatorMetadata
        include_fk = True
        load_instance = True
