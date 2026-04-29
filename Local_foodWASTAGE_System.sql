DROP DATABASE IF EXISTS food_donations;
CREATE DATABASE food_donations;
USE food_donations;

CREATE TABLE providers (
    provider_id INT PRIMARY KEY,
    name VARCHAR(255),
    provider_type VARCHAR(100),
    address VARCHAR(255),
    city VARCHAR(100),
    contact VARCHAR(100)
);

CREATE TABLE receivers (
    receiver_id INT PRIMARY KEY,
    name VARCHAR(255),
    receiver_type VARCHAR(100),
	city VARCHAR(100),
    contact VARCHAR(100)
);

CREATE TABLE food_listings (
    food_id INT PRIMARY KEY,
    food_name VARCHAR(255),
    quantity INT,
    expiry_date DATE,
    provider_id INT,
    provider_type VARCHAR(255),
    location VARCHAR(255),
    food_type VARCHAR(100),
    meal_type VARCHAR(100),
    FOREIGN KEY (provider_id) REFERENCES providers(provider_id)
);

CREATE TABLE claims (
    claim_id INT PRIMARY KEY,
    food_id INT,
    receiver_id INT,
    status VARCHAR(50),
    timestamp DATETIME,
    FOREIGN KEY (food_id) REFERENCES food_listings(food_id),
    FOREIGN KEY (receiver_id) REFERENCES receivers(receiver_id)
);

LOAD DATA INFILE "C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/providers_clean.csv"
INTO TABLE providers
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(provider_id, name, provider_type, address, city, contact);

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/receivers_clean.csv'
INTO TABLE receivers
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(receiver_id, name, receiver_type, city, contact);

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/food_listings_clean.csv'
INTO TABLE food_listings
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(food_id, food_name, quantity, expiry_date, provider_id, provider_type, location, food_type, meal_type);

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/claims_clean.csv'
INTO TABLE claims
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(claim_id, food_id, receiver_id, status, timestamp);

SELECT * FROM providers LIMIT 10;
SELECT * FROM receivers LIMIT 10;
SELECT * FROM food_listings LIMIT 10;
SELECT * FROM claims LIMIT 10;    
