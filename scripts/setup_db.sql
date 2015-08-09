CREATE DATABASE IF NOT EXISTS db;
CREATE DATABASE IF NOT EXISTS test;
CREATE USER 'steerclear'@'localhost' IDENTIFIED BY 'St33rCl3@r';
GRANT ALL PRIVILEGES ON db.* TO 'steerclear'@'localhost';
GRANT ALL PRIVILEGES ON test.* TO 'steerclear'@'localhost';