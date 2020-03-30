from models import Application
from models import Activator
import activator_extension


def build_application(app):
    app_dict = {
        'id': app.id,
        'name': app.name,
        'env': app.env,
        'status': app.status,
        'description': app.description
    }
    acts = Activator.query.filter(Activator.id == app.activatorId).all()
    act_dict = {}
    for act in acts:
      act_dict = activator_extension.build_activator(act)

    app_dict['activator'] = act_dict
    return app_dict
