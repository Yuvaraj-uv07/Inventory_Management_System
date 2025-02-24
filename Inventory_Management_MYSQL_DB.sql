CREATE DATABASE Inventory;

USE Inventory;

CREATE TABLE Product (
    Product_ID VARCHAR(10) PRIMARY KEY,
    Product_Name VARCHAR(250) NOT NULL,
    Product_In INT DEFAULT 0,  -- Initial incoming stock
    Product_Out INT DEFAULT 0, -- Initial outgoing stock
    Product_Qty INT GENERATED ALWAYS AS (Product_In - Product_Out) STORED -- Auto-calculated quantity
);

-- Insert initial product details along with stock values
INSERT INTO Product (Product_ID, Product_Name, Product_In, Product_Out)  
VALUES  
('101', "Rice", 200, 0),  
('102', "Wheat Flour", 200, 0),  
('103', "Sugar", 200, 0),  
('104', "Salt", 200, 0),  
('105', "Cooking Oil", 200, 0),  
('106', "Milk", 200, 0),  
('107', "Tea Powder", 200, 0),  
('108', "Coffee Beans", 200, 0),  
('109', "Spices Pack", 200, 0),  
('110', "Bread", 200, 0);

SELECT * FROM Product;
-- drop table product;


CREATE TABLE Location (
    Location_ID VARCHAR(10) PRIMARY KEY,
    Location_Name VARCHAR(50) NOT NULL
);

INSERT INTO Location (Location_ID, Location_Name)  
VALUES  
('MW001', 'Central Warehouse'),  
('SW001', 'East Warehouse'),  
('SW002', 'West Warehouse'),  
('SW003', 'North Warehouse'),  
('SW004', 'South Warehouse');

SELECT * FROM location;
-- DROP TABLE Location;

CREATE TABLE Product_Movement (
    Movement_ID INT AUTO_INCREMENT PRIMARY KEY,
    From_Location VARCHAR(50) NOT NULL,
    To_Location VARCHAR(50) NOT NULL,
    Product_ID VARCHAR(10) NOT NULL,
    Quantity INT NOT NULL,  -- Quantity moved
    Timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Auto timestamp
);


SELECT * FROM Product_Movement;

-- DROP TABLE Product_Movement;

