-- MySQL password reset script
-- Run this after connecting to safe-mode MySQL
FLUSH PRIVILEGES;
ALTER USER 'root'@'localhost' IDENTIFIED BY 'CloudHire@123';
FLUSH PRIVILEGES;
CREATE DATABASE IF NOT EXISTS cloudhire_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
SHOW DATABASES;
