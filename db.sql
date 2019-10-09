CREATE TABLE shop_user (
    uid int unsigned AUTO_INCREMENT,
    uname varchar(20) NOT NULL UNIQUE,
    upass char(32) NOT NULL,  -- md5加密
    phone char(11) NOT NULL, 
    reg_time datetime NOT NULL,
    last_login_time datetime NOT NULL,
    priv enum ('1', '2') NOT NULL DEFAULT '1',  -- 1表示为普通用户，2表示为后台管理员
    state enum ('0', '1', '2', '3') NOT NULL DEFAULT '1',  -- 0表示已删除，1表示正常，2表示冻结，3表示异常
    PRIMARY KEY (uid)
) ENGINE=InnoDB AUTO_INCREMENT=1001 DEFAULT CHARSET=utf8;
-- 内置管理员
INSERT INTO shop_user values (DEFAULT, 'root', md5('rootabc123'),'12345678911', now(), now(), 2, 1);

-- 商品信息表
CREATE TABLE `merchinfo` (
  `MerchID` int unsigned AUTO_INCREMENT,
  `MerchName` varchar(50) NOT NULL,
  `MerchType` varchar(20) NOT NULL,
  `MerchPrice` decimal(10,2) NOT NULL,
  `MerchUnit` varchar(10) DEFAULT NULL,
	`MerchState` enum ('1', '2') NOT NULL DEFAULT '1',  -- 1表示商品存在  --2表示商品已删除
	`MerchPhoto` varchar(20) NOT NULL,  -- 商品图片
  PRIMARY KEY (`MerchID`)
) ENGINE=InnoDB AUTO_INCREMENT=1001 DEFAULT CHARSET=utf8;

-- 收货地址表
DROP TABLE IF EXISTS `shipaddr`;  
CREATE TABLE `shipaddr` (
  addrID int unsigned AUTO_INCREMENT,
  uname varchar(20) NOT NULL,
  `Receiver` varchar(10) NOT NULL COMMENT '收货人',
  `ShipPhone` varchar(20) NOT NULL,
  `Adress` varchar(255) NOT NULL,
	Addrstate enum ( '1','2') NOT NULL DEFAULT '1', -- 1表示存在，2表示删除
  PRIMARY KEY (`addrID`)
) ENGINE=InnoDB AUTO_INCREMENT=1001 DEFAULT CHARSET=utf8;

-- 订单表
DROP TABLE IF EXISTS `ordertable`;  
CREATE TABLE `ordertable` (
  `OrderID`  int unsigned AUTO_INCREMENT,
  `addrID` int unsigned,
  `OrderState` enum ('1', '2','3') NOT NULL DEFAULT '1', -- 1表示未收货，2表示已经收货,3表示已删除
  OrderTime datetime NOT NULL,
	PRIMARY KEY (`OrderID`),
	FOREIGN KEY (`addrID`) REFERENCES shipaddr (`addrID`)
) ENGINE=InnoDB  AUTO_INCREMENT=1001 DEFAULT CHARSET=utf8;




-- 订单信息表
DROP TABLE IF EXISTS `orderinfo`;  
CREATE TABLE `orderinfo` (
  `OrderID`  int unsigned ,
  `MerchID` varchar(10) NOT NULL,
	`MerchName` varchar(50) NOT NULL,
  `Num` int(11) NOT NULL,
  `price` decimal(10,2) NOT NULL,
  FOREIGN KEY (`OrderID`) REFERENCES `ordertable` (`OrderID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
