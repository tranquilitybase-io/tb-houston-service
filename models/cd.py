from sqlalchemy.ext.declarative import declarative_base
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from config import db

Base = declarative_base()

class CD(Base):
    __tablename__ = "cd"
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(255))

    def __repr__(self):
        return "<CD(id={self.id!r}, name={self.id!r})>".format(self=self)

class CDSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = CD
        include_fk = True
        load_instance = True
