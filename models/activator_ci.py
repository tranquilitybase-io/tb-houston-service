from config import db, ma


class ActivatorCI(db.Model):
    __tablename__ = "activatorCI"
    __table_args__ = {"schema": "eagle_db"}
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    activatorId = db.Column(db.Integer(), db.ForeignKey("eagle_db.activator.id"))
    ciId = db.Column(db.Integer(), db.ForeignKey("eagle_db.ci.id"))
    lastUpdated = db.Column(db.String(20))
    isActive = db.Column(db.Boolean())

    def __repr__(self):
        return "<Activator(id={self.id!r}, activatorId={self.activatorId!r}, activatorId={self.ciId!r})>".format(
            self=self
        )


class ActivatorCISchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ActivatorCI
        include_fk = True
        load_instance = True
