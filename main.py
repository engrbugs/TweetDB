#Connecting to an Oracle Autonomous Database using the Python-OracleDB driver.
import time

import oracledb
from datetime import datetime
from ini_io import SecretsManager  # Importing the SecretsManager class from secrets_manager.py
import os

import pyperclip
import threading
import time


VERSION = '0.6'
terminate_thread = False  # Flag to control thread termination


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


def write_database(text, parent_id=-1):
    # Create a cursor to interact with the database
    connection = connect_database()
    cursor = connection.cursor()

    # Now you can use the 'connection' and 'cursor' for database operations
    # print("Database version:", connection.version)

    # get date today
    current_date = datetime.now().date()

    # Execute the SQL statement with parameters
    cursor.execute("INSERT INTO Tweets_Table (tweet_date, parent_tweet_id, text) VALUES (:1, :2, :3)",
                   [current_date, parent_id, text])
    connection.commit()  # Commit the changes

    # Displaying confirmation
    print("Inserted data along with a specified date and parent ID into Tweets_Table.")

    # Don't forget to close the cursor and connection when you're done
    cursor.close()
    connection.close()

# get last id value from database:

def get_last_id():
    connection = connect_database()

    cursor = connection.cursor()

    cursor.execute("SELECT MAX(id) FROM Tweets_Table")
    last_id = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    # Check if last_id is None (when the table is empty) and set it to -1
    return last_id if last_id is not None else -1


def clipboard_listener():
    recent_value = pyperclip.paste()
    global terminate_thread  # Access the flag to control the thread
    while not terminate_thread:  # Loop until the flag is set to True
        current_value = pyperclip.paste()
        if current_value != recent_value:
            recent_value = current_value
            print("\nClipboard content changed:\n", recent_value, "\n", end="Press Ctrl+C to exit or [Y]: ")
        time.sleep(1)  # Adjust the time interval for checking the clipboard


def check_clipboard():
    global terminate_thread  # Access the flag to control the thread
    print("I'll start listening to your clipboard press. Press 'Y' when adding to the tweets database.")
    response = ""
    while response.strip().lower() != 'y':
        response = input("Press Ctrl+C to exit or [Y]: ")
        if response.strip().lower() == 'y':
            terminate_thread = True  # Set the flag to end the clipboard_listener thread
            clipboard_thread.join()  # Wait for the thread to terminate
            clipboard_text = pyperclip.paste()
            parent_id = input("Enter the parent tweet id, press [Enter] if nothing: ")
            if parent_id:
                parent_id = int(parent_id)
                write_database(clipboard_text, parent_id)
            else:
                write_database(clipboard_text)
            response = input(f"Do you want to save this tweet id ({next_id})? [Y/N*]")
            if response.strip().lower() == 'y':
                pyperclip.copy(str(next_id))
            print("Tweet added to the database.")


def write_database_complete(id, tweet_date, parent_tweet_id, text):
    # Create a cursor to interact with the database
    connection = connect_database()
    cursor = connection.cursor()

    # Use the provided tweet_date directly, assuming it's already a datetime object
    formatted_date = tweet_date.date()

    # Execute the SQL statement with parameters
    cursor.execute("INSERT INTO Tweets_Table (id, tweet_date, parent_tweet_id, text) VALUES (:1, :2, :3, :4)",
                   [id, formatted_date, parent_tweet_id, text])
    connection.commit()  # Commit the changes

    # Display a confirmation message
    print("Inserted data into Tweets_Table.")

    # Don't forget to close the cursor and connection when you're done
    cursor.close()
    connection.close()



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    next_id = get_last_id() + 1
    print("Tweets listener " + VERSION)
    print("Next tweet id:", next_id)

    clipboard_thread = threading.Thread(target=clipboard_listener)
    clipboard_thread.start()
    check_clipboard()
