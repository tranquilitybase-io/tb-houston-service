from config import db, ma

class SolutionEnvironment(db.Model):
    __tablename__ = "solutionenvironment"
    __table_args__ = {'schema': 'eagle_db'}
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    solutionId = db.Column(db.Integer(), db.ForeignKey("eagle_db.solution.id"))
    environmentId = db.Column(db.Integer(), db.ForeignKey("eagle_db.lzenvironment.id"))
    lastUpdated = db.Column(db.String(20))
    isActive = db.Column(db.Boolean())

    def __repr__(self):
        return "<Solution(id={self.id!r}, solutionId={self.solutionId!r}, solutionId={self.environmentId!r})>".format(
            self=self
        )

class SolutionEnvironmentSchema(ma.ModelSchema):
    class Meta:
        model = SolutionEnvironment
        include_fk = True
        load_instance = True
