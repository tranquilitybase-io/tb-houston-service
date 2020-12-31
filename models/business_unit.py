from config import db, ma


class BusinessUnit(db.Model):
    __tablename__ = "businessunit"
    __table_args__ = {"schema": "eagle_db"}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(200))
    isActive = db.Column(db.Boolean())

    def __repr__(self):
        return "<BusinessUnit(id={self.id!r}, name={self.name!r})>".format(self=self)


class BusinessUnitSchema(ma.ModelSchema):
    class Meta:
        model = BusinessUnit
        include_fk = True
        load_instance = True
