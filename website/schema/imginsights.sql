/*
 Navicat Premium Data Transfer

 Source Server         : MySQL
 Source Server Type    : MySQL
 Source Server Version : 50725
 Source Host           : localhost
 Source Database       : imginsights

 Target Server Type    : MySQL
 Target Server Version : 50725
 File Encoding         : utf-8

 Date: 09/08/2019 12:15:24 PM
*/

SET NAMES utf8;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
--  Table structure for `image_colors`
-- ----------------------------
DROP TABLE IF EXISTS `image_colors`;
CREATE TABLE `image_colors` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `image_id` int(11) NOT NULL,
  `color_code` varchar(7) NOT NULL,
  `code_frequency` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_img_id` (`image_id`),
  KEY `idx_color_code` (`color_code`)
) ENGINE=InnoDB AUTO_INCREMENT=1373221 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `images`
-- ----------------------------
DROP TABLE IF EXISTS `images`;
CREATE TABLE `images` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(300) NOT NULL,
  `status` tinyint(4) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

SET FOREIGN_KEY_CHECKS = 1;
