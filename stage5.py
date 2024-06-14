import speech_recognition as sr
import sounddevice as sd
import pygame
import sys
import random

# Function to find the index of a specific audio device
def find_device_index(device_name):
    devices = sd.query_devices()
    for i, device in enumerate(devices):
        if device["name"] == device_name:
            return i
    return None

# Function to recognize speech
def speech_to_text(device_index):
    recognizer = sr.Recognizer()
    with sr.Microphone(device_index=device_index) as source:
        print("Say the word...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        audio = recognizer.listen(source)  # Listen for audio input

    try:
        # Use Google Web Speech API to convert audio to text
        text = recognizer.recognize_google(audio)
        return text.lower()
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    return ""

# Function to read words from a file into a list
def read_word_list(filename):
    with open(filename, 'r') as file:
        word_list = [line.strip() for line in file]
    return word_list

# Function to choose a new random word
def choose_new_word():
    return random.choice(word_list)

# Function to prepare the game state
def prepare_game():
    global word_to_pronounce, word_text, word_text_rect, repeat_text, repeat_text_rect, back_button, back_button_rect

    # Choose the initial word
    word_to_pronounce = choose_new_word()

    # Render the word and notifications
    word_text = font.render("Word: " + word_to_pronounce, True, (255, 255, 255))
    word_text_rect = word_text.get_rect(center=(screen_width // 2, screen_height // 2))
    repeat_text = font.render("Please repeat the word...", True, (255, 0, 0))
    repeat_text_rect = repeat_text.get_rect(center=(screen_width // 2, screen_height // 2 + 100))

    # Create a "Back" button
    back_button = font.render("Back", True, (255, 255, 255))
    back_button_rect = back_button.get_rect(center=(screen_width // 2, screen_height - 50))

# Function for the main game loop
def stage5_game():
    global game_over
    game_over = False  # Initialize game_over state

    # Initialize Pygame within this function to avoid reinitializing in main menu
    pygame.init()
    pygame.mixer.init()

    # Get screen dimensions
    global screen_width, screen_height
    screen_width = pygame.display.Info().current_w
    screen_height = pygame.display.Info().current_h

    # Set up font for text rendering
    global font
    font = pygame.font.SysFont("Arial", 48)

    # Set up Pygame window
    global screen
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
    pygame.display.set_caption("Word Pronunciation Game")

    # Load the background image
    background_image = pygame.image.load('stage5.jpg').convert()
    background_image = pygame.transform.scale(background_image, (screen_width, screen_height))  # Scale the image to fit the screen

    # Set up Pygame clock
    global clock, FPS
    clock = pygame.time.Clock()
    FPS = 60  # Adjust the frame rate as needed, e.g., 60 frames per second

    # Read word list from file
    global word_list
    word_list = read_word_list("wordlist5.txt")

    prepare_game()

    while True:
        clock.tick(FPS)  # Limit the loop to a maximum of FPS iterations per second

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if back_button_rect.collidepoint(pos):
                    return  # Exit the game and return to the menu

        # Find the index of the microphone
        device_name = "Microphone Array (Realtek(R) Au"
        device_index = find_device_index(device_name)

        # Recognize speech
        recognized_text = speech_to_text(device_index)

        # Display the background image
        screen.blit(background_image, (0, 0))  # Draw the background image

        # Display the word and initial notification
        screen.blit(word_text, word_text_rect)  # Display the word
        screen.blit(repeat_text, repeat_text_rect)  # Display the initial notification
        screen.blit(back_button, back_button_rect)  # Display the back button

        # Check if the recognized text matches the word
        if recognized_text.strip() == word_to_pronounce:
            result_text = font.render("You said the word correctly!", True, (0, 255, 0))
            result_text_rect = result_text.get_rect(center=(screen_width // 2, screen_height // 2 + 200))
            screen.blit(result_text, result_text_rect)
            pygame.display.update()
            # pygame.time.delay(3000)  # Delay for 3 seconds

            # Choose a new random word
            prepare_game()

        # If the recognized text doesn't match the word, display a message and repeat
        elif recognized_text.strip():
            wrong_text = font.render("You are saying it wrong, try again...", True, (255, 0, 0))
            wrong_text_rect = wrong_text.get_rect(center=(screen_width // 2, screen_height // 2 + 200))
            screen.blit(wrong_text, wrong_text_rect)
            pygame.display.update()
            # pygame.time.delay(3000)  # Delay for 3 seconds

        pygame.display.update()

# Ensure the game only runs when this file is executed directly
if __name__ == "__main__":
    stage5_game()
