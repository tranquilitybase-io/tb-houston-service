from config import db, ma


class Notification(db.Model):
    __tablename__ = "notification"
    __table_args__ = {"schema": "eagle_db"}
    id = db.Column(db.Integer(), primary_key=True)
    isActive = db.Column(db.Boolean())
    lastUpdated = db.Column(db.String(20))
    toUserId = db.Column(db.Integer(), db.ForeignKey("eagle_db.user.id"))
    fromUserId = db.Column(db.Integer, db.ForeignKey("eagle_db.user.id"))
    importance = db.Column(db.Integer())
    message = db.Column(db.String(255))
    isRead = db.Column(db.Boolean())
    typeId = db.Column(db.Integer(), db.ForeignKey("eagle_db.notificationType.id"))

    def __repr__(self):
        return "<Notification(id={self.id!r})>".format(self=self)


class NotificationSchema(ma.ModelSchema):
    class Meta:
        model = Notification
        include_fk = True
        load_instance = True
