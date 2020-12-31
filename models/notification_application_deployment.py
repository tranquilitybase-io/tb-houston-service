from config import db, ma


class NotificationApplicationDeployment(db.Model):
    __tablename__ = "notificationApplicationDeployment"
    __table_args__ = {"schema": "eagle_db"}
    isActive = db.Column(db.Boolean())
    lastUpdated = db.Column(db.String(20))
    notificationId = db.Column(
        db.Integer(), db.ForeignKey("eagle_db.notification.id"), primary_key=True
    )
    applicationId = db.Column(
        db.Integer(), db.ForeignKey("eagle_db.application.id"), primary_key=True
    )

    def __repr__(self):
        return "<NotificationApplicationDeployment(notificationId={self.notificationId!r}, applicationId={self.applicationId!r})>".format(
            self=self
        )


class NotificationApplicationDeploymentSchema(ma.ModelSchema):
    class Meta:
        model = NotificationApplicationDeployment
        include_fk = True
        load_instance = True
