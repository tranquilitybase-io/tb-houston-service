from marshmallow import Schema, fields, pre_load, post_load, pre_dump, post_dump, pprint
#from flask import Flask

#from flask_sqlalchemy import SQLAlchemy
#from flask_marshmallow import Marshmallow
#import json

#app = Flask(__name__)
#db = SQLAlchemy(app)
#ma = Marshmallow(app)

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
    available = fields.Str()
    sensitivity = fields.Str()
    category = fields.Str()
    envs = fields.List(fields.Str())
    platforms = fields.List(fields.Str())
    lastUpdated = fields.Str()
    userCapacity = fields.Str()
    serverCapacity = fields.Str()
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


class ExtendedApplicationSchema(Schema):
    solutionId = fields.Int()
    activatorId = fields.Int()
    name = fields.Str()
    env = fields.Str()
    status = fields.Str()
    description = fields.Str()
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
    teams = fields.Str()
    lastUpdated = fields.Str()
    applications = fields.Nested(ExtendedApplicationSchema(many=True))


class GoogleSessonSchema(Schema):
    primaryGcpVpcSubnet = fields.Str()
    primaryRegion = fields.Str()
    primarySubnetName = fields.Str()
    secondaryGcpVpcSubnet = fields.Str()
    secondaryRegion = fields.Str()
    secondarySubnetName = fields.Str()


class OnPremiseSessonSchema(Schema):
    onPremiseSession__primaryBgpPeer = fields.Str()
    onPremiseSession__primaryPeerIp = fields.Str()
    onPremiseSession__primaryPeerIpSubnet = fields.Str()
    onPremiseSession__primarySharedSecret = fields.Str()
    onPremiseSession__primaryVpnTunnel = fields.Str()
    onPremiseSession__secondaryBgpPeer = fields.Str()
    onPremiseSession__secondaryPeerIp = fields.Str()
    onPremiseSession__secondaryPeerIpSubnet = fields.Str()
    onPremiseSession__secondarySharedSecret = fields.Str()
    onPremiseSession__secondaryVpnTunnel = fields.Str()
    onPremiseSession__vendor = fields.Str()


class VPNSchema(Schema):
    vpn__bgpInterfaceNetLength = fields.Str()
    vpn__bgpRoutingMode = fields.Str()
    vpn__cloudRouterName = fields.Str()
    vpn__description = fields.Str()
    vpn__externalVpnGateway = fields.Str()
    vpn__googleASN = fields.Int()
    vpn__haVpnGateway = fields.Str()
    vpn__peerASN = fields.Int()
    vpn__projectName = fields.Str()
    vpn__subnetMode = fields.Str()
    vpn__vpcName = fields.Str()


class LandingZoneWANSchema(Schema):
    __envelope__ = {"single": "landingZoneWAN", "many": "landingZoneWANs"}
    id = fields.Int()
    googleSesson = fields.Nested(GoogleSessionSchema(many=False))
    onPremiseSession = fields.Nested(OnPremiseSessionSchema(many=False))
    vpn = fields.Nested(vpnSchema(many=False))
