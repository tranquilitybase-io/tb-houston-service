from config import db, ma


class CI(db.Model):
    __tablename__ = "ci"
    __table_args__ = {"schema": "eagle_db"}
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(255))

    def __repr__(self):
        return "<CI(id={self.id!r}, name={self.id!r})>".format(self=self)


class CISchema(ma.ModelSchema):
    class Meta:
        model = CI
        include_fk = True
        load_instance = True
