from config import db, ma

class ActivatorMetadata(db.Model):
    __tablename__ = "activatorMetadata"
    __table_args__ = {'schema': 'eagle_db'}
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    activatorId = db.Column(db.Integer(), db.ForeignKey("eagle_db.activator.id"))
    name = db.Column(db.String(255))
    description = db.Column(db.String(255))
    category = db.Column(db.String(255))
    typeId = db.Column(db.Integer(), db.ForeignKey("eagle_db.type.id"))
    activatorLink = db.Column(db.String(255))
    lastUpdated = db.Column(db.String(20))
    latestVersion = db.Column(db.String(30))
   
    def __repr__(self):
        return "<ActivatorMetadata(id={self.id!r}, name={self.name!r})>".format(self=self)

class ActivatorMetadataSchema(ma.ModelSchema):
    class Meta:
        model = ActivatorMetadata
        include_fk = True
        load_instance = True
