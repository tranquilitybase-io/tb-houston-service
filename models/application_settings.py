from config import db, ma


class ApplicationSettings(db.Model):
    __tablename__ = "applicationsettings"
    __table_args__ = {"schema": "eagle_db"}
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    applicationId = db.Column(db.Integer(), db.ForeignKey("eagle_db.application.id"))
    name = db.Column(db.String(255))
    type = db.Column(db.String(255))
    value = db.Column(db.String(255))
    defaultValue = db.Column(db.String(255))
    isOptional = db.Column(db.Boolean())

    def __repr__(self):
        return "<ApplicationSettings(id={self.id!r}, applicationId={self.applicationId!r})>".format(
            self=self
        )


class ApplicationSettingsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ApplicationSettings
        include_fk = True
        load_instance = True
