from config import db, ma

class CloudRole(db.Model):
    __tablename__ = "cloudRole"
    __table_args__ = {'schema': 'eagle_db'}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    cloudIdentityGroup = db.Column(db.String(200))
    description = db.Column(db.String(200))

class CloudRoleSchema(ma.ModelSchema):
    class Meta:
        model = CloudRole
        include_fk = True
        load_instance = True
