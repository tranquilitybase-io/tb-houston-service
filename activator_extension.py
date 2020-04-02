from models import ModelTools
import user_extension
from extendedSchemas import ExtendedUserSchema


def build_activator(act):
    act_dict = {
        'id': act.id,
        'name': act.name,
        'type': act.type,
        'available': act.available,
        'sensitivity': act.sensitivity,
        'category': act.category,
        'envs': ModelTools.load_json_array(act.envs),
        'platforms': ModelTools.load_json_array(act.platforms),
        'lastUpdated': ModelTools.datetime_as_string(act.lastUpdated),
        'userCapacity': act.userCapacity,
        'serverCapacity': act.serverCapacity,
        'regions': ModelTools.load_json_array(act.regions),
        'hosting': ModelTools.load_json_array(act.hosting),
        'apiManagement': ModelTools.load_json_array(act.apiManagement),
        'ci': ModelTools.load_json_array(act.ci),
        'cd': ModelTools.load_json_array(act.cd),
        'sourceControl': ModelTools.load_json_array(act.sourceControl),
        'businessUnit': act.businessUnit,
        'technologyOwner': act.technologyOwner,
        'technologyOwnerEmail': act.technologyOwnerEmail,
        'billing': act.billing,
        'activator': act.activator,
        'resources': ModelTools.load_json_array(act.resources),
        'status': act.status,
        'description': act.description
    }
    act_dict['accessRequestedBy'] = user_extension.build_user(act.accessRequestedBy)

    return act_dict
