from sqlalchemy.ext.declarative import declarative_base
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from config import db

Base = declarative_base()

class Type(Base):
    __tablename__ = "type"
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(255))

    def __repr__(self):
        return "<CI(id={self.id!r}, name={self.id!r})>".format(self=self)


class TypeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Type
        include_fk = True
        load_instance = True
