from config import db, ma


class SharedServicesProgressItem(db.Model):
    __tablename__ = "sharedservicesprogressitem"
    __table_args__ = {"schema": "eagle_db"}
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String)
    completed = db.Column(db.Boolean())

    def __repr__(self):
        return (
            "<SharedServicesProgressItem(id={self.id!r}, name={self.label!r})>".format(
                self=self
            )
        )


class SharedServicesProgressItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SharedServicesProgressItem
        include_fk = True
        load_instance = True
