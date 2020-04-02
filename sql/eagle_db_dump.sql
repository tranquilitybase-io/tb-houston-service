-- MySQL dump 10.13  Distrib 8.0.19, for osx10.15 (x86_64)
--
-- Host: localhost    Database: eagle_db
-- ------------------------------------------------------
-- Server version	5.7.29

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
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
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `activator` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `type` varchar(255) DEFAULT NULL,
  `available` tinyint(1) DEFAULT NULL,
  `sensitivity` varchar(255) DEFAULT NULL,
  `category` varchar(255) DEFAULT NULL,
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
  `resources` varchar(255) DEFAULT NULL,
  `status` varchar(255) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `userId` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=104 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `activator`
--

LOCK TABLES `activator` WRITE;
/*!40000 ALTER TABLE `activator` DISABLE KEYS */;
INSERT INTO `activator` VALUES (1,'CMS Web App','Web application',1,'Public','Tier 3','[\"POC\", \"DEV\"]','[\"GCP\"]','2020-01-09 15:59:10',1000,1200,'[\"UK\", \"DB\"]','[\"Appengine\"]','[\"ApiGee\"]','[\"Jenkins\", \"Travis\"]','[\"Codeship\", \"Option\"]','[\"JIRA\", \"Option\"]','FICC Business Unit','Sanjeev Gupta','s.gupta@company.name','Monthly: Eagle tier 3','Single Region Kubernetes','[{\"ipAddress\": \"40.123.45.236\", \"name\": \"GKE Cluster\"}, {\"ipAddress\": \"40.123.45.236\", \"name\": \"Cloud SQL\"}]','Available','Some very long description that I did not want to copy. Some very long description that I did not want to copy. Some very long description that I did not want to copy',0),(2,'Multi region kubernetes','Micro-services',1,'Restricted','Tier 1','[\"POC\", \"AWS\", \"Other\", \"Fancy\"]','[\"GCP\"]','2020-01-09 15:59:10',1300,2000,'[\"UK\", \"DB\"]','[\"Appengine\"]','[\"ApiGee\"]','[\"Jenkins\", \"Travis\"]','[\"Codeship\", \"Option\"]','[\"JIRA\", \"Option\"]','M&A Business Unit','Nathanael Stoltenberg','Nathanael.Stoltenberg@yahoo.com','Monthly: Eagle tier 1','Multi Region Kubernetes','[{\"name\": \"GKE Cluster\", \"ipAddress\": \"40.123.45.236\"}, {\"name\": \"Cloud SQL\", \"ipAddress\": \"40.123.45.236\"}]','Available','Some very long description that I did not want to copy. Some very long description that I did not want to copy. Some very long description that I did not want to copy',NULL),(3,'SQL Single region kubernetes','Micro-services',1,'Restricted','Tier 2','[\"POC\", \"Prod\"]','[\"Azure\", \"GCP\", \"AWS\", \"Other\", \"Fancy\"]','2020-01-09 15:59:10',100,120,'[\"UK\", \"DB\"]','[\"Appengine\"]','[\"ApiGee\"]','[\"Jenkins\", \"Travis\"]','[\"Codeship\", \"Option\"]','[\"JIRA\", \"Option\"]','Equity Capital Business Unit','Brando Howell','Brando.Howell@hotmail.com','Monthly: Eagle tier 2','SQL Single region kubernetes','[{\"name\": \"ITSO\", \"ipAddress\": \"40.123.45.236\"}, {\"name\": \"Cloud SQL\", \"ipAddress\": \"40.123.45.236\"}]','Available','Some very long description that I did not want to copy. Some very long description that I did not want to copy. Some very long description that I did not want to copy',NULL),(101,'CMS Web App','Web application',1,'Public','Tier 3','[\"POC\", \"DEV\"]','[\"GCP\"]','2020-01-09 15:59:10',500,300,'[\"UK\", \"DB\"]','[\"Appengine\"]','[\"ApiGee\"]','[\"Jenkins\", \"Travis\"]','[\"Codeship\", \"Option\"]','[\"JIRA\", \"Option\"]','Debit Capital Business Unit','Mohammed Will PhD','Mohammed.Will@gmail.com','Monthly: Eagle tier 3','CMS Web App','[{\"name\": \"GKE Cluster\", \"ipAddress\": \"40.123.45.236\"}, {\"name\": \"ITSO\", \"ipAddress\": \"40.123.45.236\"}]','Locked','Some very long description that I did not want to copy. Some very long description that I did not want to copy. Some very long description that I did not want to copy',NULL),(102,'Multi region kubernetes','Micro-services',1,'Restricted','Tier 1','[\"POC\", \"AWS\", \"Other\", \"Fancy\"]','[\"GCP\"]','2020-01-09 15:59:10',1600,2500,'[\"UK\", \"DB\"]','[\"Appengine\"]','[\"ApiGee\"]','[\"Jenkins\", \"Travis\"]','[\"Codeship\", \"Option\"]','[\"JIRA\", \"Option\"]','FICC Business Unit','Tressa Ullrich','Tressa97@yahoo.com','Monthly: Eagle tier 1','Multi region kubernetes','[{\"name\": \"ITSO\", \"ipAddress\": \"40.123.45.236\"}, {\"name\": \"Cloud SQL\", \"ipAddress\": \"40.123.45.236\"}]','Locked','Some very long description that I did not want to copy. Some very long description that I did not want to copy. Some very long description that I did not want to copy',NULL),(103,'SQL Single region kubernetes','Micro-services',1,'Restricted','Tier 2','[\"POC\", \"Prod\"]','[\"Azure\", \"GCP\", \"AWS\", \"Other\", \"Fancy\"]','2020-01-09 15:59:10',900,600,'[\"UK\", \"DB\"]','[\"Appengine\"]','[\"ApiGee\"]','[\"Jenkins\", \"Travis\"]','[\"Codeship\", \"Option\"]','[\"JIRA\", \"Option\"]','M&A Business Unit','Rose Dickens Sr.','Rose.Dickens19@hotmail.com','Monthly: Eagle tier 2','SQL Single region kubernetes','[{\"name\": \"GKE Cluster\", \"ipAddress\": \"40.123.45.236\"}, {\"name\": \"ITSO\", \"ipAddress\": \"40.123.45.236\"}]','Available','Some very long description that I did not want to copy. Some very long description that I did not want to copy. Some very long description that I did not want to copy',NULL);
/*!40000 ALTER TABLE `activator` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `application`
--

DROP TABLE IF EXISTS `application`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `application` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `solutionId` int(11) NOT NULL,
  `activatorId` int(11) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `env` varchar(255) DEFAULT NULL,
  `status` varchar(255) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4;

/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `application`
--

LOCK TABLES `application` WRITE;
/*!40000 ALTER TABLE `application` DISABLE KEYS */;
INSERT INTO `application` VALUES (1,1,1,'Placeholder','DEV','Active','Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et do'),(2,1,2,'Other App','POC','Active','Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et do'),(3,2,3,'Other App','POC','Active','Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et do'),(4,2,2,'Great App','Prod','Active','Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et do'),(5,3,3,'Placeholder','Prod','Active','Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et do'),(6,1,2,'My First App','POC','Active','Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et do'),(7,1,2,'Application v1.0.1','POC','Active','Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et do'),(8,4,1,'Application v1.0.2','dev','Active','Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et do'),(9,4,2,'Application v1.1.0','dev','Active','Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et do'),(10,5,3,'Application v1.1.1','dev','Active','Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et do'),(11,5,4,'Application v1.1.2','dev','Active','Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et do'),(12,5,5,'Application v2.0.0','dev','Active','Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et do'),(13,6,6,'Application v2.0.1','dev','Inactive','Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et do'),(14,7,7,'Application v3.0.0','dev','Inactive','Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et do'),(15,8,8,'Application v4.0.0','dev','Inactive','Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et do'),(16,9,9,'Application v5.0.0','dev','Inactive','Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et do'),(17,0,0,'test','dev','Locked','test'),(18,0,0,'string',NULL,NULL,'string');
/*!40000 ALTER TABLE `application` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bgproutingmode`
--

DROP TABLE IF EXISTS `bgproutingmode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bgproutingmode` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `key` varchar(45) DEFAULT NULL,
  `value` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
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
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `businessunit` (
  `key` varchar(255) NOT NULL,
  `value` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `businessunit`
--

LOCK TABLES `businessunit` WRITE;
/*!40000 ALTER TABLE `businessunit` DISABLE KEYS */;
INSERT INTO `businessunit` VALUES ('Data','Data'),('FICC','FICC'),('Modern Apps','Modern Apps');
/*!40000 ALTER TABLE `businessunit` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cd`
--

DROP TABLE IF EXISTS `cd`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
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
/*!50503 SET character_set_client = utf8mb4 */;
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
-- Table structure for table `environment`
--

DROP TABLE IF EXISTS `environment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
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
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `landingzoneaction` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `categoryName` varchar(255) NOT NULL,
  `categoryClass` varchar(255) NOT NULL,
  `completionRate` int(11) NOT NULL DEFAULT '0',
  `locked` tinyint(1) NOT NULL DEFAULT '0',
  `routerLink` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;
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
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `landingzoneprogressitem` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `label` varchar(255) DEFAULT NULL,
  `completed` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
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
/*!50503 SET character_set_client = utf8mb4 */;
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
) ENGINE=InnoDB AUTO_INCREMENT=59 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `landingzonewan`
--

LOCK TABLES `landingzonewan` WRITE;
/*!40000 ALTER TABLE `landingzonewan` DISABLE KEYS */;
INSERT INTO `landingzonewan` VALUES (1,'dev','dev','dev','dev','dev','dev','dev','dev','dev','dev','dev','dev','dev','dev','dev','dev','Fortinet','dev','Global','dev','Backup VPN connection between GCP US and CISCO 5505 on prem','dev',60000,'dev',60005,'dev','dev ','dev'),(2,'Subnet','abc','abc','abc','abc','abc','string','string','string','string','string','string','string','string','string','string','string','abc','abc','abc','abc','abc',12345,'abc',56789,'abc','abc','abc'),(3,'string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string',0,'string',0,'string','string','string'),(4,'string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string',0,'string',0,'string','string','string'),(5,'string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string',0,'string',0,'string','string','string'),(6,'string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string',0,'string',0,'string','string','string'),(7,'string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string',0,'string',0,'string','string','string'),(8,'string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string',0,'string',0,'string','string','string'),(9,'string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string',0,'string',0,'string','string','string'),(10,'string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string',0,'string',0,'string','string','string'),(11,'string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string',0,'string',0,'string','string','string'),(12,'string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string',0,'string',0,'string','string','string'),(13,'string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string',0,'string',0,'string','string','string'),(14,'string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string',0,'string',0,'string','string','string'),(15,'string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string',0,'string',0,'string','string','string'),(16,'string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string',0,'string',0,'string','string','string'),(17,'string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string',0,'string',0,'string','string','string'),(18,'string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string',0,'string',0,'string','string','string'),(19,'string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string',0,'string',0,'string','string','string'),(20,'string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string',12345,'string',56789,'string','string','string'),(21,'string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string',12345,'string',56789,'string','string','string'),(22,'string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string',12345,'string',56789,'string','string','string'),(23,'string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string',12345,'string',56789,'string','string','string'),(24,'string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string',12345,'string',56789,'string','string','string'),(25,'string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string',12345,'string',56789,'string','string','string'),(26,'string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string',12345,'string',56789,'string','string','string'),(27,'string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string',12345,'string',56789,'string','string','string'),(28,'string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string',12345,'string',56789,'string','string','string'),(29,'string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string',12345,'string',56789,'string','string','string'),(30,'string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string',12345,'string',56789,'string','string','string'),(31,'string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string',12345,'string',56789,'string','string','string'),(32,'string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string',12345,'string',56789,'string','string','string'),(33,'string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string',12345,'string',56789,'string','string','string'),(34,'string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string',12345,'string',56789,'string','string','string'),(35,'string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string',12345,'string',56789,'string','string','string'),(36,'string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string',12345,'string',56789,'string','string','string'),(37,'string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string',12345,'string',56789,'string','string','string'),(38,'string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string',12345,'string',56789,'string','string','string'),(39,'string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string',12345,'string',56789,'string','string','string'),(40,'string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string',12345,'string',56789,'string','string','string'),(41,'string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string',12345,'string',56789,'string','string','string'),(42,'string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string',12345,'string',56789,'string','string','string'),(43,'string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string',12345,'string',56789,'string','string','string'),(44,'string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string',12345,'string',56789,'string','string','string'),(45,'string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string',12345,'string',56789,'string','string','string'),(46,'string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string',12345,'string',56789,'string','string','string'),(47,'string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string',12345,'string',56789,'string','string','string'),(48,'string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string',12345,'string',56789,'string','string','string'),(49,'string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string',12345,'string',56789,'string','string','string'),(50,'string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string',12345,'string',56789,'string','string','string'),(51,'string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string',12345,'string',56789,'string','string','string'),(52,'string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string',12345,'string',56789,'string','string','string'),(53,'string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string',12345,'string',56789,'string','string','string'),(54,'string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string',12345,'string',56789,'string','string','string'),(55,'string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string',12345,'string',56789,'string','string','string'),(56,'string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string',12345,'string',56789,'string','string','string'),(57,'string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string','string',12345,'string',56789,'string','string','string');
/*!40000 ALTER TABLE `landingzonewan` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `solution`
--

DROP TABLE IF EXISTS `solution`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
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
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `solution`
--

LOCK TABLES `solution` WRITE;
/*!40000 ALTER TABLE `solution` DISABLE KEYS */;
INSERT INTO `solution` VALUES (1,'Risk Engine','Solution for internal users to be able to process settlement for FX transactions','Modern Apps','XXX-123-456-YYY','Jenkins CI','Spinnaker','GitHub','[\"Development\"]',1,1,'2','2020-03-08 23:07:00'),(2,'Back Office Settlements','Solution for internal users to be able to process settlement for FX transactions','Modern Apps','XXX-111-444-YYY','Jenkins CI','Spinnaker','GitHub','[\"Production\"]',1,0,'2','2020-03-08 23:07:00'),(3,'FX Engine','Solution for internal users to be able to process settlement for FX transactions','Modern Apps','XXX-554-325-YYY','Jenkins CI','Spinnaker','GitHub','[\"Development\"]',0,0,'2','2020-03-08 23:07:00'),(11,'Portfolio Valuation','A portfolio valuation is done to determine and report alternative investments\' performance, which is often required for financial reporting and tax compliance, and also affects the investment manager\'s compensation.','Data','XXX-333-222-IUY','Bamboo','Screwdriver','Cloud native','[\"Production\"]',1,1,'0','2020-03-18 21:02:02'),(12,'Corporate Treasury','The treasury department occupies a central role in the finances of the modern corporation. It takes responsible for the company\'s liquidity—ensures that a company has enough cash available at all times to meet the needs of its primary business operations.','Modern Apps','XXX-333-222-IUY','Team City','Team City','GitHub','[\"Production\"]',1,1,'0','2020-03-18 21:13:14'),(13,'Internal Audit','Internal auditing is the independent and objective evaluation of an organisation\'s internal controls to effectively manage risk within its risk appetite. Internal audit should monitor that any weaknesses identified are also addressed.','Modern Apps','XXX-333-222-IUY','Travis','Screwdriver','Cloud native','[\"Development\"]',1,1,'0','2020-03-18 21:15:22'),(14,'Realtime Margin','Use real-time margin monitoring to see your current margin requirements at a glance, and to understand the margin implications of any transaction before you transmit an order. The Account window shows your account details.','Data','ABC-123-ABC-123','Cloud native','Spinnaker','Cloud native','[\"Development\"]',1,1,'0','2020-03-18 21:19:58'),(15,'Product Control','product control are a center of cost responsible for the daily PnL(Profit and Loss) and its explanation for a dedicated trading desk. The team is responsible to communicate this result within the bank and to the authority FED or ECB.','Data','dat-000-ser-322','Bamboo','Screwdriver','BitBucket','[\"Production\"]',1,1,'0','2020-03-18 21:25:10'),(16,'General Ledger','A general ledger (GL) is a set of numbered accounts a business uses to keep track of its financial transactions and to prepare financial reports. Each account is a unique record summarizing each type of asset, liability, equity, revenue and expense.','Data','ldf-343-sds-232','Cloud native','Team City','Cloud native','[\"Development\", \"Production\"]',1,1,'0','2020-03-18 21:43:54'),(17,'Corporate Finance','Corporate finance is the division of finance that deals with financing, capital structuring, and investment decisions. Corporate finance is primarily concerned with maximizing shareholder value throug','Modern Apps','ASD-456-FFH-234','Bamboo','Screwdriver','Cloud native','[\"Production\"]',1,1,'0','2020-03-19 23:41:59'),(18,'string','string','string','string','string','string','string','[{}]',1,1,'0','2020-04-01 14:49:48'),(19,'string','string','string','string','string','string','string','[{}]',1,1,'0','2020-04-01 14:56:21'),(20,'dev','dev','Data','xxx-xxx-xxx-xxx','Cloud native','Screwdriver','Cloud native','[\"Development\"]',1,1,'0','2020-04-01 15:00:42'),(21,'string','string','string','string','string','string','string','[{}]',1,1,'0','2020-04-01 22:22:46');
/*!40000 ALTER TABLE `solution` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sourcecontrol`
--

DROP TABLE IF EXISTS `sourcecontrol`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
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
/*!50503 SET character_set_client = utf8mb4 */;
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
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `team` (
  `key` varchar(100) NOT NULL,
  `value` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `team`
--

LOCK TABLES `team` WRITE;
/*!40000 ALTER TABLE `team` DISABLE KEYS */;
INSERT INTO `team` VALUES ('Developers','Developers');
/*!40000 ALTER TABLE `team` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(100) NOT NULL,
  `firstName` varchar(100) NOT NULL,
  `lastName` varchar(100) NOT NULL,
  `isAdmin` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'dev@your.company','Jon','Snow',0),(2,'admin@your.company','Adam','Smith',1);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vpnonpremisevendor`
--

DROP TABLE IF EXISTS `vpnonpremisevendor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vpnonpremisevendor` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `key` varchar(45) DEFAULT NULL,
  `value` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
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

-- Dump completed on 2020-04-02  9:14:04
