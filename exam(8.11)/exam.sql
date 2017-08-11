/*
Navicat MySQL Data Transfer

Source Server         : connect
Source Server Version : 50707
Source Host           : 127.0.0.1:3306
Source Database       : exam

Target Server Type    : MYSQL
Target Server Version : 50707
File Encoding         : 65001

Date: 2017-08-11 20:33:43
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for class
-- ----------------------------
DROP TABLE IF EXISTS `class`;
CREATE TABLE `class` (
  `cid` int(11) NOT NULL AUTO_INCREMENT,
  `pid` int(11) NOT NULL,
  `tid` int(11) NOT NULL,
  `mid` int(11) DEFAULT NULL,
  `crid` int(11) DEFAULT NULL,
  `cname` varchar(255) DEFAULT NULL,
  `begindate` date DEFAULT NULL,
  `begintime` tinyint(1) DEFAULT NULL,
  `enddate` date DEFAULT NULL,
  `endtime` tinyint(1) DEFAULT NULL,
  `approve` varchar(255) DEFAULT NULL,
  `ctime` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`cid`),
  KEY `ctid` (`tid`),
  KEY `cpid` (`pid`),
  KEY `cmid` (`mid`),
  KEY `ccrid` (`crid`) USING BTREE,
  CONSTRAINT `ccrid` FOREIGN KEY (`crid`) REFERENCES `classroom` (`crid`),
  CONSTRAINT `cmid` FOREIGN KEY (`mid`) REFERENCES `manager` (`mid`),
  CONSTRAINT `cpid` FOREIGN KEY (`pid`) REFERENCES `project` (`pid`),
  CONSTRAINT `ctid` FOREIGN KEY (`tid`) REFERENCES `teacher` (`tid`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of class
-- ----------------------------
INSERT INTO `class` VALUES ('1', '2', '1218', '34', '1', '培训班', '2017-08-03', '1', '2017-08-03', '0', '已审批', '2017-08-10 10:24:17');
INSERT INTO `class` VALUES ('2', '7', '1218', '36', '1', '培训班1', '2017-08-03', '0', '2017-08-03', '0', '已审批', '2017-08-10 10:24:36');
INSERT INTO `class` VALUES ('3', '7', '1218', '37', '1', '培训班2', '2017-08-03', '0', '2017-08-03', '0', '已审批', '2017-08-10 10:44:36');
INSERT INTO `class` VALUES ('4', '2', '1223', '37', '1', '培训班', '2017-08-03', '0', '2017-08-03', '0', '已审批', '2017-08-07 20:31:33');
INSERT INTO `class` VALUES ('8', '8', '1255', '34', '1', '培训细项', '2017-08-03', '0', '2017-08-03', '0', '已审批', '2017-08-09 15:49:31');
INSERT INTO `class` VALUES ('9', '9', '1218', '37', '1', '培训班', '2017-08-08', '0', '2017-08-09', '1', '已审批', '2017-08-09 17:07:27');
INSERT INTO `class` VALUES ('10', '9', '1218', '37', '1', '培训班', '2017-08-08', '0', '2017-08-09', '1', '已审批', '2017-08-09 17:29:17');
INSERT INTO `class` VALUES ('11', '9', '1218', '37', '1', '培训班', '2017-08-08', '0', '2017-08-09', '1', '已审批', '2017-08-09 17:32:31');
INSERT INTO `class` VALUES ('12', '9', '1218', '37', '1', '培训班', '2017-08-08', '0', '2017-08-09', '1', '已审批', '2017-08-09 17:32:36');
INSERT INTO `class` VALUES ('13', '9', '1218', '37', '1', '培训班', '2017-08-08', '0', '2017-08-09', '1', '已审批', '2017-08-09 17:34:22');
INSERT INTO `class` VALUES ('14', '9', '1218', '37', '1', '培训班', '2017-08-08', '0', '2017-08-09', '1', '已审批', '2017-08-09 17:35:09');
INSERT INTO `class` VALUES ('16', '9', '1252', '34', '5', '培训班', '2017-08-10', '0', '2017-08-10', '0', '已审批', '2017-08-11 20:24:53');
INSERT INTO `class` VALUES ('17', '9', '1218', '37', '2', '培训班', '2017-08-10', '0', '2017-08-10', '0', '已审批', '2017-08-11 20:25:57');
INSERT INTO `class` VALUES ('18', '9', '1218', '37', '5', '培训班', '2017-08-10', '0', '2017-08-10', '0', '已审批', '2017-08-10 16:29:09');
INSERT INTO `class` VALUES ('19', '9', '1252', null, '5', '培训班', '2017-08-10', '0', '2017-08-10', '0', '未审批', '2017-08-11 20:23:31');
INSERT INTO `class` VALUES ('21', '9', '1252', '22', '2', '培训班', '2017-08-10', '0', '2017-08-10', '0', '已审批', '2017-08-11 20:23:12');

-- ----------------------------
-- Table structure for classroom
-- ----------------------------
DROP TABLE IF EXISTS `classroom`;
CREATE TABLE `classroom` (
  `crid` int(11) NOT NULL AUTO_INCREMENT,
  `place` varchar(255) DEFAULT NULL,
  `classroom` varchar(255) DEFAULT NULL,
  `crtime` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`crid`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of classroom
-- ----------------------------
INSERT INTO `classroom` VALUES ('1', '东圃', '201', '2017-08-10 10:42:10');
INSERT INTO `classroom` VALUES ('2', '东圃', '201', '2017-08-11 19:30:03');
INSERT INTO `classroom` VALUES ('5', '东圃', '101', '2017-08-10 15:14:39');

-- ----------------------------
-- Table structure for manager
-- ----------------------------
DROP TABLE IF EXISTS `manager`;
CREATE TABLE `manager` (
  `mid` int(11) NOT NULL AUTO_INCREMENT,
  `mname` varchar(255) DEFAULT NULL,
  `mtime` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`mid`)
) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of manager
-- ----------------------------
INSERT INTO `manager` VALUES ('22', '管理者b', '2017-08-11 17:56:44');
INSERT INTO `manager` VALUES ('33', '管理者c', '2017-08-11 17:56:35');
INSERT INTO `manager` VALUES ('34', '管理者d', '2017-08-11 17:56:29');
INSERT INTO `manager` VALUES ('36', '管理者e', '2017-08-11 17:56:22');
INSERT INTO `manager` VALUES ('37', '管理者a', '2017-08-11 17:56:15');

-- ----------------------------
-- Table structure for organizer
-- ----------------------------
DROP TABLE IF EXISTS `organizer`;
CREATE TABLE `organizer` (
  `oid` int(11) NOT NULL AUTO_INCREMENT,
  `oname` varchar(255) DEFAULT NULL,
  `otime` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`oid`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of organizer
-- ----------------------------
INSERT INTO `organizer` VALUES ('6', '组织者a', '2017-08-11 17:58:48');
INSERT INTO `organizer` VALUES ('7', '组织者b', '2017-08-11 17:58:40');
INSERT INTO `organizer` VALUES ('8', '组织者c', '2017-08-11 17:58:31');

-- ----------------------------
-- Table structure for project
-- ----------------------------
DROP TABLE IF EXISTS `project`;
CREATE TABLE `project` (
  `pid` int(11) NOT NULL AUTO_INCREMENT,
  `oid` int(11) DEFAULT NULL,
  `pname` varchar(255) DEFAULT NULL,
  `budget` int(11) DEFAULT NULL,
  `apply` varchar(20) DEFAULT NULL,
  `ptime` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`pid`),
  KEY `poid` (`oid`),
  CONSTRAINT `poid` FOREIGN KEY (`oid`) REFERENCES `organizer` (`oid`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of project
-- ----------------------------
INSERT INTO `project` VALUES ('2', '8', '项目5', '100000', '已申请', '2017-08-11 18:00:45');
INSERT INTO `project` VALUES ('4', '8', '项目7', '10000', '已申请', '2017-08-11 18:01:00');
INSERT INTO `project` VALUES ('7', '8', '项目6', '1000000', '已申请', '2017-08-11 18:00:53');
INSERT INTO `project` VALUES ('8', '6', '项目3', '1000', '已申请', '2017-08-11 18:00:31');
INSERT INTO `project` VALUES ('9', '8', '项目2', '10000', '已申请', '2017-08-11 19:29:44');
INSERT INTO `project` VALUES ('10', '8', '项目4', '1000', '已申请', '2017-08-11 18:00:38');
INSERT INTO `project` VALUES ('11', '7', '项目1', '1000', '已申请', '2017-08-10 17:18:40');

-- ----------------------------
-- Table structure for student
-- ----------------------------
DROP TABLE IF EXISTS `student`;
CREATE TABLE `student` (
  `sid` int(11) NOT NULL AUTO_INCREMENT,
  `sname` varchar(255) DEFAULT NULL,
  `studenttime` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`sid`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of student
-- ----------------------------
INSERT INTO `student` VALUES ('9', '小明', '2017-08-03 15:20:04');
INSERT INTO `student` VALUES ('10', '小黄', '2017-08-03 15:32:36');
INSERT INTO `student` VALUES ('11', '小蓝', '2017-08-03 15:32:42');

-- ----------------------------
-- Table structure for study
-- ----------------------------
DROP TABLE IF EXISTS `study`;
CREATE TABLE `study` (
  `pid` int(11) NOT NULL,
  `sid` int(11) NOT NULL,
  `studytime` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`pid`,`sid`),
  KEY `study_sid` (`sid`),
  CONSTRAINT `study_pid` FOREIGN KEY (`pid`) REFERENCES `project` (`pid`),
  CONSTRAINT `study_sid` FOREIGN KEY (`sid`) REFERENCES `student` (`sid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of study
-- ----------------------------

-- ----------------------------
-- Table structure for teacher
-- ----------------------------
DROP TABLE IF EXISTS `teacher`;
CREATE TABLE `teacher` (
  `tid` int(11) NOT NULL AUTO_INCREMENT,
  `tname` varchar(255) NOT NULL,
  `bank_number` varchar(255) DEFAULT NULL,
  `ttime` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`tid`)
) ENGINE=InnoDB AUTO_INCREMENT=1256 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of teacher
-- ----------------------------
INSERT INTO `teacher` VALUES ('1218', '教师2', '112', '2017-08-11 17:57:25');
INSERT INTO `teacher` VALUES ('1219', '教师4', '223', '2017-08-11 17:57:55');
INSERT INTO `teacher` VALUES ('1223', '教师4', '444', '2017-08-11 17:57:35');
INSERT INTO `teacher` VALUES ('1224', '教师3', '123', '2017-08-11 17:57:45');
INSERT INTO `teacher` VALUES ('1250', '教师5', '123', '2017-08-11 17:58:08');
INSERT INTO `teacher` VALUES ('1252', '教师6', '123', '2017-08-11 17:58:17');
INSERT INTO `teacher` VALUES ('1255', '教师1', '123', '2017-08-11 17:57:16');
