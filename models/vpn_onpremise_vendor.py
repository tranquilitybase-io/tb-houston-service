from config import db, ma


class VPNOnPremiseVendor(db.Model):
    __tablename__ = "vpnonpremisevendor"
    __table_args__ = {"schema": "eagle_db"}
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String)
    value = db.Column(db.String)


class VPNOnPremiseVendorSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = VPNOnPremiseVendor
        include_fk = True
        load_instance = True
