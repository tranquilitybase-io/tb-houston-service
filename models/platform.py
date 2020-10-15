from sqlalchemy.ext.declarative import declarative_base
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from config import db

Base = declarative_base()

class Platform(Base):
    __tablename__ = "platform"
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(255))

    def __repr__(self):
        return "<CI(id={self.id!r}, name={self.id!r})>".format(self=self)

class PlatformSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Platform
        include_fk = True
        load_instance = True
