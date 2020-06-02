from sqlalchemy.ext.declarative import declarative_base
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from config import db

Base = declarative_base()

# Team
class Team(Base):
    __tablename__ = "team"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(200))
    businessUnitId = db.Column(db.Integer)
    isActive = db.Column(db.Boolean())


class TeamSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Team
        include_fk = True
        load_instance = True


# Team Member
class TeamMember(Base):
    __tablename__ = "teammember"
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer)
    teamId = db.Column(db.Integer)
    role = db.Column(db.String(100))
    isActive = db.Column(db.Boolean())


class TeamMemberSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = TeamMember
        include_fk = True
        load_instance = True
