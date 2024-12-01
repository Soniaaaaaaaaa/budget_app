DROP USER IF EXISTS 'sofayankovich0106'@'localhost';
CREATE USER 'sofayankovich0106'@'localhost' IDENTIFIED BY '';
DROP DATABASE IF EXISTS budget_app;
CREATE DATABASE budget_app;
GRANT ALL PRIVILEGES ON budget_app.* TO 'sofayankovich0106'@'localhost';
USE budget_app;

CREATE TABLE group (
    group_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    group_name VARCHAR(255) NOT NULL UNIQUE
);
CREATE TABLE member (
    group_id INT NOT NULL,
    user_id INT NOT NULL,
    PRIMARY KEY (group_id, user_id),
    CONSTRAINT `fk_group_id` FOREIGN KEY (`group_id`) REFERENCES `group` (`group_id`)
    CONSTRAINT `fk_user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`)
);
CREATE TABLE user (
    user_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    user_role ENUM('owner', 'member') NOT NULL,
);
CREATE TABLE budget (
    budget_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    group_id INT,
    total_budget INT NOT NULL,
    current_expenses INT NOT NULL,
    planned_expenses INT NOT NULL,
    remaining_amount INT AS (planned_expenses - current_expenses) STORED,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_group_id_budget FOREIGN KEY (group_id) REFERENCES group(group_id)
);
INSERT INTO group (group_name) VALUES ("personal");
INSERT INTO member (user_id, group_id)
VALUES (
    (SELECT user_id FROM user WHERE email = 'sofayankovich0106@gmail.com'),
    (SELECT group_id FROM `group` WHERE group_name = 'personal')
);
INSERT INTO user (email, password, user_role, group_id) VALUES ('sofayankovich0106@gmail.com', 'admin123',"owner","1");

-- for uploading changes to db use command mysql -uroot -p < init.sql for password press enter
-- delete all previou db entities mysql -uroot -p -e"DROP DATABASE auth", mysql -uroot -p -e"DROP USER auth_user@localhost"
-- SELECT user, host FROM mysql.user;
-- mysql> exit 