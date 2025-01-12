import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import mysql.connector
from datetime import date, datetime
from decimal import Decimal

# Database Configuration
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "password",
    "database": "food_delivery_db"
}

# Get a database connection
def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

# Custom JSON encoder to handle special data types
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (date, datetime)):
            return obj.isoformat()  # Convert to ISO 8601 string
        if isinstance(obj, Decimal):
            return float(obj)  # Convert Decimal to float
        return super().default(obj)

# Request Handler
class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            with get_db_connection() as conn:
                with conn.cursor(dictionary=True) as cursor:
                    if self.path == "/orders":
                        # Fetch all orders
                        cursor.execute("SELECT * FROM orders")
                        result = cursor.fetchall()
                    elif self.path.startswith("/order/"):
                        # Fetch details of a specific order
                        order_id = self.path.split("/")[-1]
                        cursor.execute("SELECT * FROM orders WHERE OrderID = %s", (order_id,))
                        result = cursor.fetchone()
                    elif self.path == "/available_agents":
                        # Fetch available delivery agents
                        cursor.execute("SELECT * FROM delivery_agents WHERE Status = 'Available'")
                        result = cursor.fetchall()
                    else:
                        self.send_error(404, "Invalid endpoint")
                        return

            # Respond with the query result
            response_body = json.dumps(result, cls=CustomJSONEncoder)
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(response_body.encode())
        except Exception as e:
            self.send_error(500, f"Server error: {str(e)}")

    def do_POST(self):
        try:
            # Read and parse the request body
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))

            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    if self.path == "/assign_agent":
                        # Assign a delivery agent to an order
                        cursor.execute("""
                            SELECT AgentID FROM delivery_agents 
                            WHERE Status = 'Available' LIMIT 1
                        """)
                        agent = cursor.fetchone()

                        if agent:
                            agent_id = agent["AgentID"]
                            cursor.execute("""
                                UPDATE orders SET AgentID = %s, OrderStatus = 'Assigned'
                                WHERE OrderID = %s
                            """, (agent_id, data["OrderID"]))
                            cursor.execute("""
                                UPDATE delivery_agents SET Status = 'Busy'
                                WHERE AgentID = %s
                            """, (agent_id,))
                            conn.commit()

                            response = {"message": "Agent assigned successfully", "AgentID": agent_id}
                        else:
                            response = {"message": "No available agents"}
                    elif self.path == "/update_status":
                        # Update order status
                        cursor.execute("""
                            UPDATE orders SET OrderStatus = %s
                            WHERE OrderID = %s
                        """, (data["OrderStatus"], data["OrderID"]))
                        conn.commit()

                        response = {"message": "Order status updated successfully"}
                    else:
                        self.send_error(404, "Invalid endpoint")
                        return

            # Respond with success
            self.send_response(201)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
        except Exception as e:
            self.send_error(500, f"Server error: {str(e)}")

# Run the HTTP server
def run(server_class=HTTPServer, handler_class=RequestHandler, port=8080):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Server started on port {port}")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
