from config import db, ma


class ActivatorMetadataPlatform(db.Model):
    __tablename__ = "activatorMetadataPlatform"
    __table_args__ = {"schema": "eagle_db"}
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    activatorMetadataId = db.Column(
        db.Integer(), db.ForeignKey("eagle_db.activatorMetadata.id")
    )
    platformId = db.Column(db.Integer(), db.ForeignKey("eagle_db.platform.id"))
    lastUpdated = db.Column(db.String(20))
    isActive = db.Column(db.Boolean())

    def __repr__(self):
        return "<ActivatorMetadataPlatform(id={self.id!r}, activatorMetadataId={self.activatorMetadataId!r})>".format(
            self=self
        )


class ActivatorMetadataPlatformSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ActivatorMetadataPlatform
        include_fk = True
        load_instance = True
