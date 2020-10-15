from sqlalchemy.ext.declarative import declarative_base
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from config import db

Base = declarative_base()

class LZMetadata(Base):
    __tablename__ = "lzmetadata"
    key = db.Column(db.String(), primary_key=True)
    value = db.Column(db.String())

class LZMetadataSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = LZMetadata
        include_fk = True
        load_instance = True
