from config import db, ma

class TeamMember(db.Model):
    __tablename__ = "teammember"
    __table_args__ = {'schema': 'eagle_db'}
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer)
    teamId = db.Column(db.Integer)
    isTeamAdmin = db.Column(db.Boolean())
    isActive = db.Column(db.Boolean())

class TeamMemberSchema(ma.ModelSchema):
    class Meta:
        model = TeamMember
        include_fk = True
        load_instance = True
