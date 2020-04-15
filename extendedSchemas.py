from marshmallow import Schema, fields, pre_load, post_load, pre_dump, post_dump
#from flask import Flask

#from flask_sqlalchemy import SQLAlchemy
#from flask_marshmallow import Marshmallow
#import json

#app = Flask(__name__)
#db = SQLAlchemy(app)
#ma = Marshmallow(app)


class IdSchema(Schema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    id = fields.Int()


class HealthSchema(Schema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    status = fields.Str()


class ExtendedUserSchema(Schema):
    id = fields.Int()
    email = fields.Str()
    firstName = fields.Str()
    lastName = fields.Str()
    isAdmin = fields.Boolean()


class ExtendedActivatorSchema(Schema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    id = fields.Int()
    name = fields.Str()
    type = fields.Str()
    available = fields.Boolean()
    sensitivity = fields.Str()
    category = fields.Str()
    envs = fields.List(fields.Str())
    platforms = fields.List(fields.Str())
    lastUpdated = fields.Str()
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
    technologyOwnerEmail  = fields.Str()
    billing = fields.Str()
    activator = fields.Str()
    resources = fields.List(fields.Dict())
    status = fields.Str()
    description = fields.Str()
    accessRequestedBy = fields.Nested(ExtendedUserSchema(many=False))
    source = fields.Str()
    activatorLink = fields.Str()


class ExtendedApplicationSchema(Schema):
    solutionId = fields.Int()
    activatorId = fields.Int()
    name = fields.Str()
    env = fields.Str()
    status = fields.Str()
    description = fields.Str()
    lastUpdated = fields.Str()
    activator = fields.Nested(ExtendedActivatorSchema(many=False))



class ExtendedSolutionSchema(Schema):
    __envelope__ = {"single": "solution", "many": "solutions"}

    id = fields.Int()
    name = fields.Str()
    description = fields.Str()
    buinessUnit = fields.Str()
    costCentre = fields.Str()
    ci = fields.Str()
    cd = fields.Str()
    sourceControl = fields.Str()
    environments = fields.List(fields.Str())
    active = fields.Boolean()
    favourite = fields.Boolean()
    teams = fields.Int()
    lastUpdated = fields.Str()
    applications = fields.Nested(ExtendedApplicationSchema(many=True))


class SolutionNamesOnlySchema(Schema):
    __envelope__ = {"single": "solution", "many": "solutions"}

    id = fields.Int()
    name = fields.Str()


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
