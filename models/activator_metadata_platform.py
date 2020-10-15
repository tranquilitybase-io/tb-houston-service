from sqlalchemy import ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from config import db

Base = declarative_base()

class ActivatorMetadataPlatform(Base):
    __tablename__ = "activatorMetadataPlatform"
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    activatorMetadataId = db.Column(db.Integer(), ForeignKey("activatorMetadata.id"))
    platformId = db.Column(db.Integer(), ForeignKey("platform.id"))
    lastUpdated = db.Column(db.String(20))
    isActive = db.Column(db.Boolean())

    def __repr__(self):
        return "<ActivatorMetadataPlatform(id={self.id!r}, activatorMetadataId={self.activatorMetadataId!r})>".format(self=self)

class ActivatorMetadataPlatformSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ActivatorMetadataPlatform
        include_fk = True
        load_instance = True
