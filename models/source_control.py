from config import db, ma


class SourceControl(db.Model):
    __tablename__ = "sourcecontrol"
    __table_args__ = {"schema": "eagle_db"}
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(255))


class SourceControlSchema(ma.ModelSchema):
    class Meta:
        model = SourceControl
        include_fk = True
        load_instance = True
