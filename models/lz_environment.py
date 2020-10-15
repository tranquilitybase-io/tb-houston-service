from sqlalchemy.ext.declarative import declarative_base
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from config import db

Base = declarative_base()

class LZEnvironment(Base):
    __tablename__ = "lzenvironment"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    isActive = db.Column(db.Boolean)

    def __repr__(self):
        return "<LZEnvironment(id={self.id!r}, name={self.name!r}, isActive={self.isActive!r})>".format(
            self=self
        )


class LZEnvironmentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = LZEnvironment
        include_fk = True
        load_instance = True
