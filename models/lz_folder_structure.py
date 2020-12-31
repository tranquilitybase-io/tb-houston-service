from config import db, ma


class LZFolderStructure(db.Model):
    __tablename__ = "lzfolderstructure"
    __table_args__ = {"schema": "eagle_db"}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    isActive = db.Column(db.Boolean)

    def __repr__(self):
        return "<LZFolderStructure(id={self.id!r}, name={self.name!r})>".format(
            self=self
        )


class LZFolderStructureSchema(ma.ModelSchema):
    class Meta:
        model = LZFolderStructure
        include_fk = True
        load_instance = True
