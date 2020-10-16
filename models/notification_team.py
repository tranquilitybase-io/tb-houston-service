from config import db, ma

class NotificationTeam(db.Model):
    __tablename__ = "notificationTeam"
    __table_args__ = {'schema': 'eagle_db'}
    isActive = db.Column(db.Boolean())
    lastUpdated = db.Column(db.String(20))
    notificationId = db.Column(db.Integer(), db.ForeignKey("eagle_db.notification.id"), primary_key=True)
    teamId = db.Column(db.Integer(), db.ForeignKey("eagle_db.team.id"), primary_key=True)

    def __repr__(self):
        return "<NotificationTeam(notificationId={self.notificationId!r}, teamId={self.teamId!r})>".format(self=self)

class NotificationTeamSchema(ma.ModelSchema):
    class Meta:
        model = NotificationTeam
        include_fk = True
        load_instance = True
