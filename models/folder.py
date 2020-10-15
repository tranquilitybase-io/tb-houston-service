from sqlalchemy.ext.declarative import declarative_base
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from config import db

Base = declarative_base()

class Folder(Base):
    __tablename__ = "folder"
    id = db.Column(db.Integer, primary_key=True)
    parentFolderId = db.Column(db.String(45))
    folderId = db.Column(db.String(45))
    folderName = db.Column(db.String(100))
    status = db.Column(db.String(50))
    taskId = db.Column(db.String(50))

    def __repr__(self):
        return "<Folder(id={self.id!r}, name={self.folderName!r})>".format(self=self)

class FolderSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Folder
        include_fk = True
        load_instance = True
