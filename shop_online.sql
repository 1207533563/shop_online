/*
Navicat MySQL Data Transfer

Source Server         : local
Source Server Version : 50645
Source Host           : localhost:3306
Source Database       : shop_online

Target Server Type    : MYSQL
Target Server Version : 50645
File Encoding         : 65001

Date: 2019-10-10 19:01:49
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for merchinfo
-- ----------------------------
DROP TABLE IF EXISTS `merchinfo`;
CREATE TABLE `merchinfo` (
  `MerchID` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `MerchName` varchar(50) NOT NULL,
  `MerchType` varchar(20) NOT NULL,
  `MerchPrice` decimal(10,2) NOT NULL,
  `MerchUnit` varchar(10) DEFAULT NULL,
  `MerchState` enum('1','2') NOT NULL DEFAULT '1',
  `MerchPhoto` varchar(20) NOT NULL,
  PRIMARY KEY (`MerchID`)
) ENGINE=InnoDB AUTO_INCREMENT=1014 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of merchinfo
-- ----------------------------
INSERT INTO `merchinfo` VALUES ('1001', '红豆面包', '早餐面包', '5.00', '包', '1', '红豆面包.jpg');
INSERT INTO `merchinfo` VALUES ('1002', '法式手撕面包', '早餐面包', '7.00', '包', '1', '法式手撕面包.jpg');
INSERT INTO `merchinfo` VALUES ('1003', '奶香面包', '早餐面包', '8.00', '包', '1', '奶香面包.jpg');
INSERT INTO `merchinfo` VALUES ('1004', '可比克薯片（黄瓜味）', '膨化食品', '4.00', '包', '1', '可比克薯片（黄瓜味）.jpg');
INSERT INTO `merchinfo` VALUES ('1008', '雪碧', '碳酸饮料', '3.00', '罐', '1', '雪碧.jpg');
INSERT INTO `merchinfo` VALUES ('1009', '可口可乐(罐装)', '碳酸饮料', '2.50', '罐', '1', '可口可乐(罐装).jpg');
INSERT INTO `merchinfo` VALUES ('1010', '海飞丝(小瓶)', '洗浴用品', '27.00', '瓶', '1', '海飞丝(小瓶).jpg');
INSERT INTO `merchinfo` VALUES ('1011', '水果刀(小)', '杂货', '4.00', '份', '1', '水果刀(小).jpg');
INSERT INTO `merchinfo` VALUES ('1012', '可口可乐(瓶装)', '碳酸饮料', '2.50', '罐', '2', '可口可乐(瓶装).jpg');
INSERT INTO `merchinfo` VALUES ('1013', '冰红茶', '碳酸饮料', '3.00', '瓶', '1', '冰红茶.jpg');

-- ----------------------------
-- Table structure for orderinfo
-- ----------------------------
DROP TABLE IF EXISTS `orderinfo`;
CREATE TABLE `orderinfo` (
  `OrderID` int(10) unsigned DEFAULT NULL,
  `MerchID` varchar(10) NOT NULL,
  `MerchName` varchar(50) NOT NULL,
  `Num` int(11) NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `MerchPhoto` varchar(20) NOT NULL,
  KEY `OrderID` (`OrderID`),
  CONSTRAINT `orderinfo_ibfk_1` FOREIGN KEY (`OrderID`) REFERENCES `ordertable` (`OrderID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of orderinfo
-- ----------------------------
INSERT INTO `orderinfo` VALUES ('1001', '1001', '红豆面包', '2', '5.00', '红豆面包.jpg');
INSERT INTO `orderinfo` VALUES ('1001', '1009', '可口可乐(罐装)', '4', '2.50', '可口可乐(罐装).jpg');
INSERT INTO `orderinfo` VALUES ('1002', '1002', '奶香面包', '1', '8.00', '奶香面包.jpg');
INSERT INTO `orderinfo` VALUES ('1002', '1003', '法式手撕面包', '1', '7.00', '法式手撕面包.jpg');

-- ----------------------------
-- Table structure for ordertable
-- ----------------------------
DROP TABLE IF EXISTS `ordertable`;
CREATE TABLE `ordertable` (
  `OrderID` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `addrID` int(10) unsigned DEFAULT NULL,
  `OrderState` enum('1','2','3') NOT NULL DEFAULT '1',
  `OrderTime` datetime NOT NULL,
  `Merchsum` decimal(10,2) NOT NULL,
  PRIMARY KEY (`OrderID`),
  KEY `addrID` (`addrID`),
  CONSTRAINT `ordertable_ibfk_1` FOREIGN KEY (`addrID`) REFERENCES `shipaddr` (`addrID`)
) ENGINE=InnoDB AUTO_INCREMENT=1005 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of ordertable
-- ----------------------------
INSERT INTO `ordertable` VALUES ('1001', '1001', '3', '2019-10-10 15:18:50', '20.00');
INSERT INTO `ordertable` VALUES ('1002', '1001', '1', '2019-10-10 15:19:27', '15.00');

-- ----------------------------
-- Table structure for shipaddr
-- ----------------------------
DROP TABLE IF EXISTS `shipaddr`;
CREATE TABLE `shipaddr` (
  `addrID` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `uname` varchar(20) NOT NULL,
  `Receiver` varchar(10) NOT NULL COMMENT '收货人',
  `ShipPhone` varchar(20) NOT NULL,
  `Adress` varchar(255) NOT NULL,
  `Addrstate` enum('1','2') NOT NULL DEFAULT '1',
  PRIMARY KEY (`addrID`)
) ENGINE=InnoDB AUTO_INCREMENT=1004 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of shipaddr
-- ----------------------------
INSERT INTO `shipaddr` VALUES ('1001', 'root', '张三丰', '12345678912', '湖北武汉软帝', '1');
INSERT INTO `shipaddr` VALUES ('1002', 'root', '李四', '13035189425', '湖北武汉', '2');
INSERT INTO `shipaddr` VALUES ('1003', 'root', '王五', '13035189425', '湖北武汉', '2');

-- ----------------------------
-- Table structure for shoppingcart
-- ----------------------------
DROP TABLE IF EXISTS `shoppingcart`;
CREATE TABLE `shoppingcart` (
  `uname` varchar(20) NOT NULL,
  `MerchID` varchar(10) NOT NULL,
  `MerchName` varchar(50) NOT NULL,
  `Num` int(11) NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `MerchPhoto` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of shoppingcart
-- ----------------------------
INSERT INTO `shoppingcart` VALUES ('abc123', '1002', '可口可乐(罐装)', '4', '2.50', '可口可乐(罐装).jpg');
INSERT INTO `shoppingcart` VALUES ('abc123', '1001', '红豆面包', '2', '5.00', '红豆面包.jpg');

-- ----------------------------
-- Table structure for shop_user
-- ----------------------------
DROP TABLE IF EXISTS `shop_user`;
CREATE TABLE `shop_user` (
  `uid` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `uname` varchar(20) NOT NULL,
  `upass` char(32) NOT NULL,
  `phone` char(11) NOT NULL,
  `reg_time` datetime NOT NULL,
  `last_login_time` datetime NOT NULL,
  `priv` enum('1','2') NOT NULL DEFAULT '1',
  `state` enum('0','1','2','3') NOT NULL DEFAULT '1',
  PRIMARY KEY (`uid`),
  UNIQUE KEY `uname` (`uname`)
) ENGINE=InnoDB AUTO_INCREMENT=1003 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of shop_user
-- ----------------------------
INSERT INTO `shop_user` VALUES ('1001', 'root', 'c0382a3d2ff603d8222ec3a4cdfb5801', '12345678911', '2019-10-06 11:43:35', '2019-10-10 17:55:42', '2', '0');
INSERT INTO `shop_user` VALUES ('1002', 'abc123', 'a6f70dedd698be90addd35abe38d3876', '13035189425', '2019-10-06 15:20:50', '2019-10-10 17:50:29', '1', '0');
