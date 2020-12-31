from config import db, ma


class Platform(db.Model):
    __tablename__ = "platform"
    __table_args__ = {"schema": "eagle_db"}
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(255))

    def __repr__(self):
        return "<CI(id={self.id!r}, name={self.id!r})>".format(self=self)


class PlatformSchema(ma.ModelSchema):
    class Meta:
        model = Platform
        include_fk = True
        load_instance = True
