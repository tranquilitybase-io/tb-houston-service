from config import db, ma


class NotificationType(db.Model):
    __tablename__ = "notificationType"
    __table_args__ = {"schema": "eagle_db"}
    id = db.Column(db.Integer, primary_key=True)
    isActive = db.Column(db.Boolean)
    lastUpdated = db.Column(db.String(20))
    name = db.Column(db.String(45))

    def __repr__(self):
        return "<NotificationType(id={self.id!r})>".format(self=self)


class NotificationTypeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = NotificationType
        include_fk = True
        load_instance = True
