from config import db, ma


class SolutionResource(db.Model):
    __tablename__ = "solutionresource"
    __table_args__ = {"schema": "eagle_db"}
    solutionId = db.Column(db.Integer(), primary_key=True)
    key = db.Column(db.String(50), primary_key=True)
    value = db.Column(db.String(255))


class SolutionResourceSchema(ma.ModelSchema):
    class Meta:
        model = SolutionResource
        include_fk = True
        load_instance = True
