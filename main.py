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

    # clipboard_thread = threading.Thread(target=clipboard_listener)
    # clipboard_thread.start()
    #
    # check_clipboard()

    eight_data_entries = [
    (9, datetime(2023, 7, 12), -1, "Discover the power of agreeableness: be liked without being a pushover. Balance kindness and assertiveness. Show politeness and ruthlessness. Charm through enthusiasm. Take responsibility, be authentic, and make a positive change. Embrace agreeableness, not people-pleasing."),
    (10, datetime(2023, 7, 12), -1, "In wars, good versus bad is a naïve oversimplification. Investigate, understand complexities. Educate, challenge preconceptions. Embrace truth for impact. Engage in honest dialogue, be the catalyst for change. Step up, make a difference. Are you ready?"),
    (11, datetime(2023, 7, 12), -1, "Small talk: mundane but impactful. It builds trust, forges connections. Let's explore casual conversation's hidden potential. Trust forms the foundation, change fuels a brighter future. Get ready for this journey."),
    (12, datetime(2023, 7, 12), 11, "Trust's icebreaker: Small talk breaks barriers, fosters comfort. Start with 'How are you?' or 'What's new?' to spark authentic connections and deeper conversations."),
    (13, datetime(2023, 7, 12), 11, "Business customer engagement: Engaging unhappy customers with 'How are you?' risks negative outcomes. Instead, ask, 'What can I do to make your day easier?' to show empathy, solve problems, and foster trust for positive resolutions."),
    (14, datetime(2023, 7, 12), 11, "Emotional Intimacy: Meaningful conversations build trust and deep connections. Sharing personal experiences, dreams, and fears fosters vulnerability, strengthening bonds and creating a safe space for support and understanding."),
    (15, datetime(2023, 7, 12), 11, "Embrace the art of fluidity, adaptability, and connection. Dare to initiate those seemingly small conversations that can make a significant impact."),
    (16, datetime(2023, 7, 17), -1, "When you think about a recent conversation, do you remember the words or the feelings they brought up? Emotions stay with us more than exact words. Use this to your advantage: focus on making others feel great. You'll leave a positive, lasting impression."),
    (17, datetime(2023, 8, 24), -1, "Imagine this: When a girl and a boy talk, only a small 10% of what she really means comes out as words. But surprise! The big 90% is in how she acts and looks, not what she says. So, put aside texting and online chats. Instead, go meet face-to-face for real connections."),
    (18, datetime(2023, 8, 27), -1, "Women communicate in two modes: reality and wishes. They discuss things as they are or express how they'd prefer things to be. When unsure, assume the latter. It's like decoding their desires from their words."),
    (19, datetime(2023, 8, 28), -1, "Enhance your flirting: subtle kino. Hand grazes to waist support, these gestures work wonders. Start gently, respect boundaries. Touch deepens bonds, comfort. No touch may indicate obstacles. Embrace touch to build connections."),
    (20, datetime(2023, 9, 4), -1,
     "Know the people you’re dealing with: they may seek adventure, attention, or romance. Recognize these desires to reveal their hidden attractions. See beyond the surface; a carefree individual might secretly desire structure, while a minimalist might quietly wish for abundance."),
    (21, datetime(2023, 9, 13), -1,
     "Harness the strength within you and the power of your actions. Courage! In a world where the line between the human and divine may blur, trust the Spirit and disregard what people think."),
    (22, datetime(2023, 9, 15), -1,
     "We should assess our relationships critically. A subtle, ongoing influence can lead to our downfall. While it works for celebrities rekindling romances, it may not apply in real life. If you did everything right before the breakup, the other person must have been no good."),
    (23, datetime(2023, 9, 25), -1,
     "Have you ever thought about the true cost of constant phone interruptions? It's possible that you could miss out on meaningful connections with your family and friends. There's a real price we pay for not mastering our phone distractions."),
    (24, datetime(2023, 10, 1), -1,
     "In a world full of challenges and surprises, there's a secret skill that can change the game: cunning. Life plays fair. When force isn't viable, wield your cunning, even resort to surrender as a tactic. The ultimate goal here is victory in war, not ego."),
    (25, datetime(2023, 10, 6), -1,
     "Stay Cool, Stay Wise. Don't let passion rule you; it can cloud judgment. Use a mediator in heated moments. Keep composure, avoid hasty actions. Reflection prevents future regrets. Choose wisdom over impulse."),
    (26, datetime(2023, 10, 15), -1,
     "A girl typically expects a call within 2 days. Call her after a week, and she will still accept the date if she's interested. Playfully tease her; challenge and coquetry represent another kind of emotional currency. Like a savings account, waiting leads to interest growth."),
    (27, datetime(2023, 10, 16), -1,
     "As Sun Tzu said, 'know the enemy and know yourself'; doing your homework brings success, much like understanding your date's soft spots before courting begins. Love is war. Build a strong Frame will give you the confidence you need for success, not only in love but also in war.")
    ]

    for entry in eight_data_entries:
        id, tweet_date, parent_id, text = entry
        write_database_complete(id, tweet_date, parent_id, text)