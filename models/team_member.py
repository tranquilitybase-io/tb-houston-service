from sqlalchemy.ext.declarative import declarative_base
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from config import db

Base = declarative_base()

class TeamMember(Base):
    __tablename__ = "teammember"
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer)
    teamId = db.Column(db.Integer)
    isTeamAdmin = db.Column(db.Boolean())
    isActive = db.Column(db.Boolean())

class TeamMemberSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = TeamMember
        include_fk = True
        load_instance = True
