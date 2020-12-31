from config import db, ma


class SubnetMode(db.Model):
    __tablename__ = "subnetmode"
    __table_args__ = {"schema": "eagle_db"}
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String)
    value = db.Column(db.String)


class SubnetModeSchema(ma.ModelSchema):
    class Meta:
        model = SubnetMode
        include_fk = True
        load_instance = True
