from sqlalchemy.ext.declarative import declarative_base
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from config import db

Base = declarative_base()

class BGPRoutingMode(Base):
    __tablename__ = "bgproutingmode"
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String)
    value = db.Column(db.String)

    def __repr__(self):
        return "<BGPRoutingMode(id={self.id!r}, name={self.key!r})>".format(self=self)

class BGPRoutingModeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = BGPRoutingMode
        include_fk = True
        load_instance = True
