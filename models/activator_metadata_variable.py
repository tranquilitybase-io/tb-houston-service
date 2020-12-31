from config import db, ma


class ActivatorMetadataVariable(db.Model):
    __tablename__ = "activatorMetadataVariables"
    __table_args__ = {"schema": "eagle_db"}
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    activatorMetadataId = db.Column(
        db.Integer(), db.ForeignKey("eagle_db.activatorMetadata.id")
    )
    name = db.Column(db.String(255))
    type = db.Column(db.String(255))
    value = db.Column(db.String(255))
    defaultValue = db.Column(db.String(255))
    isOptional = db.Column(db.Boolean())

    def __repr__(self):
        return "<ActivatorMetadataVariable(id={self.id!r}, activatorMetadataId={self.activatorMetadataId!r})>".format(
            self=self
        )


class ActivatorMetadataVariableSchema(ma.ModelSchema):
    class Meta:
        model = ActivatorMetadataVariable
        include_fk = True
        load_instance = True
