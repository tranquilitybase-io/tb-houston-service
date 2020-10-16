from config import db, ma

class ActivatorEnvironment(db.Model):
    __tablename__ = "activatorEnvironment"
    __table_args__ = {'schema': 'eagle_db'}
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    activatorId = db.Column(db.Integer(), db.ForeignKey("eagle_db.activator.id"))
    envId = db.Column(db.Integer(), db.ForeignKey("eagle_db.lzenvironment.id"))
    lastUpdated = db.Column(db.String(20))
    isActive = db.Column(db.Boolean())

    def __repr__(self):
        return "<Activator(id={self.id!r}, activatorId={self.activatorId!r}, activatorId={self.envId!r})>".format(
            self=self
        )

class ActivatorEnvironmentSchema(ma.ModelSchema):
    class Meta:
        model = ActivatorEnvironment
        include_fk = True
        load_instance = True
