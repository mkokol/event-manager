CREATE DATABASE event_manager;
USE event_manager;


CREATE TABLE `events` (
  `id` varchar(64) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `device_type` enum('mobile','tablet','desktop') CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `category` int(11) DEFAULT NULL,
  `client` int(11) NOT NULL,
  `client_group` int(11) NOT NULL,
  `valid` tinyint(1) NOT NULL,
  `value` decimal(10,2) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

ALTER TABLE `events` ADD PRIMARY KEY (`id`);
