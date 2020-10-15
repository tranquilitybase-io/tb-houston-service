from sqlalchemy.ext.declarative import declarative_base
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from config import db

Base = declarative_base()

class LZFolderStructure(Base):
    __tablename__ = "lzfolderstructure"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    isActive = db.Column(db.Boolean)

    def __repr__(self):
        return "<LZFolderStructure(id={self.id!r}, name={self.name!r})>".format(
            self=self
        )

class LZFolderStructureSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = LZFolderStructure
        include_fk = True
        load_instance = True

