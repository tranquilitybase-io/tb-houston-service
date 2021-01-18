from config import db, ma


class SolutionResourceJSON(db.Model):
    __tablename__ = "solutionresourcejson"
    __table_args__ = {"schema": "eagle_db"}
    solutionId = db.Column(db.Integer(), primary_key=True)
    json = db.Column(db.String(30000))


class SolutionResourceJSONSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SolutionResourceJSON
        include_fk = True
        load_instance = True
