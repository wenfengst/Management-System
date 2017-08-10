/*
Navicat MySQL Data Transfer

Source Server         : connect
Source Server Version : 50707
Source Host           : localhost:3306
Source Database       : exam

Target Server Type    : MYSQL
Target Server Version : 50707
File Encoding         : 65001

Date: 2017-08-10 17:57:57
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
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8;

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
INSERT INTO `class` VALUES ('16', '9', '1218', '34', '2', '培训班', '2017-08-10', '0', '2017-08-10', '0', '已审批', '2017-08-10 16:30:22');
INSERT INTO `class` VALUES ('17', '9', '1218', '37', '2', '培训班', '2017-08-10', '0', '2017-08-10', '0', '已审批', '2017-08-10 16:30:10');
INSERT INTO `class` VALUES ('18', '9', '1218', '37', '5', '培训班', '2017-08-10', '0', '2017-08-10', '0', '已审批', '2017-08-10 16:29:09');

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
INSERT INTO `classroom` VALUES ('2', '东圃', '201', '2017-08-10 10:43:40');
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
INSERT INTO `manager` VALUES ('22', 'bbb', '2017-08-03 07:03:09');
INSERT INTO `manager` VALUES ('33', 'ccc', '2017-08-03 07:03:20');
INSERT INTO `manager` VALUES ('34', 'ddd', '2017-08-03 15:03:24');
INSERT INTO `manager` VALUES ('36', 'eee', '2017-08-03 15:08:02');
INSERT INTO `manager` VALUES ('37', 'aaa', '2017-08-03 15:37:27');

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
INSERT INTO `organizer` VALUES ('6', 'aaa', '2017-08-03 07:30:33');
INSERT INTO `organizer` VALUES ('7', 'bbb', '2017-08-03 15:37:38');
INSERT INTO `organizer` VALUES ('8', 'ccc', '2017-08-03 15:37:43');

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
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of project
-- ----------------------------
INSERT INTO `project` VALUES ('2', '7', '职能培训', '100000', '已申请', '2017-08-04 20:06:04');
INSERT INTO `project` VALUES ('4', '8', '技能培训', '10000', '已申请', '2017-08-04 20:06:14');
INSERT INTO `project` VALUES ('7', '8', '培训项目', '1000000', '已申请', '2017-08-04 20:06:28');
INSERT INTO `project` VALUES ('8', '6', '项目', '1000', '已申请', '2017-08-07 19:58:39');
INSERT INTO `project` VALUES ('9', '7', '项目1', '10000', '已申请', '2017-08-10 17:21:11');
INSERT INTO `project` VALUES ('10', '8', '项目', '1000', '已申请', '2017-08-10 17:18:06');
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
INSERT INTO `teacher` VALUES ('1218', '陈奕迅', '112', '2017-08-09 15:10:10');
INSERT INTO `teacher` VALUES ('1219', '周杰伦', '223', '2017-08-03 15:51:40');
INSERT INTO `teacher` VALUES ('1223', '那英', '444', '2017-08-03 16:15:31');
INSERT INTO `teacher` VALUES ('1224', '刘欢', '123', '2017-08-03 15:51:45');
INSERT INTO `teacher` VALUES ('1250', '李四', '123', '2017-08-03 15:51:35');
INSERT INTO `teacher` VALUES ('1252', '王五', '123', '2017-08-03 15:51:28');
INSERT INTO `teacher` VALUES ('1255', '张三', '123', '2017-08-03 16:13:22');
