from config import db, ma


class LZEnvironment(db.Model):
    __tablename__ = "lzenvironment"
    __table_args__ = {"schema": "eagle_db"}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    isActive = db.Column(db.Boolean)

    def __repr__(self):
        return "<LZEnvironment(id={self.id!r}, name={self.name!r}, isActive={self.isActive!r})>".format(
            self=self
        )


class LZEnvironmentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = LZEnvironment
        include_fk = True
        load_instance = True
