from config import db, ma


class NotificationActivator(db.Model):
    __tablename__ = "notificationActivator"
    __table_args__ = {"schema": "eagle_db"}
    isActive = db.Column(db.Boolean())
    lastUpdated = db.Column(db.String(20))
    notificationId = db.Column(
        db.Integer(), db.ForeignKey("eagle_db.notification.id"), primary_key=True
    )
    activatorId = db.Column(
        db.Integer(), db.ForeignKey("eagle_db.activator.id"), primary_key=True
    )

    def __repr__(self):
        return "<NotificationActivator(notificationId={self.notificationId!r}, activatorId={self.activatorId!r})>".format(
            self=self
        )


class NotificationActivatorSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = NotificationActivator
        include_fk = True
        load_instance = True
