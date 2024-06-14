import pygame
import random
import subprocess
import os
import sys

# Initialize Pygame
pygame.init()

# Get screen dimensions
screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h

# Set up the screen
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)  # Set display mode to fullscreen
pygame.display.set_caption('Word Knight Quest - Stage 1')

# Define fonts
font_size = int(screen_height / 15)  # Increase font size for the words
font = pygame.font.Font(None, font_size)
large_font = pygame.font.Font(None, int(font_size * 2))

# Define letter size
letter_size = int(screen_height / 20)  # Increase letter size

# Load background image
background_image = pygame.image.load("stage1.jpg").convert()
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# Function to fetch words and their explanations from a file
def fetch_words_and_explanations(filename):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            words_with_explanations = [line.strip().split(', ') for line in lines]
            return words_with_explanations
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return []

# Function to prepare the game
def prepare_game():
    global correct_word, correct_definition, answer_rects, letter_blocks, placed_letters, original_positions, hint_count, game_over
    # Fetch words and explanations
    words_explanations = fetch_words_and_explanations('wordlist1.txt')
    if words_explanations:
        # Separate words and explanations
        words_bank = [word_explanation[0] for word_explanation in words_explanations]
        definitions_bank = [word_explanation[1] for word_explanation in words_explanations]
        index = random.randint(0, len(words_bank) - 1)
        correct_word = words_bank[index].upper()
        correct_definition = definitions_bank[index]
    else:
        print("Error: No words found in the wordlist file.")
        pygame.quit()
        exit()
    word_length = len(correct_word)
    
    # Center the answer brackets horizontally
    answer_start_x = (screen_width - (word_length * (letter_size + 10) - 10)) // 2
    answer_rects = [pygame.Rect(answer_start_x + i * (letter_size + 10), screen_height * 0.7, letter_size, letter_size) for i in range(word_length)]
    
    # Add random extra letters to ensure 8 choices
    all_letters = list(correct_word)
    while len(all_letters) < 8:
        random_letter = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        if random_letter not in all_letters:
            all_letters.append(random_letter)
    
    random.shuffle(all_letters)
    
    # Center the letter blocks horizontally
    total_blocks_width = len(all_letters) * (letter_size + 10) - 10
    blocks_start_x = (screen_width - total_blocks_width) // 2
    
    letter_positions = {letter: (blocks_start_x + i * (letter_size + 10), screen_height * 0.4) for i, letter in enumerate(all_letters)}

    letter_blocks = {letter: pygame.Rect(pos[0], pos[1], letter_size, letter_size) for letter, pos in letter_positions.items()}
    placed_letters = []
    original_positions = {letter: rect.topleft for letter, rect in letter_blocks.items()}
    hint_count = 0
    game_over = False

# Calculate hint button position
hint_button_width = screen_width * 0.2
hint_button_height = screen_height * 0.08
hint_button_x = (screen_width - hint_button_width) // 2
hint_button_y = screen_height * 0.83
hint_button = pygame.Rect(hint_button_x, hint_button_y, hint_button_width, hint_button_height)

back_button = pygame.Rect(screen_width * 0.025, screen_height * 0.033, screen_width * 0.125, screen_height * 0.067)
end_back_button = pygame.Rect((screen_width - screen_width * 0.25) // 2, (screen_height * 0.5) + screen_height * 0.083, screen_width * 0.25, screen_height * 0.083)
again_button = pygame.Rect((screen_width - screen_width * 0.25) // 2, (screen_height * 0.5) + screen_height * 0.083 + screen_height * 0.125, screen_width * 0.25, screen_height * 0.083)

# Function to draw the game
def draw_game():
    screen.blit(background_image, (0, 0))  # Draw background image

    if game_over:
        # Display the congrats message and back button
        congratz_text = large_font.render("Congratz you answered correctly!", True, (0, 0, 0))
        screen.blit(congratz_text, congratz_text.get_rect(center=(screen_width // 2, screen_height // 2)))
        
        pygame.draw.rect(screen, (0, 0, 0), end_back_button)
        back_text = font.render("Back to Menu", True, (255, 255, 255))
        screen.blit(back_text, back_text.get_rect(center=end_back_button.center))
        
        pygame.draw.rect(screen, (0, 0, 0), again_button)
        again_text = font.render("Play Again", True, (255, 255, 255))
        screen.blit(again_text, again_text.get_rect(center=again_button.center))
    else:
        # Display the definition above the answer brackets
        definition_text = font.render("Definition: " + correct_definition, True, (0, 0, 0))
        screen.blit(definition_text, (screen_width // 2 - definition_text.get_width() // 2, screen_height * 0.08))
        
        # Draw letter blocks with outline
        for letter, rect in letter_blocks.items():
            if letter not in [pl[0] for pl in placed_letters]:
                pygame.draw.rect(screen, (255, 255, 255), rect, 2)  # Draw letter block with outline
                text_surface = font.render(letter, True, (255, 255, 255))  # Render letter text
                text_rect = text_surface.get_rect(center=rect.center)  # Position text in the center of the block
                screen.blit(text_surface, text_rect)  # Draw text on the screen

        # Draw answer brackets and placed letters with outline
        for idx, rect in enumerate(answer_rects):
            pygame.draw.rect(screen, (0, 0, 0), rect, 2)  # Draw bracket with outline
            if idx < len(placed_letters):
                letter, color, is_hint = placed_letter, color, is_hint = placed_letters[idx]
                if is_hint:
                    color = (255, 0, 0)  # Change color if hint
                text_surface = font.render(letter, True, color)
                text_rect = text_surface.get_rect(center=rect.center)
                screen.blit(text_surface, text_rect)
        
        # Draw hint button
        pygame.draw.rect(screen, (0, 0, 0), hint_button)
        hint_text = large_font.render("Hint", True, (255, 255, 255))
        screen.blit(hint_text, hint_text.get_rect(center =hint_button.center))

        # Draw back button
        pygame.draw.rect(screen, (0, 0, 0), back_button)
        back_text = font.render("Back", True, (255, 255, 255))
        screen.blit(back_text, back_text.get_rect(center=back_button.center))

    pygame.display.flip()  # Update the display

# Function to give a hint
def give_hint():
    global hint_count
    if hint_count < len(correct_word) - 1:
        next_letter_index = len(placed_letters)
        next_letter = correct_word[next_letter_index]
        for letter, l_rect in letter_blocks.items():
            if letter == next_letter and letter not in [pl[0] for pl in placed_letters]:
                # Change the color of the hint alphabet
                placed_letters.append((letter, (0, 0, 0), True))  # Set color to black and mark as hint
                hint_count += 1
                return

# Modify the stage1_game() function
def stage1_game():
    global game_over  # Declare game_over as global at the beginning of the function
    prepare_game()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if game_over:
                    if end_back_button.collidepoint(pos):
                        return True  # Return to the menu
                    elif again_button.collidepoint(pos):
                        return False  # Restart the game
                else:
                    if hint_button.collidepoint(pos):
                        give_hint()
                    elif back_button.collidepoint(pos):
                        return True  # Return to the menu
                    else:
                        for letter, rect in letter_blocks.items():
                            if rect.collidepoint(pos) and letter not in [pl[0] for pl in placed_letters]:
                                for idx, a_rect in enumerate(answer_rects):
                                    if idx >= len(placed_letters):
                                        placed_letters.append((letter, (0, 0, 0), False))  # Set color to black and mark as regular letter
                                        break
                                break
                        else:
                            for idx, (letter, _, _) in enumerate(placed_letters):
                                if answer_rects[idx].collidepoint(pos):
                                    if not placed_letters[idx][2]:  # Check if it's not a hint letter
                                        placed_letters.pop(idx)
                                        break

        draw_game()

        # Check if the word is correct
        if len(placed_letters) == len(correct_word):
            formed_word = ''.join(placed_letters[i][0] for i in range(len(correct_word)))
            if formed_word == correct_word:
                game_over = True
            else:
                # Clear all the alphabets in the bracket except the hint alphabet
                hint_indexes = [idx for idx, (_, _, is_hint) in enumerate(placed_letters) if is_hint]
                for idx in range(len(placed_letters) - 1, -1, -1):
                    if idx not in hint_indexes:
                        placed_letters.pop(idx)

    # Outside the game loop, return to the menu
    return True

if __name__ == "__main__":
    while True:
        if stage1_game():  # Check if the game returned True, indicating a return to the menu
            subprocess.run([sys.executable, "menu.py"])  # Launch menu.py
            pygame.quit()  # Quit Pygame
            exit()
