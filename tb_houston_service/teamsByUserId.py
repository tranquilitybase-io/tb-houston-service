from marshmallow import Schema, fields
from config import app, db

from tb_houston_service.models import TeamMember, Team


class KeyValueSchema(Schema):
    key = fields.Str()
    value = fields.Str()


def read_all(userId):
    teams = (
        db.session.query(Team)
        .filter(
            TeamMember.teamId == Team.id,
            TeamMember.userId == userId,
            Team.isActive,
            TeamMember.isActive,
        )
        .all()
    )

    teams_key_values = []
    for team in teams:
        kv = {}
        kv["key"] = team.id
        kv["value"] = team.name
        teams_key_values.append(kv)

    schema = KeyValueSchema(many=True)

    # Convert to JSON (Serialization)
    data = schema.dump(teams_key_values)
    app.logger.debug(f"{data} type: {type(data)}")
    return data, 200
