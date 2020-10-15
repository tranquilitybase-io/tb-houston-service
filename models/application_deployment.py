from sqlalchemy.ext.declarative import declarative_base
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from config import db

Base = declarative_base()

class ApplicationDeployment(Base):
    __tablename__ = "applicationDeployment"
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

class ApplicationDeploymentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ApplicationDeployment
        include_fk = True
        load_instance = True
