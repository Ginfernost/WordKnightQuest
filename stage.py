import pygame
import stage1
import stage2
import stage3
import stage4
import stage5

# Initialize Pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # Set display mode to fullscreen
pygame.display.set_caption('Word Knight Quest - Stage Selection')

# Define fonts
font_size = 36
font = pygame.font.Font(None, font_size)
large_font = pygame.font.Font(None, 74)
info_font = pygame.font.Font(None, 48)  # Larger font for information text

def show_information_screen(stage_number):
    info_screen = pygame.Surface(screen.get_size())  # Create a new surface for the information screen
    info_screen.fill((0, 0, 0))  # Fill with black background

    # Load stage-specific background image
    background_image = pygame.image.load(f"stage{stage_number}.jpg").convert()
    background_image = pygame.transform.scale(background_image, (screen.get_width(), screen.get_height()))

    info_screen.blit(background_image, (0, 0))  # Blit stage-specific background

    # Example information texts, replace with actual information for each stage
    if stage_number == 1:
        information_text = """Welcome to Stage 1 of Word Knight Quest!
Objective:
Your quest begins in the ancient halls of a medieval castle. Your goal is to uncover hidden words from ancient scrolls. 
Each word you unravel brings you closer to unraveling the mysteries of the castle and progressing in your adventure.
How to Play:
Word Display: Look at the empty brackets at the bottom of the screen. Each bracket represents a letter in the hidden word.
Choose Letters: Click on any letter from the scattered blocks to pick it up. 
Then, click on an empty bracket to place it. Correctly placed letters will appear in the brackets.
Hints: If you're stuck, use the "Hint" button sparingly to reveal the next correct letter. 
Hints are limited, so use them wisely!
Complete the Word: Fill all the brackets with the correct letters to solve the puzzle and 
advance to the next stage of your adventure.
Tips for Success:
- Start with vowels and common letters to narrow down your choices.
- Take your time to think before placing each letter.
- Use hints strategically to overcome challenging words."""

    elif stage_number == 2:
        information_text = """Welcome to Stage 2 of Word Knight Quest!
Objective:
In this stage, you find yourself amidst the ancient scrolls and cryptic puzzles of the castle's library. 
Your task is to unscramble words that have been jumbled. Each correct answer brings you closer to unveiling the castle's secrets.
How to Play:
Unscramble the Word: A mixed-up word will be displayed on the screen. Rearrange the letters to form the correct word.
Definition: A hint will be provided to help you decipher the word's meaning.
Input Answer: Type your answer into the input box located at the bottom of the screen. Press Enter to submit your answer.
Hints: If you're stuck, click the "Hint" button to reveal the first half of the word. Use hints wisely, as they are limited.
Time Limit: You have 30 seconds to solve each word puzzle. If time runs out, your game will end.
Enjoy the Challenge: Immerse yourself in the medieval ambiance and sharpen your wits as you decipher the mysteries of the castle!
Tips for Success:
- Focus on recognizing common letter patterns to quickly unscramble words.
- Use hints strategically, especially on longer or more challenging words.
- Stay alert and keep an eye on the countdown timer to manage your time effectively."""

    elif stage_number == 3:
        information_text = """Welcome to Stage 3 of Word Knight Quest!
Objective:
You have reached the final stage in the castle's grand library. 
Your challenge here is to complete sentences by choosing the correct words from a selection. 
Each correct answer brings you closer to unlocking the castle's ultimate secret.
How to Play:
Complete Sentences: Each round presents you with a sentence missing a word. Choose the correct word from the options provided.
Timer: You have 30 seconds to answer each question. If time runs out, the game ends.
Score: Earn points for each correct answer. Your total score is displayed at the end of the stage.
Tips for Success:
- Read the sentence carefully to understand the context before selecting an answer.
- Manage your time wisely as you have a limited amount to answer each question.
- If unsure, take a guess; you might get it right!
Best of luck in your quest to unravel the castle's secrets!"""

    elif stage_number == 4:
        information_text = """Welcome to Stage 4 of Word Knight Quest!
Objective:
You have reached the castle's hidden library. Here, your memory and vocabulary skills are put to the test in a challenging memory game. 
Match pairs of words to uncover their hidden meanings and reveal the castle's deepest secrets.
How to Play:
Memory Matching: Flip two tiles at a time to find matching word pairs. Click on a tile to reveal its word.
Scoring: Earn points for each correctly matched pair. Your score is displayed on the screen throughout the game.
Time Limit: You have 30 seconds to match as many pairs as you can. The game ends when time runs out.
Strategic Tips:
- Memorize the location of words to uncover matching pairs quickly.
- Focus on matching pairs to maximize your score within the time limit.
- Use the "Back" button strategically to manage your progress through the game.
Enjoy the Challenge: Immerse yourself in the castle's mysteries and unravel its secrets hidden within the library!
Best of luck in mastering the memory game and uncovering all the hidden word pairs!"""

    elif stage_number == 5:
        information_text = """Welcome to Stage 5 of Word Knight Quest!
Objective:
In this stage, you will test your pronunciation skills by speaking the given word into the microphone. 
Listen carefully and repeat the word correctly to proceed. Use your voice to unlock the secrets hidden within the castle's library.
How to Play:
1. Listen: The screen will display a word. Pay attention to the word you need to pronounce.
2. Speak: Say the word into your microphone clearly and audibly.
3. Check: The game will recognize your speech. If you pronounce the word correctly, you will proceed to the next word. Otherwise, you will receive feedback to try again.
4. Score: Your score is based on how many words you pronounce correctly within the time limit.
Tips for Success:
- Speak clearly and audibly into the microphone.
- Listen attentively to the word displayed on the screen.
- Use the "Back" button strategically to navigate between stages.
Prepare yourself to uncover the castle's secrets through accurate pronunciation and mastery of the spoken word!
Best of luck in mastering pronunciation and advancing through the castle's library of words!"""


    # Render the information text with outline
    text_lines = information_text.splitlines()
    y_offset = (screen.get_height() - len(text_lines) * info_font.get_linesize()) // 2  # Center vertically
    for line in text_lines:
        # Render black outline text
        outline_text = info_font.render(line, True, (0, 0, 0))
        outline_rect = outline_text.get_rect(center=(screen.get_width() // 2 + 2, y_offset + 2))
        info_screen.blit(outline_text, outline_rect)

        # Render white text over the outline
        info_text = info_font.render(line, True, (255, 255, 255))
        info_rect = info_text.get_rect(center=(screen.get_width() // 2, y_offset))
        info_screen.blit(info_text, info_rect)

        y_offset += info_font.get_linesize()  # Move to the next line

    # Create a Back button
    back_button = pygame.Rect(20, 20, 100, 50)
    pygame.draw.rect(info_screen, (255, 0, 0), back_button)
    back_text = font.render("Back", True, (255, 255, 255))
    info_screen.blit(back_text, back_button.move(15, 10))

    # Create a Play button
    play_button = pygame.Rect((screen.get_width() - 200) // 2, screen.get_height() - 100, 200, 50)
    pygame.draw.rect(info_screen, (0, 150, 0), play_button)
    play_text = font.render("Play", True, (255, 255, 255))
    info_screen.blit(play_text, play_button.move(40, 10))

    # Update the display with the information screen
    screen.blit(info_screen, (0, 0))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return "Quit"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if back_button.collidepoint(pos):
                    return "Back"  # Return "Back" to indicate go back to stage selection
                elif stage_number == 1:
                    return "Play"  # Return "Play" to indicate start the game for Stage 1
                elif stage_number == 2:
                    return "Play"  # Return "Play" to indicate start the game for Stage 2
                elif stage_number == 3:
                    return "Play"  # Return "Play" to indicate start the game for Stage 3
                elif stage_number == 4:
                    return "Play"  # Return "Play" to indicate start the game for Stage 4
                elif stage_number == 5:
                    return "Play"  # Return "Play" to indicate start the game for Stage 5
def show_stage_selection():
    running = True

    # Load the background image for the stage selection screen
    background = pygame.image.load("stage.jpg").convert()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "Quit"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if stage1_button.collidepoint(pos):
                    action = show_information_screen(1)
                    if action == "Play":
                        stage1.stage1_game()  # Go to Stage 1
                    elif action == "Back":
                        continue  # Stay on the stage selection screen
                elif stage2_button.collidepoint(pos):
                    action = show_information_screen(2)
                    if action == "Play":
                        stage2.main()  # Go to Stage 2
                    elif action == "Back":
                        continue  # Stay on the stage selection screen
                elif stage3_button.collidepoint(pos):
                    action = show_information_screen(3)
                    if action == "Play":
                        stage3.stage3_game()  # Go to Stage 3
                    elif action == "Back":
                        continue  # Stay on the stage selection screen
                elif stage4_button.collidepoint(pos):
                    action = show_information_screen(4)
                    if action == "Play":
                        stage4.run_stage4()  # Go to Stage 4
                    elif action == "Back":
                        continue  # Stay on the stage selection screen
                elif stage5_button.collidepoint(pos):
                    action = show_information_screen(5)
                    if action == "Play":
                        stage5.stage5_game()  # Go to Stage 5
                    elif action == "Back":
                        continue  # Stay on the stage selection screen
                elif back_button.collidepoint(pos):
                    return "Menu"  # Return to the menu

        # Scale the background image to match the screen resolution
        background = pygame.transform.scale(background, (screen.get_width(), screen.get_height()))

        # Blit the background image onto the screen
        screen.blit(background, (0, 0))

        # Calculate button positions
        button_width = screen.get_width() * 0.3
        button_height = screen.get_height() * 0.1
        spacing = screen.get_height() * 0.05  # Space between buttons

        # Calculate the starting y position for the first button to center all buttons vertically
        total_buttons_height = (button_height * 6) + (spacing * 5)
        start_y = (screen.get_height() - total_buttons_height) // 2

        # Stage 1 button
        stage1_button_x = (screen.get_width() - button_width) // 2
        stage1_button_y = start_y
        stage1_button = pygame.Rect(stage1_button_x, stage1_button_y, button_width, button_height)

        # Stage 2 button
        stage2_button_x = (screen.get_width() - button_width) // 2
        stage2_button_y = stage1_button_y + button_height + spacing
        stage2_button = pygame.Rect(stage2_button_x, stage2_button_y, button_width, button_height)

        # Stage 3 button
        stage3_button_x = (screen.get_width() - button_width) // 2
        stage3_button_y = stage2_button_y + button_height + spacing
        stage3_button = pygame.Rect(stage3_button_x, stage3_button_y, button_width, button_height)

        # Stage 4 button
        stage4_button_x = (screen.get_width() - button_width) // 2
        stage4_button_y = stage3_button_y + button_height + spacing
        stage4_button = pygame.Rect(stage4_button_x, stage4_button_y, button_width, button_height)

        # Stage 5 button
        stage5_button_x = (screen.get_width() - button_width) // 2
        stage5_button_y = stage4_button_y + button_height + spacing
        stage5_button = pygame.Rect(stage5_button_x, stage5_button_y, button_width, button_height)

        # Back button
        back_button_x = (screen.get_width() - button_width) // 2
        back_button_y = stage5_button_y + button_height + spacing
        back_button = pygame.Rect(back_button_x, back_button_y, button_width, button_height)

        # Draw buttons
        pygame.draw.rect(screen, (0, 0, 0), stage1_button)
        stage1_text = large_font.render("Stage 1", True, (255, 255, 255))
        screen.blit(stage1_text, stage1_text.get_rect(center=stage1_button.center))

        pygame.draw.rect(screen, (0, 0, 0), stage2_button)
        stage2_text = large_font.render("Stage 2", True, (255, 255, 255))
        screen.blit(stage2_text, stage2_text.get_rect(center=stage2_button.center))

        pygame.draw.rect(screen, (0, 0, 0), stage3_button)
        stage3_text = large_font.render("Stage 3", True, (255, 255, 255))
        screen.blit(stage3_text, stage3_text.get_rect(center=stage3_button.center))

        pygame.draw.rect(screen, (0, 0, 0), stage4_button)
        stage4_text = large_font.render("Stage 4", True, (255, 255, 255))
        screen.blit(stage4_text, stage4_text.get_rect(center=stage4_button.center))

        pygame.draw.rect(screen, (0, 0, 0), stage5_button)
        stage5_text = large_font.render("Stage 5", True, (255, 255, 255))
        screen.blit(stage5_text, stage5_text.get_rect(center=stage5_button.center))

        pygame.draw.rect(screen, (255, 0, 0), back_button)
        back_text = large_font.render("Back", True, (255, 255, 255))
        screen.blit(back_text, back_text.get_rect(center=back_button.center))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    show_stage_selection()
