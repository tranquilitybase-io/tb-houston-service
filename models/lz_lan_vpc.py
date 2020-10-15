from sqlalchemy.ext.declarative import declarative_base
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from config import db

Base = declarative_base()

class LZLanVpc(Base):
    __tablename__ = "lzlanvpc"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    sharedVPCProjectId = db.Column(db.String)
    isActive = db.Column(db.Boolean)

    def __repr__(self):
        return "<LZLanVpc(id={self.id!r}, name={self.name!r})>".format(self=self)

class LZLanVpcSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = LZLanVpc
        include_fk = True
        load_instance = True
