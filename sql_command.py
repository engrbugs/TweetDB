import oracledb
from ini_io import SecretsManager  # Importing the SecretsManager class from secrets_manager.py
import os
from datetime import datetime


# Function for connecting to the Oracle Autonomous Data Warehouse database with a client wallet
def connect_database():
    secrets_manager = SecretsManager('secret.ini')

    # Retrieve the secrets
    secrets = secrets_manager.get_secrets()

    # Establish the connection using the retrieved secrets
    connection = oracledb.connect(
        user=secrets['user'],
        password=secrets['password'],
        dsn=secrets['dsn'],
        config_dir=secrets['config_dir'],
        wallet_location=secrets['wallet_location'],
        wallet_password=secrets['wallet_password']
    )
    return connection


def write_database(id, text, parent_id=-1):
    # Create a cursor to interact with the database
    connection = connect_database()
    cursor = connection.cursor()

    # Now you can use the 'connection' and 'cursor' for database operations
    # print("Database version:", connection.version)

    # get date today
    current_date = datetime.now().date()

    # Execute the SQL statement with parameters
    cursor.execute("INSERT INTO Tweets_Table (id, tweet_date, parent_tweet_id, text) VALUES (:1, :2, :3, :4)",
                   [id, current_date, parent_id, text])
    connection.commit()  # Commit the changes

    # Displaying confirmation
    # print("Tweet added to DB.")  too many printlines to show

    # Don't forget to close the cursor and connection when you're done
    cursor.close()
    connection.close()


# Function get last id value from database:
def get_last_id():
    connection = connect_database()

    cursor = connection.cursor()

    cursor.execute("SELECT MAX(id) FROM Tweets_Table")
    last_id = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    # Check if last_id is None (when the table is empty) and set it to -1
    return last_id if last_id is not None else -1

