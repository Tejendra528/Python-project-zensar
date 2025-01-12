Food Delivery Management System using REST  API

Name:- Tejandrasing Chandrasing Patil
Email:- patiltejandrasing@gmail.com

Project Overview
This project is a RESTful API built using Python's http.server module and mysql.connector. The API provides functionality for managing orders and delivery agents in a food delivery management system. It supports various endpoints to fetch, assign, and update orders, along with querying available delivery agents.

Features:
GET /orders – Fetch all orders.
GET /order/{id} – Fetch details of a specific order by OrderID.
GET /available_agents – Fetch available delivery agents.
POST /assign_agent – Assign an available delivery agent to an order.
POST /update_status – Update the status of an order.
Requirements
Python 3.x
MySQL Database
Python Libraries:
mysql-connector-python
json
datetime
Installation and Setup
Step 1: Clone the Repository
bash
Copy code
git clone https://github.com/your-repo/food-delivery-api.git
cd food-delivery-api
Step 2: Install Required Libraries
bash
Copy code
pip install mysql-connector-python
Step 3: Set Up the Database
Create a database named food_delivery_db in MySQL.
Create the following tables:
sql
Copy code
CREATE TABLE orders (
    OrderID INT AUTO_INCREMENT PRIMARY KEY,
    CustomerName VARCHAR(100),
    Address VARCHAR(255),
    OrderStatus VARCHAR(50),
    AgentID INT NULL
);

CREATE TABLE delivery_agents (
    AgentID INT AUTO_INCREMENT PRIMARY KEY,
    AgentName VARCHAR(100),
    Status ENUM('Available', 'Busy') DEFAULT 'Available'
);
Step 4: Configure Database Connection
Update the DB_CONFIG dictionary in the Python code with your MySQL credentials:

python
Copy code
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "your_password",
    "database": "food_delivery_db"
}
Step 5: Run the Server
bash
Copy code
python server.py
The server will start on http://localhost:8080.

API Endpoints
GET /orders
Fetches all orders from the database.

Response Example:
json
Copy code
[
    {
        "OrderID": 1,
        "CustomerName": "John Doe",
        "Address": "123 Main St",
        "OrderStatus": "Pending",
        "AgentID": null
    },
    ...
]
GET /order/{id}
Fetches details of a specific order by OrderID.

Response Example:
json
Copy code
{
    "OrderID": 1,
    "CustomerName": "John Doe",
    "Address": "123 Main St",
    "OrderStatus": "Pending",
    "AgentID": null
}
GET /available_agents
Fetches all delivery agents with the status Available.

Response Example:
json
Copy code
[
    {
        "AgentID": 1,
        "AgentName": "Alice",
        "Status": "Available"
    }
]
POST /assign_agent
Assigns an available agent to an order.

Request Example:
json
Copy code
{
    "OrderID": 1
}
Response Example:
json
Copy code
{
    "message": "Agent assigned successfully",
    "AgentID": 1
}
POST /update_status
Updates the status of an existing order.

Request Example:
json
Copy code
{
    "OrderID": 1,
    "OrderStatus": "Delivered"
}
Response Example:
json
Copy code
{
    "message": "Order status updated successfully"
}
Error Handling
404 Not Found: Returned when an invalid endpoint is accessed.
500 Internal Server Error: Returned when there is a server-side error (e.g., database connection failure).
