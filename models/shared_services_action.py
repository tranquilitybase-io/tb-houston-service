from config import db, ma


class SharedServicesAction(db.Model):
    __tablename__ = "sharedservicesaction"
    __table_args__ = {"schema": "eagle_db"}
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    categoryName = db.Column(db.String)
    categoryClass = db.Column(db.String)
    completionRate = db.Column(db.Integer)
    locked = db.Column(db.Boolean())
    routerLink = db.Column(db.String)
    dependantOn = db.Column(db.Integer)
    isOptional = db.Column(db.Boolean())

    def __repr__(self):
        return "<SharedServicesAction(id={self.id!r}, name={self.title!r})>".format(
            self=self
        )


class SharedServicesActionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SharedServicesAction
        include_fk = True
        load_instance = True
