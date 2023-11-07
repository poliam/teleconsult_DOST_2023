/*
SQLyog Ultimate v11.33 (64 bit)
MySQL - 10.4.19-MariaDB : Database - teleconsult
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`teleconsult` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci */;

USE `teleconsult`;

/*Table structure for table `auth_group` */

DROP TABLE IF EXISTS `auth_group`;

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `auth_group` */

/*Table structure for table `auth_group_permissions` */

DROP TABLE IF EXISTS `auth_group_permissions`;

CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `auth_group_permissions` */

/*Table structure for table `auth_permission` */

DROP TABLE IF EXISTS `auth_permission`;

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=125 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `auth_permission` */

insert  into `auth_permission`(`id`,`name`,`content_type_id`,`codename`) values (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add details',7,'add_details'),(26,'Can change details',7,'change_details'),(27,'Can delete details',7,'delete_details'),(28,'Can view details',7,'view_details'),(29,'Can add address',8,'add_address'),(30,'Can change address',8,'change_address'),(31,'Can delete address',8,'delete_address'),(32,'Can view address',8,'view_address'),(33,'Can add relatives',9,'add_relatives'),(34,'Can change relatives',9,'change_relatives'),(35,'Can delete relatives',9,'delete_relatives'),(36,'Can view relatives',9,'view_relatives'),(37,'Can add allergies',10,'add_allergies'),(38,'Can change allergies',10,'change_allergies'),(39,'Can delete allergies',10,'delete_allergies'),(40,'Can view allergies',10,'view_allergies'),(41,'Can add medicine',11,'add_medicine'),(42,'Can change medicine',11,'change_medicine'),(43,'Can delete medicine',11,'delete_medicine'),(44,'Can view medicine',11,'view_medicine'),(45,'Can add dress_and_grooming',12,'add_dress_and_grooming'),(46,'Can change dress_and_grooming',12,'change_dress_and_grooming'),(47,'Can delete dress_and_grooming',12,'delete_dress_and_grooming'),(48,'Can view dress_and_grooming',12,'view_dress_and_grooming'),(49,'Can add attitude',13,'add_attitude'),(50,'Can change attitude',13,'change_attitude'),(51,'Can delete attitude',13,'delete_attitude'),(52,'Can view attitude',13,'view_attitude'),(53,'Can add facialexpression',14,'add_facialexpression'),(54,'Can change facialexpression',14,'change_facialexpression'),(55,'Can delete facialexpression',14,'delete_facialexpression'),(56,'Can view facialexpression',14,'view_facialexpression'),(57,'Can add movement',15,'add_movement'),(58,'Can change movement',15,'change_movement'),(59,'Can delete movement',15,'delete_movement'),(60,'Can view movement',15,'view_movement'),(61,'Can add motoactive',16,'add_motoactive'),(62,'Can change motoactive',16,'change_motoactive'),(63,'Can delete motoactive',16,'delete_motoactive'),(64,'Can view motoactive',16,'view_motoactive'),(65,'Can add speech',17,'add_speech'),(66,'Can change speech',17,'change_speech'),(67,'Can delete speech',17,'delete_speech'),(68,'Can view speech',17,'view_speech'),(69,'Can add aphasia',18,'add_aphasia'),(70,'Can change aphasia',18,'change_aphasia'),(71,'Can delete aphasia',18,'delete_aphasia'),(72,'Can view aphasia',18,'view_aphasia'),(73,'Can add mood',19,'add_mood'),(74,'Can change mood',19,'change_mood'),(75,'Can delete mood',19,'delete_mood'),(76,'Can view mood',19,'view_mood'),(77,'Can add affect',20,'add_affect'),(78,'Can change affect',20,'change_affect'),(79,'Can delete affect',20,'delete_affect'),(80,'Can view affect',20,'view_affect'),(81,'Can add insomnia',21,'add_insomnia'),(82,'Can change insomnia',21,'change_insomnia'),(83,'Can delete insomnia',21,'delete_insomnia'),(84,'Can view insomnia',21,'view_insomnia'),(85,'Can add memory',22,'add_memory'),(86,'Can change memory',22,'change_memory'),(87,'Can delete memory',22,'delete_memory'),(88,'Can view memory',22,'view_memory'),(89,'Can add orientation',23,'add_orientation'),(90,'Can change orientation',23,'change_orientation'),(91,'Can delete orientation',23,'delete_orientation'),(92,'Can view orientation',23,'view_orientation'),(93,'Can add disorderedperception',24,'add_disorderedperception'),(94,'Can change disorderedperception',24,'change_disorderedperception'),(95,'Can delete disorderedperception',24,'delete_disorderedperception'),(96,'Can view disorderedperception',24,'view_disorderedperception'),(97,'Can add thoughtcontent',25,'add_thoughtcontent'),(98,'Can change thoughtcontent',25,'change_thoughtcontent'),(99,'Can delete thoughtcontent',25,'delete_thoughtcontent'),(100,'Can view thoughtcontent',25,'view_thoughtcontent'),(101,'Can add delusioncontent',26,'add_delusioncontent'),(102,'Can change delusioncontent',26,'change_delusioncontent'),(103,'Can delete delusioncontent',26,'delete_delusioncontent'),(104,'Can view delusioncontent',26,'view_delusioncontent'),(105,'Can add thoughtform',27,'add_thoughtform'),(106,'Can change thoughtform',27,'change_thoughtform'),(107,'Can delete thoughtform',27,'delete_thoughtform'),(108,'Can view thoughtform',27,'view_thoughtform'),(109,'Can add preoccupation',28,'add_preoccupation'),(110,'Can change preoccupation',28,'change_preoccupation'),(111,'Can delete preoccupation',28,'delete_preoccupation'),(112,'Can view preoccupation',28,'view_preoccupation'),(113,'Can add condition',29,'add_condition'),(114,'Can change condition',29,'change_condition'),(115,'Can delete condition',29,'delete_condition'),(116,'Can view condition',29,'view_condition'),(117,'Can add global_psychotrauma_screen',30,'add_global_psychotrauma_screen'),(118,'Can change global_psychotrauma_screen',30,'change_global_psychotrauma_screen'),(119,'Can delete global_psychotrauma_screen',30,'delete_global_psychotrauma_screen'),(120,'Can view global_psychotrauma_screen',30,'view_global_psychotrauma_screen'),(121,'Can add considering_event',31,'add_considering_event'),(122,'Can change considering_event',31,'change_considering_event'),(123,'Can delete considering_event',31,'delete_considering_event'),(124,'Can view considering_event',31,'view_considering_event');

/*Table structure for table `auth_user` */

DROP TABLE IF EXISTS `auth_user`;

CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `first_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(254) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `auth_user` */

insert  into `auth_user`(`id`,`password`,`last_login`,`is_superuser`,`username`,`first_name`,`last_name`,`email`,`is_staff`,`is_active`,`date_joined`) values (4,'pbkdf2_sha256$600000$nu1jNivWMlGkJeTDkMKbll$L0NMfCCbxxDiuKW2vluJL/LP6amJHFE1HVoYOA5c+9E=','2023-11-02 03:19:05.080502',0,'poliamusername','William','Crumb','poliamcrumb@gmail.com',0,1,'2023-08-03 05:05:03.665995');

/*Table structure for table `auth_user_groups` */

DROP TABLE IF EXISTS `auth_user_groups`;

CREATE TABLE `auth_user_groups` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `auth_user_groups` */

/*Table structure for table `auth_user_user_permissions` */

DROP TABLE IF EXISTS `auth_user_user_permissions`;

CREATE TABLE `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `auth_user_user_permissions` */

/*Table structure for table `consultation_affect` */

DROP TABLE IF EXISTS `consultation_affect`;

CREATE TABLE `consultation_affect` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(250) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `status` tinyint(1) NOT NULL,
  `is_delete` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `consultation_affect` */

insert  into `consultation_affect`(`id`,`name`,`status`,`is_delete`) values (1,'Broad',1,0),(2,'Appropriate',1,0),(3,'Constricted',1,0),(4,'Empty',1,0),(5,'Guilty',1,0),(6,'Irritable',1,0),(7,'Angry',1,0),(8,'Enraged',1,0),(9,'Terrified',1,0),(10,'Expansive',1,0),(11,'Euphoric',1,0),(12,'Elated',1,0),(13,'Sullen',1,0),(14,'Dejected',1,0),(15,'Anxious',1,0),(16,'Depressed',1,0);

/*Table structure for table `consultation_aphasia` */

DROP TABLE IF EXISTS `consultation_aphasia`;

CREATE TABLE `consultation_aphasia` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(250) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `status` tinyint(1) NOT NULL,
  `is_delete` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `consultation_aphasia` */

insert  into `consultation_aphasia`(`id`,`name`,`status`,`is_delete`) values (1,'Global aphasia',1,0),(2,'Broca\'s aphasia',1,0),(3,'Wernicke\'s aphasia',1,0),(4,'Dysarthria',1,0),(5,'Perseveration',1,0),(6,'Stereotypy',1,0);

/*Table structure for table `consultation_attitude` */

DROP TABLE IF EXISTS `consultation_attitude`;

CREATE TABLE `consultation_attitude` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(250) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `status` tinyint(1) NOT NULL,
  `is_delete` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `consultation_attitude` */

insert  into `consultation_attitude`(`id`,`name`,`status`,`is_delete`) values (1,'Cooperative',1,0),(2,'Attentive',1,0),(3,'Frank',1,0),(4,'Playful',1,0),(5,'Ingratiating',1,0),(6,'Evasive',1,0),(7,'Guarded',1,0),(8,'Hostile',1,0),(9,'Belligerent',1,0),(10,'Contemptuous',1,0),(11,'Seductive',1,0),(12,'Demanding',1,0),(13,'Sullen',1,0),(14,'Passive',1,0),(15,'Manipulative',1,0),(16,'Complaining',1,0),(17,'Suspicious',1,0),(18,'Withdrawn',1,0),(19,'Obsequious',1,0);

/*Table structure for table `consultation_condition` */

DROP TABLE IF EXISTS `consultation_condition`;

CREATE TABLE `consultation_condition` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(250) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `status` tinyint(1) NOT NULL,
  `is_delete` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=601 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `consultation_condition` */

insert  into `consultation_condition`(`id`,`name`,`status`,`is_delete`) values (1,'AF',1,0),(2,'AKA',1,0),(3,'AKI',1,0),(4,'ALL',1,0),(5,'AML',1,0),(6,'ARDS',1,0),(7,'Abscess',1,0),(8,'Achalasia',1,0),(9,'Acne vulgaris',1,0),(10,'Acromegaly',1,0),(11,'Actinomycosis',1,0),(12,'Acute CMV',1,0),(13,'Acute Confusional State',1,0),(14,'Acute Coronary Syndrome',1,0),(15,'Acute EBV',1,0),(16,'Acute Liver Failure',1,0),(17,'Acute Pancreatitis',1,0),(18,'Acute Sinusitis',1,0),(19,'Acute on chronic SDH',1,0),(20,'Addisons Disease',1,0),(21,'Adhesions',1,0),(22,'African Tick Bite Fever',1,0),(23,'Alcohol Dependence',1,0),(24,'Allograft',1,0),(25,'Alopecia',1,0),(26,'Alzheimer\'s',1,0),(27,'Amoebic Dysentry',1,0),(28,'Amoebic liver abscess',1,0),(29,'Amyloid',1,0),(30,'Anaemia',1,0),(31,'Anaemia of Chronic Disease',1,0),(32,'Ancylostoma',1,0),(33,'Anisakiasis',1,0),(34,'Ankylosing Spondylitis',1,0),(35,'Anthrax',1,0),(36,'Anti-phospholipid Syndrome',1,0),(37,'Aortic dissection',1,0),(38,'Aphthous ulcer',1,0),(39,'Aplastic anemia',1,0),(40,'Appendicitis',1,0),(41,'Arthroplasty (hip)',1,0),(42,'Arthroplasty (knee)',1,0),(43,'Asbestosis',1,0),(44,'Ascariasis',1,0),(45,'Aseptic Meningitis',1,0),(46,'Aspergillosis',1,0),(47,'Aspiration Pneumonia',1,0),(48,'Asthma',1,0),(49,'Atrial flutter',1,0),(50,'Atypical Pneumonia',1,0),(51,'Autograft',1,0),(52,'Avascular Necrosis',1,0),(53,'BKA',1,0),(54,'BMT',1,0),(55,'Babesiosis',1,0),(56,'Bacteraemia',1,0),(57,'Bacterial Gastroenteritis',1,0),(58,'Bacterial Meningitis',1,0),(59,'Balanitis',1,0),(60,'Barrett\'s Oesophagus',1,0),(61,'Basal Cell Carcinoma',1,0),(62,'Behcet\'s Syndrome',1,0),(63,'Bejel',1,0),(64,'Bell\'s Palsy',1,0),(65,'Benign Intracranial Hypertension',1,0),(66,'Benign Prostatic Hypertrophy',1,0),(67,'Beri-beri',1,0),(68,'Bicuspid valve',1,0),(69,'Bipolar Syndrome',1,0),(70,'Bipolar disorder',1,0),(71,'Bladder Cancer',1,0),(72,'Bladder stricture',1,0),(73,'Blind',1,0),(74,'Blocked intrathecal pump',1,0),(75,'Boil',1,0),(76,'Botfly',1,0),(77,'Botulism',1,0),(78,'Bowl obstruction',1,0),(79,'Brain Abscess',1,0),(80,'Brainstem encephalitis',1,0),(81,'Breast Cancer',1,0),(82,'Bronchiectasis',1,0),(83,'Brucellosis',1,0),(84,'Burkitts Lymphoma',1,0),(85,'Bursitis',1,0),(86,'Bursititis',1,0),(87,'Buttock Abscess',1,0),(88,'C diff',1,0),(89,'CADASIL',1,0),(90,'CAP',1,0),(91,'CCHF',1,0),(92,'CJD',1,0),(93,'CKD',1,0),(94,'CLL',1,0),(95,'CLM',1,0),(96,'CML',1,0),(97,'COPD',1,0),(98,'CVID',1,0),(99,'Candidaemia',1,0),(100,'Candidiaemia',1,0),(101,'Carcinoid',1,0),(102,'Cardiomyopathy',1,0),(103,'Cat-scratch disease',1,0),(104,'Cauda Equina',1,0),(105,'Cellulitis',1,0),(106,'Cerebellar Syndrome',1,0),(107,'Cerebral Vasculitis',1,0),(108,'Cervical Cancer',1,0),(109,'Cervicitis',1,0),(110,'Chagas Disease',1,0),(111,'Chancroid',1,0),(112,'Chest crisis',1,0),(113,'Chickenpox',1,0),(114,'Chikungunya',1,0),(115,'Cholangitis',1,0),(116,'Cholecystitis',1,0),(117,'Cholera',1,0),(118,'Chronic Granulomatis Disease',1,0),(119,'Chronic Pain',1,0),(120,'Chronic Pancreatitis',1,0),(121,'Chronic SDH',1,0),(122,'Chronic Sinusitis',1,0),(123,'Chronic venous ulcer',1,0),(124,'Churg Strauss Syndrome',1,0),(125,'Ciguatera Poisoning',1,0),(126,'Cirrhosis',1,0),(127,'Coccidioidomycosis',1,0),(128,'Coeliac',1,0),(129,'Colon Cancer',1,0),(130,'Condyloma acuminatum',1,0),(131,'Conjuncitivitis',1,0),(132,'Connective Tissue Disease',1,0),(133,'Contact Dermatitis',1,0),(134,'Conyloma acuminata',1,0),(135,'Cor Pulmonale',1,0),(136,'Cord Compression',1,0),(137,'Cowpox',1,0),(138,'Crohn\'s Disease',1,0),(139,'Cryptococcal IRIS',1,0),(140,'Cryptococcal Meningitis',1,0),(141,'Cryptosporidium',1,0),(142,'Cushing\'s',1,0),(143,'Cutaneous Leishmaniasis',1,0),(144,'Cystic Fibrosis',1,0),(145,'DKA',1,0),(146,'DLBCL',1,0),(147,'DVT',1,0),(148,'Dehydration',1,0),(149,'Delirium',1,0),(150,'Delusional parasitosis',1,0),(151,'Dementia',1,0),(152,'Dengue fever',1,0),(153,'Dental Abscess',1,0),(154,'Depression',1,0),(155,'Dermatitis herpetiformis',1,0),(156,'Dermatomyositis',1,0),(157,'Dermatophytosis',1,0),(158,'Devics Disease',1,0),(159,'Diabetes Insipidus',1,0),(160,'Diabetic Foot Infection',1,0),(161,'Diarrhoea',1,0),(162,'Diffuse Systemic Sclerosis',1,0),(163,'Diphtheria',1,0),(164,'Disc Prolapse',1,0),(165,'Disciitis',1,0),(166,'Discitis',1,0),(167,'Diverticular Disease',1,0),(168,'Drug Overdose',1,0),(169,'Drug Reaction',1,0),(170,'Drug induced psychosis',1,0),(171,'Duodenal ulcer',1,0),(172,'Duodenitis',1,0),(173,'East African Trypanosomiasis',1,0),(174,'Ebola',1,0),(175,'Eclampsia',1,0),(176,'Ectopic Pregnancy',1,0),(177,'Eczema',1,0),(178,'Eczema herpeticum',1,0),(179,'Ehrlichosis',1,0),(180,'Empyema',1,0),(181,'Encephalitis',1,0),(182,'Endometrial Cancer',1,0),(183,'Endometriosis',1,0),(184,'Endophtalmitis',1,0),(185,'Enteric Fever',1,0),(186,'Eosinophilia',1,0),(187,'Eosinophilic Meninigitis',1,0),(188,'Epidemic Typhus',1,0),(189,'Epididymitis',1,0),(190,'Epidural Abscess',1,0),(191,'Epiglottitis',1,0),(192,'Epilepsy',1,0),(193,'Episcleritis',1,0),(194,'Erysipelas',1,0),(195,'Erythema Multiforme',1,0),(196,'Erythema Nodosum',1,0),(197,'Erythema Nodosum Leprosum',1,0),(198,'Erythema Nodousm',1,0),(199,'Erythroderma',1,0),(200,'EtOH Withdrawal',1,0),(201,'Ewings Sarcoma',1,0),(202,'Extrinsic allergic alveolitis',1,0),(203,'FMF',1,0),(204,'Facial Cellulitis',1,0),(205,'Falciparum Malaria',1,0),(206,'Fasciola',1,0),(207,'Febrile neutropaenia',1,0),(208,'Folate Deficiency',1,0),(209,'Fracture',1,0),(210,'G6PD Deficiency',1,0),(211,'GORD',1,0),(212,'GVHD',1,0),(213,'Gallbladder Cancer',1,0),(214,'Gallstones',1,0),(215,'Gastric Cancer',1,0),(216,'Gastric ulcer',1,0),(217,'Gastritis',1,0),(218,'Gastroenteritis',1,0),(219,'Gastroparesis',1,0),(220,'Genital herpes',1,0),(221,'Giardia',1,0),(222,'Glanders',1,0),(223,'Glaucoma',1,0),(224,'Glioblastoma',1,0),(225,'Glomerulonephritis',1,0),(226,'Goiter',1,0),(227,'Gonoccoal arthritis',1,0),(228,'Gonorrhea',1,0),(229,'Gout',1,0),(230,'Graves Disease',1,0),(231,'Groin Abscess',1,0),(232,'Guillain-Barré syndrome',1,0),(233,'HAP',1,0),(234,'HHT',1,0),(235,'HIV',1,0),(236,'HIV Encephalitis',1,0),(237,'HIV Encephalopathy',1,0),(238,'HIV Seroconversion',1,0),(239,'HONK',1,0),(240,'HSV Encephalitis',1,0),(241,'Haematuria',1,0),(242,'Haemolytic Anaemia',1,0),(243,'Haemophagocytic Syndrome',1,0),(244,'Haemophilia',1,0),(245,'Hand, foot and mouth disease',1,0),(246,'Heart failure',1,0),(247,'Henoch-Schönlein purpura',1,0),(248,'Hepatic Encephalopathy',1,0),(249,'Hepatitis A',1,0),(250,'Hepatitis B',1,0),(251,'Hepatitis C',1,0),(252,'Hepatitis D',1,0),(253,'Hepatitis E',1,0),(254,'Hepatitits',1,0),(255,'Hepatorenal syndrome',1,0),(256,'Hereditary spherocytosis',1,0),(257,'Hernia',1,0),(258,'Herpangina',1,0),(259,'Herpes simplex',1,0),(260,'Herpes zoster',1,0),(261,'Herpetic gingivostomatitis',1,0),(262,'Hidranitits suppurative',1,0),(263,'Histoplasmosis',1,0),(264,'Hodgkins Lymphoma',1,0),(265,'Huntingdon\'s',1,0),(266,'Hydatid Disease',1,0),(267,'Hyper-emesis gravidarum',1,0),(268,'Hyper-reactive Malarial Splenomegaly',1,0),(269,'Hypercalcaemia',1,0),(270,'Hypercholesterolaemia',1,0),(271,'Hypereosinophilia Syndrome',1,0),(272,'Hyperlipidaemia',1,0),(273,'Hyperparathyroidism',1,0),(274,'Hypersplenism',1,0),(275,'Hypertension',1,0),(276,'Hypertriglyeridaemia',1,0),(277,'Hypogammaglobulinaemia',1,0),(278,'Hypokalaemia',1,0),(279,'Hyponatraemia',1,0),(280,'Hypoparathyroidism',1,0),(281,'Hypothyroidism',1,0),(282,'IBD',1,0),(283,'IHD',1,0),(284,'ITP',1,0),(285,'IVDU',1,0),(286,'Immune Thrombocytopenia',1,0),(287,'Impetigo',1,0),(288,'Infected IVC Filter',1,0),(289,'Infected Prosthetic Joint',1,0),(290,'Infected THR',1,0),(291,'Infected TKR',1,0),(292,'Infectious mononucleosis',1,0),(293,'Infective Endocarditis',1,0),(294,'Influenza',1,0),(295,'Influenza A',1,0),(296,'Influenza B',1,0),(297,'Interstitial Lung Disease',1,0),(298,'Intestinal Malabsorption',1,0),(299,'Iron deficiency anaemia',1,0),(300,'Irritable Bowel Syndrome',1,0),(301,'Ischaemic Colitis',1,0),(302,'JRA',1,0),(303,'Jigger',1,0),(304,'Kaposi\'s Sarcoma',1,0),(305,'Keratitis',1,0),(306,'Kikuchi\'s Disease',1,0),(307,'Knowlesi Malaria',1,0),(308,'LGV',1,0),(309,'LRTI',1,0),(310,'Lambert Eaton Syndrome',1,0),(311,'Large Vessel Vasculitis',1,0),(312,'Laryngeal Cancer',1,0),(313,'Laryngitis',1,0),(314,'Lassa',1,0),(315,'Lemierres Syndrome ',1,0),(316,'Leprosy',1,0),(317,'Leptospirosis',1,0),(318,'Leucopenia',1,0),(319,'Lichen Simplex',1,0),(320,'Lichen planus',1,0),(321,'Limited Systemic Sclerosis',1,0),(322,'Line Infection',1,0),(323,'Line Thrombosis',1,0),(324,'Listeriosis',1,0),(325,'Liver Abscess',1,0),(326,'Liver Cancer',1,0),(327,'Loa loa',1,0),(328,'Loeffler Syndrome',1,0),(329,'Lower GI Bleed',1,0),(330,'Lung Absces',1,0),(331,'Lung Cancer',1,0),(332,'Lyme Disease',1,0),(333,'Lymphadenopathy',1,0),(334,'Lymphatic filariasis',1,0),(335,'Lymphopenia',1,0),(336,'Madura Foot',1,0),(337,'Malariae Malaria',1,0),(338,'Marfan\'s ',1,0),(339,'Mastoiditis',1,0),(340,'Measles',1,0),(341,'Mediterranean spotted fever',1,0),(342,'Medium Vessel Vasculitis',1,0),(343,'Megaloblastic Anaemia',1,0),(344,'Melanoma',1,0),(345,'Melioidosis',1,0),(346,'Meningitis',1,0),(347,'Meningococcal meningitis',1,0),(348,'Meningoencepahlitis',1,0),(349,'Mesothelioma',1,0),(350,'Microscopic Polyangiitis',1,0),(351,'Migraine',1,0),(352,'Molluscum contagiosum',1,0),(353,'Mononeuritis multiplex',1,0),(354,'Motor Neuron Disease',1,0),(355,'Mucocutaenous Leishmaniasis',1,0),(356,'Mucositis',1,0),(357,'Multicentric Castleman\'s',1,0),(358,'Multicentric Castlemans',1,0),(359,'Multiple Myeloma',1,0),(360,'Multiple sclerosis',1,0),(361,'Mumps',1,0),(362,'Murine Typhus',1,0),(363,'Muscle spasm',1,0),(364,'Muscular dystrophy',1,0),(365,'Myasthenia gravia',1,0),(366,'Mycosis Fungoides',1,0),(367,'Myelofibrosis',1,0),(368,'Myeloma',1,0),(369,'Myositis',1,0),(370,'Ménière’s disease',1,0),(371,'Necrotising Fasciitis',1,0),(372,'Neurocystercicosis',1,0),(373,'Neurofibromatosis',1,0),(374,'Neurogenic Bladder',1,0),(375,'Neutropenia',1,0),(376,'Non-Hodgkins Lymphoma',1,0),(377,'Non-Typhoidal Salmonella',1,0),(378,'Non-tuberculosis Mycobacterial Infection',1,0),(379,'Normal pressure hydrocephalus',1,0),(380,'Norovirus',1,0),(381,'Oesophageal Candiasis',1,0),(382,'Oesophageal Candidia',1,0),(383,'Oesophageal cancer',1,0),(384,'Oesophageal candida',1,0),(385,'Oesophagitis',1,0),(386,'Olceranon bursitis',1,0),(387,'Onchocerciasis',1,0),(388,'Oophritis',1,0),(389,'Opthalmic Herpes Simplex',1,0),(390,'Optic Neuritis',1,0),(391,'Oral Candidia',1,0),(392,'Oral Hairy Leukoplakia',1,0),(393,'Oral cancer',1,0),(394,'Oral candida',1,0),(395,'Orbital cellulits',1,0),(396,'Orchitis',1,0),(397,'Osteoarthritis',1,0),(398,'Osteomyelitis',1,0),(399,'Osteoporosis',1,0),(400,'Otitis Externa',1,0),(401,'Otitis Media',1,0),(402,'Ovale Malaria',1,0),(403,'Ovarian Cancer',1,0),(404,'PCP',1,0),(405,'PCP IRIS',1,0),(406,'PML',1,0),(407,'PUO',1,0),(408,'PVD',1,0),(409,'Pancreatic Cancer',1,0),(410,'Pancytopenia',1,0),(411,'Papillodema',1,0),(412,'Paraspinal Abscess',1,0),(413,'Parkinson\'s disease',1,0),(414,'Patent Ductus Arteriosus',1,0),(415,'Pellagra',1,0),(416,'Pelvic Inflammatory Disease',1,0),(417,'Pemphigoid',1,0),(418,'Pemphigus',1,0),(419,'Penile Cancer',1,0),(420,'Perforation',1,0),(421,'Peri-anal abscess',1,0),(422,'Periorbital Cellulitis',1,0),(423,'Peripheral Neuropathy',1,0),(424,'Peritonitis',1,0),(425,'Pernicious Anaemia',1,0),(426,'Pharyngitis',1,0),(427,'Pinta',1,0),(428,'Pituitary Adenoma',1,0),(429,'Plague',1,0),(430,'Pleural Effusion',1,0),(431,'Pneumothorax',1,0),(432,'Polio',1,0),(433,'Polyarteritis Nodosa',1,0),(434,'Polycythaemia rubra vera',1,0),(435,'Polymyalgia rheumatica',1,0),(436,'Polymyositis',1,0),(437,'Portal hypertension',1,0),(438,'Post malaria neurological syndrome',1,0),(439,'Postherpetic neuralgia',1,0),(440,'Pre-eclampsia',1,0),(441,'Pregnant',1,0),(442,'Primary Biliary Cirrhosis',1,0),(443,'Primary CNS Lymphoma',1,0),(444,'Primary Scleorsing Cholangitis',1,0),(445,'Primary Syphilis',1,0),(446,'Proctitis',1,0),(447,'Prostate Cancer',1,0),(448,'Prostatits',1,0),(449,'Protein losing enteropathy',1,0),(450,'Pseudogout',1,0),(451,'Psoas abcess',1,0),(452,'Psoriasis',1,0),(453,'Psoriatic arthritis',1,0),(454,'Pulmonary Fibrosis',1,0),(455,'Pulmonary Odema',1,0),(456,'Pulmonary hypertension',1,0),(457,'Pyelonephritis',1,0),(458,'Pyoderma gangrenosum',1,0),(459,'Pyogenic Granuloma',1,0),(460,'Q Fever',1,0),(461,'Quinsey',1,0),(462,'Rabies',1,0),(463,'Rash of Unknown Aetiology',1,0),(464,'Rat-bite fever',1,0),(465,'Reactive Arthritis',1,0),(466,'Refeeding Syndrome',1,0),(467,'Relapsed AML',1,0),(468,'Renal Calculi',1,0),(469,'Renal Cancer',1,0),(470,'Renal Tubular Acidosis',1,0),(471,'Retinoblastoma',1,0),(472,'Rhabdomyolysis',1,0),(473,'Rheumatoid Arthritis',1,0),(474,'Rickettsial infection',1,0),(475,'Rickettsialpox',1,0),(476,'Rocky mountain spotted fever',1,0),(477,'Rosacea',1,0),(478,'Roseola infantum',1,0),(479,'Rotavirus',1,0),(480,'Rubella',1,0),(481,'SARS',1,0),(482,'SBP',1,0),(483,'SDH',1,0),(484,'STEWARDSHIP',1,0),(485,'Sacroiliitis',1,0),(486,'Sarcoid',1,0),(487,'Sarcoma',1,0),(488,'Scabies',1,0),(489,'Scarlet Fever',1,0),(490,'Schistosomiasis',1,0),(491,'Schizophrenia',1,0),(492,'Sciatica',1,0),(493,'Scleritis',1,0),(494,'Scrub Typhus',1,0),(495,'Seborrheic dermatitis',1,0),(496,'Secondary Syphilis',1,0),(497,'Sepsis',1,0),(498,'Sepsis (neutropaenic)',1,0),(499,'Sepsis (non-neutropaenic)',1,0),(500,'Septic Arthritis',1,0),(501,'Septic Arthtitis',1,0),(502,'Septic Bursitis',1,0),(503,'Septicaemia',1,0),(504,'Seronegative inflammatory arthritis',1,0),(505,'Severe Combined Immunodeficiency',1,0),(506,'Severe falciparum malaria',1,0),(507,'Shigella',1,0),(508,'Shingles',1,0),(509,'Short Bowel Syndrome',1,0),(510,'Sickle-cell anemia',1,0),(511,'Sickle-cell trait',1,0),(512,'Sinusitis',1,0),(513,'Sjögren\'s syndrome',1,0),(514,'Sleep apnea',1,0),(515,'Small Vessel Vasculitis',1,0),(516,'Smallpox',1,0),(517,'Spinal Abscess',1,0),(518,'St Louis Encephalitis',1,0),(519,'Stevens-Johnsons Syndrome',1,0),(520,'Still\'s Disease',1,0),(521,'Streptococcal throat infection',1,0),(522,'Stroke',1,0),(523,'Strongyloidiasis',1,0),(524,'Sub-Arachnoid Haemorrhage',1,0),(525,'Sweets\'s Syndrome',1,0),(526,'Syndrome of Inappropriate Antidiuretic Hormone',1,0),(527,'Synovitis',1,0),(528,'Systemic lupus erythematosus',1,0),(529,'T1DM',1,0),(530,'T2DM',1,0),(531,'TB',1,0),(532,'THR',1,0),(533,'TKR',1,0),(534,'Takayasu\'s Arteritis',1,0),(535,'Tapeworm',1,0),(536,'Temporal Arteritis',1,0),(537,'Tension headache',1,0),(538,'Tertiary Syphilis',1,0),(539,'Testicular Cancer',1,0),(540,'Testicular Torsion',1,0),(541,'Tetanus',1,0),(542,'Thrombocytopenia',1,0),(543,'Thyroid Cancer',1,0),(544,'Thyroiditis',1,0),(545,'Thyrotoxicosis',1,0),(546,'Tick-borne encephalitis',1,0),(547,'Tinea Capita',1,0),(548,'Tinea Corporis',1,0),(549,'Tinea Pedis',1,0),(550,'Tonsillitis',1,0),(551,'Toxoplasma',1,0),(552,'Toxoplasma IRIS',1,0),(553,'Trachoma',1,0),(554,'Transverse myelitis',1,0),(555,'Trench Fever',1,0),(556,'Trichuris',1,0),(557,'Tropical Pulmonary Eosinophilia',1,0),(558,'Tropical Sprue',1,0),(559,'Tuberculosis',1,0),(560,'Tubo ovarian abscess',1,0),(561,'Tularemia',1,0),(562,'Tumbo Fly',1,0),(563,'URTI',1,0),(564,'UTI',1,0),(565,'Ulcerative Colitis',1,0),(566,'Upper GI Bleed',1,0),(567,'Urethritis',1,0),(568,'Urinary retention',1,0),(569,'Urticaria',1,0),(570,'Uterine fibroid',1,0),(571,'Uveitis',1,0),(572,'VAP',1,0),(573,'VHF',1,0),(574,'VP shunt infection',1,0),(575,'Variceal bleed',1,0),(576,'Vascular Dementia',1,0),(577,'Venous sinus thrombosis',1,0),(578,'Vincent\'s angina',1,0),(579,'Viral Exanthem',1,0),(580,'Viral Gastroenteritis',1,0),(581,'Viral Illness',1,0),(582,'Viral Meningitis',1,0),(583,'Viral Pneumonia',1,0),(584,'Visceral Leishmaniasis',1,0),(585,'Vitamin D Deficiency',1,0),(586,'Vitiligo',1,0),(587,'Vivax Malaria',1,0),(588,'Von Willebrand\'s disease',1,0),(589,'Von-Hippel Lindau Syndrome',1,0),(590,'Wegners Granulomatosis',1,0),(591,'Wernicke\'s encephalopathy',1,0),(592,'West African Trypanosomiasis',1,0),(593,'West Nile',1,0),(594,'Whooping cough',1,0),(595,'Wilson\'s Disease',1,0),(596,'Wound infection (non-surgical)',1,0),(597,'Wound infection (surgical site)',1,0),(598,'Yaws',1,0),(599,'Yellow fever',1,0),(600,'cmml',1,0);

/*Table structure for table `consultation_delusioncontent` */

DROP TABLE IF EXISTS `consultation_delusioncontent`;

CREATE TABLE `consultation_delusioncontent` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(250) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `status` tinyint(1) NOT NULL,
  `is_delete` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `consultation_delusioncontent` */

insert  into `consultation_delusioncontent`(`id`,`name`,`status`,`is_delete`) values (1,'Thought withdrawal',1,0),(2,'Thought insertion',1,0),(3,'Thought broadcast',1,0),(4,'Suspiciousness',1,0),(5,'Grandiose delusions',1,0),(6,'Somatic delusions',1,0),(7,'Delusional guilt',1,0),(8,'Nihilistic delusions',1,0),(9,'Ideas of inference',1,0),(10,'Magical thinking',1,0),(11,'Thought contentt',1,0),(12,'Bizarre behavior',1,0);

/*Table structure for table `consultation_disorderedperception` */

DROP TABLE IF EXISTS `consultation_disorderedperception`;

CREATE TABLE `consultation_disorderedperception` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(250) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `status` tinyint(1) NOT NULL,
  `is_delete` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `consultation_disorderedperception` */

insert  into `consultation_disorderedperception`(`id`,`name`,`status`,`is_delete`) values (1,'Illusions',1,0),(2,'Hallucinations',1,0),(3,'Depersonalization',1,0),(4,'Derealizations',1,0);

/*Table structure for table `consultation_dress_and_grooming` */

DROP TABLE IF EXISTS `consultation_dress_and_grooming`;

CREATE TABLE `consultation_dress_and_grooming` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(250) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `status` tinyint(1) NOT NULL,
  `is_delete` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `consultation_dress_and_grooming` */

insert  into `consultation_dress_and_grooming`(`id`,`name`,`status`,`is_delete`) values (1,'Meticulous',1,0),(2,'Skillfully applied',1,0),(3,'Garish',1,0),(4,'Self-neglect',1,0),(5,'Dress',1,0),(6,'Immaculate',1,0),(7,'Unconventional',1,0),(8,'Fashionable',1,0);

/*Table structure for table `consultation_facialexpression` */

DROP TABLE IF EXISTS `consultation_facialexpression`;

CREATE TABLE `consultation_facialexpression` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(250) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `status` tinyint(1) NOT NULL,
  `is_delete` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `consultation_facialexpression` */

insert  into `consultation_facialexpression`(`id`,`name`,`status`,`is_delete`) values (1,'Pleasant',1,0),(2,'Happy',1,0),(3,'Sad',1,0),(4,'Perplexed',1,0),(5,'Angry',1,0),(6,'Tense',1,0),(7,'Mobile',1,0),(8,'Bland',1,0),(9,'Flat',1,0);

/*Table structure for table `consultation_insomnia` */

DROP TABLE IF EXISTS `consultation_insomnia`;

CREATE TABLE `consultation_insomnia` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(250) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `status` tinyint(1) NOT NULL,
  `is_delete` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `consultation_insomnia` */

/*Table structure for table `consultation_memory` */

DROP TABLE IF EXISTS `consultation_memory`;

CREATE TABLE `consultation_memory` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(250) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `status` tinyint(1) NOT NULL,
  `is_delete` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `consultation_memory` */

insert  into `consultation_memory`(`id`,`name`,`status`,`is_delete`) values (1,'Short-term memory',1,0),(2,'Long-term memory',1,0),(3,'Amnesia',1,0),(4,'Anterograde amnesia',1,0),(5,'Retrograde amnesia',1,0),(6,'Head injuries',1,0),(7,'Transient global amnesia',1,0);

/*Table structure for table `consultation_mood` */

DROP TABLE IF EXISTS `consultation_mood`;

CREATE TABLE `consultation_mood` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(250) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `status` tinyint(1) NOT NULL,
  `is_delete` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `consultation_mood` */

insert  into `consultation_mood`(`id`,`name`,`status`,`is_delete`) values (1,'Euthymic',1,0),(2,'Sad',1,0),(3,'Hopeless',1,0),(4,'Empty',1,0),(5,'Guilty',1,0),(6,'Irritable',1,0),(7,'Angry',1,0),(8,'Enraged',1,0),(9,'Terrified',1,0),(10,'Expansive',1,0),(11,'Euphoric',1,0),(12,'Elated',1,0),(13,'Sullen',1,0),(14,'Dejected',1,0),(15,'Anxious',1,0),(16,'Depressed',1,0);

/*Table structure for table `consultation_motoactive` */

DROP TABLE IF EXISTS `consultation_motoactive`;

CREATE TABLE `consultation_motoactive` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(250) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `status` tinyint(1) NOT NULL,
  `is_delete` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `consultation_motoactive` */

insert  into `consultation_motoactive`(`id`,`name`,`status`,`is_delete`) values (1,'Seated quietly',1,0),(2,'Hyperactive',1,0),(3,'Agitated',1,0),(4,'Combative',1,0),(5,'Clumsy',1,0),(6,'Limp',1,0),(7,'Rigid',1,0),(8,'Motor retardation',1,0),(9,'Mannerisms and posturing',1,0),(10,'Tension',1,0),(11,'Severe akathisia',1,0),(12,'Tardive dyskinesia',1,0),(13,'Catatonic behavior',1,0);

/*Table structure for table `consultation_movement` */

DROP TABLE IF EXISTS `consultation_movement`;

CREATE TABLE `consultation_movement` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(250) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `status` tinyint(1) NOT NULL,
  `is_delete` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `consultation_movement` */

insert  into `consultation_movement`(`id`,`name`,`status`,`is_delete`) values (1,'Pacing',1,0),(2,'Fidgeting',1,0),(3,'Nail biting',1,0),(4,'Trembling',1,0),(5,'Rocking',1,0),(6,'Bouncing',1,0),(7,'Tardive dyskinesia',1,0),(8,'Grimacing',1,0);

/*Table structure for table `consultation_orientation` */

DROP TABLE IF EXISTS `consultation_orientation`;

CREATE TABLE `consultation_orientation` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(250) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `status` tinyint(1) NOT NULL,
  `is_delete` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `consultation_orientation` */

insert  into `consultation_orientation`(`id`,`name`,`status`,`is_delete`) values (1,'Inattentive',1,0),(2,'Lethargy',1,0),(3,'Obtundation',1,0),(4,'Stupor',1,0),(5,'Coma',1,0),(6,'Oriented',1,0);

/*Table structure for table `consultation_preoccupation` */

DROP TABLE IF EXISTS `consultation_preoccupation`;

CREATE TABLE `consultation_preoccupation` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(250) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `status` tinyint(1) NOT NULL,
  `is_delete` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `consultation_preoccupation` */

/*Table structure for table `consultation_speech` */

DROP TABLE IF EXISTS `consultation_speech`;

CREATE TABLE `consultation_speech` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(250) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `status` tinyint(1) NOT NULL,
  `is_delete` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `consultation_speech` */

insert  into `consultation_speech`(`id`,`name`,`status`,`is_delete`) values (1,'Normal rate',1,0),(2,'Slow',1,0),(3,'Hesitant',1,0),(4,'Rapid',1,0),(5,'Pressured',1,0),(6,'Monotonous',1,0),(7,'Emotional',1,0),(8,'Loud',1,0),(9,'Whispered',1,0),(10,'Mumbled',1,0),(11,'Precise',1,0),(12,'Slurred',1,0),(13,'Accented',1,0),(14,'Stuttering',1,0),(15,'Stilted',1,0),(16,'Rambling',1,0),(17,'Impoverished',1,0),(18,'Neologisms',1,0),(19,'Aphasia',1,0);

/*Table structure for table `consultation_thoughtcontent` */

DROP TABLE IF EXISTS `consultation_thoughtcontent`;

CREATE TABLE `consultation_thoughtcontent` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(250) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `status` tinyint(1) NOT NULL,
  `is_delete` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `consultation_thoughtcontent` */

insert  into `consultation_thoughtcontent`(`id`,`name`,`status`,`is_delete`) values (1,'Distortions',1,0),(2,'Delusions',1,0);

/*Table structure for table `consultation_thoughtform` */

DROP TABLE IF EXISTS `consultation_thoughtform`;

CREATE TABLE `consultation_thoughtform` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(250) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `status` tinyint(1) NOT NULL,
  `is_delete` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `consultation_thoughtform` */

insert  into `consultation_thoughtform`(`id`,`name`,`status`,`is_delete`) values (1,'Flow of ideas',1,0),(2,'Spontaneous',1,0),(3,'Goal directed',1,0),(4,'Impoverised',1,0),(5,'Racing thoughts',1,0),(6,'Blocking',1,0),(7,'Circumstantial',1,0),(8,'Perseverative',1,0),(9,'Flight of ideas',1,0),(10,'Loose associations',1,0),(11,'Illogical',1,0),(12,'Incoherent',1,0),(13,'Neologism',1,0),(14,'Distractible',1,0),(15,'Clang association',1,0),(16,'Tangentiality',1,0),(17,'Overvalued ideas',1,0),(18,'Conceptual disorganization',1,0);

/*Table structure for table `django_admin_log` */

DROP TABLE IF EXISTS `django_admin_log`;

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `object_repr` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `django_admin_log` */

/*Table structure for table `django_content_type` */

DROP TABLE IF EXISTS `django_content_type`;

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `model` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `django_content_type` */

insert  into `django_content_type`(`id`,`app_label`,`model`) values (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(20,'consultation','affect'),(18,'consultation','aphasia'),(13,'consultation','attitude'),(29,'consultation','condition'),(26,'consultation','delusioncontent'),(24,'consultation','disorderedperception'),(12,'consultation','dress_and_grooming'),(14,'consultation','facialexpression'),(21,'consultation','insomnia'),(22,'consultation','memory'),(19,'consultation','mood'),(16,'consultation','motoactive'),(15,'consultation','movement'),(23,'consultation','orientation'),(28,'consultation','preoccupation'),(17,'consultation','speech'),(25,'consultation','thoughtcontent'),(27,'consultation','thoughtform'),(5,'contenttypes','contenttype'),(8,'patient','address'),(10,'patient','allergies'),(31,'patient','considering_event'),(7,'patient','details'),(30,'patient','global_psychotrauma_screen'),(11,'patient','medicine'),(9,'patient','relatives'),(6,'sessions','session');

/*Table structure for table `django_migrations` */

DROP TABLE IF EXISTS `django_migrations`;

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `django_migrations` */

insert  into `django_migrations`(`id`,`app`,`name`,`applied`) values (1,'contenttypes','0001_initial','2023-08-03 03:19:18.874511'),(2,'auth','0001_initial','2023-08-03 03:19:19.730004'),(3,'admin','0001_initial','2023-08-03 03:19:19.913130'),(4,'admin','0002_logentry_remove_auto_add','2023-08-03 03:19:19.920330'),(5,'admin','0003_logentry_add_action_flag_choices','2023-08-03 03:19:19.940647'),(6,'contenttypes','0002_remove_content_type_name','2023-08-03 03:19:20.031441'),(7,'auth','0002_alter_permission_name_max_length','2023-08-03 03:19:20.096554'),(8,'auth','0003_alter_user_email_max_length','2023-08-03 03:19:20.143096'),(9,'auth','0004_alter_user_username_opts','2023-08-03 03:19:20.148505'),(10,'auth','0005_alter_user_last_login_null','2023-08-03 03:19:20.212514'),(11,'auth','0006_require_contenttypes_0002','2023-08-03 03:19:20.223126'),(12,'auth','0007_alter_validators_add_error_messages','2023-08-03 03:19:20.226493'),(13,'auth','0008_alter_user_username_max_length','2023-08-03 03:19:20.272901'),(14,'auth','0009_alter_user_last_name_max_length','2023-08-03 03:19:20.307082'),(15,'auth','0010_alter_group_name_max_length','2023-08-03 03:19:20.346469'),(16,'auth','0011_update_proxy_permissions','2023-08-03 03:19:20.359442'),(17,'auth','0012_alter_user_first_name_max_length','2023-08-03 03:19:20.402231'),(18,'sessions','0001_initial','2023-08-03 03:19:20.469799'),(19,'patient','0001_initial','2023-09-26 05:05:59.945422'),(20,'patient','0002_alter_details_bod','2023-10-06 05:27:42.496619'),(21,'patient','0003_details_gender_indentity','2023-10-06 05:27:42.520590'),(22,'patient','0004_relatives','2023-10-06 07:02:44.564526'),(23,'patient','0005_relatives_workplace','2023-10-06 07:38:10.623623'),(24,'patient','0006_medicine_allergies','2023-10-09 06:43:06.745639'),(25,'consultation','0001_initial','2023-10-18 02:38:01.757096'),(26,'consultation','0002_attitude','2023-10-18 02:46:50.641566'),(27,'consultation','0003_facialexpression','2023-10-18 02:54:42.153848'),(28,'consultation','0004_movement','2023-10-18 03:00:34.511517'),(29,'consultation','0005_motoactive','2023-10-18 03:06:26.957282'),(30,'consultation','0006_speech','2023-10-18 03:13:57.375731'),(31,'consultation','0007_aphasia','2023-10-18 03:19:32.248563'),(32,'consultation','0008_mood','2023-10-18 03:26:02.555550'),(33,'consultation','0009_affect','2023-10-18 03:30:00.816129'),(34,'consultation','0010_insomnia','2023-10-18 03:34:48.549589'),(35,'consultation','0011_memory_orientation','2023-10-18 03:41:07.218015'),(36,'consultation','0012_disorderedperception','2023-10-18 13:21:58.264309'),(37,'consultation','0013_thoughtcontent','2023-10-18 13:28:38.505051'),(38,'consultation','0014_delusioncontent_thoughtform','2023-10-18 13:33:35.474295'),(39,'consultation','0015_preoccupation','2023-10-18 14:13:56.731008'),(40,'consultation','0016_condition','2023-10-18 14:36:30.375411'),(41,'patient','0007_global_psychotrauma_screen_considering_event','2023-11-02 04:04:06.659658');

/*Table structure for table `django_session` */

DROP TABLE IF EXISTS `django_session`;

CREATE TABLE `django_session` (
  `session_key` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `session_data` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `django_session` */

insert  into `django_session`(`session_key`,`session_data`,`expire_date`) values ('525825nlpbmbiik59hkfzjy7cqrhp71r','.eJxVjDsOwjAQBe_iGllZ_5eSnjNYa3uNAyiR4qRC3B0ipYD2zcx7iUjb2uLWeYljEWdhxOl3S5QfPO2g3Gm6zTLP07qMSe6KPGiX17nw83K4fweNevvWg9IMFUg79pkxFAXJO1sdVqOwEoSSlbfGaAIMwSEWD3pAbZNhAiPeH9DmNvo:1qvuGN:oZOE2xvVinZ52ynriXwxwijDU_mMDsmGsJDYcCMppn0','2023-11-09 06:54:39.474205'),('dti25gnwm0m1odzw28m3lieyx8s8z2hv','.eJxVjDsOwjAQBe_iGllZ_5eSnjNYa3uNAyiR4qRC3B0ipYD2zcx7iUjb2uLWeYljEWdhxOl3S5QfPO2g3Gm6zTLP07qMSe6KPGiX17nw83K4fweNevvWg9IMFUg79pkxFAXJO1sdVqOwEoSSlbfGaAIMwSEWD3pAbZNhAiPeH9DmNvo:1qkyJb:d6DztciWQYVDPjdiz8K_rWLufPxrAzuaJq7PimZ0n7A','2023-10-10 03:00:47.970206'),('fr505xnwyf1djtt4cg4z01c2gw9zovy5','.eJxVjDsOwjAQBe_iGllZ_5eSnjNYa3uNAyiR4qRC3B0ipYD2zcx7iUjb2uLWeYljEWdhxOl3S5QfPO2g3Gm6zTLP07qMSe6KPGiX17nw83K4fweNevvWg9IMFUg79pkxFAXJO1sdVqOwEoSSlbfGaAIMwSEWD3pAbZNhAiPeH9DmNvo:1qqnMO:DvrODntPoTuE9ClY_FWFEjYb6PDoAYrUcCDZ19e3dCU','2023-10-26 04:31:44.512720'),('hvgb53iipxfnes2d0r54q0xm3bw8qkxs','.eJxVjDsOwjAQBe_iGllZ_5eSnjNYa3uNAyiR4qRC3B0ipYD2zcx7iUjb2uLWeYljEWdhxOl3S5QfPO2g3Gm6zTLP07qMSe6KPGiX17nw83K4fweNevvWg9IMFUg79pkxFAXJO1sdVqOwEoSSlbfGaAIMwSEWD3pAbZNhAiPeH9DmNvo:1qe5FN:Fq9uPAl0OjS4EXIM-Pb8H8Y7_aKT6NdOtyMW3EdINew','2023-09-21 02:59:57.078822'),('hyzx713k3c0en3p2vjogrfort7ct96jw','.eJxVjDsOwjAQBe_iGllZ_5eSnjNYa3uNAyiR4qRC3B0ipYD2zcx7iUjb2uLWeYljEWdhxOl3S5QfPO2g3Gm6zTLP07qMSe6KPGiX17nw83K4fweNevvWg9IMFUg79pkxFAXJO1sdVqOwEoSSlbfGaAIMwSEWD3pAbZNhAiPeH9DmNvo:1qyOEb:G4VGevPyxwAhlbgJR2iFhKWkH4ru7NpwA4rBG1gMtuk','2023-11-16 03:19:05.082509'),('x4remxbf6umqdpm8zbo043bruyh4lorw','.eJxVjDsOwjAQBe_iGllZ_5eSnjNYa3uNAyiR4qRC3B0ipYD2zcx7iUjb2uLWeYljEWdhxOl3S5QfPO2g3Gm6zTLP07qMSe6KPGiX17nw83K4fweNevvWg9IMFUg79pkxFAXJO1sdVqOwEoSSlbfGaAIMwSEWD3pAbZNhAiPeH9DmNvo:1qRQgK:uNXZQiGK5FmXHtwbLL7IxBkmjB9tJBrxGzXwBMOf2Dc','2023-08-17 05:15:28.669378');

/*Table structure for table `patient_address` */

DROP TABLE IF EXISTS `patient_address`;

CREATE TABLE `patient_address` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `street` varchar(250) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `apt` varchar(250) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `barangay` varchar(250) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `province` varchar(250) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `city` varchar(250) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `country` varchar(250) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `zip_code` varchar(250) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `is_current` tinyint(1) NOT NULL,
  `create_date` datetime(6) NOT NULL,
  `update_date` datetime(6) NOT NULL,
  `status` tinyint(1) NOT NULL,
  `is_delete` tinyint(1) NOT NULL,
  `details_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `patient_address_details_id_faa9fcce_fk_patient_details_id` (`details_id`),
  CONSTRAINT `patient_address_details_id_faa9fcce_fk_patient_details_id` FOREIGN KEY (`details_id`) REFERENCES `patient_details` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `patient_address` */

insert  into `patient_address`(`id`,`street`,`apt`,`barangay`,`province`,`city`,`country`,`zip_code`,`is_current`,`create_date`,`update_date`,`status`,`is_delete`,`details_id`) values (4,'block 18 lot 35 Deca Home Cat grande','Not',NULL,NULL,'Davao City','Philippines','8000',1,'2023-09-27 04:40:06.473391','2023-09-27 04:40:06.473391',1,0,3),(5,'Block 18 Lot 35 Deca Home',NULL,'Cat Grande','Davao Del Sur','Davao City','Philippines',NULL,0,'2023-09-27 04:40:06.475831','2023-09-27 04:40:06.475831',1,0,3),(10,'','',NULL,NULL,'','','',1,'2023-10-31 02:57:44.300016','2023-10-31 02:57:44.300016',1,0,6),(11,'',NULL,'','','','Philippines',NULL,0,'2023-10-31 02:57:44.303734','2023-10-31 02:57:44.303734',1,0,6);

/*Table structure for table `patient_allergies` */

DROP TABLE IF EXISTS `patient_allergies`;

CREATE TABLE `patient_allergies` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `is_delete` tinyint(1) NOT NULL,
  `details_id` bigint(20) DEFAULT NULL,
  `medicine_name_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `patient_allergies_details_id_1f8ac3c5_fk_patient_details_id` (`details_id`),
  KEY `patient_allergies_medicine_name_id_97602c59_fk_patient_m` (`medicine_name_id`),
  CONSTRAINT `patient_allergies_details_id_1f8ac3c5_fk_patient_details_id` FOREIGN KEY (`details_id`) REFERENCES `patient_details` (`id`),
  CONSTRAINT `patient_allergies_medicine_name_id_97602c59_fk_patient_m` FOREIGN KEY (`medicine_name_id`) REFERENCES `patient_medicine` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `patient_allergies` */

insert  into `patient_allergies`(`id`,`is_delete`,`details_id`,`medicine_name_id`) values (1,0,3,3);

/*Table structure for table `patient_considering_event` */

DROP TABLE IF EXISTS `patient_considering_event`;

CREATE TABLE `patient_considering_event` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `considering_event_1` tinyint(1) NOT NULL,
  `considering_event_2` tinyint(1) NOT NULL,
  `considering_event_3` tinyint(1) NOT NULL,
  `considering_event_4` tinyint(1) NOT NULL,
  `considering_event_5` tinyint(1) NOT NULL,
  `considering_event_6` tinyint(1) NOT NULL,
  `considering_event_7` tinyint(1) NOT NULL,
  `considering_event_8` tinyint(1) NOT NULL,
  `considering_event_9` tinyint(1) NOT NULL,
  `considering_event_10` tinyint(1) NOT NULL,
  `considering_event_11` tinyint(1) NOT NULL,
  `considering_event_12` tinyint(1) NOT NULL,
  `considering_event_13` tinyint(1) NOT NULL,
  `considering_event_14` tinyint(1) NOT NULL,
  `considering_event_15` tinyint(1) NOT NULL,
  `considering_event_16` tinyint(1) NOT NULL,
  `considering_event_17` tinyint(1) NOT NULL,
  `considering_event_18` tinyint(1) NOT NULL,
  `considering_event_19` tinyint(1) NOT NULL,
  `considering_event_20` tinyint(1) NOT NULL,
  `considering_event_21` tinyint(1) NOT NULL,
  `considering_event_22` tinyint(1) NOT NULL,
  `considering_event_23` varchar(250) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `create_date` datetime(6) NOT NULL,
  `update_date` datetime(6) NOT NULL,
  `history` longtext COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `status` tinyint(1) NOT NULL,
  `is_delete` tinyint(1) NOT NULL,
  `global_psychotrauma_screen_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `patient_considering__global_psychotrauma__ac7c8b93_fk_patient_g` (`global_psychotrauma_screen_id`),
  CONSTRAINT `patient_considering__global_psychotrauma__ac7c8b93_fk_patient_g` FOREIGN KEY (`global_psychotrauma_screen_id`) REFERENCES `patient_global_psychotrauma_screen` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `patient_considering_event` */

insert  into `patient_considering_event`(`id`,`considering_event_1`,`considering_event_2`,`considering_event_3`,`considering_event_4`,`considering_event_5`,`considering_event_6`,`considering_event_7`,`considering_event_8`,`considering_event_9`,`considering_event_10`,`considering_event_11`,`considering_event_12`,`considering_event_13`,`considering_event_14`,`considering_event_15`,`considering_event_16`,`considering_event_17`,`considering_event_18`,`considering_event_19`,`considering_event_20`,`considering_event_21`,`considering_event_22`,`considering_event_23`,`create_date`,`update_date`,`history`,`status`,`is_delete`,`global_psychotrauma_screen_id`) values (1,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,'9','2023-11-02 04:40:21.143310','2023-11-02 04:40:21.143310',NULL,1,0,2);

/*Table structure for table `patient_details` */

DROP TABLE IF EXISTS `patient_details`;

CREATE TABLE `patient_details` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(250) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `middle_name` varchar(250) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `last_name` varchar(250) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `gender` varchar(250) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `BOD` date DEFAULT NULL,
  `marital_status` varchar(250) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `contact_number` varchar(250) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `alias` varchar(250) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `email` varchar(250) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `birth_place` varchar(250) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `religion` varchar(250) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `high_education` varchar(250) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `citizenship` varchar(250) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `nationality` varchar(250) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `workplace` varchar(250) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `occupation` varchar(250) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `profile_picture` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `create_date` datetime(6) NOT NULL,
  `update_date` datetime(6) NOT NULL,
  `history` longtext COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `status` tinyint(1) NOT NULL,
  `is_delete` tinyint(1) NOT NULL,
  `gender_indentity` varchar(250) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `patient_details` */

insert  into `patient_details`(`id`,`first_name`,`middle_name`,`last_name`,`gender`,`BOD`,`marital_status`,`contact_number`,`alias`,`email`,`birth_place`,`religion`,`high_education`,`citizenship`,`nationality`,`workplace`,`occupation`,`profile_picture`,`create_date`,`update_date`,`history`,`status`,`is_delete`,`gender_indentity`) values (3,'William','Valderosa','Crumb','Male','1991-10-06','Married','09663308394','Poliam','poliamcrumb@gmail.com','Davao City','Roman Catholic','Collage','Filippino','Filipino','House','Software Developer','prof_pic/profile_picture_4_844.jpg','2023-09-27 04:40:06.448807','2023-09-27 04:40:06.448807',NULL,1,0,NULL),(6,'desiderio','Lopez','ampe','Male','2023-10-31','Married','','','sample','','','','','','','','','2023-10-31 02:57:44.262642','2023-10-31 02:57:44.262642',NULL,1,0,'');

/*Table structure for table `patient_global_psychotrauma_screen` */

DROP TABLE IF EXISTS `patient_global_psychotrauma_screen`;

CREATE TABLE `patient_global_psychotrauma_screen` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `consultation_date` datetime(6) NOT NULL,
  `event_description` longtext COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `event_happened` varchar(250) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `physical_violence` varchar(250) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `sexual_violence` varchar(250) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `emotional_abuse` varchar(250) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `serious_injury` varchar(250) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `life_threatening` varchar(250) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `sudden_death_of_loved_one` tinyint(1) NOT NULL,
  `cause_harm_to_others` tinyint(1) NOT NULL,
  `covid` tinyint(1) NOT NULL,
  `single_event_occurring` varchar(250) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `range_event_occurring_from` varchar(250) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `range_event_occurring_to` varchar(250) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `create_date` datetime(6) NOT NULL,
  `update_date` datetime(6) NOT NULL,
  `history` longtext COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `status` tinyint(1) NOT NULL,
  `is_delete` tinyint(1) NOT NULL,
  `details_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `patient_global_psych_details_id_0e5f96ab_fk_patient_d` (`details_id`),
  CONSTRAINT `patient_global_psych_details_id_0e5f96ab_fk_patient_d` FOREIGN KEY (`details_id`) REFERENCES `patient_details` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `patient_global_psychotrauma_screen` */

insert  into `patient_global_psychotrauma_screen`(`id`,`consultation_date`,`event_description`,`event_happened`,`physical_violence`,`sexual_violence`,`emotional_abuse`,`serious_injury`,`life_threatening`,`sudden_death_of_loved_one`,`cause_harm_to_others`,`covid`,`single_event_occurring`,`range_event_occurring_from`,`range_event_occurring_to`,`create_date`,`update_date`,`history`,`status`,`is_delete`,`details_id`) values (2,'2023-11-02 04:40:20.658417','was','last half year','to yourself','happened to someone else','to yourself','happened to someone else','to yourself',1,0,1,'12','22','32','2023-11-02 04:40:20.658417','2023-11-02 04:40:20.658417',NULL,1,0,3);

/*Table structure for table `patient_medicine` */

DROP TABLE IF EXISTS `patient_medicine`;

CREATE TABLE `patient_medicine` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(250) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `status` tinyint(1) NOT NULL,
  `is_delete` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `patient_medicine` */

insert  into `patient_medicine`(`id`,`name`,`status`,`is_delete`) values (1,'paracetamol',1,0),(2,'citirizine',1,0),(3,'calpol',1,0);

/*Table structure for table `patient_relatives` */

DROP TABLE IF EXISTS `patient_relatives`;

CREATE TABLE `patient_relatives` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(250) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `middle_name` varchar(250) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `last_name` varchar(250) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `gender` varchar(250) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `gender_indentity` varchar(250) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `DOB` date DEFAULT NULL,
  `marital_status` varchar(250) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `relationship` varchar(250) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `high_education` varchar(250) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `occupation` varchar(250) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `contact_number` varchar(250) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `email` varchar(250) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `create_date` datetime(6) NOT NULL,
  `update_date` datetime(6) NOT NULL,
  `history` longtext COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `status` tinyint(1) NOT NULL,
  `is_delete` tinyint(1) NOT NULL,
  `details_id` bigint(20) DEFAULT NULL,
  `Workplace` varchar(250) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `patient_relatives_details_id_bd3f40cd_fk_patient_details_id` (`details_id`),
  CONSTRAINT `patient_relatives_details_id_bd3f40cd_fk_patient_details_id` FOREIGN KEY (`details_id`) REFERENCES `patient_details` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `patient_relatives` */

insert  into `patient_relatives`(`id`,`first_name`,`middle_name`,`last_name`,`gender`,`gender_indentity`,`DOB`,`marital_status`,`relationship`,`high_education`,`occupation`,`contact_number`,`email`,`create_date`,`update_date`,`history`,`status`,`is_delete`,`details_id`,`Workplace`) values (1,'Dearly','Toro-Toro','Crumb','Female','','1989-01-21','Married','Wife','Collage','Virtual Assitances','09663308394','dearlydeardee@gmail.com','2023-10-06 07:44:16.933745','2023-10-06 07:44:16.933745',NULL,1,0,3,NULL);

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
