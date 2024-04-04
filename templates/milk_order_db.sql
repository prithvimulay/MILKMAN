CREATE DATABASE milk_order_db;

USE milk_order_db;

CREATE TABLE orders (
         INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        phone VARCHAR(20) NOT NULL,
        customer_id VARCHAR(20) NOT NULL,
        address VARCHAR(200) NOT NULL,
        milk_type VARCHAR(50) NOT NULL,
        liters FLOAT NOT NULL
);

CREATE TABLE users(
    id INT NOT NULL AUTO_INCREMENT,
    name varchar(200) NULL,
    email VARCHAR(200) NULL,
    password VARCHAR(200) NULL,
    PRIMARY KEY (id)
);

CREATE TABLE subscribers (
         INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        phone VARCHAR(20) NOT NULL,
        customer_id VARCHAR(20) NOT NULL,
        milk_type VARCHAR(50) NOT NULL,
        liters INT NOT NULL
);
