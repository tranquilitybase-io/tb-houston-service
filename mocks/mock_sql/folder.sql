CREATE TABLE `folder` (
  `id` int(11) NOT NULL,
  `parentFolderId` int(11) NOT NULL,
  `folderName` varchar(80) NOT NULL,
  `status` varchar(45) NOT NULL,
  `taskId` varchar(100) DEFAULT NULL,
  `solutionId` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
