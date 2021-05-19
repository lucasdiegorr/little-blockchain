CREATE TABLE `block` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `block` blob NOT NULL,
  `hash` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;