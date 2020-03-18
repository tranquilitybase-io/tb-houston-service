-- MySQL dump 10.13  Distrib 8.0.19, for osx10.15 (x86_64)
--
-- Host: localhost    Database: eagle_db
-- ------------------------------------------------------
-- Server version	8.0.19

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
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `type` varchar(255) DEFAULT NULL,
  `available` tinyint(1) DEFAULT NULL,
  `sensitivity` varchar(255) DEFAULT NULL,
  `category` varchar(255) DEFAULT NULL,
  `envs` varchar(255) DEFAULT NULL,
  `platforms` varchar(255) DEFAULT NULL,
  `lastUpdated` datetime DEFAULT NULL,
  `userCapacity` int DEFAULT NULL,
  `serverCapacity` int DEFAULT NULL,
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
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=97 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `activator`
--

LOCK TABLES `activator` WRITE;
/*!40000 ALTER TABLE `activator` DISABLE KEYS */;
INSERT INTO `activator` VALUES (1,'CMS Web App','Web application',1,'Public','Tier 3','[\"POC\", \"DEV\"]','[\"GCP\"]','2020-01-09 15:59:10',1000,1200,'[\"UK\", \"DB\"]','[\"Appengine\"]','[\"ApiGee\"]','[\"Jenkins\", \"Travis\"]','[\"Codeship\", \"Option\"]','[\"JIRA\", \"Option\"]','FICC Business Unit','Sanjeev Gupta','s.gupta@company.name','Monthly: Eagle tier 3','Single Region Kubernetes','[{\"ipAddress\": \"40.123.45.236\", \"name\": \"GKE Cluster\"}, {\"ipAddress\": \"40.123.45.236\", \"name\": \"Cloud SQL\"}]','False','Some very long description that I did not want to copy. Some very long description that I did not want to copy. Some very long description that I did not want to copy'),(2,'Multi region kubernetes','Mirco-services',1,'Restricted','Tier 1','[\"POC\", \"AWS\", \"Other\", \"Fancy\"]','[\"GCP\"]','2020-01-09 15:59:10',1300,2000,'[\"UK\", \"DB\"]','[\"Appengine\"]','[\"ApiGee\"]','[\"Jenkins\", \"Travis\"]','[\"Codeship\", \"Option\"]','[\"JIRA\", \"Option\"]','M&A Business Unit','Nathanael Stoltenberg','Nathanael.Stoltenberg@yahoo.com','Monthly: Eagle tier 1','Multi Region Kubernetes','[{\"name\": \"GKE Cluster\", \"ipAddress\": \"40.123.45.236\"}, {\"name\": \"Cloud SQL\", \"ipAddress\": \"40.123.45.236\"}]','True','Some very long description that I did not want to copy. Some very long description that I did not want to copy. Some very long description that I did not want to copy'),(3,'Multi region kubernetes','Mirco-services',0,'Restricted','Tier 1','[\"POC\", \"AWS\", \"Other\", \"Fancy\"]','[\"GCP\"]','2020-01-09 15:59:10',1300,2000,'[\"UK\", \"DB\"]','[\"Appengine\"]','[\"ApiGee\"]','[\"Jenkins\", \"Travis\"]','[\"Codeship\", \"Option\"]','[\"JIRA\", \"Option\"]','M&A Business Unit','Nathanael Stoltenberg','Nathanael.Stoltenberg@yahoo.com','Monthly: Eagle tier 1','Multi Region Kubernetes','[{\"name\": \"GKE Cluster\", \"ipAddress\": \"40.123.45.236\"}, {\"name\": \"Cloud SQL\", \"ipAddress\": \"40.123.45.236\"}]','True','Some very long description that I did not want to copy. Some very long description that I did not want to copy. Some very long description that I did not want to copy'),(34,'TEST1','microservices',1,'string','string','[\"string\"]','[\"platform1\", \"platform2\"]','2020-03-20 11:12:13',1000,0,'[\"UK\", \"US\", \"FG\", \"DF\"]','[\"string\"]','[\"string\"]','[\"string\"]','[\"string\"]','[\"sourceControl1\"]','string','technologyOwner','technologyOwnerEmail','string','activator1','[{\"ipAddress\": \"xxx.xxx.xxx.xxx\", \"name\": \"AAA Cluster\"}, {\"ipAddress\": \"xxx.xxx.xxx.xxx\", \"name\": \"BBB Cluster\"}, {\"ipAddress\": \"xxx.xxx.xxx.xxx\", \"name\": \"GGG Cluster\"}, {\"ipAddress\": \"xxx.xxx.xxx.xxx\", \"name\": \"GGG Cluster\"}]','Active',NULL),(35,'TEST1','microservices',1,'string','string','[\"string\"]','[\"platform1\", \"platform2\"]','2020-03-20 11:12:13',1000,0,'[\"UK\", \"US\", \"FG\", \"DF\"]','[\"string\"]','[\"string\"]','[\"string\"]','[\"string\"]','[\"sourceControl1\"]','string','technologyOwner','technologyOwnerEmail','string','activator1','[{\"ipAddress\": \"xxx.xxx.xxx.xxx\", \"name\": \"AAA Cluster\"}, {\"ipAddress\": \"xxx.xxx.xxx.xxx\", \"name\": \"BBB Cluster\"}, {\"ipAddress\": \"xxx.xxx.xxx.xxx\", \"name\": \"GGG Cluster\"}, {\"ipAddress\": \"xxx.xxx.xxx.xxx\", \"name\": \"GGG Cluster\"}]','Active',NULL),(36,'TEST1','microservices',1,'string','string','[\"string\"]','[\"platform1\", \"platform2\"]','2020-03-20 11:12:13',1000,0,'[\"UK\", \"US\", \"FG\", \"DF\"]','[\"string\"]','[\"string\"]','[\"string\"]','[\"string\"]','[\"sourceControl1\"]','string','technologyOwner','technologyOwnerEmail','string','activator1','[{\"ipAddress\": \"xxx.xxx.xxx.xxx\", \"name\": \"AAA Cluster\"}, {\"ipAddress\": \"xxx.xxx.xxx.xxx\", \"name\": \"BBB Cluster\"}, {\"ipAddress\": \"xxx.xxx.xxx.xxx\", \"name\": \"GGG Cluster\"}, {\"ipAddress\": \"xxx.xxx.xxx.xxx\", \"name\": \"GGG Cluster\"}]','Active',NULL),(37,'TEST1','microservices',1,'string','string','[\"string\"]','[\"platform1\", \"platform2\"]','2020-03-20 11:12:13',1000,0,'[\"UK\", \"US\", \"FG\", \"DF\"]','[\"string\"]','[\"string\"]','[\"string\"]','[\"string\"]','[\"sourceControl1\"]','string','technologyOwner','technologyOwnerEmail','string','activator1','[{\"ipAddress\": \"xxx.xxx.xxx.xxx\", \"name\": \"AAA Cluster\"}, {\"ipAddress\": \"xxx.xxx.xxx.xxx\", \"name\": \"BBB Cluster\"}, {\"ipAddress\": \"xxx.xxx.xxx.xxx\", \"name\": \"GGG Cluster\"}, {\"ipAddress\": \"xxx.xxx.xxx.xxx\", \"name\": \"GGG Cluster\"}]','Active',NULL),(38,'TEST1','microservices',1,'string','string','[\"string\"]','[\"platform1\", \"platform2\"]','2020-03-20 11:12:13',1000,0,'[\"UK\", \"US\", \"FG\", \"DF\"]','[\"string\"]','[\"string\"]','[\"string\"]','[\"string\"]','[\"sourceControl1\"]','string','technologyOwner','technologyOwnerEmail','string','activator1','[{\"ipAddress\": \"xxx.xxx.xxx.xxx\", \"name\": \"AAA Cluster\"}, {\"ipAddress\": \"xxx.xxx.xxx.xxx\", \"name\": \"BBB Cluster\"}, {\"ipAddress\": \"xxx.xxx.xxx.xxx\", \"name\": \"GGG Cluster\"}, {\"ipAddress\": \"xxx.xxx.xxx.xxx\", \"name\": \"GGG Cluster\"}]','Active',NULL),(39,'TEST1','microservices',1,'string','string','[\"string\"]','[\"platform1\", \"platform2\"]','2020-03-20 11:12:13',1000,0,'[\"UK\", \"US\", \"FG\", \"DF\"]','[\"string\"]','[\"string\"]','[\"string\"]','[\"string\"]','[\"sourceControl1\"]','string','technologyOwner','technologyOwnerEmail','string','activator1','[{\"ipAddress\": \"xxx.xxx.xxx.xxx\", \"name\": \"AAA Cluster\"}, {\"ipAddress\": \"xxx.xxx.xxx.xxx\", \"name\": \"BBB Cluster\"}, {\"ipAddress\": \"xxx.xxx.xxx.xxx\", \"name\": \"GGG Cluster\"}, {\"ipAddress\": \"xxx.xxx.xxx.xxx\", \"name\": \"GGG Cluster\"}]','Active',NULL),(40,'TEST1','microservices',1,'string','string','[\"string\"]','[\"platform1\", \"platform2\"]','2020-03-20 11:12:13',1000,0,'[\"UK\", \"US\", \"FG\", \"DF\"]','[\"string\"]','[\"string\"]','[\"string\"]','[\"string\"]','[\"sourceControl1\"]','string','technologyOwner','technologyOwnerEmail','string','activator1','[{\"ipAddress\": \"xxx.xxx.xxx.xxx\", \"name\": \"AAA Cluster\"}, {\"ipAddress\": \"xxx.xxx.xxx.xxx\", \"name\": \"BBB Cluster\"}, {\"ipAddress\": \"xxx.xxx.xxx.xxx\", \"name\": \"GGG Cluster\"}, {\"ipAddress\": \"xxx.xxx.xxx.xxx\", \"name\": \"GGG Cluster\"}]','Active',NULL),(41,'TEST1','microservices',1,'string','string','[\"string\"]','[\"platform1\", \"platform2\"]','2020-03-20 11:12:13',1000,0,'[\"UK\", \"US\", \"FG\", \"DF\"]','[\"string\"]','[\"string\"]','[\"string\"]','[\"string\"]','[\"sourceControl1\"]','string','technologyOwner','technologyOwnerEmail','string','activator1','[{\"ipAddress\": \"xxx.xxx.xxx.xxx\", \"name\": \"AAA Cluster\"}, {\"ipAddress\": \"xxx.xxx.xxx.xxx\", \"name\": \"BBB Cluster\"}, {\"ipAddress\": \"xxx.xxx.xxx.xxx\", \"name\": \"GGG Cluster\"}, {\"ipAddress\": \"xxx.xxx.xxx.xxx\", \"name\": \"GGG Cluster\"}]','Active',NULL),(42,'TEST1','microservices',1,'string','string','[\"string\"]','[\"platform1\", \"platform2\"]','2020-03-20 11:12:13',1000,0,'[\"UK\", \"US\", \"FG\", \"DF\"]','[\"string\"]','[\"string\"]','[\"string\"]','[\"string\"]','[\"sourceControl1\"]','string','technologyOwner','technologyOwnerEmail','string','activator1','[{\"ipAddress\": \"xxx.xxx.xxx.xxx\", \"name\": \"AAA Cluster\"}, {\"ipAddress\": \"xxx.xxx.xxx.xxx\", \"name\": \"BBB Cluster\"}, {\"ipAddress\": \"xxx.xxx.xxx.xxx\", \"name\": \"GGG Cluster\"}, {\"ipAddress\": \"xxx.xxx.xxx.xxx\", \"name\": \"GGG Cluster\"}]','Active',NULL),(45,'TEST1','microservices',1,'string','string','[\"string\"]','[\"platform1\", \"platform2\"]','2020-03-20 11:12:13',1000,0,'[\"UK\", \"US\", \"FG\", \"DF\"]','[\"string\"]','[\"string\"]','[\"string\"]','[\"string\"]','[\"sourceControl1\"]','string','technologyOwner','technologyOwnerEmail','string','activator1','[{\"ipAddress\": \"xxx.xxx.xxx.xxx\", \"name\": \"AAA Cluster\"}, {\"ipAddress\": \"xxx.xxx.xxx.xxx\", \"name\": \"BBB Cluster\"}, {\"ipAddress\": \"xxx.xxx.xxx.xxx\", \"name\": \"GGG Cluster\"}, {\"ipAddress\": \"xxx.xxx.xxx.xxx\", \"name\": \"GGG Cluster\"}]','Active',NULL),(46,'TEST1','microservices',1,'string','string','[\"string\"]','[\"platform1\", \"platform2\"]','2020-03-20 11:12:13',1000,0,'[\"UK\", \"US\", \"FG\", \"DF\"]','[\"string\"]','[\"string\"]','[\"string\"]','[\"string\"]','[\"sourceControl1\"]','string','technologyOwner','technologyOwnerEmail','string','activator1','[{\"ipAddress\": \"xxx.xxx.xxx.xxx\", \"name\": \"AAA Cluster\"}, {\"ipAddress\": \"xxx.xxx.xxx.xxx\", \"name\": \"BBB Cluster\"}, {\"ipAddress\": \"xxx.xxx.xxx.xxx\", \"name\": \"GGG Cluster\"}, {\"ipAddress\": \"xxx.xxx.xxx.xxx\", \"name\": \"GGG Cluster\"}]','Active',NULL),(47,'TEST1','microservices',1,'string','string','[\"string\"]','[\"platform1\", \"platform2\"]','2020-03-20 11:12:13',1000,0,'[\"UK\", \"US\", \"FG\", \"DF\"]','[\"string\"]','[\"string\"]','[\"string\"]','[\"string\"]','[\"sourceControl1\"]','string','technologyOwner','technologyOwnerEmail','string','activator1','[{\"ipAddress\": \"xxx.xxx.xxx.xxx\", \"name\": \"AAA Cluster\"}, {\"ipAddress\": \"xxx.xxx.xxx.xxx\", \"name\": \"BBB Cluster\"}, {\"ipAddress\": \"xxx.xxx.xxx.xxx\", \"name\": \"GGG Cluster\"}, {\"ipAddress\": \"xxx.xxx.xxx.xxx\", \"name\": \"GGG Cluster\"}]','Active',NULL),(48,'TEST1','microservices',1,'string','string','[\"string\"]','[\"platform1\", \"platform2\"]','2020-03-20 11:12:13',1000,0,'[\"UK\", \"US\", \"FG\", \"DF\"]','[\"string\"]','[\"string\"]','[\"string\"]','[\"string\"]','[\"sourceControl1\"]','string','technologyOwner','technologyOwnerEmail','string','activator1','[{\"ipAddress\": \"xxx.xxx.xxx.xxx\", \"name\": \"AAA Cluster\"}, {\"ipAddress\": \"xxx.xxx.xxx.xxx\", \"name\": \"BBB Cluster\"}, {\"ipAddress\": \"xxx.xxx.xxx.xxx\", \"name\": \"GGG Cluster\"}, {\"ipAddress\": \"xxx.xxx.xxx.xxx\", \"name\": \"GGG Cluster\"}]','Active',NULL),(49,'TEST1','microservices',1,'string','string','[\"string\"]','[\"platform1\", \"platform2\"]','2020-03-20 11:12:13',1000,0,'[\"UK\", \"US\", \"FG\", \"DF\"]','[\"string\"]','[\"string\"]','[\"string\"]','[\"string\"]','[\"sourceControl1\"]','string','technologyOwner','technologyOwnerEmail','string','activator1','[{\"ipAddress\": \"xxx.xxx.xxx.xxx\", \"name\": \"AAA Cluster\"}, {\"ipAddress\": \"xxx.xxx.xxx.xxx\", \"name\": \"BBB Cluster\"}, {\"ipAddress\": \"xxx.xxx.xxx.xxx\", \"name\": \"GGG Cluster\"}, {\"ipAddress\": \"xxx.xxx.xxx.xxx\", \"name\": \"GGG Cluster\"}]','Active',NULL);
/*!40000 ALTER TABLE `activator` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `application`
--

DROP TABLE IF EXISTS `application`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `application` (
  `id` int NOT NULL AUTO_INCREMENT,
  `solutionId` int NOT NULL,
  `activatorId` int NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `env` varchar(255) DEFAULT NULL,
  `status` varchar(255) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=58 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `application`
--

LOCK TABLES `application` WRITE;
/*!40000 ALTER TABLE `application` DISABLE KEYS */;
INSERT INTO `application` VALUES (1,1,1,'Placeholder','DEV','Active','\n    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eius'),(9,1,2,'Other App','POC','Active','Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et do'),(10,2,3,'Other App','POC','Active','\n    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.\n    Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.\n  '),(11,2,2,'Great App','Prod','Active','\n    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.\n    Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.\n  '),(12,3,3,'Placeholder','Prod','Active','\n    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.\n    Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.\n  '),(13,1,2,'Other App','POC','Active','Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et do'),(14,1,2,'Other App','POC','Active','Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et do'),(49,0,0,'test','dev','status','test application'),(50,0,0,'test','dev','status','test application'),(51,0,0,'test','dev','status','test application'),(52,0,0,'test','dev','status','test application'),(53,0,0,'test','dev','status','test application'),(54,0,0,'test','dev','status','test application'),(55,0,0,'test','dev','status','test application'),(56,0,0,'test','dev','status','test application'),(57,0,0,'test','dev','status','test application');
/*!40000 ALTER TABLE `application` ENABLE KEYS */;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
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
-- Table structure for table `solution`
--

DROP TABLE IF EXISTS `solution`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `solution` (
  `id` int NOT NULL AUTO_INCREMENT,
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
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `solution`
--

LOCK TABLES `solution` WRITE;
/*!40000 ALTER TABLE `solution` DISABLE KEYS */;
INSERT INTO `solution` VALUES (1,'Risk Engine','Solution for internal users to be able to process settlement for FX transactions','Modern Apps','XXX-123-456-YYY','Jenkins CI','Spinnaker','GitHub','[\"Development\"]',1,1,'2','2020-03-08 23:07:00'),(2,'Back Office Settlements','Solution for internal users to be able to process settlement for FX transactions','Modern Apps','XXX-111-444-YYY','Jenkins CI','Spinnaker','GitHub','[\"Production\"]',1,0,'2','2020-03-08 23:07:00'),(3,'FX Engine','Solution for internal users to be able to process settlement for FX transactions','Modern Apps','XXX-554-325-YYY','Jenkins CI','Spinnaker','GitHub','[\"Development\"]',0,0,'2','2020-03-08 23:07:00'),(4,'string','string','string','string','string','string','string','[]',1,1,'0','2020-02-01 12:12:12');
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
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
-- Table structure for table `team`
--

DROP TABLE IF EXISTS `team`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `team` (
  `key` varchar(100) NOT NULL,
  `value` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `team`
--

LOCK TABLES `team` WRITE;
/*!40000 ALTER TABLE `team` DISABLE KEYS */;
INSERT INTO `team` VALUES ('Developers','Developers');
/*!40000 ALTER TABLE `team` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-03-18 14:50:37
