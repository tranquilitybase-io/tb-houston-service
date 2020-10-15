from config import db, ma

class ActivatorCD(db.Model):
    __tablename__ = "activatorCD"
    __table_args__ = {'schema': 'eagle_db'}
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    activatorId = db.Column(db.Integer(), db.ForeignKey("eagle_db.activator.id"))
    cdId = db.Column(db.Integer(), db.ForeignKey("eagle_db.cd.id"))
    lastUpdated = db.Column(db.String(20))
    isActive = db.Column(db.Boolean())

    def __repr__(self):
        return "<Activator(id={self.id!r}, activatorId={self.activatorId!r}, activatorId={self.cdId!r})>".format(
            self=self
        )

class ActivatorCDSchema(ma.ModelSchema):
    class Meta:
        model = ActivatorCD
        include_fk = True
        load_instance = True
