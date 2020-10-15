from sqlalchemy.ext.declarative import declarative_base
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from config import db

Base = declarative_base()

class LandingZoneAction(Base):
    __tablename__ = "landingzoneaction"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    categoryName = db.Column(db.String)
    categoryClass = db.Column(db.String)
    completionRate = db.Column(db.Integer)
    locked = db.Column(db.Boolean())
    routerLink = db.Column(db.String)

    def __repr__(self):
        return "<LandingZoneAction(id={self.id!r}, name={self.title!r})>".format(
            self=self
        )

class LandingZoneActionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = LandingZoneAction
        include_fk = True
        load_instance = True
