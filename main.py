import time
import sql_command
import pyperclip
import threading


VERSION = '0.6'
terminate_thread = False  # Flag to control thread termination
saved_id = -1
clipboard_thread = None


def clipboard_start_thread():
    global clipboard_thread
    clipboard_thread = threading.Thread(target=clipboard_listener)
    clipboard_thread.start()


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
    global terminate_thread, clipboard_thread, saved_id, next_id  # Access the flag to control the thread
    print("I'll start listening to your clipboard press. Press 'Y' when adding to the tweets database.")
    response = ""
    clipboard_start_thread()  # Start the clipboard listener thread
    while response.strip().lower() != 'y':
        # Adding to database
        response = input("Press Ctrl+C to exit or [Y]: ")
        if response.strip().lower() == 'y':
            terminate_thread = True  # Set the flag to end the clipboard_listener thread
            clipboard_thread.join()  # Wait for the thread to terminate
            clipboard_text = pyperclip.paste()

            if saved_id != -1:
                parent_id_prompt = (f"Enter the parent tweet id, or press [Enter] to use saved id ({saved_id}), "
                                    f"(Y* if use, N if use none) : ")
            else:
                parent_id_prompt = "Enter the parent tweet id, or press [Enter] if nothing: "

            parent_id = input(parent_id_prompt)

            if parent_id.strip() == "" and saved_id != -1:
                parent_id = saved_id
            elif parent_id.strip() != "":
                parent_id = int(parent_id)
            elif parent_id.strip() != "n":
                parent_id = -1
                saved_id = -1
            else:
                parent_id = -1
                saved_id = -1

            sql_command.write_database(next_id, clipboard_text, parent_id)

            response_inside = input(f"Do you want to save this tweet id ({next_id})? For a tweet thread [Y/N*]")
            if response_inside.strip().lower() == 'y':
                saved_id = next_id
            next_id = next_id + 1
            print(f"Tweet added to DB. [{clipboard_text[:14]}...]")
    terminate_thread = False  # Reset the flag for the next usage


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    next_id = sql_command.get_last_id() + 1
    print("Tweets listener " + VERSION)
    print("Next tweet id:", next_id)
    while True:
        print(f"Saved id: {'None' if saved_id == -1 else saved_id}")
        check_clipboard()
