CREATE DATABASE IF NOT EXISTS `face_recognition` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `face_recognition`;

DROP TABLE IF EXISTS `users`;

CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_name` varchar(100) DEFAULT NULL,
  `create_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP(),
  `update_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP() ON UPDATE CURRENT_TIMESTAMP(),
  `email` varchar(100) DEFAULT NULL,
  `password` varchar(100) DEFAULT NULL,
  `permission` varchar(100) DEFAULT 'usuário',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

UPDATE `users`
SET `permission` = 'novo_valor' 
WHERE `email` = 'email_do_usuario';


permission= 'ministro do meio ambiente', 'diretor' e 'usuário'