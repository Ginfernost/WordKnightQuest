import pygame
import sys
import random

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Button class for handling button creation and clicks
class Button:
    def __init__(self, text, x, y, width, height, font, color, hover_color):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.font = font

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        pygame.draw.rect(screen, color, self.rect)
        text_surf = self.font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

# Function to load word pairs from a file
def load_word_pairs(filename):
    word_pairs = []
    with open(filename, 'r') as file:
        for line in file:
            words = line.strip().split(':')
            if len(words) == 2:
                word_pairs.append((words[0], words[1]))
    return word_pairs

# Function to scramble synonyms for all words in the tiles
def scramble_all_words(tiles, word_pairs):
    words = [tile["word"] for tile in tiles]
    synonyms_dict = {word: scramble_synonyms(word, word_pairs) for word in words}
    new_words = []
    for word in words:
        if synonyms_dict[word]:
            new_words.append(synonyms_dict[word][0])
        else:
            new_words.append(word)
    random.shuffle(new_words)
    for i, tile in enumerate(tiles):
        tile["word"] = new_words[i]
        tile["revealed"] = False
        tile["matched"] = False

# Function to scramble synonyms for the given word
def scramble_synonyms(word, word_pairs):
    synonyms = [pair[1] for pair in word_pairs if pair[0] == word]
    random.shuffle(synonyms)
    return synonyms

def run_stage4():
    # Load word pairs from the file
    word_pairs = load_word_pairs('wordlist4.txt')

    # Initialize Pygame
    pygame.init()

    # Set up the screen
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
    pygame.display.set_caption("Word Pairs Memory Game")

    # Define fonts
    font = pygame.font.Font(None, 36)
    button_font = pygame.font.Font(None, 30)

    # Load the background image
    background_image = pygame.image.load('stage4.jpg').convert()
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Scale the image to fit the screen

    # Back button
    back_button = Button("Back", 10, SCREEN_HEIGHT - 50, 100, 40, button_font, GRAY, RED)

    # Shuffle word pairs
    random.shuffle(word_pairs)

    # Calculate grid size based on number of word pairs
    grid_cols = 4  # Number of columns in the grid
    grid_rows = 4  # Fixed to 4 rows for a 4x4 grid

    tile_width = 150
    tile_height = 100
    margin = 20

    # Calculate starting positions to center the grid
    grid_width = grid_cols * tile_width + (grid_cols - 1) * margin
    grid_height = grid_rows * tile_height + (grid_rows - 1) * margin
    start_x = (SCREEN_WIDTH - grid_width) // 2
    start_y = (SCREEN_HEIGHT - grid_height) // 2

    # Create tiles
    tiles = []
    for i in range(len(word_pairs)):
        for j in range(2):
            word = word_pairs[i][j]
            tile = {"word": word, "revealed": False, "matched": False}
            tiles.append(tile)

    # Shuffle tiles and limit to 16 for a 4x4 grid
    tiles = tiles[:16]
    random.shuffle(tiles)

    # Game variables
    selected_tiles = []
    matched_pairs = 0
    game_over = False
    flip_back_delay = 1000  # Time in milliseconds to show mismatched pairs before flipping back
    start_ticks = pygame.time.get_ticks()  # Store the starting time
    game_duration = 30 * 1000  # 30 seconds
    match_count = 0  # Count of matched pairs for shuffling logic

    # Main game loop
    running = True
    while running:
        screen.blit(background_image, (0, 0))  # Draw the background image

        # Calculate remaining time
        seconds = (pygame.time.get_ticks() - start_ticks) // 1000
        remaining_time = 30 - seconds

        if remaining_time <= 0:
            game_over = True

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.is_clicked(pygame.mouse.get_pos()):
                    return  # Return to previous stage
                elif len(selected_tiles) < 2:
                    pos = pygame.mouse.get_pos()
                    column = (pos[0] - start_x) // (tile_width + margin)
                    row = (pos[1] - start_y) // (tile_height + margin)
                    if 0 <= column < grid_cols and 0 <= row < grid_rows:
                        index = row * grid_cols + column
                        if index < len(tiles) and not tiles[index]["revealed"]:
                            tiles[index]["revealed"] = True
                            selected_tiles.append(index)
                            if len(selected_tiles) == 2:
                                # Check if selected tiles match
                                tile1 = tiles[selected_tiles[0]]
                                tile2 = tiles[selected_tiles[1]]
                                if (tile1["word"], tile2["word"]) in word_pairs or (tile2["word"], tile1["word"]) in word_pairs:
                                    matched_pairs += 1
                                    tile1["matched"] = True
                                    tile2["matched"] = True
                                    selected_tiles = []
                                    match_count += 1
                                    if matched_pairs == len(tiles) // 2:
                                        game_over = True
                                    elif match_count == 4:  # Every four pairs matched
                                        # Show message, then scramble and close all cards
                                        match_count = 0
                                        message_text = font.render("Scrambling cards...", True, BLACK)
                                        screen.blit(message_text, (SCREEN_WIDTH // 2 - message_text.get_width() // 2, SCREEN_HEIGHT // 2))
                                        pygame.display.flip()
                                        pygame.time.wait(1000)  # Display message for 1 second
                                        scramble_all_words(tiles, word_pairs)
                                else:
                                    pygame.time.set_timer(pygame.USEREVENT, flip_back_delay)
            elif event.type == pygame.USEREVENT:
                for index in selected_tiles:
                    tiles[index]["revealed"] = False
                selected_tiles = []
                pygame.time.set_timer(pygame.USEREVENT, 0)

        # Draw tiles
        for i in range(len(tiles)):
            column = i % grid_cols
            row = i // grid_cols
            if tiles[i]["matched"]:
                color = YELLOW
            else:
                color = GRAY if tiles[i]["revealed"] else RED
            x = start_x + (margin + tile_width) * column
            y = start_y + (margin + tile_height) * row
            pygame.draw.rect(screen, color, [x, y, tile_width, tile_height])
            if tiles[i]["revealed"]:
                text = font.render(tiles[i]["word"], True, BLACK)
                screen.blit(text, (x + 20, y + 30))

        # Draw back button
        back_button.draw(screen)

        # Draw score
        score_text = font.render(f"Score: {matched_pairs}", True, BLACK)
        screen.blit(score_text, (10, 10))

        # Draw timer
        timer_text = font.render(f"Time: {remaining_time}s", True, BLACK)
        screen.blit(timer_text, (SCREEN_WIDTH - 150, 10))

        if game_over:
            # Game over screen
            screen.fill(WHITE)
            game_over_text = font.render("Time's up! Your score: " + str(matched_pairs), True, BLACK)
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
            back_button.draw(screen)
        
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    run_stage4()
