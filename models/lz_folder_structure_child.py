from config import db, ma

from .lz_folder_structure import LZFolderStructure


class LZFolderStructureChild(db.Model):
    __tablename__ = "lzfolderstructurechild"
    __table_args__ = {"schema": "eagle_db"}
    id = db.Column(db.Integer, primary_key=True)
    folderId = db.Column(db.Integer, db.ForeignKey("eagle_db.lzfolderstructure.id"))
    childId = db.Column(db.Integer, db.ForeignKey("eagle_db.lzfolderstructure.id"))

    def __repr__(self):
        return "<LZFolderStructureChild(id={self.id!r}>".format(self=self)


class LZFolderStructureChildSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = LZFolderStructure
        include_fk = True
        load_instance = True
