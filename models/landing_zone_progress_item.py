from config import db, ma

class LandingZoneProgressItem(db.Model):
    __tablename__ = "landingzoneprogressitem"
    __table_args__ = {'schema': 'eagle_db'}
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String)
    completed = db.Column(db.Boolean())

    def __repr__(self):
        return "<LandingZoneProgressItem(id={self.id!r}, name={self.label!r})>".format(
            self=self
        )

class LandingZoneProgressItemSchema(ma.ModelSchema):
    class Meta:
        model = LandingZoneProgressItem
        include_fk = True
        load_instance = True
