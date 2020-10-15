from sqlalchemy.ext.declarative import declarative_base
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from config import db

Base = declarative_base()

class LandingZoneProgressItem(Base):
    __tablename__ = "landingzoneprogressitem"
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String)
    completed = db.Column(db.Boolean())

    def __repr__(self):
        return "<LandingZoneProgressItem(id={self.id!r}, name={self.label!r})>".format(
            self=self
        )

class LandingZoneProgressItemSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = LandingZoneProgressItem
        include_fk = True
        load_instance = True
