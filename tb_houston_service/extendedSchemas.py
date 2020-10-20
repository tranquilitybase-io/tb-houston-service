import logging
import json
from marshmallow import Schema, fields, post_load, post_dump
from marshmallow_oneofschema import OneOfSchema

from models import  BusinessUnitSchema, LZEnvironmentSchema, \
                    CISchema, CDSchema, SourceControlSchema, NotificationTypeSchema, \
                    NotificationActivatorSchema, NotificationTeamSchema, \
                    NotificationApplicationDeploymentSchema, NotificationSolutionDeploymentSchema, \
                    TypeSchema, PlatformSchema, ActivatorMetadataVariableSchema

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
    isActive = fields.Boolean()
    lastUpdated = fields.Str()
    teamCount = fields.Int()

class ExtendedActivatorMetadataSchema(Schema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    id = fields.Int()
    name = fields.Str()
    category = fields.Str()
    platforms = fields.Nested(PlatformSchema(many=True))
    type = fields.Nested(TypeSchema(many=False))
    typeId = fields.Int()
    description = fields.Str()
    activatorLink = fields.Str()
    variables= fields.Nested(ActivatorMetadataVariableSchema(many=True))
    lastUpdated = fields.Str()

class ExtendedActivatorSchema(Schema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    id = fields.Int()
    isActive = fields.Boolean()
    lastUpdated = fields.Str()
    isFavourite = fields.Boolean()
    name = fields.Str()
    available = fields.Boolean()
    sensitivity = fields.Str()
    envs = fields.Nested(LZEnvironmentSchema(many=True))
    userCapacity = fields.Int()
    serverCapacity = fields.Int()
    regions = fields.List(fields.Str())
    hosting = fields.List(fields.Str())
    apiManagement = fields.List(fields.Str())
    ciId = fields.Int()
    ci = fields.Nested(CISchema(many=True))
    cdId = fields.Int()
    cd = fields.Nested(CDSchema(many=True))
    sourceControlId = fields.Int()
    sourceControl = fields.Nested(SourceControlSchema(many=False))
    businessUnitId = fields.Int()
    businessUnit = fields.Nested(BusinessUnitSchema(many=False))
    technologyOwner = fields.Str()
    technologyOwnerEmail = fields.Str()
    billing = fields.Str()
    activator = fields.Str()
    status = fields.Str()
    accessRequestedById = fields.Int()
    accessRequestedBy = fields.Nested(ExtendedUserSchema(many=False))
    source = fields.Str()
    gitRepoUrl = fields.Str()
    activatorMetadata = fields.Nested(ExtendedActivatorMetadataSchema(many=False))

    @post_load(pass_original=True)
    def deserialize_post_load(self, data, original_data, **kwargs):
        # logger.debug(
        #    "ExtendedActivatorSchema::post_load::serialize_post_load: %s", data
        # )
        if original_data.regions is not None:
            data["regions"] = json.dumps(original_data.regions)
        if original_data.hosting is not None:
            data["hosting"] = json.dumps(original_data.hosting)
        if original_data.apiManagement is not None:
            data["apiManagement"] = json.dumps(original_data.apiManagement)
        return data

    @post_dump(pass_original=True)
    def deserialize_post_dump(self, data, original_data, **kwargs):
        # logger.debug("ExtendedActivatorSchema::post_dump %s", original_data)
        if original_data.regions is not None:
            data["regions"] = json.loads(original_data.regions)
        if original_data.hosting is not None:
            data["hosting"] = json.loads(original_data.hosting)
        if original_data.apiManagement is not None:
            data["apiManagement"] = json.loads(original_data.apiManagement)
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
    deploymentState = fields.Str()

    @post_load(pass_original=True)
    def serialize_post_load(self, data, original_data, **kwargs):
        logger.debug("ExtendedApplicationSchema::post_load: %s", data)
        logger.debug("serialize_resources_original data: %s", original_data)
        data["resources"] = json.dumps(original_data.resources)
        return data

    @post_dump(pass_original=True)
    def deserialize_post_dump(self, data, original_data, **kwargs):
        logger.debug("ExtendedApplicationSchema::post_dump: %s", original_data)
        logger.debug("deserialize_resources_original data: %s", original_data)
        data["resources"] = json.loads(original_data.resources)
        return data

class ExtendedTeamSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    description = fields.Str()
    cloudIdentityGroup = fields.Str()
    businessUnitId = fields.Int()
    isActive = fields.Boolean()
    businessUnit = fields.Nested(BusinessUnitSchema(many=False))
    lastUpdated = fields.Str()
    userCount = fields.Int()
    accessRequestedById = fields.Int()
    accessRequestedBy = fields.Nested(ExtendedUserSchema(many=False))

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
    ciId = fields.Int()
    ci = fields.Nested(CISchema(many=False))
    cdId = fields.Int()
    cd = fields.Nested(CDSchema(many=False))
    sourceControlId = fields.Int()
    sourceControl = fields.Nested(SourceControlSchema(many=False))
    environments = fields.Nested(LZEnvironmentSchema(many=True))
    favourite = fields.Boolean()
    teamId = fields.Int()
    applications = fields.Nested(ExtendedApplicationSchema(many=True))
    team = fields.Nested(ExtendedTeamSchema(many=False))
    deploymentFolderId = fields.Str()
    businessUnit = fields.Nested(BusinessUnitSchema(many=False))
    deploymentState = fields.Str()

class ExtendedTeamMemberSchema(Schema):
    id = fields.Int()
    user = fields.Nested(ExtendedUserSchema(many=False))

class ExtendedTeamMemberFullSchema(Schema):
    id = fields.Int()
    isActive = fields.Boolean()
    isTeamAdmin = fields.Boolean()
    teamId = fields.Int()
    team = fields.Nested(ExtendedTeamSchema(many=False))
    userId = fields.Int()
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
    teamMembers = fields.Nested(ExtendedTeamMemberFullSchema(many=True))

class ExtendedUserTeamsSchema(Schema):
    id = fields.Int()
    email = fields.Str()
    firstName = fields.Str()
    lastName = fields.Str()
    isAdmin = fields.Boolean()
    showWelcome = fields.Boolean()
    isActive = fields.Boolean()
    lastUpdated = fields.Str()
    teamMembers = fields.Nested(ExtendedTeamMemberFullSchema(many=True))

class ExtendedLZEnvironmentForDacSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    sharedVPCProjectId = fields.Str()

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
    ciId = fields.Int()
    ci = fields.Str()
    cdId = fields.Int()
    cd = fields.Str()
    sourceControlId = fields.Int()
    sourceControl = fields.Str()
    environments = fields.Nested(ExtendedLZEnvironmentForDacSchema(many=True))
    teamId = fields.Int()
    team = fields.Nested(ExtendedTeamDACSchema(many=False))
    deploymentFolderId = fields.Str()
    createdBy = fields.Str()

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

class ExtendedGoogleEndpointSchema(Schema):
    primaryGcpVpcSubnet = fields.Str()
    primaryRegion = fields.Str()
    primarySubnetName = fields.Str()
    secondaryGcpVpcSubnet = fields.Str()
    secondaryRegion = fields.Str()
    secondarySubnetName = fields.Str()

class ExtendedRemoteEndpointSchema(Schema):
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
    googleEndpoint = fields.Nested(ExtendedGoogleEndpointSchema(many=False))
    remoteEndpoint = fields.Nested(ExtendedRemoteEndpointSchema(many=False))
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
    lzEnvironmentId = fields.Int()
    lzEnvironment = fields.Nested(LZEnvironmentSchema(many=False))
    workspaceProjectId = fields.Str()
    deploymentProjectId = fields.Str()
    lastUpdated = fields.Str()

    @post_dump(pass_original=True)
    def deserialize_post_dump(self, data, original_data, **kwargs):
        # logger.debug("ExtendedApplicationDeploymentSchema::post_dump %s", original_data)
        data["id"] = original_data.applicationId
        return data

class ExtendedApplicationForDACSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    description = fields.Str()
    solutionId = fields.Int()
    lastUpdated = fields.Str()
    workspaceProjectId = fields.Str()
    activatorGitUrl = fields.Str()
    deploymentProjectId = fields.Str()
    mandatoryVariables = fields.List(fields.Dict())
    optionalVariables = fields.List(fields.Dict())
    deploymentEnvironment = fields.Nested(ExtendedLZEnvironmentForDacSchema)

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
    typeObj = fields.Nested(NotificationTypeSchema)
    details = fields.Nested(NotificationActivatorSchema)

class ExtendedNotificationTeamSchema(Schema):
    id = fields.Int()
    isActive = fields.Bool()
    lastUpdated = fields.Str()
    toUserId = fields.Int()
    fromUserId = fields.Int()
    importance = fields.Int()
    message = fields.Str()
    isRead = fields.Boolean()
    typeId = fields.Int()
    type = fields.Nested(NotificationTypeSchema)
    details = fields.Nested(NotificationTeamSchema)

class ExtendedNotificationApplicationDeploymentSchema(Schema):
    id = fields.Int()
    isActive = fields.Bool()
    lastUpdated = fields.Str()
    toUserId = fields.Int()
    fromUserId = fields.Int()
    importance = fields.Int()
    message = fields.Str()
    isRead = fields.Boolean()
    typeId = fields.Int()
    type = fields.Nested(NotificationTypeSchema)
    details = fields.Nested(NotificationApplicationDeploymentSchema)

class ExtendedNotificationSolutionDeploymentSchema(Schema):
    id = fields.Int()
    isActive = fields.Bool()
    lastUpdated = fields.Str()
    toUserId = fields.Int()
    fromUserId = fields.Int()
    importance = fields.Int()
    message = fields.Str()
    isRead = fields.Boolean()
    typeId = fields.Int()
    type = fields.Nested(NotificationTypeSchema)
    details = fields.Nested(NotificationSolutionDeploymentSchema)

class ExtendedNotificationSchema(OneOfSchema):
    type_field = "typeName"
    type_schemas = {
        "ACTIVATOR_ACCESS": ExtendedNotificationActivatorSchema,
        "TEAM_ACCESS": ExtendedNotificationTeamSchema,
        "APPLICATION_DEPLOYMENT": ExtendedNotificationApplicationDeploymentSchema,
        "SOLUTION_DEPLOYMENT": ExtendedNotificationSolutionDeploymentSchema,
    }

    def get_obj_type(self, obj):
        if obj.typeId == 1:
            return "ACTIVATOR_ACCESS"
        elif obj.typeId == 2:
            return "TEAM_ACCESS"
        elif obj.typeId == 3:
            return "APPLICATION_DEPLOYMENT"
        elif obj.typeId == 4:
            return "SOLUTION_DEPLOYMENT"
        else:
            raise Exception("Unknown object type: {}".format(obj.__class__.__name__))
