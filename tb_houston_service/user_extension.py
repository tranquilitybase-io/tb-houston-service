from tb_houston_service.models import User
from tb_houston_service.extendedSchemas import ExtendedUserSchema
from config import db


def build_user(id):
    if id == None or id == 0:
        return None

    existing_user = (
        db.session.query(User).filter(User.id == id).one_or_none()
    )

    if existing_user is not None:
        user_schema = ExtendedUserSchema(many=False)
        data = user_schema.dump(existing_user)
        return data

    return None
