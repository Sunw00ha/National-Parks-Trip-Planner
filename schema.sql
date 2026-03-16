-- parks database schema
-- Names: Irene Ha, Ejean Kuo, Henron Ruan

USE sys;

DROP DATABASE IF EXISTS parks;

CREATE DATABASE parks_db;

USE parks_db;

DROP TABLE IF EXISTS parks;

CREATE TABLE parks
{
    park varchar(4) not null,
    bucketkey varchar(128) not null, 
    UNIQUE(park)
};

DROP USER IF EXISTS 'parks-read-write';
CREATE USER 'parks-read-write' IDENTIFIED BY 'strong_password';

GRANT SELECT, INSERT, DELETE ON parks_db.* TO 'parks-read-write';

FLUSH PRIVILEGES;
