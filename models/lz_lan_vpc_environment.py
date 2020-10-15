from sqlalchemy import ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from config import db

Base = declarative_base()

class LZLanVpcEnvironment(Base):
    __tablename__ = "lzlanvpc_environment"
    id = db.Column(db.Integer, primary_key=True)
    lzlanvpcId = db.Column(db.Integer, ForeignKey("lzlanvpc.id"))
    environmentId = db.Column(db.Integer, ForeignKey("lzenvironment.id"))
    isActive = db.Column(db.Boolean)

    def __repr__(self):
        return "<LZLanVpcEnvironment(id={self.id!r})>".format(self=self)


class LZLanVpcEnvironmentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = LZLanVpcEnvironment
        include_fk = True
        load_instance = True
