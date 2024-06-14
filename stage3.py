import pygame
import random
import sys

# Define colors at the top so they can be used anywhere
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
OUTLINE_COLOR = (255, 255, 255)  # Outline color for the words

class Button:
    def __init__(self, text, font, text_color, button_color, x, y, width, height, action=None):
        self.text = text
        self.font = font
        self.text_color = text_color
        self.button_color = button_color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.action = action  # New attribute to hold the action

    def draw(self, screen):
        pygame.draw.rect(screen, self.button_color, (self.x, self.y, self.width, self.height))
        text_surface = render_text_with_outline(self.font, self.text, self.text_color, WHITE)
        text_rect = text_surface.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        screen.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.x < pos[0] < self.x + self.width and self.y < pos[1] < self.height

def load_word_list(filename):
    questions_answers = []
    definitions = {}
    with open(filename, 'r') as file:
        for line in file:
            if line.strip():  # Ignore empty lines
                answer, definition = line.strip().split(') ', 1)
                answer = answer[1:]  # Remove leading '('
                questions_answers.append((definition, answer))
                definitions[answer] = definition
    return questions_answers, definitions

def new_game_round(questions_answers):
    question, correct_answer = random.choice(questions_answers)
    distractors = [qa[1] for qa in random.sample(questions_answers, 3) if qa[1] != correct_answer]
    all_words = [correct_answer] + distractors
    random.shuffle(all_words)
    return question, correct_answer, all_words

def render_text_with_outline(font, text, text_color, outline_color):
    base = font.render(text, True, text_color).convert_alpha()
    outline = font.render(text, True, outline_color).convert_alpha()

    w = outline.get_width() + 2
    h = outline.get_height() + 2

    img = pygame.Surface((w, h), pygame.SRCALPHA)
    img.blit(outline, (0, 0))
    img.blit(outline, (2, 0))
    img.blit(outline, (0, 2))
    img.blit(outline, (2, 2))
    img.blit(base, (1, 1))

    return img

def stage3_game():
    pygame.init()

    # Fullscreen mode
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    WIDTH, HEIGHT = screen.get_size()
    pygame.display.set_caption("Word Completion Game")

    # Calculate font size and spacing based on screen size
    question_font_size = min(WIDTH // 20, HEIGHT // 12)
    word_font_size = min(WIDTH // 25, HEIGHT // 15)
    word_spacing = min(WIDTH // 25, HEIGHT // 15)

    # Fonts
    question_font = pygame.font.Font(None, question_font_size)
    word_font = pygame.font.Font(None, word_font_size)
    button_font = pygame.font.Font(None, 36)  # Font for the back button

    # Timer
    total_time = 30  # Total game time in seconds (changed for testing purposes)
    start_ticks = pygame.time.get_ticks()  # Start time

    questions_answers, definitions = load_word_list("wordlist3.txt")

    # Start the first game round
    question, correct_answer, all_words = new_game_round(questions_answers)

    # Initialize word positions based on the shuffled all_words list
    word_positions = [(0, 0)] * len(all_words)

    # Game state
    completed = False
    correct_answers_count = 0  # Counter for correct answers
    score = 100  # Starting score
    wrong_answer_chosen = False
    wrong_answer_time = 0
    wrong_answer_display_duration = 5  # Display the wrong answer notification for 2 seconds
    congrats_display_duration = 1000  # Display the congrats notification for 1 second

    # Create the back button
    back_button = Button("Back", button_font, WHITE, BLACK, 20, 20, 100, 50, action='back')

    # Load the background image
    background_image = pygame.image.load('stage3.jpg').convert()
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))  # Scale the image to fit the screen

    # Main game loop
    running = True
    while running:
        screen.blit(background_image, (0, 0))  # Draw the background image

        # Calculate the remaining time
        seconds = (pygame.time.get_ticks() - start_ticks) / 1000
        remaining_time = total_time - seconds

        if remaining_time <= 0:
            running = False  # End the game when time is up
            remaining_time = 0  # Ensure remaining time does not go negative

        # Split the question into two lines if it exceeds a certain length
        question_lines = []
        line = ""
        for word in question.split():
            if question_font.size(line + word)[0] > WIDTH:
                question_lines.append(line)
                line = word
            else:
                line += " " + word
        question_lines.append(line)

        # Display the question lines
        question_y = HEIGHT // 4
        for line in question_lines:
            question_surface = render_text_with_outline(question_font, line, BLACK, OUTLINE_COLOR)
            question_rect = question_surface.get_rect(center=(WIDTH // 2, question_y))
            screen.blit(question_surface, question_rect)
            question_y += question_surface.get_height()

        # Display the words to choose from
        word_surfaces = [render_text_with_outline(word_font, word, BLACK, OUTLINE_COLOR) for word in all_words]
        total_words_width = sum([surface.get_width() for surface in word_surfaces]) + (len(all_words) - 1) * word_spacing
        x_start = (WIDTH - total_words_width) // 2

        word_positions = []  # Reset word_positions list
        for i, word_surface in enumerate(word_surfaces):
            word_pos = (x_start, HEIGHT - 100)
            word_positions.append(word_pos)
            screen.blit(word_surface, word_pos)
            x_start += word_surface.get_width() + word_spacing

        # Display the timer
        timer_surface = render_text_with_outline(word_font, f"Time left: {int(remaining_time)}s", RED, OUTLINE_COLOR)
        screen.blit(timer_surface, ((WIDTH - timer_surface.get_width()) // 2, 20))

        # Draw the back button
        back_button.draw(screen)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.is_clicked(pygame.mouse.get_pos()):
                    return  # Return to previous stage

                for i, word in enumerate(all_words):
                    word_surface = word_font.render(word, True, BLACK)
                    word_rect = word_surface.get_rect(topleft=word_positions[i])
                    if word_rect.collidepoint(event.pos):
                        if word == correct_answer:
                            completed = True
                            correct_answers_count += 1  # Increment the counter for correct answers
                            question, correct_answer, all_words = new_game_round(questions_answers)  # Start a new game round
                            break
                        else:
                            # Move the selected word to the end of the list to simulate returning it to its original position
                            all_words.remove(word)
                            all_words.append(word)
                            random.shuffle(all_words)
                            wrong_answer_chosen = True
                            wrong_answer_time = pygame.time.get_ticks()
                            wrong_answer_definition = definitions.get(word, "No definition available.")
                        break

        # Display notifications
        if completed:
            congrats_surface = render_text_with_outline(word_font, "Congratulations! You answered correctly.", GREEN, OUTLINE_COLOR)
            congrats_rect = congrats_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(congrats_surface, congrats_rect)
            pygame.display.flip()
            pygame.time.wait(congrats_display_duration)  # Display the congratulations notification for 1 second
            completed = False  # Reset completion flag

        elif wrong_answer_chosen:
            current_time = pygame.time.get_ticks()
            if current_time - wrong_answer_time <= wrong_answer_display_duration * 1000:
                wrong_answer_surface = render_text_with_outline(word_font, f"Wrong answer!\n{wrong_answer_definition}", RED, OUTLINE_COLOR)
                wrong_answer_rect = wrong_answer_surface.get_rect(center=(WIDTH // 2, 100))
                screen.blit(wrong_answer_surface, wrong_answer_rect)
            else:
                wrong_answer_chosen = False

        pygame.display.flip()

    # Display the final score
    screen.fill(WHITE)
    final_score_surface = render_text_with_outline(word_font, f"Time's up! You answered {correct_answers_count} questions correctly.", BLACK, OUTLINE_COLOR)
    final_score_rect = final_score_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(final_score_surface, final_score_rect)

    # Create the back button for the final score screen
    back_button_end = Button("Back", button_font, WHITE, BLACK, 20, 20, 100, 50, action='back')
    back_button_end.draw(screen)
    pygame.display.flip()

    # Event handling for the final score screen
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button_end.is_clicked(event.pos):
                    pygame.quit()
                    return 'back'  # Return to previous stage

# Only run the game if this script is run directly (not imported)
if __name__ == "__main__":
    action = stage3_game()
    if action == 'back':
        import stage  # Import stage.py to move back to it
