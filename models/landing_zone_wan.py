from config import db, ma


class LandingZoneWAN(db.Model):
    __tablename__ = "landingzonewan"
    __table_args__ = {"schema": "eagle_db"}
    id = db.Column(db.Integer, primary_key=True)
    googleEndpoint__primaryGcpVpcSubnet = db.Column(db.String)
    googleEndpoint__primaryRegion = db.Column(db.String)
    googleEndpoint__primarySubnetName = db.Column(db.String)
    googleEndpoint__secondaryGcpVpcSubnet = db.Column(db.String)
    googleEndpoint__secondaryRegion = db.Column(db.String)
    googleEndpoint__secondarySubnetName = db.Column(db.String)
    remoteEndpoint__primaryBgpPeer = db.Column(db.String)
    remoteEndpoint__primaryPeerIp = db.Column(db.String)
    remoteEndpoint__primaryPeerIpSubnet = db.Column(db.String)
    remoteEndpoint__primarySharedSecret = db.Column(db.String)
    remoteEndpoint__primaryVpnTunnel = db.Column(db.String)
    remoteEndpoint__secondaryBgpPeer = db.Column(db.String)
    remoteEndpoint__secondaryPeerIp = db.Column(db.String)
    remoteEndpoint__secondaryPeerIpSubnet = db.Column(db.String)
    remoteEndpoint__secondarySharedSecret = db.Column(db.String)
    remoteEndpoint__secondaryVpnTunnel = db.Column(db.String)
    remoteEndpoint__vendor = db.Column(db.String)
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


class LandingZoneWANSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = LandingZoneWAN
        include_fk = True
        load_instance = True
