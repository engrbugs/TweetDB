#Connecting to an Oracle Autonomous Database using the Python-OracleDB driver.
import time

import oracledb
import datetime  # Import the datetime module
from ini_io import SecretsManager  # Importing the SecretsManager class from secrets_manager.py


# Function for connecting to the Oracle Autonomous Data Warehouse database with a client wallet
def connect_database():
    # Initialize SecretsManager with the secret file path
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

    # Create a cursor to interact with the database
    cursor = connection.cursor()

    # Now you can use the 'connection' and 'cursor' for database operations
    print("Database version:", connection.version)

    # Inserting "Hello World" along with a correctly formatted date and handling the parent ID
    hello_world_text = "Hello World2"
    current_date = datetime.date(2023, 10, 13)  # Providing the date in the YYYY, MM, DD format
    parent_tweet_id = -1  # Default value if no parent ID provided

    # Execute the SQL statement with parameters
    cursor.execute("INSERT INTO Tweets_Table (tweet_date, parent_tweet_id, text) VALUES (:1, :2, :3)",
                   [current_date, parent_tweet_id, hello_world_text])
    connection.commit()  # Commit the changes

    # Displaying confirmation
    print("Inserted 'Hello World' along with a specified date and parent ID into Tweets_Table.")

    # Don't forget to close the cursor and connection when you're done
    cursor.close()
    connection.close()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    connect_database()
