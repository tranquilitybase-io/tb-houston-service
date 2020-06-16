from config import db
from tb_houston_service.models import User


def expand_activator(act):
    act.accessRequestedBy = (
        db.session.query(User).filter(User.id == act.accessRequestedBy).one_or_none()
    )
    return act