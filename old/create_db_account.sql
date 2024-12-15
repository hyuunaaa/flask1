ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '555555';
ALTER USER 'root'@'%' IDENTIFIED WITH mysql_native_password BY '555555';

CREATE USER IF NOT EXISTS 'flask_user'@'localhost' IDENTIFIED BY '555555';
ALTER USER 'flask_user'@'localhost' IDENTIFIED WITH mysql_native_password BY '555555';
GRANT ALL PRIVILEGES ON saramin_db.* TO 'flask_user'@'localhost';

CREATE USER IF NOT EXISTS 'flask_user'@'%' IDENTIFIED BY '555555';
ALTER USER 'flask_user'@'%' IDENTIFIED WITH mysql_native_password BY '555555';
GRANT ALL PRIVILEGES ON saramin_db.* TO 'flask_user'@'%';