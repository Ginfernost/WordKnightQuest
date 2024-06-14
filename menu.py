import pygame
import stage

# Initialize Pygame
pygame.init()
pygame.mixer.init()  # Initialize the mixer

# Load and play the background music
pygame.mixer.music.load('music.mp3')
pygame.mixer.music.set_volume(0.25)  # Set the volume to 75% (25% quieter)
pygame.mixer.music.play(-1)  # Play the music indefinitely

# Set up the screen
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # Set display mode to fullscreen
pygame.display.set_caption('Word Knight Quest')

# Define fonts
font_size = 36
font = pygame.font.Font(None, font_size)
large_font = pygame.font.Font(None, 74)

def show_menu():
    running = True

    # Load the background image
    background = pygame.image.load("menu.jpg").convert()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "Quit"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                # Calculate button positions
                button_width = screen.get_width() * 0.3  # Modify the width of the buttons
                button_height = screen.get_height() * 0.1  # Modify the height of the buttons

                play_button_x = (screen.get_width() - button_width) // 2
                play_button_y = (screen.get_height() - button_height) // 2 - screen.get_height() * 0.1
                play_button = pygame.Rect(play_button_x, play_button_y, button_width, button_height)

                quit_button_x = (screen.get_width() - button_width) // 2
                quit_button_y = (screen.get_height() - button_height) // 2 + screen.get_height() * 0.1
                quit_button = pygame.Rect(quit_button_x, quit_button_y, button_width, button_height)

                if play_button.collidepoint(pos):
                    return "Stage Selection"  # Return the selected stage
                elif quit_button.collidepoint(pos):
                    return "Quit"  # Quit the game

        # Scale the background image to match the screen resolution
        background = pygame.transform.scale(background, (screen.get_width(), screen.get_height()))

        # Blit the background image onto the screen
        screen.blit(background, (0, 0))

        # Calculate button positions
        button_width = screen.get_width() * 0.3  # Modify the width of the buttons
        button_height = screen.get_height() * 0.1  # Modify the height of the buttons

        play_button_x = (screen.get_width() - button_width) // 2
        play_button_y = (screen.get_height() - button_height) // 2 - screen.get_height() * 0.1
        play_button = pygame.Rect(play_button_x, play_button_y, button_width, button_height)
        pygame.draw.rect(screen, (0, 0, 0), play_button)
        play_text = large_font.render("Play", True, (255, 255, 255))
        screen.blit(play_text, play_text.get_rect(center=play_button.center))

        quit_button_x = (screen.get_width() - button_width) // 2
        quit_button_y = (screen.get_height() - button_height) // 2 + screen.get_height() * 0.1
        quit_button = pygame.Rect(quit_button_x, quit_button_y, button_width, button_height)
        pygame.draw.rect(screen, (255, 0, 0), quit_button)
        quit_text = large_font.render("Quit", True, (255, 255, 255))
        screen.blit(quit_text, quit_text.get_rect(center=quit_button.center))

        pygame.display.flip()

    return "Quit"  # Ensure the function returns "Quit" to handle quitting properly in the main loop

if __name__ == "__main__":
    current_screen = "Menu"
    while True:
        if current_screen == "Menu":
            selection = show_menu()
            if selection == "Stage Selection":
                current_screen = "Stage Selection"
            elif selection == "Quit":
                break
        elif current_screen == "Stage Selection":
            selection = stage.show_stage_selection()
            if selection == "Menu":
                current_screen = "Menu"
            elif selection == "Quit":
                break
    pygame.quit()
    exit()
