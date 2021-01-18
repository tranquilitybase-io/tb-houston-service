from config import db, ma


class LZLanVpc(db.Model):
    __tablename__ = "lzlanvpc"
    __table_args__ = {"schema": "eagle_db"}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    sharedVPCProjectId = db.Column(db.String)
    isActive = db.Column(db.Boolean)

    def __repr__(self):
        return "<LZLanVpc(id={self.id!r}, name={self.name!r})>".format(self=self)


class LZLanVpcSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = LZLanVpc
        include_fk = True
        load_instance = True
