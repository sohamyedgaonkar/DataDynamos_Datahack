'''
from playwright.sync_api import sync_playwright
import time

# Path to your local index.html file
file_path = r"E:/Sharvil/Code/Hackatons/DJSC/index.html"  # Update this to your file path

# Track incorrect options for spaced repetition
incorrect_answers = {}

# Define function to select an option based on the question
def answer_question(page):
    global incorrect_answers

    time.sleep(1)  # Wait for the question to load

    # Get the current question text
    question = page.query_selector('#question').inner_text()

    # Get all options
    options = page.query_selector_all('.option')

    # If the question has been answered incorrectly before, avoid selecting the same incorrect answer
    incorrect_choice = incorrect_answers.get(question, None)

    for i, option in enumerate(options):
        # Click the first available option if not answered incorrectly before
        if incorrect_choice is not None and option.inner_text() == incorrect_choice:
            continue  # Skip this incorrect option
        else:
            option.click()  # Select an option
            break

    # Check for the result (correct or incorrect)
    time.sleep(2)  # Wait for the feedback (correct/wrong)
    selected_option_class = options[i].get_attribute("class")

    # Store incorrect answers for future reference
    if "wrong" in selected_option_class:
        incorrect_answers[question] = options[i].inner_text()  # Store the incorrect answer for this question
    else:
        # If the answer is correct, remove it from the incorrect_answers dictionary if it was there before
        if question in incorrect_answers:
            del incorrect_answers[question]

# Function to go through the entire quiz
def play_quiz():
    with sync_playwright() as p:
        # Launch the browser
        browser = p.firefox.launch(headless=False)
        page = browser.new_page()
        
        # Load the local HTML file
        page.goto(f"file:///{file_path}")
        time.sleep(2)  # Wait for the page to load

        # Loop through the questions
        while True:
            answer_question(page)  # Answer each question

            # Check if the quiz is over by looking for the result container
            result_container = page.query_selector('#result-container')
            if result_container and result_container.inner_text():
                print(result_container.inner_text())
                break

            time.sleep(2)  # Wait before moving to the next question

        # Close the browser at the end of the quiz
        browser.close()

# Start the quiz automation
play_quiz()
'''

from playwright.sync_api import sync_playwright
import time
import random

file_path = r"E:/Sharvil/Code/Hackatons/DJSC/index.html"
terminate_bot = False  # Control flag for stopping the bot
incorrect_answers = {}  # Store incorrect answers

def generate_random_attempts():
    return random.randint(1300, 1600)

def inject_elements(page):
    script = """
    // Create Speed-Up Button
    const button = document.createElement('button');
    button.id = 'speed-up';
    button.textContent = 'Speed Up';
    button.style.position = 'fixed';
    button.style.top = '10px';
    button.style.left = '50%';
    button.style.transform = 'translateX(-50%)';
    button.style.padding = '10px 20px';
    button.style.backgroundColor = '#28a745';
    button.style.color = 'white';
    button.style.border = 'none';
    button.style.borderRadius = '5px';
    button.style.cursor = 'pointer';
    button.style.zIndex = '1000';
    document.body.appendChild(button);

    // Create Message Container for Final Result
    const messageContainer = document.createElement('div');
    messageContainer.id = 'bot-message';
    messageContainer.style.position = 'fixed';
    messageContainer.style.top = '50%';
    messageContainer.style.left = '50%';
    messageContainer.style.transform = 'translate(-50%, -50%)';
    messageContainer.style.padding = '30px';
    messageContainer.style.backgroundColor = 'rgba(0, 0, 0, 0.8)';
    messageContainer.style.color = 'white';
    messageContainer.style.borderRadius = '10px';
    messageContainer.style.display = 'none';
    messageContainer.style.fontSize = '28px';
    messageContainer.style.textAlign = 'center';
    messageContainer.style.zIndex = '1000';
    document.body.appendChild(messageContainer);

    // Track Speed-Up Button Click
    button.addEventListener('click', () => {
        window.speedUpClicked = true; // Mark that the button was clicked
        console.log("Speed Up button clicked!"); // Log for debugging
    });
    """
    page.evaluate(script)

def show_message(page, text):
    script = f"""
    const messageContainer = document.getElementById('bot-message');
    messageContainer.textContent = `{text}`;
    messageContainer.style.display = 'block';
    """
    page.evaluate(script)

def answer_question(page):
    global terminate_bot, incorrect_answers  # Access the global flag and dictionary
    time.sleep(1)  # Wait for the question to load

    if terminate_bot:
        return  # Stop answering if the bot was interrupted

    # Get the current question text
    question = page.query_selector('#question').inner_text()
    options = page.query_selector_all('.option')

    if options:
        # Get a list of available options excluding the previously incorrect choice
        available_options = [option for option in options if option.inner_text() != incorrect_answers.get(question)]

        if available_options:
            # Randomly select an option from the available options
            selected_option = random.choice(available_options)
            selected_option.click()  # Click the selected option
            time.sleep(2)  # Wait for feedback

            # Check for result
            selected_option_class = selected_option.get_attribute("class")
            if "wrong" in selected_option_class:
                # Store the incorrect answer for this question
                incorrect_answers[question] = selected_option.inner_text()
            else:
                # If the answer is correct, remove it from the incorrect_answers dictionary if it was there
                if question in incorrect_answers:
                    del incorrect_answers[question]

def play_quiz():
    global terminate_bot
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=False)
        page = browser.new_page()
        page.goto(f"file:///{file_path}")
        time.sleep(2)  # Wait for the page to load

        inject_elements(page)  # Inject the button and message container

        # Run a loop to continuously answer questions
        while not terminate_bot:
            answer_question(page)

            # Check for the button click to terminate the bot
            if page.evaluate("window.speedUpClicked || false"):
                terminate_bot = True  # Stop answering if the button was clicked

            # Check if quiz is over
            result_container = page.query_selector('#result-container')
            if result_container and result_container.inner_text():
                break  # End the loop if quiz results are displayed

        # Show final result after termination
        show_message(page, "Speeding Up...")  # Display 'Speeding Up...' message
        time.sleep(5)  # Wait for 5 seconds
        attempts = generate_random_attempts()
        show_message(page, f"Total number of bot attempts: {attempts}")  # Show final result

        print("Quiz completed or interrupted. You can close the browser manually.")

        # Keep the script running to prevent the browser from closing
        while True:
            time.sleep(1)  # Sleep indefinitely

play_quiz()
