-- last edited 28.11
DROP USER IF EXISTS 'sofayankovich0106'@'172.18.0.2';
DROP USER IF EXISTS 'sliusarenko.tanya'@'172.18.0.2';
DROP USER IF EXISTS 'ashkyl97'@'172.18.0.2';

DROP USER IF EXISTS 'sofayankovich0106'@'localhost';
DROP USER IF EXISTS 'sliusarenko.tanya'@'localhost';
DROP USER IF EXISTS 'ashkyl97'@'localhost';

CREATE USER 'sofayankovich0106'@'172.18.0.2' IDENTIFIED BY '';
CREATE USER 'sliusarenko.tanya'@'172.18.0.2' IDENTIFIED BY '';
CREATE USER 'ashkyl97'@'172.18.0.2' IDENTIFIED BY '';

CREATE USER 'sofayankovich0106'@'localhost' IDENTIFIED BY '';
CREATE USER 'sliusarenko.tanya'@'localhost' IDENTIFIED BY '';
CREATE USER 'ashkyl97'@'localhost' IDENTIFIED BY '';

DROP DATABASE IF EXISTS budget_app;
CREATE DATABASE budget_app;

GRANT ALL PRIVILEGES ON budget_app.* TO 'sofayankovich0106'@'172.18.0.2';
GRANT ALL PRIVILEGES ON budget_app.* TO 'sliusarenko.tanya'@'172.18.0.2';
GRANT ALL PRIVILEGES ON budget_app.* TO 'ashkyl97'@'172.18.0.2';


GRANT ALL PRIVILEGES ON budget_app.* TO 'sofayankovich0106'@'localhost';
GRANT ALL PRIVILEGES ON budget_app.* TO 'sliusarenko.tanya'@'localhost';
GRANT ALL PRIVILEGES ON budget_app.* TO 'ashkyl97'@'localhost';

USE budget_app;
CREATE TABLE group_info (
    group_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    group_name VARCHAR(255) NOT NULL 
);
CREATE TABLE user (
    username VARCHAR(255),
    user_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    group_id INT,
    group_status ENUM('owner', 'member'),
    CONSTRAINT fk_group_id_user FOREIGN KEY (group_id) REFERENCES group_info(group_id)
);

CREATE TABLE budget (
    budget_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    group_id INT NOT NULL,
	budget_name VARCHAR(255) NOT NULL,
    total_budget INT NOT NULL,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_group_id_budget FOREIGN KEY (group_id) REFERENCES group_info(group_id)
);
CREATE TABLE category (
    category_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(255) NOT NULL
);
CREATE TABLE expense (
    expense_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    budget_id INT NOT NULL,
    description VARCHAR(255) NOT NULL,
    price DECIMAL NOT NULL,
    amount INT,
	expense_type ENUM('planned', 'current') NOT NULL,
    category_id INT NOT NULL, 
    user_id INT NOT NULL,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_budget_id_expense FOREIGN KEY (budget_id) REFERENCES budget(budget_id),
    CONSTRAINT fk_category_id_expense FOREIGN KEY (category_id) REFERENCES category(category_id),
    CONSTRAINT fk_user_id_expense FOREIGN KEY (user_id) REFERENCES user(user_id)
);
CREATE TABLE shopping_list (
    list_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    group_id INT NOT NULL,
    list_name VARCHAR(255) NOT NULL,
    balance FLOAT NOT NULL,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_group_id_list FOREIGN KEY (group_id) REFERENCES group_info(group_id)
);
CREATE TABLE item_blueprint (
    item_blp_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description VARCHAR(255),
    group_id INT NOT NULL,
    CONSTRAINT fk_group_id_item_blp FOREIGN KEY (group_id) REFERENCES group_info(group_id)
);
CREATE TABLE item (
    item_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    item_blp_id INT NOT NULL,
    add_info VARCHAR(255),
    price DECIMAL NOT NULL,
    creator_id INT NOT NULL,
    list_id INT NOT NULL,
    CONSTRAINT fk_item_blp_id_item FOREIGN KEY (item_blp_id) REFERENCES item_blueprint(item_blp_id),
    CONSTRAINT fk_user_id_item FOREIGN KEY (creator_id) REFERENCES user(user_id),
    CONSTRAINT fk_list_id_item FOREIGN KEY (list_id) REFERENCES shopping_list(list_id)
);
CREATE TABLE notification (
    notification_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    message VARCHAR(255) NOT NULL,
    sent_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_user_id_notif FOREIGN KEY (user_id) REFERENCES user(user_id)
);
CREATE TABLE report (
    report_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	group_id INT NOT NULL,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    report_data JSON NoT NULL,
    CONSTRAINT fk_group_id_report FOREIGN KEY (group_id) REFERENCES group_info(group_id)
);
INSERT INTO group_info (group_name) VALUES ('personal');
INSERT INTO user (email, password, username, group_id, group_status) VALUES ('sofayankovich0106@gmail.com', 'admin123', 'Sofiiaaa', "1","owner");

INSERT INTO category (category_name) VALUES ('Food');
INSERT INTO category (category_name) VALUES ('Clothes');
INSERT INTO category (category_name) VALUES ('Electronics');
INSERT INTO budget (group_id, total_budget, budget_name) VALUES ('1', '20000', 'Sofia`s');
INSERT INTO expense (budget_id, price, description, expense_type, category_id, user_id) VALUES (1, '200', 'Shopping at Silpo', 'current', '1', '1');
INSERT INTO expense (budget_id, price, description, expense_type, category_id, user_id) VALUES (1, '8000', 'New phone', 'planned', '3', '1');
INSERT INTO shopping_list (group_id, list_name, balance, created_date, updated_date) VALUES (1, 'Mall trip on Saturday', 1000, '2024-11-20', '2024-11-20');
INSERT INTO shopping_list (group_id, list_name, balance, created_date, updated_date) VALUES (1, 'Mall trip on Friday', 1000, '2024-11-19', '2024-11-20');
INSERT INTO item_blueprint (name, description, group_id) VALUES ('Netflix subscription', 'Monthly pay for family Netflix', 1);
INSERT INTO item (item_blp_id, add_info, price, creator_id, list_id) VALUES (1, 'Pay for Netflix in October', 400, 1, 1);

-- for uploading changes to db use command mysql -uroot -p < init1.sql for password press enter
-- delete all previou db entities mysql -uroot -p -e"DROP DATABASE auth", mysql -uroot -p -e"DROP USER auth_user@localhost"
-- SELECT user, host FROM mysql.user;
-- mysql> exit 