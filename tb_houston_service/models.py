from sqlalchemy.ext.declarative import declarative_base
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from config import db

Base = declarative_base()


# Activator
class Activator(Base):
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


class ActivatorSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Activator
        include_fk = True
        load_instance = True


# Application
class Application(Base):
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


class ApplicationSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Application
        include_fk = True
        load_instance = True

    #solutionId = fields.Int()
    #activatorId = fields.Int()


# BusinessUnit
class BusinessUnit(Base):
    __tablename__ = "businessunit"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(200))
    isActive = db.Column(db.Boolean())


class BusinessUnitSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = BusinessUnit
        include_fk = True
        load_instance = True


# BGPRoutingMode
class BGPRoutingMode(Base):
    __tablename__ = "bgproutingmode"
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String)
    value = db.Column(db.String)


class BGPRoutingModeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = BGPRoutingMode
        include_fk = True
        load_instance = True


# CD
class CD(Base):
    __tablename__ = "cd"
    key = db.Column(db.String(255), primary_key=True)
    value = db.Column(db.String(255))


class CDSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = CD
        include_fk = True
        load_instance = True


# CI
class CI(Base):
    __tablename__ = "ci"
    key = db.Column(db.String(255), primary_key=True)
    value = db.Column(db.String(255))


class CISchema(SQLAlchemyAutoSchema):
    class Meta:
        model = CI
        include_fk = True
        load_instance = True


# Cloud Account
class CloudAccount(Base):
    __tablename__ = "cloudaccount"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    userId = db.Column(db.Integer)
    isActive = db.Column(db.Boolean())


class CloudAccountSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = CloudAccount
        include_fk = True
        load_instance = True


# Environment
class Environment(Base):
    __tablename__ = "environment"
    key = db.Column(db.String(255), primary_key=True)
    value = db.Column(db.String(255))


class EnvironmentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Environment
        include_fk = True
        load_instance = True


# Folder
class Folder(Base):
    __tablename__ = "folder"
    id = db.Column(db.Integer, primary_key=True)
    parentFolderId = db.Column(db.String(45))
    folderId = db.Column(db.String(45))
    folderName = db.Column(db.String(100))
    status = db.Column(db.String(50))
    taskId = db.Column(db.String(50))


class FolderSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Folder
        include_fk = True
        load_instance = True


# LandingZoneAction
class LandingZoneAction(Base):
    __tablename__ = "landingzoneaction"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    categoryName = db.Column(db.String)
    categoryClass= db.Column(db.String)
    completionRate = db.Column(db.Integer)
    locked = db.Column(db.Boolean())
    routerLink = db.Column(db.String)


class LandingZoneActionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = LandingZoneAction
        include_fk = True
        load_instance = True


# LandingZoneProgressItem
class LandingZoneProgressItem(Base):
    __tablename__ = "landingzoneprogressitem"
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String)
    completed = db.Column(db.Boolean())


class LandingZoneProgressItemSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = LandingZoneProgressItem
        include_fk = True
        load_instance = True


# LandingZoneWAN
class LandingZoneWAN(Base):
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


class LandingZoneWANSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = LandingZoneWAN
        include_fk = True
        load_instance = True


# LZLANVPCMeta
class LZMetadata(Base):
    __tablename__ = "lzmetadata"
    group = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, primary_key=True)
    value = db.Column(db.String)
    description = db.Column(db.String)
    active = db.Column(db.Boolean)


class LZMetadataSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = LZMetadata
        include_fk = True
        load_instance = True


# Role
class Role(Base):
    __tablename__ = "role"
    name = db.Column(db.String(100), primary_key=True)
    cloudIdentityGroup = db.Column(db.String(200))
    description = db.Column(db.String(200))


class RoleSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Role
        include_fk = True
        load_instance = True


# Solutions
class Solution(Base):
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
    teamId = db.Column(db.Integer())
    lastUpdated = db.Column(db.String(255))
    deployed = db.Column(db.Boolean())
    deploymentState = db.Column(db.String(45))
    statusId = db.Column(db.Integer())
    statusCode = db.Column(db.String(45))
    statusMessage = db.Column(db.String(255))
    taskId = db.Column(db.String(100))
    deploymentFolderId = db.Column(db.String(50))
    applications = db.relationship('Application')


class SolutionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Solution
        include_fk = True
        load_instance = True


# SolutionResource
class SolutionResource(Base):
    __tablename__ = "solutionresource"
    solutionId = db.Column(db.Integer(), primary_key=True)
    key = db.Column(db.String(50), primary_key=True)
    value = db.Column(db.String(255))


class SolutionResourceSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = SolutionResource
        include_fk = True
        load_instance = True


# SolutionResourceJSON
class SolutionResourceJSON(Base):
    __tablename__ = "solutionresourcejson"
    solutionId = db.Column(db.Integer(), primary_key=True)
    json = db.Column(db.String(30000))


class SolutionResourceJSONSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = SolutionResourceJSON
        include_fk = True
        load_instance = True


# SourceControl
class SourceControl(Base):
    __tablename__ = "sourcecontrol"
    key = db.Column(db.String(255), primary_key=True)
    value = db.Column(db.String(255))


class SourceControlSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = SourceControl
        include_fk = True
        load_instance = True


# SubnetMode
class SubnetMode(Base):
    __tablename__ = "subnetmode"
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String)
    value = db.Column(db.String)


class SubnetModeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = SubnetMode
        include_fk = True
        load_instance = True


# Team
class Team(Base):
    __tablename__ = "team"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(200))
    businessUnitId = db.Column(db.Integer)
    isActive = db.Column(db.Boolean())


class TeamSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Team
        include_fk = True
        load_instance = True


# Team Member
class TeamMember(Base):
    __tablename__ = "teammember"
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer)
    teamId = db.Column(db.Integer)
    role = db.Column(db.String(100))
    isActive = db.Column(db.Boolean())


class TeamMemberSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = TeamMember
        include_fk = True
        load_instance = True


# User
class User(Base):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100))
    firstName = db.Column(db.String(100))
    lastName = db.Column(db.String(100))
    isAdmin = db.Column(db.Boolean())
    isActive = db.Column(db.Boolean())
    showWelcome = db.Column(db.Boolean())


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_fk = True
        load_instance = True


# VPNOnPremiseVendor
class VPNOnPremiseVendor(Base):
    __tablename__ = "vpnonpremisevendor"
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String)
    value = db.Column(db.String)


class VPNOnPremiseVendorSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = VPNOnPremiseVendor
        include_fk = True
        load_instance = True
