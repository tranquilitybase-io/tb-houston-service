from config import db, ma

class UserCloudRole(db.Model):
    __tablename__ = "userCloudRole"
    __table_args__ = {'schema': 'eagle_db'}
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer)
    cloudRoleId = db.Column(db.Integer)
    isActive = db.Column(db.Boolean())

class UserCloudRoleSchema(ma.ModelSchema):
    class Meta:
        model = UserCloudRole
        include_fk = True
        load_instance = True
