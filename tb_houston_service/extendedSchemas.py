import logging
import json
from marshmallow import Schema, fields, post_load, post_dump
from tb_houston_service.models import TeamSchema
from tb_houston_service.models import BusinessUnitSchema
from tb_houston_service.models import LZEnvironmentSchema
from tb_houston_service.models import LZLanVpcSchema
from tb_houston_service.models import RoleSchema


logger = logging.getLogger("tb_houston_service.extendedSchemas")

class IdSchema(Schema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    id = fields.Int()


class HealthSchema(Schema):
    status = fields.Str()


class ResourceSchema(Schema):
    ipaddress = fields.Str()
    name = fields.Str()


class ExtendedLoginSchema(Schema):
    id = fields.Int()
    email = fields.Str()
    firstName = fields.Str()
    lastName = fields.Str()
    isAdmin = fields.Boolean()
    showWelcome = fields.Boolean()
    teams = fields.List(fields.Str())


class ExtendedUserSchema(Schema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    id = fields.Int()
    email = fields.Str()
    firstName = fields.Str()
    lastName = fields.Str()
    isAdmin = fields.Boolean()
    showWelcome = fields.Boolean()
    role = fields.Str()
    isActive = fields.Boolean()


class ExtendedActivatorSchema(Schema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    id = fields.Int()
    isActive = fields.Boolean()
    lastUpdated = fields.Str()
    isFavourite = fields.Boolean()   
    name = fields.Str()
    type = fields.Str()
    available = fields.Boolean()
    sensitivity = fields.Str()
    category = fields.Str()
    envs = fields.List(fields.Str())
    platforms = fields.List(fields.Str())
    userCapacity = fields.Int()
    serverCapacity = fields.Int()
    regions = fields.List(fields.Str())
    hosting = fields.List(fields.Str())
    apiManagement = fields.List(fields.Str())
    ci = fields.List(fields.Str())
    cd = fields.List(fields.Str())
    sourceControl = fields.List(fields.Str())
    businessUnit = fields.Str()
    technologyOwner = fields.Str()
    technologyOwnerEmail = fields.Str()
    billing = fields.Str()
    activator = fields.Str()
    status = fields.Str()
    description = fields.Str()
    accessRequestedById = fields.Int()
    accessRequestedBy = fields.Nested(ExtendedUserSchema(many=False))
    source = fields.Str()
    activatorLink = fields.Str()

    @post_load(pass_original=True)
    def deserialize_post_load(self, data, original_data, **kwargs):
        logger.debug("ExtendedActivatorSchema::post_load::serialize_post_load: %s", data)
        data["envs"] = json.dumps(original_data.envs)
        data["platforms"] = json.dumps(original_data.platforms)
        data["regions"] = json.dumps(original_data.regions)
        data["hosting"] = json.dumps(original_data.hosting)
        data["apiManagement"] = json.dumps(original_data.apiManagement)
        data["ci"] = json.dumps(original_data.ci)
        data["cd"] = json.dumps(original_data.cd)
        data["sourceControl"] = json.dumps(original_data.sourceControl)
        return data

    @post_dump(pass_original=True)
    def deserialize_post_dump(self, data, original_data, **kwargs):
        logger.debug("ExtendedActivatorSchema::post_dump %s", original_data)
        data["envs"] = json.loads(original_data.envs)
        data["platforms"] = json.loads(original_data.platforms)
        data["regions"] = json.loads(original_data.regions)
        data["hosting"] = json.loads(original_data.hosting)
        data["apiManagement"] = json.loads(original_data.apiManagement)
        data["ci"] = json.loads(original_data.ci)
        data["cd"] = json.loads(original_data.cd)
        data["sourceControl"] = json.loads(original_data.sourceControl)
        return data


class ExtendedApplicationSchema(Schema):
    id = fields.Int()
    solutionId = fields.Int()
    activatorId = fields.Int()
    isActive = fields.Boolean()
    lastUpdated = fields.Str()
    isFavourite = fields.Boolean()      
    name = fields.Str()
    env = fields.Str()
    status = fields.Str()
    description = fields.Str()
    resources = fields.Nested(ResourceSchema(many=True))
    activator = fields.Nested(ExtendedActivatorSchema(many=False))

    @post_load(pass_original=True)
    def serialize_post_load(self, data, original_data, **kwargs):
        logger.debug("ExtendedApplicationSchema::post_load: %s", data)
        logger.debug("serialize_resources_original data: %s", original_data)            
        data['resources'] = json.dumps(original_data.resources)
        return data

    @post_dump(pass_original=True)
    def deserialize_post_dump(self, data, original_data, **kwargs):
        logger.debug("ExtendedApplicationSchema::post_dump: %s", original_data)
        logger.debug("deserialize_resources_original data: %s", original_data)
        data['resources'] = json.loads(original_data.resources)
        return data


class ExtendedTeamSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    description = fields.Str()
    businessUnitId = fields.Int()
    isActive = fields.Boolean()
    businessUnit = fields.Nested(BusinessUnitSchema(many=False))
    lastUpdated = fields.Str()
    userCount = fields.Int()

class ExtendedSolutionSchema(Schema):
    __envelope__ = {"single": "solution", "many": "solutions"}

    id = fields.Int()
    isActive = fields.Boolean()
    lastUpdated = fields.Str()
    isFavourite = fields.Boolean()      
    name = fields.Str()
    description = fields.Str()
    businessUnitId = fields.Int()
    costCentre = fields.Str()
    ci = fields.Str()
    cd = fields.Str()
    sourceControl = fields.Str()
    environments = fields.Nested(LZEnvironmentSchema(many=True))
    favourite = fields.Boolean()
    teamId = fields.Int()
    applications = fields.Nested(ExtendedApplicationSchema(many=True))
    team = fields.Nested(ExtendedTeamSchema(many=False))
    deploymentFolderId = fields.Str()
    businessUnit = fields.Nested(BusinessUnitSchema(many=False))


class ExtendedTeamMemberSchema(Schema):
    id = fields.Int()
    user = fields.Nested(ExtendedUserSchema(many=False))
    role = fields.Str()

class ExtendedTeamMemberFullSchema(Schema):
    id = fields.Int()
    isActive = fields.Boolean()
    isTeamAdmin = fields.Boolean()
    roleId = fields.Int()
    role = fields.Nested(RoleSchema(many=False))
    teamId = fields.Int()
    team = fields.Nested(ExtendedTeamSchema(many=False))
    userId= fields.Int()
    user = fields.Nested(ExtendedUserSchema(many=False))
    class Meta:
        ordered = True


class ExtendedTeamDACSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    description = fields.Str()
    businessUnitId = fields.Int()
    isActive = fields.Boolean()
    businessUnit = fields.Nested(BusinessUnitSchema(many=False))
    lastUpdated = fields.Str()
    teamMembers = fields.Nested(ExtendedTeamMemberSchema(many=True))


class ExtendedSolutionForDACSchema(Schema):
    __envelope__ = {"single": "solution", "many": "solutions"}

    id = fields.Int()
    isActive = fields.Boolean()
    lastUpdated = fields.Str()
    isFavourite = fields.Boolean()      
    name = fields.Str()
    description = fields.Str()
    businessUnit = fields.Str()
    costCentre = fields.Str()
    ci = fields.Str()
    cd = fields.Str()
    sourceControl = fields.Str()
    environments = fields.List(fields.Str())
    teamId = fields.Int()
    team = fields.Nested(ExtendedTeamDACSchema(many=False))
    deploymentFolderId = fields.Str()


class SolutionNamesOnlySchema(Schema):
    __envelope__ = {"single": "solution", "many": "solutions"}

    id = fields.Int()
    name = fields.Str()


class SolutionDeploymentSchema(Schema):
    __envelope__ = {"single": "solutiondeployment", "many": "solutiondeployments"}

    id = fields.Int()
    deployed = fields.Boolean()
    deploymentState = fields.Str()
    statusId = fields.Int()
    statusCode = fields.Str()
    statusMessage = fields.Str()
    taskId = fields.Str()


class ExtendedGoogleSessionSchema(Schema):
    primaryGcpVpcSubnet = fields.Str()
    primaryRegion = fields.Str()
    primarySubnetName = fields.Str()
    secondaryGcpVpcSubnet = fields.Str()
    secondaryRegion = fields.Str()
    secondarySubnetName = fields.Str()


class ExtendedOnPremiseSessionSchema(Schema):
    primaryBgpPeer = fields.Str()
    primaryPeerIp = fields.Str()
    primaryPeerIpSubnet = fields.Str()
    primarySharedSecret = fields.Str()
    primaryVpnTunnel = fields.Str()
    secondaryBgpPeer = fields.Str()
    secondaryPeerIp = fields.Str()
    secondaryPeerIpSubnet = fields.Str()
    secondarySharedSecret = fields.Str()
    secondaryVpnTunnel = fields.Str()
    vendor = fields.Str()


class ExtendedVPNSchema(Schema):
    bgpInterfaceNetLength = fields.Str()
    bgpRoutingMode = fields.Str()
    cloudRouterName = fields.Str()
    description = fields.Str()
    externalVpnGateway = fields.Str()
    googleASN = fields.Int()
    haVpnGateway = fields.Str()
    peerASN = fields.Int()
    projectName = fields.Str()
    subnetMode = fields.Str()
    vpcName = fields.Str()


class ExtendedLandingZoneWANSchema(Schema):
    __envelope__ = {"single": "landingZoneWAN", "many": "landingZoneWANs"}
    id = fields.Int()
    googleSession = fields.Nested(ExtendedGoogleSessionSchema(many=False))
    onPremiseSession = fields.Nested(ExtendedOnPremiseSessionSchema(many=False))
    vpn = fields.Nested(ExtendedVPNSchema(many=False))


class ExtendedActivatorCategorySchema(Schema):
    __envelope__ = {"single": "activatorCategory", "many": "activatorCategories"}
    category = fields.Str()


class ExtendedLZMetadataSchema(Schema):
    active = fields.Boolean()
    group = fields.Str()
    name = fields.Str()
    description = fields.Str()
    value = fields.List(fields.Str())


class ExtendedLZMetadataListSchema(Schema):
    name = fields.Str()
    value = fields.List(fields.Str())
    description = fields.Str()
    isActive = fields.Boolean()


class ExtendedLZMetadataFSSolutionSchema(Schema):
    id = fields.Int()
    isActive = fields.Boolean()
    name = fields.String()


class ExtendedLZMetadataFSTeamSchema(Schema):
    id = fields.Int()
    isActive = fields.Boolean()
    name = fields.String()
    children = fields.Nested(ExtendedLZMetadataFSSolutionSchema(many=True))


class ExtendedLZMetadataFSBusinessUnitSchema(Schema):
    id = fields.Int()
    isActive = fields.Boolean()
    name = fields.String()
    children = fields.Nested(ExtendedLZMetadataFSTeamSchema(many=True))


class ExtendedLZMetadataFSApplicationSchema(Schema):
    id = fields.Int()
    isActive = fields.Boolean()
    name = fields.String()
    children = fields.Nested(ExtendedLZMetadataFSBusinessUnitSchema(many=True))


class ExtendedLZMetadataFSSchema(Schema):
    isActive = fields.Boolean()
    name = fields.String()
    value = fields.Nested(ExtendedLZMetadataFSApplicationSchema(many=True))


class KeyValueSchema(Schema):
    key = fields.Int()
    value = fields.Str()


class ExtendedLZLanVpcSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    isActive = fields.Boolean()
    environments = fields.Nested(LZEnvironmentSchema(many=True))


class ExtendedApplicationDeploymentSchema(Schema):
    __envelope__ = {"single": "applicationdeployment", "many": "applicationdeployments"}

    id = fields.Int()
    deploymentState = fields.Str()
    taskId = fields.Str()
    lastUpdated = fields.Str()

    @post_dump(pass_original=True)
    def deserialize_post_dump(self, data, original_data, **kwargs):
        logger.debug("ExtendedActivatorSchema::post_dump %s", original_data)
        data["id"] = original_data.applicationId
        return data        


class ExtendedApplicationForDACSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    description = fields.Str()
    solutionId = fields.Int()

class ExtendedNotificationActivatorSchema(Schema):
    id = fields.Int()
    isActive = fields.Bool()
    lastUpdated = fields.Str()
    toUserId = fields.Int()
    fromUserId = fields.Int()
    importance = fields.Int()
    message = fields.Str()
    isRead = fields.Boolean()
    typeId = fields.Int()
    activatorId = fields.Int()

