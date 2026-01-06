import os
import oracledb

# Configuration for Oracle DB
# In a real shared VPC setup, the DB_HOST would be the private IP of the Oracle instance
# reachable from this service project.
DB_USER = os.getenv("DB_USER", "admin")
DB_PASSWORD = os.getenv("DB_PASSWORD", "Welcome12345")
DB_DSN = os.getenv("DB_DSN", "(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=10.0.1.50)(PORT=1521))(CONNECT_DATA=(SERVER=DEDICATED)(SERVICE_NAME=pdb1)))")

def get_db_connection():
    """
    Establishes a connection to the Oracle Database.
    Note: For Autonomous Database, you often use a Wallet (mtls).
    Here we simulate a standard connection or wallet-less connection.
    """
    try:
        # In a real Autonomous DB scenario, you might pass config_dir and wallet_location
        # connection = oracledb.connect(user=DB_USER, password=DB_PASSWORD, dsn=DB_DSN, wallet_location="/app/wallet")

        # For this demo code, we'll assume a connection can be made, or we'll mock it if running without actual DB.
        # This function returns a connection object.
        print(f"Connecting to Oracle DB at {DB_DSN}...")
        connection = oracledb.connect(user=DB_USER, password=DB_PASSWORD, dsn=DB_DSN, thin=True)
        return connection
    except Exception as e:
        print(f"Error connecting to Oracle DB: {e}")
        return None

# Mocking the connection for the purpose of the demo code structure,
# since we don't have a live Oracle DB to connect to in this sandbox.
class MockConnection:
    def cursor(self):
        return MockCursor()
    def close(self):
        pass

class MockCursor:
    def execute(self, sql, params=None):
        print(f"Executing SQL: {sql} | Params: {params}")

    def fetchall(self):
        # Return dummy data matching the supermarket schema
        return [
            (1, "Blue Running Shoes", "Boys", 7, "Blue", 45.99, "https://storage.googleapis.com/demo-retail-bucket/shoe_blue_7.jpg"),
            (2, "Red Sneakers", "Boys", 7, "Red", 39.99, "https://storage.googleapis.com/demo-retail-bucket/shoe_red_7.jpg"),
            (3, "Blue Sport Shoes", "Boys", 7, "Blue", 55.00, "https://storage.googleapis.com/demo-retail-bucket/shoe_blue_sport.jpg"),
        ]

    def close(self):
        pass
