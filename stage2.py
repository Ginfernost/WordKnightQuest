import pygame
import random
import time

class Button:
    def __init__(self, text, font, text_color, button_color, x, y, width, height):
        self.text = text
        self.font = font
        self.text_color = text_color
        self.button_color = button_color
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, screen):
        pygame.draw.rect(screen, self.button_color, (self.x, self.y, self.width, self.height))
        draw_text(self.text, self.font, self.text_color, self.x + self.width // 2, self.y + self.height // 2)

    def is_clicked(self, pos):
        x, y = pos
        return self.x < x < self.x + self.width and self.y < y < self.y + self.height

class InputBox:
    def __init__(self, x, y, font, max_length):
        self.x = x
        self.y = y
        self.color = BLACK
        self.text = ''
        self.font = font
        self.txt_surface = self.font.render(self.text, True, self.color)
        self.active = True
        self.max_length = max_length

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    answer = self.text
                    self.text = ''
                    return answer
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif len(self.text) < self.max_length:
                    self.text += event.unicode
                self.txt_surface = self.font.render(self.text, True, self.color)
        return None

    def draw(self, screen):
        input_text = "Answer: " + self.text + "_" * (self.max_length - len(self.text))
        txt_surface = self.font.render(input_text, True, self.color)
        screen.blit(txt_surface, (self.x, self.y))

# Initialize Pygame
pygame.init()
pygame.display.set_caption("Stage 2: Unscramble the Word")
screen_info = pygame.display.Info()
WIDTH, HEIGHT = screen_info.current_w, screen_info.current_h
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)  # New color for hint text
FONT_SIZE = 40
WORD_FONT_SIZE = 30
WORDLIST_FILENAME = "wordlist2.txt"
NUM_DISTRACTORS = 3
COUNTDOWN = 30

# Load word list from file
def load_word_list(filename):
    word_list = []
    with open(filename, 'r') as file:
        for line in file:
            word, definition = line.strip().split(", ", 1)  # Split only at the first occurrence of ", "
            word_list.append((word, definition))
    return word_list

# Function to select a random word from the word list
def select_word(word_list):
    return random.choice(word_list)

# Function to generate distractor letters
def generate_distractors(word, num_distractors):
    all_letters = 'abcdefghijklmnopqrstuvwxyz'  # All lowercase alphabets
    letters = random.sample(all_letters, 10)  # Select 10 random alphabets
    distractors = []
    for _ in range(num_distractors):
        distractor = random.choice(letters)
        while distractor in distractors or distractor in word:  # Avoid using the same letter or letters from the word
            distractor = random.choice(letters)
        distractors.append(distractor)
    return distractors

# Function to display the word with distractors
def display_word(word, distractors):
    mixed_word = list(word)
    for distractor in distractors:
        index = random.randint(0, len(mixed_word))
        mixed_word.insert(index, distractor)
    return ''.join(mixed_word)

# Function to draw text on the screen with an outline
def draw_text(text, font, color, x, y, outline_color=None):
    # Render the outline text
    outline_surface = font.render(text, True, outline_color if outline_color else BLACK)
    outline_rect = outline_surface.get_rect(center=(x, y))
    screen.blit(outline_surface, outline_rect.move(2, 2))  # Offset the outline text slightly

    # Render the actual text
    surface = font.render(text, True, color)
    text_rect = surface.get_rect(center=(x, y))
    screen.blit(surface, text_rect)

# Function to display end screen when time runs out
def time_up_screen(score, font):
    screen.fill(WHITE)
    draw_text(f"Time's up! You answered {score} questions correctly.", font, BLACK, WIDTH / 2, HEIGHT / 2)
    back_button = Button("Back", font, WHITE, BLACK, 20, 20, 100, 50)
    back_button.draw(screen)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.is_clicked(pygame.mouse.get_pos()):
                    return  # Return to previous stage

# Function to play Stage 2
def play_stage2(word_list, num_distractors, font, background_image):
    back_button = Button("Back", font, WHITE, BLACK, 20, 20, 100, 50)
    hint_button = Button("Hint", font, WHITE, BLACK, 140, 20, 100, 50)  # Add hint button
    input_box = InputBox(WIDTH // 2 - 100, HEIGHT // 2 + 50, font, 0)
    correct_answers = 0
    hint_text = None  # Initialize hint text variable
    answer = None  # Initialize answer variable
    start_time = time.time()

    while True:
        word, definition = select_word(word_list)
        hint_limit = len(word) // 2  # Set hint limit to half of the word length
        distractors = generate_distractors(word, num_distractors)
        mixed_word = display_word(word, distractors)
        input_box.max_length = len(word)
        hint_text = None  # Clear hint text from previous question

        while True:
            screen.blit(background_image, (0, 0))  # Draw the background image
            draw_text("Unscramble the word:", font, BLACK, WIDTH / 2, HEIGHT / 2 - 100, outline_color=WHITE)
            draw_text(mixed_word, font, BLACK, WIDTH / 2, HEIGHT / 2 - 30, outline_color=WHITE)
            draw_text("Definition: " + definition, font, BLACK, WIDTH / 2, HEIGHT / 2 + 100, outline_color=WHITE)

            back_button.draw(screen)
            hint_button.draw(screen)  # Draw hint button
            input_box.draw(screen)

            # Correct text position
            correct_text_y = HEIGHT / 2 + 250
            # If hint text is not None, display it in red
            if hint_text:
                draw_text("Hint: " + hint_text, font, RED, WIDTH / 2, correct_text_y + 50, outline_color=WHITE)

            # Timer
            elapsed_time = time.time() - start_time
            remaining_time = COUNTDOWN - elapsed_time
            if remaining_time <= 0:
                time_up_screen(correct_answers, font)
                return

            # Draw remaining time
            draw_text("Time remaining: " + str(round(remaining_time)) + " seconds", font, BLACK, WIDTH / 2, HEIGHT / 2 + 200, outline_color=WHITE)

            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back_button.is_clicked(pygame.mouse.get_pos()):
                        return  # Return to previous stage
                    if hint_button.is_clicked(pygame.mouse.get_pos()):  # Check if hint button is clicked
                        hint_text = word[:hint_limit]  # Get the hint text (first half of the word)

                answer = input_box.handle_event(event)
                if answer is not None:
                    if answer.lower() == word.lower():
                        draw_text("Correct!", font, BLACK, WIDTH / 2, correct_text_y, outline_color=WHITE)
                        pygame.display.update()
                        pygame.time.wait(1000)
                        correct_answers += 1
                        break  # Break out of the inner loop to pick a new word
                    else:
                        draw_text("Incorrect!", font, BLACK, WIDTH / 2, correct_text_y, outline_color=WHITE)
                        pygame.display.update()
                        pygame.time.wait(1000)
                        input_box.text = ''  # Clear the input
                        input_box.txt_surface = input_box.font.render(input_box.text, True, input_box.color)
            if answer is not None and answer.lower() == word.lower():
                hint_text = None  # Clear hint text when moving to the next word
                break  # Move to the next word

# Main function
def main():
    global screen
    # Set fullscreen mode
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    # Load word list
    word_list = load_word_list(WORDLIST_FILENAME)
    # Load font
    font = pygame.font.SysFont(None, FONT_SIZE)
    # Load background image
    background_image = pygame.image.load('stage2.jpg').convert()
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))  # Scale the image to fit the screen
    # Start Stage 2
    print("Welcome to Stage 2!")
    play_stage2(word_list, NUM_DISTRACTORS, font, background_image)

if __name__ == "__main__":
    main()
