USE `biddingsystem`;

CREATE TABLE IF NOT EXISTS `jobs` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
  	`jobname` varchar(50) NOT NULL,
  	`jobdesc` varchar(255) NOT NULL,
  	`userid` int(11) NOT NULL,
    `price` float(50),
    `data` BLOB          NOT NULL,
    PRIMARY KEY (`id`),
     FOREIGN KEY (userid)
      REFERENCES accounts(id)
    
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;





