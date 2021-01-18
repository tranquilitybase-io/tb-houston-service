from config import db, ma


class LZLanVpcEnvironment(db.Model):
    __tablename__ = "lzlanvpc_environment"
    __table_args__ = {"schema": "eagle_db"}
    id = db.Column(db.Integer, primary_key=True)
    lzlanvpcId = db.Column(db.Integer, db.ForeignKey("eagle_db.lzlanvpc.id"))
    environmentId = db.Column(db.Integer, db.ForeignKey("eagle_db.lzenvironment.id"))
    isActive = db.Column(db.Boolean)

    def __repr__(self):
        return "<LZLanVpcEnvironment(id={self.id!r})>".format(self=self)


class LZLanVpcEnvironmentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = LZLanVpcEnvironment
        include_fk = True
        load_instance = True
