from sqlalchemy import ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from config import db
from .lz_folder_structure import LZFolderStructure

Base = declarative_base()

class LZFolderStructureChild(Base):
    __tablename__ = "lzfolderstructurechild"
    id = db.Column(db.Integer, primary_key=True)
    folderId = db.Column(db.Integer, ForeignKey("lzfolderstructure.id"))
    childId = db.Column(db.Integer, ForeignKey("lzfolderstructure.id"))

    def __repr__(self):
        return "<LZFolderStructureChild(id={self.id!r}>".format(self=self)

class LZFolderStructureChildSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = LZFolderStructure
        include_fk = True
        load_instance = True
