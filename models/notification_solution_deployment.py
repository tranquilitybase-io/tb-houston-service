from config import db, ma

class NotificationSolutionDeployment(db.Model):
    __tablename__ = "notificationSolutionDeployment"
    __table_args__ = {'schema': 'eagle_db'}
    isActive = db.Column(db.Boolean())
    lastUpdated = db.Column(db.String(20))
    notificationId = db.Column(db.Integer(), db.ForeignKey("eagle_db.notification.id"), primary_key=True)
    solutionId = db.Column(db.Integer(), db.ForeignKey("eagle_db.solution.id"), primary_key=True)

    def __repr__(self):
        return "<NotificationSolutionDeployment(notificationId={self.notificationId!r}, solutionId={self.solutionId!r})>".format(self=self)

class NotificationSolutionDeploymentSchema(ma.ModelSchema):
    class Meta:
        model = NotificationSolutionDeployment
        include_fk = True
        load_instance = True
