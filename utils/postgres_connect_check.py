"""
Purpose:
    Demonstrates how to connect to a PostgreSQL database using psycopg2,
    execute a test query, and properly clean up resources.

What this code does:
    - Establishes a TCP connection to a PostgreSQL instance
    - Executes a simple query to verify connectivity
    - Retrieves and prints the PostgreSQL version
    - Closes cursor and connection to prevent resource leaks

Why this matters:
    This pattern validates database connectivity and forms the foundation
    for building data pipelines, APIs, and microservices that interact
    with PostgreSQL-compatible databases.

Key Concepts:
    - psycopg2: PostgreSQL adapter (bridge) for Python
    - Connection: Network session to the database
    - Cursor: Interface for executing SQL commands
    - Resource cleanup: Prevents connection leaks

Security Note:
    - Do NOT hardcode credentials in production
    - Use environment variables or a secrets manager

Limitations:
    - Basic error handling only
    - No explicit transaction management
    - No connection pooling (not suitable for production)
"""
import os
from pathlib import Path
import psycopg2
from dotenv import load_dotenv

# Load environment variables from the .env file into Python's environment
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

# Ensure all required environment variables are set before attempting to connect
required_vars = ["DB_HOST", "DB_NAME", "DB_USER", "DB_PASSWORD"]

# This loop checks for the presence of each required environment variable. If any variable is
# missing, it raises a ValueError with a message indicating which variable is missing. This
# is a proactive way to catch configuration issues early, before attempting to connect to
# the database, which would result in a more cryptic error if the connection fails due to
# missing parameters.
for var in required_vars:
    if not os.getenv(var):
        raise ValueError(f"Missing required environment variable: {var}")

try:
    # Establish a TCP connection to PostgreSQL
    # The connection parameters are sourced from environment variables for security and flexibility.
    # The psycopg2.connect() function will attempt to connect to the database using the provided
    # parameters.
    # If the connection is successful, it returns a connection object that can be used to interact
    # with the database.
    # If the connection fails (e.g., due to incorrect credentials, network issues, or database
    # server problems), psycopg2 will raise an exception, which we catch and print as an error
    # message.
    # The connection parameters include:
    # - host: The hostname or IP address of the PostgreSQL server
    # - port: The port number on which the PostgreSQL server is listening (default is 5432)
    # - dbname: The name of the target database to connect to
    # - user: The username for authentication
    # - password: The password for authentication
    # The connection is established within a context manager (the 'with' statement), which ensures
    # that the connection is properly closed after the block of code is executed, even if an error
    # occurs.
    # Note: psycopg2.connect() will raise an exception if the connection fails
    with psycopg2.connect(
          host=os.getenv("DB_HOST"),
          port=int(os.getenv("DB_PORT", "5432")),
          dbname=os.getenv("DB_NAME"),
          user=os.getenv("DB_USER"),
          password=os.getenv("DB_PASSWORD")
      ) as conn:
        with conn.cursor() as cursor:
            cursor.execute('SELECT version();')
            print(cursor.fetchone())

except psycopg2.Error as e:
    # Catch PostgreSQL-specific database errors
    print(f"PostgreSQL error: {e}")
