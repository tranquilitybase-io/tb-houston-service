use eagle_db;

-- MySQL dump 10.13  Distrib 5.7.29, for macos10.14 (x86_64)
--
-- Host: localhost    Database: eagle_db
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
) ENGINE=InnoDB AUTO_INCREMENT=115 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `activator`
--

LOCK TABLES `activator` WRITE;
/*!40000 ALTER TABLE `activator` DISABLE KEYS */;
INSERT INTO `activator` VALUES (1,'CMS Web App','Web application',1,'Public','Tier 3','[\"POC\", \"DEV\"]','[\"GCP\"]','2020-05-12 08:29:07',1000,1200,'[\"UK\", \"DB\"]','[\"Appengine\"]','[\"ApiGee\"]','[\"Jenkins\", \"Travis\"]','[\"Codeship\", \"Option\"]','[\"JIRA\", \"Option\"]','FICC Business Unit','Sanjeev Gupta','s.gupta@company.name','Monthly: Eagle tier 3','Single Region Kubernetes','Available','Some very long description that I did not want to copy. Some very long description that I did not want to copy. Some very long description that I did not want to copy',0,'open',''),(2,'Multi region kubernetes','Micro-services',1,'Restricted','Tier 1','[\"POC\", \"AWS\", \"Other\", \"Fancy\"]','[\"GCP\"]','2020-05-07 08:38:56',1300,2000,'[\"UK\", \"DB\"]','[\"Appengine\"]','[\"ApiGee\"]','[\"Jenkins\", \"Travis\"]','[\"Codeship\", \"Option\"]','[\"JIRA\", \"Option\"]','M&A Business Unit','Nathanael Stoltenberg','Nathanael.Stoltenberg@yahoo.com','Monthly: Eagle tier 1','Multi Region Kubernetes','Deprecated','Some very long description that I did not want to copy. Some very long description that I did not want to copy. Some very long description that I did not want to copy',0,'open',''),(3,'SQL Single region kubernetes','Micro-services',1,'Restricted','Tier 2','[\"POC\", \"Prod\"]','[\"Azure\", \"GCP\", \"AWS\", \"Other\", \"Fancy\"]','2020-05-07 10:49:44',100,120,'[\"UK\", \"DB\"]','[\"Appengine\"]','[\"ApiGee\"]','[\"Jenkins\", \"Travis\"]','[\"Codeship\", \"Option\"]','[\"JIRA\", \"Option\"]','Equity Capital Business Unit','Brando Howell','Brando.Howell@hotmail.com','Monthly: Eagle tier 2','SQL Single region kubernetes','Deprecated','Some very long description that I did not want to copy. Some very long description that I did not want to copy. Some very long description that I did not want to copy',0,'open',''),(4,'CMS Web App','Tier 3',1,'Public','Web application','[\"POC\", \"DEV\", \"PRD\"]','[\"GCP\", \"Cloud Foundry\"]','2020-05-12 08:29:57',500,300,'[\"UK\", \"DB\"]','[\"Appengine\"]','[\"ApiGee\"]','[\"Jenkins\", \"Travis\"]','[\"Codeship\", \"Option\"]','[\"JIRA\", \"Option\"]','Debit Capital Business Unit','Mohammed Will PhD','Mohammed.Will@gmail.com','Monthly: Eagle tier 3','CMS Web App','Available','Some very long description that I did not want to copy. Some very long description that I did not want to copy. Some very long description that I did not want to copy',0,'thirdparty',''),(5,'Multi region kubernetes','Micro-services',1,'Restricted','Tier 1','[\"POC\", \"AWS\", \"Other\", \"Fancy\"]','[\"GCP\"]','2020-05-07 10:56:43',1600,2500,'[\"UK\", \"DB\"]','[\"Appengine\"]','[\"ApiGee\"]','[\"Jenkins\", \"Travis\"]','[\"Codeship\", \"Option\"]','[\"JIRA\", \"Option\"]','FICC Business Unit','Tressa Ullrich','Tressa97@yahoo.com','Monthly: Eagle tier 1','Multi region kubernetes','Locked','Some very long description that I did not want to copy. Some very long description that I did not want to copy. Some very long description that I did not want to copy',0,'thirdparty',''),(6,'SQL Single region kubernetes','Micro-services',1,'Restricted','Tier 2','[\"POC\", \"Prod\"]','[\"Azure\", \"GCP\", \"AWS\", \"Other\", \"Fancy\"]','2020-04-02 19:25:52',900,600,'[\"UK\", \"DB\", \"HK\", \"US\", \"AU\"]','[\"Appengine\"]','[\"ApiGee\"]','[\"Jenkins\", \"Travis\"]','[\"Codeship\", \"Option\"]','[\"JIRA\", \"Option\"]','M&A Business Unit','Rose Dickens Sr.','Rose.Dickens19@hotmail.com','Monthly: Eagle tier 2','SQL Single region kubernetes','Available','Some very long description that I did not want to copy. Some very long description that I did not want to copy. Some very long description that I did not want to copy',0,'internal',''),(7,'CMS Web App','Web application',1,'Public','Tier 3','[\"POC\", \"DEV\", \"PRD\"]','[\"GCP\"]','2020-04-07 13:39:47',1000,1200,'[\"UK\", \"DB\"]','[\"Appengine\"]','[\"ApiGee\"]','[\"Jenkins\", \"Travis\"]','[\"Codeship\", \"Option\"]','[\"JIRA\", \"Option\"]','FICC Business Unit','Sanjeev Gupta','s.gupta@company.name','Monthly: Eagle tier 3','Single Region Kubernetes','Available','Some very long description that I did not want to copy. Some very long description that I did not want to copy. Some very long description that I did not want to copy',0,'open',''),(8,'CMS Web App','Web application',1,'Public','Tier 3','[\"POC\", \"DEV\", \"PRD\"]','[\"GCP\"]','2020-04-07 13:38:22',1000,1200,'[\"UK\", \"DB\"]','[\"Appengine\"]','[\"ApiGee\"]','[\"Jenkins\", \"Travis\"]','[\"Codeship\", \"Option\"]','[\"JIRA\", \"Option\"]','FICC Business Unit','Sanjeev Gupta','s.gupta@company.name','Monthly: Eagle tier 3','Single Region Kubernetes','Available','Some very long description that I did not want to copy. Some very long description that I did not want to copy. Some very long description that I did not want to copy',0,'open',''),(9,'CMS Web App','Web application',1,'Public','Tier 3','[\"POC\", \"DEV\"]','[\"GCP\"]','2020-05-07 10:55:49',1000,1200,'[\"UK\", \"DB\"]','[\"Appengine\"]','[\"ApiGee\"]','[\"Jenkins\", \"Travis\"]','[\"Codeship\", \"Option\"]','[\"JIRA\", \"Option\"]','FICC Business Unit','Sanjeev Gupta','s.gupta@company.name','Monthly: Eagle tier 3','Single Region Kubernetes','Locked','Some very long description that I did not want to copy. Some very long description that I did not want to copy. Some very long description that I did not want to copy',0,'open','');
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
INSERT INTO `application` VALUES (1,1,1,'Placeholder','DEV','Active','Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et do','2020-04-16 17:58:21','[{\"ipAddress\": \"40.123.45.236\", \"name\": \"GKE Cluster\"}, {\"ipAddress\": \"40.123.45.236\", \"name\": \"Cloud SQL\"}]'),(2,1,2,'Other App','POC','Active','Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et do','2020-04-02 00:00:00','[{\"name\": \"GKE Cluster\", \"ipAddress\": \"40.123.45.236\"}, {\"name\": \"Cloud SQL\", \"ipAddress\": \"40.123.45.236\"}]'),(3,2,3,'Other App','POC','Active','Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et do','2020-04-02 00:00:00','[{\"name\": \"ITSO\", \"ipAddress\": \"40.123.45.236\"}, {\"name\": \"Cloud SQL\", \"ipAddress\": \"40.123.45.236\"}]'),(4,2,2,'Great App','Prod','Active','Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et do','2020-04-02 00:00:00','[{\"name\": \"GKE Cluster\", \"ipAddress\": \"40.123.45.236\"}, {\"name\": \"Cloud SQL\", \"ipAddress\": \"40.123.45.236\"}]');
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
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
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
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `businessunit`
--

LOCK TABLES `businessunit` WRITE;
/*!40000 ALTER TABLE `businessunit` DISABLE KEYS */;
INSERT INTO `businessunit` VALUES (1,'Modern Apps','Modern Apps',1),(2,'Data','Data',1),(3,'FICC','FICC',1);
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
-- Table structure for table `folder`
--

DROP TABLE IF EXISTS `folder`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `folder` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `parentFolderId` varchar(45) NOT NULL,
  `folderId` varchar(45) DEFAULT NULL,
  `folderName` varchar(80) NOT NULL,
  `status` varchar(45) NOT NULL,
  `taskId` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `folder`
--

LOCK TABLES `folder` WRITE;
/*!40000 ALTER TABLE `folder` DISABLE KEYS */;
INSERT INTO `folder` VALUES (1,'rootfolderid','MOCKFOLDERID1','Applications','SUCCESS','MOCKTASKID0'),(2,'MOCKFOLDERID1','MOCKFOLDERID3','Modern Apps','SUCCESS','MOCKTASKID2'),(3,'MOCKFOLDERID3','MOCKFOLDERID5','Developers','SUCCESS','MOCKTASKID4');
/*!40000 ALTER TABLE `folder` ENABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `landingzoneaction`
--

LOCK TABLES `landingzoneaction` WRITE;
/*!40000 ALTER TABLE `landingzoneaction` DISABLE KEYS */;
INSERT INTO `landingzoneaction` VALUES (1,'Environment','','environment',0,0,'/administration/landing-zone/environment'),(2,'WAN','Network Setup','network-setup',0,1,'/administration/landing-zone/wan'),(3,'DNS','Network Setup','network-setup',75,1,''),(4,'Internet access','Network Setup','network-setup',9,1,''),(5,'SSO','AD Integration','ad-integration',25,1,''),(6,'ADFS','AD Integration','ad-integration',0,1,''),(7,'Stackdriver','Logging','logging',50,1,''),(8,'Data Dog','Logging','logging',30,1,''),(9,'Cloud Health','Billing/Cost Management','billing-cost-management',19,1,''),(10,'Security','','security',13,1,''),(11,'Multizone setup','','multizone-setup',12,1,'');
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
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `landingzoneprogressitem`
--

LOCK TABLES `landingzoneprogressitem` WRITE;
/*!40000 ALTER TABLE `landingzoneprogressitem` DISABLE KEYS */;
INSERT INTO `landingzoneprogressitem` VALUES (0,'Environment',0),(1,'WAN',0),(2,'DNS',0),(3,'ADFS',0),(4,'SSO',0),(5,'Logging',0),(6,'Billing',0);
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
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `landingzonewan`
--

LOCK TABLES `landingzonewan` WRITE;
/*!40000 ALTER TABLE `landingzonewan` DISABLE KEYS */;
/*!40000 ALTER TABLE `landingzonewan` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lzenvironment`
--

DROP TABLE IF EXISTS `lzenvironment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `lzenvironment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(30) NOT NULL,
  `isActive` tinyint(4) DEFAULT '1',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  UNIQUE KEY `name_UNIQUE` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lzenvironment`
--

LOCK TABLES `lzenvironment` WRITE;
/*!40000 ALTER TABLE `lzenvironment` DISABLE KEYS */;
INSERT INTO `lzenvironment` VALUES (1,'Development',1),(2,'Production',1),(3,'test-env',1);
/*!40000 ALTER TABLE `lzenvironment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lzfolderstructure`
--

DROP TABLE IF EXISTS `lzfolderstructure`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `lzfolderstructure` (
  `id` int(11) NOT NULL,
  `name` varchar(45) NOT NULL,
  `isActive` tinyint(4) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lzfolderstructure`
--

LOCK TABLES `lzfolderstructure` WRITE;
/*!40000 ALTER TABLE `lzfolderstructure` DISABLE KEYS */;
INSERT INTO `lzfolderstructure` VALUES (1,'Applications',1),(2,'Business Unit',1),(3,'Team',1),(4,'Solutions',1);
/*!40000 ALTER TABLE `lzfolderstructure` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lzfolderstructurechild`
--

DROP TABLE IF EXISTS `lzfolderstructurechild`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `lzfolderstructurechild` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `folderId` int(11) NOT NULL,
  `childId` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lzfolderstructurechild`
--

LOCK TABLES `lzfolderstructurechild` WRITE;
/*!40000 ALTER TABLE `lzfolderstructurechild` DISABLE KEYS */;
INSERT INTO `lzfolderstructurechild` VALUES (1,1,2),(2,2,3),(3,3,4),(4,4,NULL);
/*!40000 ALTER TABLE `lzfolderstructurechild` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lzlanvpc`
--

DROP TABLE IF EXISTS `lzlanvpc`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `lzlanvpc` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) DEFAULT NULL,
  `isActive` tinyint(4) DEFAULT '1',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idlzlanvpc_UNIQUE` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lzlanvpc`
--

LOCK TABLES `lzlanvpc` WRITE;
/*!40000 ALTER TABLE `lzlanvpc` DISABLE KEYS */;
INSERT INTO `lzlanvpc` VALUES (1,'string',1),(2,'Development VPC',1),(3,'Production VPC',1),(4,'PoC VPC',0);
/*!40000 ALTER TABLE `lzlanvpc` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lzlanvpc_environment`
--

DROP TABLE IF EXISTS `lzlanvpc_environment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `lzlanvpc_environment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `lzlanvpcId` int(11) NOT NULL,
  `environmentId` int(11) NOT NULL,
  `isActive` tinyint(4) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lzlanvpc_environment`
--

LOCK TABLES `lzlanvpc_environment` WRITE;
/*!40000 ALTER TABLE `lzlanvpc_environment` DISABLE KEYS */;
INSERT INTO `lzlanvpc_environment` VALUES (1,1,1),(2,2,1),(3,1,2),(4,0,0);
/*!40000 ALTER TABLE `lzlanvpc_environment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lzmetadata`
--

DROP TABLE IF EXISTS `lzmetadata`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `lzmetadata` (
  `group` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `value` text NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `isActive` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`group`,`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lzmetadata`
--

LOCK TABLES `lzmetadata` WRITE;
/*!40000 ALTER TABLE `lzmetadata` DISABLE KEYS */;
INSERT INTO `lzmetadata` VALUES ('environments','environments','[\"Development\",\"UAT\",\"Staging\",\"PoC\",\"Production\"]','List of environments available',1),('folder_structure','folder_structure','[{\"id\": 1, \"isEnabled\": true, \"name\": \"Applications\", \"children\": [{\"id\": 2, \"isEnabled\": true, \"name\": \"Business Unit\", \"children\": [{\"id\": 3, \"isEnabled\": true, \"name\": \"Team\", \"children\": [{\"id\": 4, \"isEnabled\": true, \"name\": \"Solutions\"}]}]}]}]','Landing Zone metadata for folder structure',0),('lan_vpc','development','[\"Development\",\"PoC\", \"UAT\", \"Staging\"]','Landing Zone metadata for LAN VPC of Dev environment',1),('lan_vpc','production','[\"Production\", \"Staging\"]','Landing Zone metadata for LAN VPC of Prod environment',1);
/*!40000 ALTER TABLE `lzmetadata` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `role`
--

DROP TABLE IF EXISTS `role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `role` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `cloudIdentityGroup` varchar(200) NOT NULL,
  `description` varchar(200) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `role`
--

LOCK TABLES `role` WRITE;
/*!40000 ALTER TABLE `role` DISABLE KEYS */;
INSERT INTO `role` VALUES (1,'admin','ecadmins@gftdevgcp.com','eagle console admin role'),(2,'user','ecusers@gftdevgcp.com','eagle console user role');
/*!40000 ALTER TABLE `role` ENABLE KEYS */;
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
  `favourite` tinyint(1) DEFAULT NULL,
  `lastUpdated` datetime DEFAULT NULL,
  `deployed` tinyint(4) NOT NULL DEFAULT '0',
  `deploymentState` varchar(45) NOT NULL,
  `statusId` int(11) DEFAULT NULL,
  `statusCode` varchar(45) DEFAULT NULL,
  `statusMessage` varchar(255) DEFAULT NULL,
  `taskId` varchar(100) DEFAULT NULL,
  `teamId` int(11) DEFAULT NULL,
  `deploymentFolderId` varchar(50) DEFAULT NULL,
  `isActive` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `solution`
--

LOCK TABLES `solution` WRITE;
/*!40000 ALTER TABLE `solution` DISABLE KEYS */;
INSERT INTO `solution` VALUES (1,'Risk Engine','Solution for internal users to be able to process settlement for FX transactions','Modern Apps','XXX-123-456-YYY','Jenkins','Spinnaker','GitHub',1,'2020-06-09 11:12:31',1,'SUCCESS',200,'200','Solution deployment updated.','MOCKTASKID2',1,'MOCKFOLDERID5',1),(2,'Back Office Settlements','Solution for internal users to be able to process settlement for FX transactions','Modern Apps','XXX-111-444-YYY','Jenkins','Spinnaker','GitHub',0,'2020-03-08 23:07:00',0,'',NULL,NULL,NULL,NULL,1,NULL,1),(3,'FX Engine','Solution for internal users to be able to process settlement for FX transactions','Modern Apps','XXX-554-325-YYY','Jenkins','Spinnaker','GitHub',0,'2020-03-08 23:07:00',0,'',NULL,NULL,NULL,NULL,1,NULL,1),(11,'Portfolio Valuation','A portfolio valuation is done to determine and report alternative investments\' performance, which is often required for financial reporting and tax compliance, and also affects the investment manager\'s compensation.','Data','XXX-333-222-IUY','Bamboo','Screwdriver','Cloud native',1,'2020-03-18 21:02:02',0,'',NULL,NULL,NULL,NULL,1,NULL,1),(12,'Corporate Treasury','The treasury department occupies a central role in the finances of the modern corporation. It takes responsible for the company\'s liquidity—ensures that a company has enough cash available at all times to meet the needs of its primary business operations.','Modern Apps','XXX-333-222-IUY','Team City','Team City','GitHub',1,'2020-03-18 21:13:14',0,'',NULL,NULL,NULL,NULL,1,NULL,1),(13,'Internal Audit','Internal auditing is the independent and objective evaluation of an organisation\'s internal controls to effectively manage risk within its risk appetite. Internal audit should monitor that any weaknesses identified are also addressed.','Modern Apps','XXX-333-222-IUY','Travis','Screwdriver','Cloud native',1,'2020-03-18 21:15:22',0,'',NULL,NULL,NULL,NULL,1,NULL,1),(14,'Realtime Margin','Use real-time margin monitoring to see your current margin requirements at a glance, and to understand the margin implications of any transaction before you transmit an order. The Account window shows your account details.','Data','ABC-123-ABC-123','Cloud native','Spinnaker','Cloud native',1,'2020-03-18 21:19:58',0,'',NULL,NULL,NULL,NULL,1,NULL,1),(15,'Product Control','product control are a center of cost responsible for the daily PnL(Profit and Loss) and its explanation for a dedicated trading desk. The team is responsible to communicate this result within the bank and to the authority FED or ECB.','Data','dat-000-ser-322','Bamboo','Screwdriver','BitBucket',1,'2020-03-18 21:25:10',0,'',NULL,NULL,NULL,NULL,1,NULL,1),(16,'General Ledger','A general ledger (GL) is a set of numbered accounts a business uses to keep track of its financial transactions and to prepare financial reports. Each account is a unique record summarizing each type of asset, liability, equity, revenue and expense.','Data','ldf-343-sds-232','Cloud native','Team City','Cloud native',1,'2020-03-18 21:43:54',0,'',NULL,NULL,NULL,NULL,1,NULL,1),(17,'Corporate Finance','Corporate finance is the division of finance that deals with financing, capital structuring, and investment decisions. Corporate finance is primarily concerned with maximizing shareholder value throug','Modern Apps','ASD-456-FFH-234','Bamboo','Screwdriver','Cloud native',1,'2020-03-19 23:41:59',0,'',NULL,NULL,NULL,NULL,1,NULL,1);
/*!40000 ALTER TABLE `solution` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `solutionenvironment`
--

DROP TABLE IF EXISTS `solutionenvironment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `solutionenvironment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `solutionId` int(11) NOT NULL,
  `environmentId` int(11) NOT NULL,
  `lastUpdated` datetime DEFAULT NULL,
  `isActive` tinyint(4) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `solutionenvironment`
--

LOCK TABLES `solutionenvironment` WRITE;
/*!40000 ALTER TABLE `solutionenvironment` DISABLE KEYS */;
INSERT INTO `solutionenvironment` VALUES (1,1,1,'2020-06-09 11:12:31',1),(2,2,1,'2020-06-06 15:38:02',1),(3,3,1,'2020-06-06 15:38:08',1),(4,4,1,'2020-06-06 15:38:12',1),(5,5,1,'2020-06-06 15:38:16',1),(6,6,1,'2020-06-06 15:38:21',1),(7,7,1,'2020-06-06 15:38:25',1),(8,1,2,'2020-06-09 11:12:31',1),(9,2,2,'2020-06-09 11:12:31',1),(10,19,1,'2020-06-06 18:08:46',1);
/*!40000 ALTER TABLE `solutionenvironment` ENABLE KEYS */;
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
INSERT INTO `solutionresource` VALUES (1,'project-id-development-1','development-1-h08aez-ksjs726s'),(1,'project-id-development-2','development-2-h08aez-ksjs726s'),(1,'project-id-production','production-h08aez-ksjs726s'),(1,'project-id-qa','qa-h08aez-ksjs726s'),(1,'project-id-staging','staging-h08aez-ksjs726s'),(2,'project-id-development-1','development-1-h08aez-ksjs726s'),(2,'project-id-development-2','development-2-h08aez-ksjs726s'),(2,'project-id-production','production-h08aez-ksjs726s'),(2,'project-id-qa','qa-h08aez-ksjs726s'),(2,'project-id-staging','staging-h08aez-ksjs726s'),(2,'project_id_dev','sol22-dev-env-ksjs726s'),(2,'project_id_prod','sol22-prod-env-ksjs726s'),(2,'project_id_staging','sol22-staging-env-ksjs726s'),(2,'project_id_workspace','sol22-workspace-ksjs726s'),(3,'project-id-development-1','development-1-h08aez-ksjs726s'),(3,'project-id-development-2','development-2-h08aez-ksjs726s'),(3,'project-id-production','production-h08aez-ksjs726s'),(3,'project-id-qa','qa-h08aez-ksjs726s'),(3,'project-id-staging','staging-h08aez-ksjs726s'),(3,'project_id_dev','sol22-dev-env-ksjs726s'),(3,'project_id_prod','sol22-prod-env-ksjs726s'),(3,'project_id_staging','sol22-staging-env-ksjs726s'),(3,'project_id_workspace','sol22-workspace-ksjs726s'),(4,'project-id-development-1','development-1-hello-world'),(4,'project-id-development-2','development-2-hello-world'),(4,'project-id-production','production-hello-world'),(4,'project-id-qa','qa-hello-world'),(4,'project-id-staging','staging-hello-world'),(4,'project_id_dev','sol23-dev-env-ksjs726s'),(4,'project_id_prod','sol23-prod-env-ksjs726s'),(4,'project_id_staging','sol23-staging-env-ksjs726s'),(4,'project_id_workspace','sol23-workspace-ksjs726s');
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
INSERT INTO `solutionresourcejson` VALUES (2,'{\"environment_projects\": {\"sensitive\": false, \"type\": [\"tuple\", [[\"object\", {\"auto_create_network\": \"bool\", \"billing_account\": \"string\", \"folder_id\": \"string\", \"id\": \"string\", \"labels\": [\"map\", \"string\"], \"name\": \"string\", \"number\": \"string\", \"org_id\": \"string\", \"project_id\": \"string\", \"skip_delete\": \"bool\", \"timeouts\": [\"object\", {\"create\": \"string\", \"delete\": \"string\", \"read\": \"string\", \"update\": \"string\"}]}], [\"object\", {\"auto_create_network\": \"bool\", \"billing_account\": \"string\", \"folder_id\": \"string\", \"id\": \"string\", \"labels\": [\"map\", \"string\"], \"name\": \"string\", \"number\": \"string\", \"org_id\": \"string\", \"project_id\": \"string\", \"skip_delete\": \"bool\", \"timeouts\": [\"object\", {\"create\": \"string\", \"delete\": \"string\", \"read\": \"string\", \"update\": \"string\"}]}], [\"object\", {\"auto_create_network\": \"bool\", \"billing_account\": \"string\", \"folder_id\": \"string\", \"id\": \"string\", \"labels\": [\"map\", \"string\"], \"name\": \"string\", \"number\": \"string\", \"org_id\": \"string\", \"project_id\": \"string\", \"skip_delete\": \"bool\", \"timeouts\": [\"object\", {\"create\": \"string\", \"delete\": \"string\", \"read\": \"string\", \"update\": \"string\"}]}], [\"object\", {\"auto_create_network\": \"bool\", \"billing_account\": \"string\", \"folder_id\": \"string\", \"id\": \"string\", \"labels\": [\"map\", \"string\"], \"name\": \"string\", \"number\": \"string\", \"org_id\": \"string\", \"project_id\": \"string\", \"skip_delete\": \"bool\", \"timeouts\": [\"object\", {\"create\": \"string\", \"delete\": \"string\", \"read\": \"string\", \"update\": \"string\"}]}], [\"object\", {\"auto_create_network\": \"bool\", \"billing_account\": \"string\", \"folder_id\": \"string\", \"id\": \"string\", \"labels\": [\"map\", \"string\"], \"name\": \"string\", \"number\": \"string\", \"org_id\": \"string\", \"project_id\": \"string\", \"skip_delete\": \"bool\", \"timeouts\": [\"object\", {\"create\": \"string\", \"delete\": \"string\", \"read\": \"string\", \"update\": \"string\"}]}]]], \"value\": [{\"auto_create_network\": true, \"billing_account\": \"01A2F5-73127B-50AE5B\", \"folder_id\": \"282083654038\", \"id\": \"projects/development-1-h08aez-ksjs726s\", \"labels\": {\"business_unit\": \"bu-gft\", \"cost_centre\": \"cc-gft\", \"environment\": \"development-1\"}, \"name\": \"sol999-development-1\", \"number\": \"119312718634\", \"org_id\": \"\", \"project_id\": \"development-1-h08aez-ksjs726s\", \"skip_delete\": null, \"timeouts\": null}, {\"auto_create_network\": true, \"billing_account\": \"REDACTED\", \"folder_id\": \"282083654038\", \"id\": \"projects/development-2-h08aez-ksjs726s\", \"labels\": {\"business_unit\": \"bu-gft\", \"cost_centre\": \"cc-gft\", \"environment\": \"development-2\"}, \"name\": \"sol999-development-2\", \"number\": \"878261862220\", \"org_id\": \"\", \"project_id\": \"development-2-h08aez-ksjs726s\", \"skip_delete\": null, \"timeouts\": null}, {\"auto_create_network\": true, \"billing_account\": \"REDACTED\", \"folder_id\": \"282083654038\", \"id\": \"projects/staging-h08aez-ksjs726s\", \"labels\": {\"business_unit\": \"bu-gft\", \"cost_centre\": \"cc-gft\", \"environment\": \"staging\"}, \"name\": \"sol999-staging\", \"number\": \"971423854825\", \"org_id\": \"\", \"project_id\": \"staging-h08aez-ksjs726s\", \"skip_delete\": null, \"timeouts\": null}, {\"auto_create_network\": true, \"billing_account\": \"REDACTED\", \"folder_id\": \"282083654038\", \"id\": \"projects/qa-h08aez-ksjs726s\", \"labels\": {\"business_unit\": \"bu-gft\", \"cost_centre\": \"cc-gft\", \"environment\": \"qa\"}, \"name\": \"sol999-qa\", \"number\": \"662646863463\", \"org_id\": \"\", \"project_id\": \"qa-h08aez-ksjs726s\", \"skip_delete\": null, \"timeouts\": null}, {\"auto_create_network\": true, \"billing_account\": \"REDACTED\", \"folder_id\": \"282083654038\", \"id\": \"projects/production-h08aez-ksjs726s\", \"labels\": {\"business_unit\": \"bu-gft\", \"cost_centre\": \"cc-gft\", \"environment\": \"production\"}, \"name\": \"sol999-production\", \"number\": \"544667916764\", \"org_id\": \"\", \"project_id\": \"production-h08aez-ksjs726s\", \"skip_delete\": null, \"timeouts\": null}]}, \"solution_folder\": {\"sensitive\": false, \"type\": [\"object\", {\"create_time\": \"string\", \"display_name\": \"string\", \"id\": \"string\", \"lifecycle_state\": \"string\", \"name\": \"string\", \"parent\": \"string\", \"timeouts\": [\"object\", {\"create\": \"string\", \"delete\": \"string\", \"read\": \"string\", \"update\": \"string\"}]}], \"value\": {\"create_time\": \"2020-05-20T08:05:09.507Z\", \"display_name\": \"sol999\", \"id\": \"folders/282083654038\", \"lifecycle_state\": \"ACTIVE\", \"name\": \"folders/282083654038\", \"parent\": \"folders/940168182397\", \"timeouts\": null}}, \"workspace_project\": {\"sensitive\": false, \"type\": [\"object\", {\"auto_create_network\": \"bool\", \"billing_account\": \"string\", \"folder_id\": \"string\", \"id\": \"string\", \"labels\": [\"map\", \"string\"], \"name\": \"string\", \"number\": \"string\", \"org_id\": \"string\", \"project_id\": \"string\", \"skip_delete\": \"bool\", \"timeouts\": [\"object\", {\"create\": \"string\", \"delete\": \"string\", \"read\": \"string\", \"update\": \"string\"}]}], \"value\": {\"auto_create_network\": true, \"billing_account\": \"REDACTED\", \"folder_id\": \"282083654038\", \"id\": \"projects/workspace-h08aez-ksjs726s\", \"labels\": {\"business_unit\": \"bu-gft\", \"cost_centre\": \"cc-gft\"}, \"name\": \"sol999-workspace\", \"number\": \"3227416706\", \"org_id\": \"\", \"project_id\": \"workspace-h08aez-ksjs726s\", \"skip_delete\": null, \"timeouts\": null}}}'),(3,'{\"environment_projects\": {\"sensitive\": false, \"type\": [\"tuple\", [[\"object\", {\"auto_create_network\": \"bool\", \"billing_account\": \"string\", \"folder_id\": \"string\", \"id\": \"string\", \"labels\": [\"map\", \"string\"], \"name\": \"string\", \"number\": \"string\", \"org_id\": \"string\", \"project_id\": \"string\", \"skip_delete\": \"bool\", \"timeouts\": [\"object\", {\"create\": \"string\", \"delete\": \"string\", \"read\": \"string\", \"update\": \"string\"}]}], [\"object\", {\"auto_create_network\": \"bool\", \"billing_account\": \"string\", \"folder_id\": \"string\", \"id\": \"string\", \"labels\": [\"map\", \"string\"], \"name\": \"string\", \"number\": \"string\", \"org_id\": \"string\", \"project_id\": \"string\", \"skip_delete\": \"bool\", \"timeouts\": [\"object\", {\"create\": \"string\", \"delete\": \"string\", \"read\": \"string\", \"update\": \"string\"}]}], [\"object\", {\"auto_create_network\": \"bool\", \"billing_account\": \"string\", \"folder_id\": \"string\", \"id\": \"string\", \"labels\": [\"map\", \"string\"], \"name\": \"string\", \"number\": \"string\", \"org_id\": \"string\", \"project_id\": \"string\", \"skip_delete\": \"bool\", \"timeouts\": [\"object\", {\"create\": \"string\", \"delete\": \"string\", \"read\": \"string\", \"update\": \"string\"}]}], [\"object\", {\"auto_create_network\": \"bool\", \"billing_account\": \"string\", \"folder_id\": \"string\", \"id\": \"string\", \"labels\": [\"map\", \"string\"], \"name\": \"string\", \"number\": \"string\", \"org_id\": \"string\", \"project_id\": \"string\", \"skip_delete\": \"bool\", \"timeouts\": [\"object\", {\"create\": \"string\", \"delete\": \"string\", \"read\": \"string\", \"update\": \"string\"}]}], [\"object\", {\"auto_create_network\": \"bool\", \"billing_account\": \"string\", \"folder_id\": \"string\", \"id\": \"string\", \"labels\": [\"map\", \"string\"], \"name\": \"string\", \"number\": \"string\", \"org_id\": \"string\", \"project_id\": \"string\", \"skip_delete\": \"bool\", \"timeouts\": [\"object\", {\"create\": \"string\", \"delete\": \"string\", \"read\": \"string\", \"update\": \"string\"}]}]]], \"value\": [{\"auto_create_network\": true, \"billing_account\": \"01A2F5-73127B-50AE5B\", \"folder_id\": \"282083654038\", \"id\": \"projects/development-1-h08aez-ksjs726s\", \"labels\": {\"business_unit\": \"bu-gft\", \"cost_centre\": \"cc-gft\", \"environment\": \"development-1\"}, \"name\": \"sol999-development-1\", \"number\": \"119312718634\", \"org_id\": \"\", \"project_id\": \"development-1-h08aez-ksjs726s\", \"skip_delete\": null, \"timeouts\": null}, {\"auto_create_network\": true, \"billing_account\": \"REDACTED\", \"folder_id\": \"282083654038\", \"id\": \"projects/development-2-h08aez-ksjs726s\", \"labels\": {\"business_unit\": \"bu-gft\", \"cost_centre\": \"cc-gft\", \"environment\": \"development-2\"}, \"name\": \"sol999-development-2\", \"number\": \"878261862220\", \"org_id\": \"\", \"project_id\": \"development-2-h08aez-ksjs726s\", \"skip_delete\": null, \"timeouts\": null}, {\"auto_create_network\": true, \"billing_account\": \"REDACTED\", \"folder_id\": \"282083654038\", \"id\": \"projects/staging-h08aez-ksjs726s\", \"labels\": {\"business_unit\": \"bu-gft\", \"cost_centre\": \"cc-gft\", \"environment\": \"staging\"}, \"name\": \"sol999-staging\", \"number\": \"971423854825\", \"org_id\": \"\", \"project_id\": \"staging-h08aez-ksjs726s\", \"skip_delete\": null, \"timeouts\": null}, {\"auto_create_network\": true, \"billing_account\": \"REDACTED\", \"folder_id\": \"282083654038\", \"id\": \"projects/qa-h08aez-ksjs726s\", \"labels\": {\"business_unit\": \"bu-gft\", \"cost_centre\": \"cc-gft\", \"environment\": \"qa\"}, \"name\": \"sol999-qa\", \"number\": \"662646863463\", \"org_id\": \"\", \"project_id\": \"qa-h08aez-ksjs726s\", \"skip_delete\": null, \"timeouts\": null}, {\"auto_create_network\": true, \"billing_account\": \"REDACTED\", \"folder_id\": \"282083654038\", \"id\": \"projects/production-h08aez-ksjs726s\", \"labels\": {\"business_unit\": \"bu-gft\", \"cost_centre\": \"cc-gft\", \"environment\": \"production\"}, \"name\": \"sol999-production\", \"number\": \"544667916764\", \"org_id\": \"\", \"project_id\": \"production-h08aez-ksjs726s\", \"skip_delete\": null, \"timeouts\": null}]}, \"solution_folder\": {\"sensitive\": false, \"type\": [\"object\", {\"create_time\": \"string\", \"display_name\": \"string\", \"id\": \"string\", \"lifecycle_state\": \"string\", \"name\": \"string\", \"parent\": \"string\", \"timeouts\": [\"object\", {\"create\": \"string\", \"delete\": \"string\", \"read\": \"string\", \"update\": \"string\"}]}], \"value\": {\"create_time\": \"2020-05-20T08:05:09.507Z\", \"display_name\": \"sol999\", \"id\": \"folders/282083654038\", \"lifecycle_state\": \"ACTIVE\", \"name\": \"folders/282083654038\", \"parent\": \"folders/940168182397\", \"timeouts\": null}}, \"workspace_project\": {\"sensitive\": false, \"type\": [\"object\", {\"auto_create_network\": \"bool\", \"billing_account\": \"string\", \"folder_id\": \"string\", \"id\": \"string\", \"labels\": [\"map\", \"string\"], \"name\": \"string\", \"number\": \"string\", \"org_id\": \"string\", \"project_id\": \"string\", \"skip_delete\": \"bool\", \"timeouts\": [\"object\", {\"create\": \"string\", \"delete\": \"string\", \"read\": \"string\", \"update\": \"string\"}]}], \"value\": {\"auto_create_network\": true, \"billing_account\": \"REDACTED\", \"folder_id\": \"282083654038\", \"id\": \"projects/workspace-h08aez-ksjs726s\", \"labels\": {\"business_unit\": \"bu-gft\", \"cost_centre\": \"cc-gft\"}, \"name\": \"sol999-workspace\", \"number\": \"3227416706\", \"org_id\": \"\", \"project_id\": \"workspace-h08aez-ksjs726s\", \"skip_delete\": null, \"timeouts\": null}}}'),(4,'{\"environment_projects\": {\"sensitive\": false, \"type\": [\"tuple\", [[\"object\", {\"auto_create_network\": \"bool\", \"billing_account\": \"string\", \"folder_id\": \"string\", \"id\": \"string\", \"labels\": [\"map\", \"string\"], \"name\": \"string\", \"number\": \"string\", \"org_id\": \"string\", \"project_id\": \"string\", \"skip_delete\": \"bool\", \"timeouts\": [\"object\", {\"create\": \"string\", \"delete\": \"string\", \"read\": \"string\", \"update\": \"string\"}]}], [\"object\", {\"auto_create_network\": \"bool\", \"billing_account\": \"string\", \"folder_id\": \"string\", \"id\": \"string\", \"labels\": [\"map\", \"string\"], \"name\": \"string\", \"number\": \"string\", \"org_id\": \"string\", \"project_id\": \"string\", \"skip_delete\": \"bool\", \"timeouts\": [\"object\", {\"create\": \"string\", \"delete\": \"string\", \"read\": \"string\", \"update\": \"string\"}]}], [\"object\", {\"auto_create_network\": \"bool\", \"billing_account\": \"string\", \"folder_id\": \"string\", \"id\": \"string\", \"labels\": [\"map\", \"string\"], \"name\": \"string\", \"number\": \"string\", \"org_id\": \"string\", \"project_id\": \"string\", \"skip_delete\": \"bool\", \"timeouts\": [\"object\", {\"create\": \"string\", \"delete\": \"string\", \"read\": \"string\", \"update\": \"string\"}]}], [\"object\", {\"auto_create_network\": \"bool\", \"billing_account\": \"string\", \"folder_id\": \"string\", \"id\": \"string\", \"labels\": [\"map\", \"string\"], \"name\": \"string\", \"number\": \"string\", \"org_id\": \"string\", \"project_id\": \"string\", \"skip_delete\": \"bool\", \"timeouts\": [\"object\", {\"create\": \"string\", \"delete\": \"string\", \"read\": \"string\", \"update\": \"string\"}]}], [\"object\", {\"auto_create_network\": \"bool\", \"billing_account\": \"string\", \"folder_id\": \"string\", \"id\": \"string\", \"labels\": [\"map\", \"string\"], \"name\": \"string\", \"number\": \"string\", \"org_id\": \"string\", \"project_id\": \"string\", \"skip_delete\": \"bool\", \"timeouts\": [\"object\", {\"create\": \"string\", \"delete\": \"string\", \"read\": \"string\", \"update\": \"string\"}]}]]], \"value\": [{\"auto_create_network\": true, \"billing_account\": \"01A2F5-73127B-50AE5B\", \"folder_id\": \"282083654038\", \"id\": \"projects/development-1-hello-world\", \"labels\": {\"business_unit\": \"bu-gft\", \"cost_centre\": \"cc-gft\", \"environment\": \"development-1\"}, \"name\": \"sol999-development-1\", \"number\": \"119312718634\", \"org_id\": \"\", \"project_id\": \"development-1-hello-world\", \"skip_delete\": null, \"timeouts\": null}, {\"auto_create_network\": true, \"billing_account\": \"REDACTED\", \"folder_id\": \"282083654038\", \"id\": \"projects/development-2-hello-world\", \"labels\": {\"business_unit\": \"bu-gft\", \"cost_centre\": \"cc-gft\", \"environment\": \"development-2\"}, \"name\": \"sol999-development-2\", \"number\": \"878261862220\", \"org_id\": \"\", \"project_id\": \"development-2-hello-world\", \"skip_delete\": null, \"timeouts\": null}, {\"auto_create_network\": true, \"billing_account\": \"REDACTED\", \"folder_id\": \"282083654038\", \"id\": \"projects/staging-hello-world\", \"labels\": {\"business_unit\": \"bu-gft\", \"cost_centre\": \"cc-gft\", \"environment\": \"staging\"}, \"name\": \"sol999-staging\", \"number\": \"971423854825\", \"org_id\": \"\", \"project_id\": \"staging-hello-world\", \"skip_delete\": null, \"timeouts\": null}, {\"auto_create_network\": true, \"billing_account\": \"REDACTED\", \"folder_id\": \"282083654038\", \"id\": \"projects/qa-hello-world\", \"labels\": {\"business_unit\": \"bu-gft\", \"cost_centre\": \"cc-gft\", \"environment\": \"qa\"}, \"name\": \"sol999-qa\", \"number\": \"662646863463\", \"org_id\": \"\", \"project_id\": \"qa-hello-world\", \"skip_delete\": null, \"timeouts\": null}, {\"auto_create_network\": true, \"billing_account\": \"REDACTED\", \"folder_id\": \"282083654038\", \"id\": \"projects/production-hello-world\", \"labels\": {\"business_unit\": \"bu-gft\", \"cost_centre\": \"cc-gft\", \"environment\": \"production\"}, \"name\": \"sol999-production\", \"number\": \"544667916764\", \"org_id\": \"\", \"project_id\": \"production-hello-world\", \"skip_delete\": null, \"timeouts\": null}]}, \"solution_folder\": {\"sensitive\": false, \"type\": [\"object\", {\"create_time\": \"string\", \"display_name\": \"string\", \"id\": \"string\", \"lifecycle_state\": \"string\", \"name\": \"string\", \"parent\": \"string\", \"timeouts\": [\"object\", {\"create\": \"string\", \"delete\": \"string\", \"read\": \"string\", \"update\": \"string\"}]}], \"value\": {\"create_time\": \"2020-05-20T08:05:09.507Z\", \"display_name\": \"sol999\", \"id\": \"folders/282083654038\", \"lifecycle_state\": \"ACTIVE\", \"name\": \"folders/282083654038\", \"parent\": \"folders/940168182397\", \"timeouts\": null}}, \"workspace_project\": {\"sensitive\": false, \"type\": [\"object\", {\"auto_create_network\": \"bool\", \"billing_account\": \"string\", \"folder_id\": \"string\", \"id\": \"string\", \"labels\": [\"map\", \"string\"], \"name\": \"string\", \"number\": \"string\", \"org_id\": \"string\", \"project_id\": \"string\", \"skip_delete\": \"bool\", \"timeouts\": [\"object\", {\"create\": \"string\", \"delete\": \"string\", \"read\": \"string\", \"update\": \"string\"}]}], \"value\": {\"auto_create_network\": true, \"billing_account\": \"REDACTED\", \"folder_id\": \"282083654038\", \"id\": \"projects/workspace-hello-world\", \"labels\": {\"business_unit\": \"bu-gft\", \"cost_centre\": \"cc-gft\"}, \"name\": \"sol999-workspace\", \"number\": \"3227416706\", \"org_id\": \"\", \"project_id\": \"workspace-hello-world\", \"skip_delete\": null, \"timeouts\": null}}}');
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
  `lastUpdated` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `team`
--

LOCK TABLES `team` WRITE;
/*!40000 ALTER TABLE `team` DISABLE KEYS */;
INSERT INTO `team` VALUES (1,'Developers','All Developers',1,1,'2020-03-01 12:34:56'),(2,'Admins','All Admins',1,1,'2020-03-01 12:34:56');
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
  `roleId` int(11) NOT NULL,
  `isTeamAdmin` tinyint(1) NOT NULL DEFAULT '1',
  `isActive` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `teammember`
--

LOCK TABLES `teammember` WRITE;
/*!40000 ALTER TABLE `teammember` DISABLE KEYS */;
INSERT INTO `teammember` VALUES (1,2,2,2,1,1),(2,1,1,1,0,1);
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
  `showWelcome` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'dev@your.company','Jon','Snow',0,1,1),(2,'admin@your.company','Adam','Smith',1,1,1);
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
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
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

-- Dump completed on 2020-06-12 15:27:32
