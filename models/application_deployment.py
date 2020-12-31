from config import db, ma


class ApplicationDeployment(db.Model):
    __tablename__ = "applicationDeployment"
    __table_args__ = {"schema": "eagle_db"}
    applicationId = db.Column(db.Integer, primary_key=True)
    solutionId = db.Column(db.Integer, primary_key=True)
    lzEnvironmentId = db.Column(db.Integer, primary_key=True)
    deploymentState = db.Column(db.String)
    taskId = db.Column(db.String)
    workspaceProjectId = db.Column(db.String)
    deploymentProjectId = db.Column(db.String)
    lastUpdated = db.Column(db.String(20))

    def __repr__(self):
        return "<ApplicationDeployment(applicationId={self.applicationId!r}, solutionId={self.solutionId!r})>".format(
            self=self
        )


class ApplicationDeploymentSchema(ma.ModelSchema):
    class Meta:
        model = ApplicationDeployment
        include_fk = True
        load_instance = True
