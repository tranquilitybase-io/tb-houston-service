from config import db, ma

class LandingZoneAction(db.Model):
    __tablename__ = "landingzoneaction"
    __table_args__ = {'schema': 'eagle_db'}
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    categoryName = db.Column(db.String)
    categoryClass = db.Column(db.String)
    completionRate = db.Column(db.Integer)
    locked = db.Column(db.Boolean())
    routerLink = db.Column(db.String)

    def __repr__(self):
        return "<LandingZoneAction(id={self.id!r}, name={self.title!r})>".format(
            self=self
        )

class LandingZoneActionSchema(ma.ModelSchema):
    class Meta:
        model = LandingZoneAction
        include_fk = True
        load_instance = True
