# Inventory Management System

## Overview
This **Flask-based Inventory Management System** is designed to help businesses efficiently manage their inventory, track product movements, and maintain accurate stock levels. Built using **Flask** for the backend and **MySQL** for data storage, this system provides a structured and scalable approach to inventory management.

## Features
- **Product Management:**
  - Add, edit, delete, and search for products.
  - Maintain stock levels with `Product_In` and `Product_Out` tracking.

- **Location Management:**
  - Manage different storage locations.
  - Add, edit, delete, and search for locations.

- **Product Movements:**
  - Track stock movements between locations.
  - Ensure accurate inventory updates when transferring products.
  - Prevent stock depletion errors by verifying available quantity before transfers.

- **Database Integration:**
  - Uses **MySQL** for structured data storage and retrieval.
  - Supports relational data consistency across products, locations, and movements.

## How It Works
- Users can **add new products** with unique IDs and names.
- The **inventory is updated automatically** when stock is moved between locations.
- **Movement records** track each transaction to maintain accountability.
- The system ensures that `Product_In` remains unchanged when transferring stock, with only `Product_Out` being updated.
- A centralized warehouse (`Central Warehouse`) serves as the main stock hub, preventing unnecessary data duplication.

## Future Improvements
- Implement **user authentication** with role-based access control.
- Develop a **detailed reporting dashboard** for inventory analysis.
- Improve UI with **Bootstrap** or a modern frontend framework for better user experience.
- Implement an **API** for seamless integration with other business applications.

## End ##