from models import User
from extendedSchemas import ExtendedUserSchema

def build_user(id):
    existing_user = (
        User.query.filter(User.id == id).one_or_none()
    )

    if existing_user is not None:
        user_schema = ExtendedUserSchema(many=False)
        data = user_schema.dump(existing_user)
        return data

    return None
