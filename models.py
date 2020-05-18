from datetime import datetime
from marshmallow import fields, pre_load, post_dump
from config import db, ma, app
import json

class ModelTools():

    @staticmethod
    def get_utc_epoch():
        return datetime.utcnow().strftime('%s')

    @staticmethod
    def get_utc_timestamp():
        return datetime.utcnow().strftime(("%Y-%m-%d %H:%M:%S"))

    @staticmethod
    def get_timestamp():
        return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))

    @staticmethod
    def datetime_as_string(dt):
        if dt is None:
            return datetime.utcnow().strftime(("%Y-%m-%d %H:%M:%S"))
        else:
            return dt.strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def json_dump(obj):
        #return json.dumps(obj, indent=2, sort_keys=True)
        return json.dumps(obj)

    # simple redact function, used prior to logging
    @staticmethod
    def redact_dict(my_dict):
        new_dict = my_dict.copy()
        new_dict['username'] = "XXXXX"
        new_dict['password'] = "XXXXX"
        return new_dict


# User
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100))
    firstName = db.Column(db.String(100))
    lastName = db.Column(db.String(100))
    isAdmin = db.Column(db.Boolean())
    isActive = db.Column(db.Boolean())

class UserSchema(ma.ModelSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = User
        sqla_session = db.session

# Activator
class Activator(db.Model):
    __tablename__ = "activator"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    type = db.Column(db.String(255))
    available = db.Column(db.Boolean())
    sensitivity = db.Column(db.String(255))
    category = db.Column(db.String(255))
    envs = db.Column(db.String(255))
    platforms = db.Column(db.String(255))
    lastUpdated = db.Column(db.String(255))
    userCapacity = db.Column(db.Integer)
    serverCapacity = db.Column(db.Integer)
    regions = db.Column(db.String(255))
    hosting = db.Column(db.String(255))
    apiManagement = db.Column(db.String(255))
    ci = db.Column(db.String(255))
    cd = db.Column(db.String(255))
    sourceControl = db.Column(db.String(255))
    businessUnit = db.Column(db.String(255))
    technologyOwner = db.Column(db.String(255))
    technologyOwnerEmail  = db.Column(db.String(255))
    billing = db.Column(db.String(255))
    activator = db.Column(db.String(255))
    status = db.Column(db.String(255))
    description = db.Column(db.String(255))
    accessRequestedBy = db.Column(db.Integer)
    source = db.Column(db.String(100))
    activatorLink = db.Column(db.String(255))


class ActivatorSchema(ma.ModelSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = Activator
        sqla_session = db.session


# Application
class Application(db.Model):
    __tablename__ = "application"
    id = db.Column(db.Integer, primary_key=True)
    solutionId = db.Column(db.Integer, db.ForeignKey('solution.id'))
    activatorId = db.Column(db.Integer, db.ForeignKey('activator.id'))
    name = db.Column(db.String(255))
    env = db.Column(db.String(64))
    status = db.Column(db.String(64))
    description = db.Column(db.String(255))
    lastUpdated = db.Column(db.String(255))
    resources = db.Column(db.String(255))


class ApplicationSchema(ma.ModelSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = Application
        sqla_session = db.session

    solutionId = fields.Int()
    activatorId = fields.Int()


# Solutions
class Solution(db.Model):
    __tablename__ = "solution"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.String(255))
    businessUnit = db.Column(db.String(255))
    costCentre = db.Column(db.String(255))
    ci = db.Column(db.String(255))
    cd = db.Column(db.String(255))
    sourceControl = db.Column(db.String(255))
    environments = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    favourite = db.Column(db.Boolean())
    teams = db.Column(db.Integer())
    lastUpdated = db.Column(db.String(255))
    deployed = db.Column(db.Boolean())
    deploymentState = db.Column(db.String(45))
    statusId = db.Column(db.Integer())
    statusCode = db.Column(db.String(45))
    statusMessage = db.Column(db.String(255))
    taskId = db.Column(db.String(100))

    applications = db.relationship('Application')

class SolutionSchema(ma.ModelSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = Solution
        sqla_session = db.session

# SolutionResource
class SolutionResource(db.Model):
    __tablename__ = "solutionresource"
    solutionId = db.Column(db.Integer(), primary_key=True)
    key = db.Column(db.String(50), primary_key=True)
    value = db.Column(db.String(255))

class SolutionResourceSchema(ma.ModelSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = SolutionResource
        sqla_session = db.session

# SolutionResourceJSON
class SolutionResourceJSON(db.Model):
    __tablename__ = "solutionresourcejson"
    solutionId = db.Column(db.Integer(), primary_key=True)
    json = db.Column(db.String(30000))

class SolutionResourceJSONSchema(ma.ModelSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = SolutionResourceJSON
        sqla_session = db.session

# Team
class Team(db.Model):
    __tablename__ = "team"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(200))
    businessUnitId = db.Column(db.Integer)
    isActive = db.Column(db.Boolean())


class TeamSchema(ma.ModelSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = Team
        sqla_session = db.session


# Team Member
class TeamMember(db.Model):
    __tablename__ = "teammember"
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer)
    teamId = db.Column(db.Integer)
    role = db.Column(db.String(100))
    isActive = db.Column(db.Boolean())


class TeamMemberSchema(ma.ModelSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = TeamMember
        sqla_session = db.session

# Cloud Account
class CloudAccount(db.Model):
    __tablename__ = "cloudaccount"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    userId = db.Column(db.Integer)
    isActive = db.Column(db.Boolean())


class CloudAccountSchema(ma.ModelSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = CloudAccount
        sqla_session = db.session

# Role
class Role(db.Model):
    __tablename__ = "role"
    name = db.Column(db.String(100), primary_key=True)
    cloudIdentityGroup = db.Column(db.String(200))
    description = db.Column(db.String(200))


class RoleSchema(ma.ModelSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = Role
        sqla_session = db.session



# Environment
class Environment(db.Model):
    __tablename__ = "environment"
    key = db.Column(db.String(255), primary_key=True)
    value = db.Column(db.String(255))

class EnvironmentSchema(ma.ModelSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = Environment
        sqla_session = db.session



# CI
class CI(db.Model):
    __tablename__ = "ci"
    key = db.Column(db.String(255), primary_key=True)
    value = db.Column(db.String(255))


class CISchema(ma.ModelSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = CI
        sqla_session = db.session
# CD
class CD(db.Model):
    __tablename__ = "cd"
    key = db.Column(db.String(255), primary_key=True)
    value = db.Column(db.String(255))


class CDSchema(ma.ModelSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = CD
        sqla_session = db.session

# SourceControl
class SourceControl(db.Model):
    __tablename__ = "sourcecontrol"
    key = db.Column(db.String(255), primary_key=True)
    value = db.Column(db.String(255))

class SourceControlSchema(ma.ModelSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = SourceControl
        sqla_session = db.session

# BusinessUnit
class BusinessUnit(db.Model):
    __tablename__ = "businessunit"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(200))
    isActive = db.Column(db.Boolean())

class BusinessUnitSchema(ma.ModelSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = BusinessUnit
        sqla_session = db.session

        
# LandingZoneProgressItem
class LandingZoneProgressItem(db.Model):
    __tablename__ = "landingzoneprogressitem"
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String)
    completed = db.Column(db.Boolean())

class LandingZoneProgressItemSchema(ma.ModelSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = LandingZoneProgressItem
        sqla_session = db.session

# LandingZoneAction
class LandingZoneAction(db.Model):
    __tablename__ = "landingzoneaction"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    categoryName = db.Column(db.String)
    categoryClass= db.Column(db.String)
    completionRate = db.Column(db.Integer)
    locked = db.Column(db.Boolean())
    routerLink = db.Column(db.String)

class LandingZoneActionSchema(ma.ModelSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = LandingZoneAction
        sqla_session = db.session

        
# LandingZoneWAN
class LandingZoneWAN(db.Model):
    __tablename__ = "landingzonewan"
    id = db.Column(db.Integer, primary_key=True)
    googleSession__primaryGcpVpcSubnet = db.Column(db.String)
    googleSession__primaryRegion = db.Column(db.String)
    googleSession__primarySubnetName = db.Column(db.String)
    googleSession__secondaryGcpVpcSubnet = db.Column(db.String)
    googleSession__secondaryRegion = db.Column(db.String)
    googleSession__secondarySubnetName = db.Column(db.String)
    onPremiseSession__primaryBgpPeer = db.Column(db.String)
    onPremiseSession__primaryPeerIp = db.Column(db.String)
    onPremiseSession__primaryPeerIpSubnet = db.Column(db.String)
    onPremiseSession__primarySharedSecret = db.Column(db.String)
    onPremiseSession__primaryVpnTunnel = db.Column(db.String)
    onPremiseSession__secondaryBgpPeer = db.Column(db.String)
    onPremiseSession__secondaryPeerIp = db.Column(db.String)
    onPremiseSession__secondaryPeerIpSubnet = db.Column(db.String)
    onPremiseSession__secondarySharedSecret = db.Column(db.String)
    onPremiseSession__secondaryVpnTunnel = db.Column(db.String)
    onPremiseSession__vendor = db.Column(db.String)
    vpn__bgpInterfaceNetLength = db.Column(db.String)
    vpn__bgpRoutingMode = db.Column(db.String)
    vpn__cloudRouterName = db.Column(db.String)
    vpn__description = db.Column(db.String)
    vpn__externalVpnGateway = db.Column(db.String)
    vpn__googleASN = db.Column(db.Integer)
    vpn__haVpnGateway = db.Column(db.String)
    vpn__peerASN = db.Column(db.Integer)
    vpn__projectName = db.Column(db.String)
    vpn__subnetMode = db.Column(db.String)
    vpn__vpcName = db.Column(db.String)


class LandingZoneWANSchema(ma.ModelSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = LandingZoneWAN
        sqla_session = db.session


# BGPRoutingMode 
class BGPRoutingMode(db.Model):
    __tablename__ = "bgproutingmode"
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String)
    value = db.Column(db.String)


class BGPRoutingModeSchema(ma.ModelSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = BGPRoutingMode
        sqla_session = db.session


# SubnetMode
class SubnetMode(db.Model):
    __tablename__ = "subnetmode"
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String)
    value = db.Column(db.String)


class SubnetModeSchema(ma.ModelSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = SubnetMode
        sqla_session = db.session
 

# VPNOnPremiseVendor
class VPNOnPremiseVendor(db.Model):
    __tablename__ = "vpnonpremisevendor"
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String)
    value = db.Column(db.String)


class VPNOnPremiseVendorSchema(ma.ModelSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = VPNOnPremiseVendor
        sqla_session = db.session


# LZFolderStructureMeta
class LZFolderStructureMeta(db.Model):
    __tablename__ = "lzfolderstructuremeta"
    id = db.Column(db.Integer, primary_key=True)
    isEnable = db.Column(db.Boolean)
    name = db.Column(db.String)
    childrenId = db.Column(db.Integer)

class LZFolderStructureMeta(ma.ModelSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = LZFolderStructureMeta
        sqla_session = db.session

# LZLANVPCMeta
class LZLANVPCMeta(db.Model):
    __tablename__ = "lzlanvpcmeta"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    environments = db.Column(db.String)

class LZLANVPCMeta(ma.ModelSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = LZLANVPCMeta
        sqla_session = db.session
