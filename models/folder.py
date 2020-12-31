from config import db, ma


class Folder(db.Model):
    __tablename__ = "folder"
    __table_args__ = {"schema": "eagle_db"}
    id = db.Column(db.Integer, primary_key=True)
    parentFolderId = db.Column(db.String(45))
    folderId = db.Column(db.String(45))
    folderName = db.Column(db.String(100))
    status = db.Column(db.String(50))
    taskId = db.Column(db.String(50))

    def __repr__(self):
        return "<Folder(id={self.id!r}, name={self.folderName!r})>".format(self=self)


class FolderSchema(ma.ModelSchema):
    class Meta:
        model = Folder
        include_fk = True
        load_instance = True
