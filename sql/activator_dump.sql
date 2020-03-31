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
  `userId` integer DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=104 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `activator`
--

LOCK TABLES `activator` WRITE;
/*!40000 ALTER TABLE `activator` DISABLE KEYS */;
INSERT INTO `activator` (id, name, type, available, sensitivity, category, envs, platforms, lastUpdated, userCapacity, serverCapacity, regions, hosting, apiManagement, ci, cd, sourceControl, businessUnit, technologyOwner, technologyOwnerEmail, billing, activator, resources, status, description  ) VALUES (1,'CMS Web App','Web application',1,'Public','Tier 3','[\"POC\", \"DEV\"]','[\"GCP\"]','2020-01-09 15:59:10',1000,1200,'[\"UK\", \"DB\"]','[\"Appengine\"]','[\"ApiGee\"]','[\"Jenkins\", \"Travis\"]','[\"Codeship\", \"Option\"]','[\"JIRA\", \"Option\"]','FICC Business Unit','Sanjeev Gupta','s.gupta@company.name','Monthly: Eagle tier 3','Single Region Kubernetes','[{\"ipAddress\": \"40.123.45.236\", \"name\": \"GKE Cluster\"}, {\"ipAddress\": \"40.123.45.236\", \"name\": \"Cloud SQL\"}]','Available','Some very long description that I did not want to copy. Some very long description that I did not want to copy. Some very long description that I did not want to copy'),(2,'Multi region kubernetes','Micro-services',1,'Restricted','Tier 1','[\"POC\", \"AWS\", \"Other\", \"Fancy\"]','[\"GCP\"]','2020-01-09 15:59:10',1300,2000,'[\"UK\", \"DB\"]','[\"Appengine\"]','[\"ApiGee\"]','[\"Jenkins\", \"Travis\"]','[\"Codeship\", \"Option\"]','[\"JIRA\", \"Option\"]','M&A Business Unit','Nathanael Stoltenberg','Nathanael.Stoltenberg@yahoo.com','Monthly: Eagle tier 1','Multi Region Kubernetes','[{\"name\": \"GKE Cluster\", \"ipAddress\": \"40.123.45.236\"}, {\"name\": \"Cloud SQL\", \"ipAddress\": \"40.123.45.236\"}]','Available','Some very long description that I did not want to copy. Some very long description that I did not want to copy. Some very long description that I did not want to copy'),(3,'SQL Single region kubernetes','Micro-services',1,'Restricted','Tier 2','[\"POC\", \"Prod\"]','[\"Azure\", \"GCP\", \"AWS\", \"Other\", \"Fancy\"]','2020-01-09 15:59:10',100,120,'[\"UK\", \"DB\"]','[\"Appengine\"]','[\"ApiGee\"]','[\"Jenkins\", \"Travis\"]','[\"Codeship\", \"Option\"]','[\"JIRA\", \"Option\"]','Equity Capital Business Unit','Brando Howell','Brando.Howell@hotmail.com','Monthly: Eagle tier 2','SQL Single region kubernetes','[{\"name\": \"ITSO\", \"ipAddress\": \"40.123.45.236\"}, {\"name\": \"Cloud SQL\", \"ipAddress\": \"40.123.45.236\"}]','Available','Some very long description that I did not want to copy. Some very long description that I did not want to copy. Some very long description that I did not want to copy'),(101,'CMS Web App','Web application',1,'Public','Tier 3','[\"POC\", \"DEV\"]','[\"GCP\"]','2020-01-09 15:59:10',500,300,'[\"UK\", \"DB\"]','[\"Appengine\"]','[\"ApiGee\"]','[\"Jenkins\", \"Travis\"]','[\"Codeship\", \"Option\"]','[\"JIRA\", \"Option\"]','Debit Capital Business Unit','Mohammed Will PhD','Mohammed.Will@gmail.com','Monthly: Eagle tier 3','CMS Web App','[{\"name\": \"GKE Cluster\", \"ipAddress\": \"40.123.45.236\"}, {\"name\": \"ITSO\", \"ipAddress\": \"40.123.45.236\"}]','Locked','Some very long description that I did not want to copy. Some very long description that I did not want to copy. Some very long description that I did not want to copy'),(102,'Multi region kubernetes','Micro-services',1,'Restricted','Tier 1','[\"POC\", \"AWS\", \"Other\", \"Fancy\"]','[\"GCP\"]','2020-01-09 15:59:10',1600,2500,'[\"UK\", \"DB\"]','[\"Appengine\"]','[\"ApiGee\"]','[\"Jenkins\", \"Travis\"]','[\"Codeship\", \"Option\"]','[\"JIRA\", \"Option\"]','FICC Business Unit','Tressa Ullrich','Tressa97@yahoo.com','Monthly: Eagle tier 1','Multi region kubernetes','[{\"name\": \"ITSO\", \"ipAddress\": \"40.123.45.236\"}, {\"name\": \"Cloud SQL\", \"ipAddress\": \"40.123.45.236\"}]','Locked','Some very long description that I did not want to copy. Some very long description that I did not want to copy. Some very long description that I did not want to copy'),(103,'SQL Single region kubernetes','Micro-services',1,'Restricted','Tier 2','[\"POC\", \"Prod\"]','[\"Azure\", \"GCP\", \"AWS\", \"Other\", \"Fancy\"]','2020-01-09 15:59:10',900,600,'[\"UK\", \"DB\"]','[\"Appengine\"]','[\"ApiGee\"]','[\"Jenkins\", \"Travis\"]','[\"Codeship\", \"Option\"]','[\"JIRA\", \"Option\"]','M&A Business Unit','Rose Dickens Sr.','Rose.Dickens19@hotmail.com','Monthly: Eagle tier 2','SQL Single region kubernetes','[{\"name\": \"GKE Cluster\", \"ipAddress\": \"40.123.45.236\"}, {\"name\": \"ITSO\", \"ipAddress\": \"40.123.45.236\"}]','Available','Some very long description that I did not want to copy. Some very long description that I did not want to copy. Some very long description that I did not want to copy');
/*!40000 ALTER TABLE `activator` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-03-30 22:15:12
