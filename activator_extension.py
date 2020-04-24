from models import ModelTools
import user_extension
import json


def build_activator(act):
    act_dict = {
        'id': act.id,
        'name': act.name,
        'type': act.type,
        'available': act.available,
        'sensitivity': act.sensitivity,
        'category': act.category,
        'envs': json.loads(act.envs or '[]'),
        'platforms': json.loads(act.platforms or '[]'),
        'lastUpdated': ModelTools.datetime_as_string(act.lastUpdated),
        'userCapacity': act.userCapacity,
        'serverCapacity': act.serverCapacity,
        'regions': json.loads(act.regions or '[]'),
        'hosting': json.loads(act.hosting or '[]'),
        'apiManagement': json.loads(act.apiManagement or '[]'),
        'ci': json.loads(act.ci or '[]'),
        'cd': json.loads(act.cd or '[]'),
        'sourceControl': json.loads(act.sourceControl or '[]'),
        'businessUnit': act.businessUnit,
        'technologyOwner': act.technologyOwner,
        'technologyOwnerEmail': act.technologyOwnerEmail,
        'billing': act.billing,
        'activator': act.activator,
        'status': act.status,
        'description': act.description,
        'accessRequestedBy': act.accessRequestedBy,
        'source': act.source,
        'activatorLink': act.activatorLink
    }
    act_dict['accessRequestedBy'] = user_extension.build_user(act.accessRequestedBy)

    return act_dict
