-- MySQL dump 10.13  Distrib 5.7.29, for macos10.14 (x86_64)
--
-- Host: 0.0.0.0    Database: eagle_db
-- ------------------------------------------------------
-- Server version	5.7.29

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `activator`
--

DROP TABLE IF EXISTS `activator`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `activator` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `category` varchar(255) DEFAULT NULL,
  `available` tinyint(1) DEFAULT NULL,
  `sensitivity` varchar(255) DEFAULT NULL,
  `type` varchar(255) DEFAULT NULL,
  `envs` varchar(255) DEFAULT NULL,
  `platforms` varchar(255) DEFAULT NULL,
  `lastUpdated` datetime DEFAULT NULL,
  `userCapacity` int(11) DEFAULT NULL,
  `serverCapacity` int(11) DEFAULT NULL,
  `regions` varchar(255) DEFAULT NULL,
  `hosting` varchar(255) DEFAULT NULL,
  `apiManagement` varchar(255) DEFAULT NULL,
  `ci` varchar(255) DEFAULT NULL,
  `cd` varchar(255) DEFAULT NULL,
  `sourceControl` varchar(255) DEFAULT NULL,
  `businessUnit` varchar(255) DEFAULT NULL,
  `technologyOwner` varchar(255) DEFAULT NULL,
  `technologyOwnerEmail` varchar(255) DEFAULT NULL,
  `billing` varchar(255) DEFAULT NULL,
  `activator` varchar(255) DEFAULT NULL,
  `status` varchar(255) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `accessRequestedBy` int(11) DEFAULT NULL,
  `source` varchar(100) DEFAULT NULL,
  `activatorLink` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=116 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `activator`
--

LOCK TABLES `activator` WRITE;
/*!40000 ALTER TABLE `activator` DISABLE KEYS */;
INSERT INTO `activator` VALUES (1,'CMS Web App','Web application',1,'Public','Tier 3','[\"POC\", \"DEV\"]','[\"GCP\"]','2020-05-12 08:29:07',1000,1200,'[\"UK\", \"DB\"]','[\"Appengine\"]','[\"ApiGee\"]','[\"Jenkins\", \"Travis\"]','[\"Codeship\", \"Option\"]','[\"JIRA\", \"Option\"]','FICC Business Unit','Sanjeev Gupta','s.gupta@company.name','Monthly: Eagle tier 3','Single Region Kubernetes','Available','Some very long description that I did not want to copy. Some very long description that I did not want to copy. Some very long description that I did not want to copy',0,'open',''),(2,'Multi region kubernetes','Micro-services',1,'Restricted','Tier 1','[\"POC\", \"AWS\", \"Other\", \"Fancy\"]','[\"GCP\"]','2020-05-07 08:38:56',1300,2000,'[\"UK\", \"DB\"]','[\"Appengine\"]','[\"ApiGee\"]','[\"Jenkins\", \"Travis\"]','[\"Codeship\", \"Option\"]','[\"JIRA\", \"Option\"]','M&A Business Unit','Nathanael Stoltenberg','Nathanael.Stoltenberg@yahoo.com','Monthly: Eagle tier 1','Multi Region Kubernetes','Deprecated','Some very long description that I did not want to copy. Some very long description that I did not want to copy. Some very long description that I did not want to copy',0,'open',''),(3,'SQL Single region kubernetes','Micro-services',1,'Restricted','Tier 2','[\"POC\", \"Prod\"]','[\"Azure\", \"GCP\", \"AWS\", \"Other\", \"Fancy\"]','2020-05-07 10:49:44',100,120,'[\"UK\", \"DB\"]','[\"Appengine\"]','[\"ApiGee\"]','[\"Jenkins\", \"Travis\"]','[\"Codeship\", \"Option\"]','[\"JIRA\", \"Option\"]','Equity Capital Business Unit','Brando Howell','Brando.Howell@hotmail.com','Monthly: Eagle tier 2','SQL Single region kubernetes','Deprecated','Some very long description that I did not want to copy. Some very long description that I did not want to copy. Some very long description that I did not want to copy',0,'open',''),(101,'CMS Web App','Tier 3',1,'Public','Web application','[\"POC\", \"DEV\", \"PRD\"]','[\"GCP\", \"Cloud Foundry\"]','2020-05-12 08:29:57',500,300,'[\"UK\", \"DB\"]','[\"Appengine\"]','[\"ApiGee\"]','[\"Jenkins\", \"Travis\"]','[\"Codeship\", \"Option\"]','[\"JIRA\", \"Option\"]','Debit Capital Business Unit','Mohammed Will PhD','Mohammed.Will@gmail.com','Monthly: Eagle tier 3','CMS Web App','Available','Some very long description that I did not want to copy. Some very long description that I did not want to copy. Some very long description that I did not want to copy',0,'thirdparty',''),(102,'Multi region kubernetes','Micro-services',1,'Restricted','Tier 1','[\"POC\", \"AWS\", \"Other\", \"Fancy\"]','[\"GCP\"]','2020-05-07 10:56:43',1600,2500,'[\"UK\", \"DB\"]','[\"Appengine\"]','[\"ApiGee\"]','[\"Jenkins\", \"Travis\"]','[\"Codeship\", \"Option\"]','[\"JIRA\", \"Option\"]','FICC Business Unit','Tressa Ullrich','Tressa97@yahoo.com','Monthly: Eagle tier 1','Multi region kubernetes','Locked','Some very long description that I did not want to copy. Some very long description that I did not want to copy. Some very long description that I did not want to copy',0,'thirdparty',''),(103,'SQL Single region kubernetes','Micro-services',1,'Restricted','Tier 2','[\"POC\", \"Prod\"]','[\"Azure\", \"GCP\", \"AWS\", \"Other\", \"Fancy\"]','2020-04-02 19:25:52',900,600,'[\"UK\", \"DB\", \"HK\", \"US\", \"AU\"]','[\"Appengine\"]','[\"ApiGee\"]','[\"Jenkins\", \"Travis\"]','[\"Codeship\", \"Option\"]','[\"JIRA\", \"Option\"]','M&A Business Unit','Rose Dickens Sr.','Rose.Dickens19@hotmail.com','Monthly: Eagle tier 2','SQL Single region kubernetes','Available','Some very long description that I did not want to copy. Some very long description that I did not want to copy. Some very long description that I did not want to copy',0,'internal',''),(109,'CMS Web App','Web application',1,'Public','Tier 3','[\"POC\", \"DEV\", \"PRD\"]','[\"GCP\"]','2020-04-07 13:39:47',1000,1200,'[\"UK\", \"DB\"]','[\"Appengine\"]','[\"ApiGee\"]','[\"Jenkins\", \"Travis\"]','[\"Codeship\", \"Option\"]','[\"JIRA\", \"Option\"]','FICC Business Unit','Sanjeev Gupta','s.gupta@company.name','Monthly: Eagle tier 3','Single Region Kubernetes','Available','Some very long description that I did not want to copy. Some very long description that I did not want to copy. Some very long description that I did not want to copy',0,'open',''),(110,'CMS Web App','Web application',1,'Public','Tier 3','[\"POC\", \"DEV\", \"PRD\"]','[\"GCP\"]','2020-04-07 13:38:22',1000,1200,'[\"UK\", \"DB\"]','[\"Appengine\"]','[\"ApiGee\"]','[\"Jenkins\", \"Travis\"]','[\"Codeship\", \"Option\"]','[\"JIRA\", \"Option\"]','FICC Business Unit','Sanjeev Gupta','s.gupta@company.name','Monthly: Eagle tier 3','Single Region Kubernetes','Available','Some very long description that I did not want to copy. Some very long description that I did not want to copy. Some very long description that I did not want to copy',0,'open',''),(111,'CMS Web App','Web application',1,'Public','Tier 3','[\"POC\", \"DEV\"]','[\"GCP\"]','2020-05-07 10:55:49',1000,1200,'[\"UK\", \"DB\"]','[\"Appengine\"]','[\"ApiGee\"]','[\"Jenkins\", \"Travis\"]','[\"Codeship\", \"Option\"]','[\"JIRA\", \"Option\"]','FICC Business Unit','Sanjeev Gupta','s.gupta@company.name','Monthly: Eagle tier 3','Single Region Kubernetes','Locked','Some very long description that I did not want to copy. Some very long description that I did not want to copy. Some very long description that I did not want to copy',0,'open','');
/*!40000 ALTER TABLE `activator` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `application`
--

DROP TABLE IF EXISTS `application`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `application` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `solutionId` int(11) NOT NULL,
  `activatorId` int(11) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `env` varchar(255) DEFAULT NULL,
  `status` varchar(255) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `lastUpdated` datetime DEFAULT NULL,
  `resources` varchar(255) DEFAULT '[]',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `application`
--

LOCK TABLES `application` WRITE;
/*!40000 ALTER TABLE `application` DISABLE KEYS */;
INSERT INTO `application` VALUES (1,1,1,'Placeholder','DEV','Active','Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et do','2020-04-16 17:58:21','[{\"ipAddress\": \"40.123.45.236\", \"name\": \"GKE Cluster\"}, {\"ipAddress\": \"40.123.45.236\", \"name\": \"Cloud SQL\"}]'),(2,1,2,'Other App','POC','Active','Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et do','2020-04-02 00:00:00','[{\"name\": \"GKE Cluster\", \"ipAddress\": \"40.123.45.236\"}, {\"name\": \"Cloud SQL\", \"ipAddress\": \"40.123.45.236\"}]'),(3,2,3,'Other App','POC','Active','Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et do','2020-04-02 00:00:00','[{\"name\": \"ITSO\", \"ipAddress\": \"40.123.45.236\"}, {\"name\": \"Cloud SQL\", \"ipAddress\": \"40.123.45.236\"}]'),(4,2,2,'Great App','Prod','Active','Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et do','2020-04-02 00:00:00','[{\"name\": \"GKE Cluster\", \"ipAddress\": \"40.123.45.236\"}, {\"name\": \"Cloud SQL\", \"ipAddress\": \"40.123.45.236\"}]'),(5,3,3,'Placeholder','Prod','Active','Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et do','2020-04-02 00:00:00','[{\"name\": \"ITSO\", \"ipAddress\": \"40.123.45.236\"}, {\"name\": \"Cloud SQL\", \"ipAddress\": \"40.123.45.236\"}]'),(6,1,2,'My First App','POC','Active','Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et do','2020-04-03 09:23:37','[{\"name\": \"GKE Cluster\", \"ipAddress\": \"40.123.45.236\"}, {\"name\": \"Cloud SQL\", \"ipAddress\": \"40.123.45.236\"}]');
/*!40000 ALTER TABLE `application` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bgproutingmode`
--

DROP TABLE IF EXISTS `bgproutingmode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bgproutingmode` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `key` varchar(45) DEFAULT NULL,
  `value` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bgproutingmode`
--

LOCK TABLES `bgproutingmode` WRITE;
/*!40000 ALTER TABLE `bgproutingmode` DISABLE KEYS */;
INSERT INTO `bgproutingmode` VALUES (1,'Global','Global');
/*!40000 ALTER TABLE `bgproutingmode` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `businessunit`
--

DROP TABLE IF EXISTS `businessunit`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `businessunit` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `description` varchar(200) NOT NULL,
  `isActive` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `businessunit`
--

LOCK TABLES `businessunit` WRITE;
/*!40000 ALTER TABLE `businessunit` DISABLE KEYS */;
INSERT INTO `businessunit` VALUES (5,'Data','Data',1),(6,'FICC','FICC',1),(7,'Modern Apps','Modern Apps',1);
/*!40000 ALTER TABLE `businessunit` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cd`
--

DROP TABLE IF EXISTS `cd`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cd` (
  `key` varchar(100) NOT NULL,
  `value` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cd`
--

LOCK TABLES `cd` WRITE;
/*!40000 ALTER TABLE `cd` DISABLE KEYS */;
INSERT INTO `cd` VALUES ('Central','Central'),('Screwdriver','Screwdriver'),('Spinnaker','Spinnaker'),('Team City','Team City');
/*!40000 ALTER TABLE `cd` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ci`
--

DROP TABLE IF EXISTS `ci`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ci` (
  `key` varchar(100) NOT NULL,
  `value` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ci`
--

LOCK TABLES `ci` WRITE;
/*!40000 ALTER TABLE `ci` DISABLE KEYS */;
INSERT INTO `ci` VALUES ('Bamboo','Bamboo'),('Cloud native','Cloud native'),('Jenkins','Jenkins'),('Team City','Team City'),('Travis','Travis');
/*!40000 ALTER TABLE `ci` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cloudaccount`
--

DROP TABLE IF EXISTS `cloudaccount`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cloudaccount` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `userId` int(11) NOT NULL,
  `isActive` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cloudaccount`
--

LOCK TABLES `cloudaccount` WRITE;
/*!40000 ALTER TABLE `cloudaccount` DISABLE KEYS */;
/*!40000 ALTER TABLE `cloudaccount` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `environment`
--

DROP TABLE IF EXISTS `environment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `environment` (
  `key` varchar(100) NOT NULL,
  `value` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `environment`
--

LOCK TABLES `environment` WRITE;
/*!40000 ALTER TABLE `environment` DISABLE KEYS */;
INSERT INTO `environment` VALUES ('Development','Development'),('Production','Production');
/*!40000 ALTER TABLE `environment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `landingzoneaction`
--

DROP TABLE IF EXISTS `landingzoneaction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `landingzoneaction` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `categoryName` varchar(255) NOT NULL,
  `categoryClass` varchar(255) NOT NULL,
  `completionRate` int(11) NOT NULL DEFAULT '0',
  `locked` tinyint(1) NOT NULL DEFAULT '0',
  `routerLink` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `landingzoneaction`
--

LOCK TABLES `landingzoneaction` WRITE;
/*!40000 ALTER TABLE `landingzoneaction` DISABLE KEYS */;
INSERT INTO `landingzoneaction` VALUES (1,'Folder structure','','folder-structure',100,0,''),(2,'LAN','Network Setup','network-setup',100,0,''),(3,'WAN','Network Setup','network-setup',0,0,'/administration/landing-zone/wan'),(4,'DNS','Network Setup','network-setup',75,1,''),(5,'Internet access','Network Setup','network-setup',9,1,''),(6,'SSO','AD Integration','ad-integration',25,1,''),(7,'ADFS','AD Integration','ad-integration',0,1,''),(8,'Stackdriver','Logging','logging',50,1,''),(9,'Data Dog','Logging','logging',30,1,''),(10,'Cloud Health','Billing/Cost Management','billing-cost-management',19,1,''),(11,'Security','','security',13,1,''),(12,'Multizone setup','','multizone-setup',12,1,'');
/*!40000 ALTER TABLE `landingzoneaction` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `landingzoneprogressitem`
--

DROP TABLE IF EXISTS `landingzoneprogressitem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `landingzoneprogressitem` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `label` varchar(255) DEFAULT NULL,
  `completed` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `landingzoneprogressitem`
--

LOCK TABLES `landingzoneprogressitem` WRITE;
/*!40000 ALTER TABLE `landingzoneprogressitem` DISABLE KEYS */;
INSERT INTO `landingzoneprogressitem` VALUES (0,'Folder structure',1),(1,'LAN',1),(2,'WAN',0),(3,'DNS',0),(4,'ADFS',0),(5,'SSO',0),(6,'Logging',0),(7,'Billing',0);
/*!40000 ALTER TABLE `landingzoneprogressitem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `landingzonewan`
--

DROP TABLE IF EXISTS `landingzonewan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `landingzonewan` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `googleSession__primaryGcpVpcSubnet` varchar(100) DEFAULT NULL,
  `googleSession__primaryRegion` varchar(45) DEFAULT NULL,
  `googleSession__primarySubnetName` varchar(45) DEFAULT NULL,
  `googleSession__secondaryGcpVpcSubnet` varchar(45) DEFAULT NULL,
  `googleSession__secondaryRegion` varchar(45) DEFAULT NULL,
  `googleSession__secondarySubnetName` varchar(45) DEFAULT NULL,
  `onPremiseSession__primaryBgpPeer` varchar(45) DEFAULT NULL,
  `onPremiseSession__primaryPeerIp` varchar(45) DEFAULT NULL,
  `onPremiseSession__primaryPeerIpSubnet` varchar(45) DEFAULT NULL,
  `onPremiseSession__primarySharedSecret` varchar(45) DEFAULT NULL,
  `onPremiseSession__primaryVpnTunnel` varchar(45) DEFAULT NULL,
  `onPremiseSession__secondaryBgpPeer` varchar(45) DEFAULT NULL,
  `onPremiseSession__secondaryPeerIp` varchar(45) DEFAULT NULL,
  `onPremiseSession__secondaryPeerIpSubnet` varchar(45) DEFAULT NULL,
  `onPremiseSession__secondarySharedSecret` varchar(45) DEFAULT NULL,
  `onPremiseSession__secondaryVpnTunnel` varchar(45) DEFAULT NULL,
  `onPremiseSession__vendor` varchar(45) DEFAULT NULL,
  `vpn__bgpInterfaceNetLength` varchar(45) DEFAULT NULL,
  `vpn__bgpRoutingMode` varchar(45) DEFAULT NULL,
  `vpn__cloudRouterName` varchar(45) DEFAULT NULL,
  `vpn__description` varchar(255) DEFAULT NULL,
  `vpn__externalVpnGateway` varchar(45) DEFAULT NULL,
  `vpn__googleASN` int(11) DEFAULT NULL,
  `vpn__haVpnGateway` varchar(45) DEFAULT NULL,
  `vpn__peerASN` int(11) DEFAULT NULL,
  `vpn__projectName` varchar(45) DEFAULT NULL,
  `vpn__subnetMode` varchar(45) DEFAULT NULL,
  `vpn__vpcName` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `landingzonewan`
--

LOCK TABLES `landingzonewan` WRITE;
/*!40000 ALTER TABLE `landingzonewan` DISABLE KEYS */;
INSERT INTO `landingzonewan` VALUES (1,'dev','dev','dev','dev','dev','dev','dev','dev','dev','dev','dev','dev','dev','dev','dev','dev','Fortinet','dev','Global','dev','Backup VPN connection between GCP US and CISCO 5505 on prem','dev',60000,'dev',60005,'dev','dev ','dev'),(2,'Subnet','abc','abc','abc','abc','abc','string','string','string','string','string','string','string','string','string','string','string','abc','abc','abc','abc','abc',12345,'abc',56789,'abc','abc','abc'),(3,'10.0.1.3/24','UK','SUBNET','','','','sds','209.11.34.56','209.11.34.56','sdds','TUN','','','','','','Fortinet','30','Global','aSA','asa','SAS',65001,'asas',65002,'asas','Custom','sasa');
/*!40000 ALTER TABLE `landingzonewan` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `solution`
--

DROP TABLE IF EXISTS `solution`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `solution` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `businessUnit` varchar(255) DEFAULT NULL,
  `costCentre` varchar(255) DEFAULT NULL,
  `ci` varchar(255) DEFAULT NULL,
  `cd` varchar(255) DEFAULT NULL,
  `sourceControl` varchar(255) DEFAULT NULL,
  `environments` varchar(255) DEFAULT NULL,
  `active` tinyint(1) DEFAULT NULL,
  `favourite` tinyint(1) DEFAULT NULL,
  `teams` varchar(255) DEFAULT NULL,
  `lastUpdated` datetime DEFAULT NULL,
  `deployed` tinyint(4) NOT NULL DEFAULT '0',
  `deploymentState` varchar(45) NOT NULL,
  `statusId` int(11) DEFAULT NULL,
  `statusCode` varchar(45) DEFAULT NULL,
  `statusMessage` varchar(255) DEFAULT NULL,
  `taskId` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `solution`
--

LOCK TABLES `solution` WRITE;
/*!40000 ALTER TABLE `solution` DISABLE KEYS */;
INSERT INTO `solution` VALUES (1,'Risk Engine','Solution for internal users to be able to process settlement for FX transactions','Modern Apps','XXX-123-456-YYY','Jenkins','Spinnaker','GitHub','[\"Development\"]',1,1,'2','2020-05-12 08:24:21',0,'',NULL,NULL,NULL,NULL),(2,'Back Office Settlements','Solution for internal users to be able to process settlement for FX transactions','Modern Apps','XXX-111-444-YYY','Jenkins','Spinnaker','GitHub','[\"Production\"]',1,0,'2','2020-03-08 23:07:00',0,'',NULL,NULL,NULL,NULL),(3,'FX Engine','Solution for internal users to be able to process settlement for FX transactions','Modern Apps','XXX-554-325-YYY','Jenkins','Spinnaker','GitHub','[\"Development\"]',0,0,'2','2020-03-08 23:07:00',0,'',NULL,NULL,NULL,NULL),(11,'Portfolio Valuation','A portfolio valuation is done to determine and report alternative investments\' performance, which is often required for financial reporting and tax compliance, and also affects the investment manager\'s compensation.','Data','XXX-333-222-IUY','Bamboo','Screwdriver','Cloud native','[\"Production\"]',1,1,'0','2020-03-18 21:02:02',0,'',NULL,NULL,NULL,NULL),(12,'Corporate Treasury','The treasury department occupies a central role in the finances of the modern corporation. It takes responsible for the company\'s liquidity—ensures that a company has enough cash available at all times to meet the needs of its primary business operations.','Modern Apps','XXX-333-222-IUY','Team City','Team City','GitHub','[\"Production\"]',1,1,'0','2020-03-18 21:13:14',0,'',NULL,NULL,NULL,NULL),(13,'Internal Audit','Internal auditing is the independent and objective evaluation of an organisation\'s internal controls to effectively manage risk within its risk appetite. Internal audit should monitor that any weaknesses identified are also addressed.','Modern Apps','XXX-333-222-IUY','Travis','Screwdriver','Cloud native','[\"Development\"]',1,1,'0','2020-03-18 21:15:22',0,'',NULL,NULL,NULL,NULL),(14,'Realtime Margin','Use real-time margin monitoring to see your current margin requirements at a glance, and to understand the margin implications of any transaction before you transmit an order. The Account window shows your account details.','Data','ABC-123-ABC-123','Cloud native','Spinnaker','Cloud native','[\"Development\"]',1,1,'0','2020-03-18 21:19:58',0,'',NULL,NULL,NULL,NULL),(15,'Product Control','product control are a center of cost responsible for the daily PnL(Profit and Loss) and its explanation for a dedicated trading desk. The team is responsible to communicate this result within the bank and to the authority FED or ECB.','Data','dat-000-ser-322','Bamboo','Screwdriver','BitBucket','[\"Production\"]',1,1,'0','2020-03-18 21:25:10',0,'',NULL,NULL,NULL,NULL),(16,'General Ledger','A general ledger (GL) is a set of numbered accounts a business uses to keep track of its financial transactions and to prepare financial reports. Each account is a unique record summarizing each type of asset, liability, equity, revenue and expense.','Data','ldf-343-sds-232','Cloud native','Team City','Cloud native','[\"Development\", \"Production\"]',1,1,'0','2020-03-18 21:43:54',0,'',NULL,NULL,NULL,NULL),(17,'Corporate Finance','Corporate finance is the division of finance that deals with financing, capital structuring, and investment decisions. Corporate finance is primarily concerned with maximizing shareholder value throug','Modern Apps','ASD-456-FFH-234','Bamboo','Screwdriver','Cloud native','[\"Production\"]',1,1,'0','2020-03-19 23:41:59',0,'',NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `solution` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `solutionresource`
--

DROP TABLE IF EXISTS `solutionresource`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `solutionresource` (
  `solutionId` int(11) NOT NULL,
  `key` varchar(50) NOT NULL,
  `value` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`solutionId`,`key`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `solutionresource`
--

LOCK TABLES `solutionresource` WRITE;
/*!40000 ALTER TABLE `solutionresource` DISABLE KEYS */;
INSERT INTO `solutionresource` VALUES (1,'project_id_dev','sol22-dev-env-ksjs726s'),(1,'project_id_prod','sol22-prod-env-ksjs726s'),(1,'project_id_staging','sol22-staging-env-ksjs726s'),(1,'project_id_workspace','sol22-workspace-ksjs726s'),(2,'project_id_dev','sol22-dev-env-ksjs726s'),(2,'project_id_prod','sol22-prod-env-ksjs726s'),(2,'project_id_staging','sol22-staging-env-ksjs726s'),(2,'project_id_workspace','sol22-workspace-ksjs726s'),(3,'project_id_dev','sol22-dev-env-ksjs726s'),(3,'project_id_prod','sol22-prod-env-ksjs726s'),(3,'project_id_staging','sol22-staging-env-ksjs726s'),(3,'project_id_workspace','sol22-workspace-ksjs726s'),(4,'project_id_dev','sol23-dev-env-ksjs726s'),(4,'project_id_prod','sol23-prod-env-ksjs726s'),(4,'project_id_staging','sol23-staging-env-ksjs726s'),(4,'project_id_workspace','sol23-workspace-ksjs726s');
/*!40000 ALTER TABLE `solutionresource` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `solutionresourcejson`
--

DROP TABLE IF EXISTS `solutionresourcejson`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `solutionresourcejson` (
  `solutionId` int(11) NOT NULL,
  `json` text NOT NULL,
  PRIMARY KEY (`solutionId`),
  UNIQUE KEY `solutionId_UNIQUE` (`solutionId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `solutionresourcejson`
--

LOCK TABLES `solutionresourcejson` WRITE;
/*!40000 ALTER TABLE `solutionresourcejson` DISABLE KEYS */;
INSERT INTO `solutionresourcejson` VALUES (2,'{\"lineage\":\"7b590a8c-e4be-d8c6-6e00-57abbdfd3c3c\",\"outputs\":{},\"resources\":[{\"instances\":[{\"attributes\":{\"create_time\":\"2020-04-30T13:51:27.390Z\",\"display_name\":\"sol22 - ksjs726s\",\"id\":\"folders/615899412414\",\"lifecycle_state\":\"ACTIVE\",\"name\":\"folders/615899412414\",\"parent\":\"folders/943956663445\",\"timeouts\":null},\"private\":\"eyJlMmJmYjczMC1lY2FhLTExZTYtOGY4OC0zNDM2M2JjN2M0YzAiOnsiY3JlYXRlIjoyNDAwMDAwMDAwMDAsImRlbGV0ZSI6MjQwMDAwMDAwMDAwLCJyZWFkIjoyNDAwMDAwMDAwMDAsInVwZGF0ZSI6MjQwMDAwMDAwMDAwfX0=\",\"schema_version\":0}],\"mode\":\"managed\",\"module\":\"module.solution_folder\",\"name\":\"solution_folder\",\"provider\":\"provider.google\",\"type\":\"google_folder\"},{\"instances\":[{\"attributes\":{\"auto_create_network\":true,\"billing_account\":null,\"folder_id\":\"615899412414\",\"id\":\"projects/sol22-dev-env-ksjs726s\",\"labels\":null,\"name\":\"sol22-dev-env\",\"number\":\"6570889872\",\"org_id\":\"\",\"project_id\":\"sol22-dev-env-ksjs726s\",\"skip_delete\":null,\"timeouts\":null},\"dependencies\":[\"module.solution_folder.google_folder.solution_folder\"],\"private\":\"eyJlMmJmYjczMC1lY2FhLTExZTYtOGY4OC0zNDM2M2JjN2M0YzAiOnsiY3JlYXRlIjoyNDAwMDAwMDAwMDAsImRlbGV0ZSI6MjQwMDAwMDAwMDAwLCJyZWFkIjoyNDAwMDAwMDAwMDAsInVwZGF0ZSI6MjQwMDAwMDAwMDAwfSwic2NoZW1hX3ZlcnNpb24iOiIxIn0=\",\"schema_version\":1}],\"mode\":\"managed\",\"module\":\"module.dev_environment\",\"name\":\"environment_project\",\"provider\":\"provider.google\",\"type\":\"google_project\"},{\"instances\":[{\"attributes\":{\"auto_create_network\":true,\"billing_account\":null,\"folder_id\":\"615899412414\",\"id\":\"projects/sol22-prod-env-ksjs726s\",\"labels\":null,\"name\":\"sol22-prod-env\",\"number\":\"1072288444773\",\"org_id\":\"\",\"project_id\":\"sol22-prod-env-ksjs726s\",\"skip_delete\":null,\"timeouts\":null},\"dependencies\":[\"module.solution_folder.google_folder.solution_folder\"],\"private\":\"eyJlMmJmYjczMC1lY2FhLTExZTYtOGY4OC0zNDM2M2JjN2M0YzAiOnsiY3JlYXRlIjoyNDAwMDAwMDAwMDAsImRlbGV0ZSI6MjQwMDAwMDAwMDAwLCJyZWFkIjoyNDAwMDAwMDAwMDAsInVwZGF0ZSI6MjQwMDAwMDAwMDAwfSwic2NoZW1hX3ZlcnNpb24iOiIxIn0=\",\"schema_version\":1}],\"mode\":\"managed\",\"module\":\"module.prod_environment\",\"name\":\"environment_project\",\"provider\":\"provider.google\",\"type\":\"google_project\"},{\"instances\":[{\"attributes\":{\"auto_create_network\":true,\"billing_account\":null,\"folder_id\":\"615899412414\",\"id\":\"projects/sol22-staging-env-ksjs726s\",\"labels\":null,\"name\":\"sol22-staging-env\",\"number\":\"292492613552\",\"org_id\":\"\",\"project_id\":\"sol22-staging-env-ksjs726s\",\"skip_delete\":null,\"timeouts\":null},\"dependencies\":[\"module.solution_folder.google_folder.solution_folder\"],\"private\":\"eyJlMmJmYjczMC1lY2FhLTExZTYtOGY4OC0zNDM2M2JjN2M0YzAiOnsiY3JlYXRlIjoyNDAwMDAwMDAwMDAsImRlbGV0ZSI6MjQwMDAwMDAwMDAwLCJyZWFkIjoyNDAwMDAwMDAwMDAsInVwZGF0ZSI6MjQwMDAwMDAwMDAwfSwic2NoZW1hX3ZlcnNpb24iOiIxIn0=\",\"schema_version\":1}],\"mode\":\"managed\",\"module\":\"module.staging_environment\",\"name\":\"environment_project\",\"provider\":\"provider.google\",\"type\":\"google_project\"},{\"instances\":[{\"attributes\":{\"auto_create_network\":true,\"billing_account\":null,\"folder_id\":\"615899412414\",\"id\":\"projects/sol22-workspace-ksjs726s\",\"labels\":null,\"name\":\"sol22-workspace\",\"number\":\"555918489693\",\"org_id\":\"\",\"project_id\":\"sol22-workspace-ksjs726s\",\"skip_delete\":null,\"timeouts\":null},\"dependencies\":[\"module.solution_folder.google_folder.solution_folder\"],\"private\":\"eyJlMmJmYjczMC1lY2FhLTExZTYtOGY4OC0zNDM2M2JjN2M0YzAiOnsiY3JlYXRlIjoyNDAwMDAwMDAwMDAsImRlbGV0ZSI6MjQwMDAwMDAwMDAwLCJyZWFkIjoyNDAwMDAwMDAwMDAsInVwZGF0ZSI6MjQwMDAwMDAwMDAwfSwic2NoZW1hX3ZlcnNpb24iOiIxIn0=\",\"schema_version\":1}],\"mode\":\"managed\",\"module\":\"module.workspace_project\",\"name\":\"workspace_project\",\"provider\":\"provider.google\",\"type\":\"google_project\"}],\"serial\":1,\"terraform_version\":\"0.12.24\",\"version\":4}'),(3,'{\"lineage\":\"7b590a8c-e4be-d8c6-6e00-57abbdfd3c3c\",\"outputs\":{},\"resources\":[{\"instances\":[{\"attributes\":{\"create_time\":\"2020-04-30T13:51:27.390Z\",\"display_name\":\"sol22 - ksjs726s\",\"id\":\"folders/615899412414\",\"lifecycle_state\":\"ACTIVE\",\"name\":\"folders/615899412414\",\"parent\":\"folders/943956663445\",\"timeouts\":null},\"private\":\"eyJlMmJmYjczMC1lY2FhLTExZTYtOGY4OC0zNDM2M2JjN2M0YzAiOnsiY3JlYXRlIjoyNDAwMDAwMDAwMDAsImRlbGV0ZSI6MjQwMDAwMDAwMDAwLCJyZWFkIjoyNDAwMDAwMDAwMDAsInVwZGF0ZSI6MjQwMDAwMDAwMDAwfX0=\",\"schema_version\":0}],\"mode\":\"managed\",\"module\":\"module.solution_folder\",\"name\":\"solution_folder\",\"provider\":\"provider.google\",\"type\":\"google_folder\"},{\"instances\":[{\"attributes\":{\"auto_create_network\":true,\"billing_account\":null,\"folder_id\":\"615899412414\",\"id\":\"projects/sol22-dev-env-ksjs726s\",\"labels\":null,\"name\":\"sol22-dev-env\",\"number\":\"6570889872\",\"org_id\":\"\",\"project_id\":\"sol22-dev-env-ksjs726s\",\"skip_delete\":null,\"timeouts\":null},\"dependencies\":[\"module.solution_folder.google_folder.solution_folder\"],\"private\":\"eyJlMmJmYjczMC1lY2FhLTExZTYtOGY4OC0zNDM2M2JjN2M0YzAiOnsiY3JlYXRlIjoyNDAwMDAwMDAwMDAsImRlbGV0ZSI6MjQwMDAwMDAwMDAwLCJyZWFkIjoyNDAwMDAwMDAwMDAsInVwZGF0ZSI6MjQwMDAwMDAwMDAwfSwic2NoZW1hX3ZlcnNpb24iOiIxIn0=\",\"schema_version\":1}],\"mode\":\"managed\",\"module\":\"module.dev_environment\",\"name\":\"environment_project\",\"provider\":\"provider.google\",\"type\":\"google_project\"},{\"instances\":[{\"attributes\":{\"auto_create_network\":true,\"billing_account\":null,\"folder_id\":\"615899412414\",\"id\":\"projects/sol22-prod-env-ksjs726s\",\"labels\":null,\"name\":\"sol22-prod-env\",\"number\":\"1072288444773\",\"org_id\":\"\",\"project_id\":\"sol22-prod-env-ksjs726s\",\"skip_delete\":null,\"timeouts\":null},\"dependencies\":[\"module.solution_folder.google_folder.solution_folder\"],\"private\":\"eyJlMmJmYjczMC1lY2FhLTExZTYtOGY4OC0zNDM2M2JjN2M0YzAiOnsiY3JlYXRlIjoyNDAwMDAwMDAwMDAsImRlbGV0ZSI6MjQwMDAwMDAwMDAwLCJyZWFkIjoyNDAwMDAwMDAwMDAsInVwZGF0ZSI6MjQwMDAwMDAwMDAwfSwic2NoZW1hX3ZlcnNpb24iOiIxIn0=\",\"schema_version\":1}],\"mode\":\"managed\",\"module\":\"module.prod_environment\",\"name\":\"environment_project\",\"provider\":\"provider.google\",\"type\":\"google_project\"},{\"instances\":[{\"attributes\":{\"auto_create_network\":true,\"billing_account\":null,\"folder_id\":\"615899412414\",\"id\":\"projects/sol22-staging-env-ksjs726s\",\"labels\":null,\"name\":\"sol22-staging-env\",\"number\":\"292492613552\",\"org_id\":\"\",\"project_id\":\"sol22-staging-env-ksjs726s\",\"skip_delete\":null,\"timeouts\":null},\"dependencies\":[\"module.solution_folder.google_folder.solution_folder\"],\"private\":\"eyJlMmJmYjczMC1lY2FhLTExZTYtOGY4OC0zNDM2M2JjN2M0YzAiOnsiY3JlYXRlIjoyNDAwMDAwMDAwMDAsImRlbGV0ZSI6MjQwMDAwMDAwMDAwLCJyZWFkIjoyNDAwMDAwMDAwMDAsInVwZGF0ZSI6MjQwMDAwMDAwMDAwfSwic2NoZW1hX3ZlcnNpb24iOiIxIn0=\",\"schema_version\":1}],\"mode\":\"managed\",\"module\":\"module.staging_environment\",\"name\":\"environment_project\",\"provider\":\"provider.google\",\"type\":\"google_project\"},{\"instances\":[{\"attributes\":{\"auto_create_network\":true,\"billing_account\":null,\"folder_id\":\"615899412414\",\"id\":\"projects/sol22-workspace-ksjs726s\",\"labels\":null,\"name\":\"sol22-workspace\",\"number\":\"555918489693\",\"org_id\":\"\",\"project_id\":\"sol22-workspace-ksjs726s\",\"skip_delete\":null,\"timeouts\":null},\"dependencies\":[\"module.solution_folder.google_folder.solution_folder\"],\"private\":\"eyJlMmJmYjczMC1lY2FhLTExZTYtOGY4OC0zNDM2M2JjN2M0YzAiOnsiY3JlYXRlIjoyNDAwMDAwMDAwMDAsImRlbGV0ZSI6MjQwMDAwMDAwMDAwLCJyZWFkIjoyNDAwMDAwMDAwMDAsInVwZGF0ZSI6MjQwMDAwMDAwMDAwfSwic2NoZW1hX3ZlcnNpb24iOiIxIn0=\",\"schema_version\":1}],\"mode\":\"managed\",\"module\":\"module.workspace_project\",\"name\":\"workspace_project\",\"provider\":\"provider.google\",\"type\":\"google_project\"}],\"serial\":1,\"terraform_version\":\"0.12.24\",\"version\":4}'),(4,'{\"lineage\":\"7b590a8c-e4be-d8c6-6e00-57abbdfd3c3c\",\"outputs\":{},\"resources\":[{\"instances\":[{\"attributes\":{\"create_time\":\"2020-04-30T13:51:27.390Z\",\"display_name\":\"sol22 - ksjs726s\",\"id\":\"folders/615899412414\",\"lifecycle_state\":\"ACTIVE\",\"name\":\"folders/615899412414\",\"parent\":\"folders/943956663445\",\"timeouts\":null},\"private\":\"eyJlMmJmYjczMC1lY2FhLTExZTYtOGY4OC0zNDM2M2JjN2M0YzAiOnsiY3JlYXRlIjoyNDAwMDAwMDAwMDAsImRlbGV0ZSI6MjQwMDAwMDAwMDAwLCJyZWFkIjoyNDAwMDAwMDAwMDAsInVwZGF0ZSI6MjQwMDAwMDAwMDAwfX0=\",\"schema_version\":0}],\"mode\":\"managed\",\"module\":\"module.solution_folder\",\"name\":\"solution_folder\",\"provider\":\"provider.google\",\"type\":\"google_folder\"},{\"instances\":[{\"attributes\":{\"auto_create_network\":true,\"billing_account\":null,\"folder_id\":\"615899412414\",\"id\":\"projects/sol22-dev-env-ksjs726s\",\"labels\":null,\"name\":\"sol22-dev-env\",\"number\":\"6570889872\",\"org_id\":\"\",\"project_id\":\"sol23-dev-env-ksjs726s\",\"skip_delete\":null,\"timeouts\":null},\"dependencies\":[\"module.solution_folder.google_folder.solution_folder\"],\"private\":\"eyJlMmJmYjczMC1lY2FhLTExZTYtOGY4OC0zNDM2M2JjN2M0YzAiOnsiY3JlYXRlIjoyNDAwMDAwMDAwMDAsImRlbGV0ZSI6MjQwMDAwMDAwMDAwLCJyZWFkIjoyNDAwMDAwMDAwMDAsInVwZGF0ZSI6MjQwMDAwMDAwMDAwfSwic2NoZW1hX3ZlcnNpb24iOiIxIn0=\",\"schema_version\":1}],\"mode\":\"managed\",\"module\":\"module.dev_environment\",\"name\":\"environment_project\",\"provider\":\"provider.google\",\"type\":\"google_project\"},{\"instances\":[{\"attributes\":{\"auto_create_network\":true,\"billing_account\":null,\"folder_id\":\"615899412414\",\"id\":\"projects/sol22-prod-env-ksjs726s\",\"labels\":null,\"name\":\"sol22-prod-env\",\"number\":\"1072288444773\",\"org_id\":\"\",\"project_id\":\"sol23-prod-env-ksjs726s\",\"skip_delete\":null,\"timeouts\":null},\"dependencies\":[\"module.solution_folder.google_folder.solution_folder\"],\"private\":\"eyJlMmJmYjczMC1lY2FhLTExZTYtOGY4OC0zNDM2M2JjN2M0YzAiOnsiY3JlYXRlIjoyNDAwMDAwMDAwMDAsImRlbGV0ZSI6MjQwMDAwMDAwMDAwLCJyZWFkIjoyNDAwMDAwMDAwMDAsInVwZGF0ZSI6MjQwMDAwMDAwMDAwfSwic2NoZW1hX3ZlcnNpb24iOiIxIn0=\",\"schema_version\":1}],\"mode\":\"managed\",\"module\":\"module.prod_environment\",\"name\":\"environment_project\",\"provider\":\"provider.google\",\"type\":\"google_project\"},{\"instances\":[{\"attributes\":{\"auto_create_network\":true,\"billing_account\":null,\"folder_id\":\"615899412414\",\"id\":\"projects/sol22-staging-env-ksjs726s\",\"labels\":null,\"name\":\"sol22-staging-env\",\"number\":\"292492613552\",\"org_id\":\"\",\"project_id\":\"sol23-staging-env-ksjs726s\",\"skip_delete\":null,\"timeouts\":null},\"dependencies\":[\"module.solution_folder.google_folder.solution_folder\"],\"private\":\"eyJlMmJmYjczMC1lY2FhLTExZTYtOGY4OC0zNDM2M2JjN2M0YzAiOnsiY3JlYXRlIjoyNDAwMDAwMDAwMDAsImRlbGV0ZSI6MjQwMDAwMDAwMDAwLCJyZWFkIjoyNDAwMDAwMDAwMDAsInVwZGF0ZSI6MjQwMDAwMDAwMDAwfSwic2NoZW1hX3ZlcnNpb24iOiIxIn0=\",\"schema_version\":1}],\"mode\":\"managed\",\"module\":\"module.staging_environment\",\"name\":\"environment_project\",\"provider\":\"provider.google\",\"type\":\"google_project\"},{\"instances\":[{\"attributes\":{\"auto_create_network\":true,\"billing_account\":null,\"folder_id\":\"615899412414\",\"id\":\"projects/sol22-workspace-ksjs726s\",\"labels\":null,\"name\":\"sol22-workspace\",\"number\":\"555918489693\",\"org_id\":\"\",\"project_id\":\"sol23-workspace-ksjs726s\",\"skip_delete\":null,\"timeouts\":null},\"dependencies\":[\"module.solution_folder.google_folder.solution_folder\"],\"private\":\"eyJlMmJmYjczMC1lY2FhLTExZTYtOGY4OC0zNDM2M2JjN2M0YzAiOnsiY3JlYXRlIjoyNDAwMDAwMDAwMDAsImRlbGV0ZSI6MjQwMDAwMDAwMDAwLCJyZWFkIjoyNDAwMDAwMDAwMDAsInVwZGF0ZSI6MjQwMDAwMDAwMDAwfSwic2NoZW1hX3ZlcnNpb24iOiIxIn0=\",\"schema_version\":1}],\"mode\":\"managed\",\"module\":\"module.workspace_project\",\"name\":\"workspace_project\",\"provider\":\"provider.google\",\"type\":\"google_project\"}],\"serial\":1,\"terraform_version\":\"0.12.24\",\"version\":4}');
/*!40000 ALTER TABLE `solutionresourcejson` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sourcecontrol`
--

DROP TABLE IF EXISTS `sourcecontrol`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sourcecontrol` (
  `key` varchar(100) NOT NULL,
  `value` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sourcecontrol`
--

LOCK TABLES `sourcecontrol` WRITE;
/*!40000 ALTER TABLE `sourcecontrol` DISABLE KEYS */;
INSERT INTO `sourcecontrol` VALUES ('BitBucket','BitBucket'),('Cloud native','Cloud native'),('GitHub','GitHub');
/*!40000 ALTER TABLE `sourcecontrol` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `subnetmode`
--

DROP TABLE IF EXISTS `subnetmode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `subnetmode` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `key` varchar(45) DEFAULT NULL,
  `value` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `subnetmode`
--

LOCK TABLES `subnetmode` WRITE;
/*!40000 ALTER TABLE `subnetmode` DISABLE KEYS */;
INSERT INTO `subnetmode` VALUES (1,'Custom','Custom');
/*!40000 ALTER TABLE `subnetmode` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `team`
--

DROP TABLE IF EXISTS `team`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `team` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `description` varchar(200) NOT NULL,
  `businessUnitId` int(11) NOT NULL,
  `isActive` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `team`
--

LOCK TABLES `team` WRITE;
/*!40000 ALTER TABLE `team` DISABLE KEYS */;
INSERT INTO `team` VALUES (2,'Developers','All Developers',1,1);
/*!40000 ALTER TABLE `team` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `teammember`
--

DROP TABLE IF EXISTS `teammember`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `teammember` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `userId` int(11) NOT NULL,
  `teamId` int(11) NOT NULL,
  `role` varchar(100) NOT NULL,
  `isActive` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `teammember`
--

LOCK TABLES `teammember` WRITE;
/*!40000 ALTER TABLE `teammember` DISABLE KEYS */;
INSERT INTO `teammember` VALUES (0,0,0,'Admin',1);
/*!40000 ALTER TABLE `teammember` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(100) NOT NULL,
  `firstName` varchar(100) NOT NULL,
  `lastName` varchar(100) NOT NULL,
  `isAdmin` tinyint(1) NOT NULL DEFAULT '0',
  `isActive` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'dev@your.company','Jon','Snow',0,1),(2,'admin@your.company','Adam','Smith',1,1);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vpnonpremisevendor`
--

DROP TABLE IF EXISTS `vpnonpremisevendor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vpnonpremisevendor` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `key` varchar(45) DEFAULT NULL,
  `value` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vpnonpremisevendor`
--

LOCK TABLES `vpnonpremisevendor` WRITE;
/*!40000 ALTER TABLE `vpnonpremisevendor` DISABLE KEYS */;
INSERT INTO `vpnonpremisevendor` VALUES (1,'Fortinet','Fortinet');
/*!40000 ALTER TABLE `vpnonpremisevendor` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-05-12  9:42:42
