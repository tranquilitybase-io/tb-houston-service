from sqlalchemy.ext.declarative import declarative_base
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from config import db

Base = declarative_base()

class VPNOnPremiseVendor(Base):
    __tablename__ = "vpnonpremisevendor"
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String)
    value = db.Column(db.String)

class VPNOnPremiseVendorSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = VPNOnPremiseVendor
        include_fk = True
        load_instance = True
