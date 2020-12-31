from config import db, ma


class BGPRoutingMode(db.Model):
    __tablename__ = "bgproutingmode"
    __table_args__ = {"schema": "eagle_db"}
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String)
    value = db.Column(db.String)

    def __repr__(self):
        return "<BGPRoutingMode(id={self.id!r}, name={self.key!r})>".format(self=self)


class BGPRoutingModeSchema(ma.ModelSchema):
    class Meta:
        model = BGPRoutingMode
        include_fk = True
        load_instance = True
