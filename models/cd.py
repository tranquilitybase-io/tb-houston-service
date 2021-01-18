from config import db, ma


class CD(db.Model):
    __tablename__ = "cd"
    __table_args__ = {"schema": "eagle_db"}
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(255))

    def __repr__(self):
        return "<CD(id={self.id!r}, name={self.id!r})>".format(self=self)


class CDSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CD
        include_fk = True
        load_instance = True
