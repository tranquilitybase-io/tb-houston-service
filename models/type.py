from config import db, ma


class Type(db.Model):
    __tablename__ = "type"
    __table_args__ = {"schema": "eagle_db"}
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(255))

    def __repr__(self):
        return "<CI(id={self.id!r}, name={self.id!r})>".format(self=self)


class TypeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Type
        include_fk = True
        load_instance = True
