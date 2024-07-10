from button import Button
from prettytable import PrettyTable
from pygame import mixer
import mysql.connector
import pygame
import pygame_gui
from slider import Slider
import sys

pygame.init()
     
screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h
SCREEN = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Menu")

POKE_BUTTON_TEXTSIZE = (int)(screen_height * 0.11)
OPTIONS_BUTTON_TEXTSIZE = (int)(screen_height * 0.08)
BACK_BUTTON_TEXTSIZE = (int)(screen_height * 0.04)

db_config = {
    'user': 'root',
    'password':'root@329',
    'host':'localhost',
    'database': 'mini'
}


BG = pygame.transform.scale(pygame.image.load("assets/Background.png"), (screen_width, screen_height))

def title_screen():
    title_bg = pygame.transform.scale(pygame.image.load("assets/TitleBackground1.png"), (screen_width, screen_height))
    SCREEN.blit(title_bg, (0, 0))
    #playsound('assets/bgm.mp3',True)
    

    while True:
        TITLE_MOUSE_POS = pygame.mouse.get_pos()

        POKE_BUTTON = Button(image=None, pos=(screen_width // 2, screen_height // 9), 
                           text_input="PokePoker", font=get_font(POKE_BUTTON_TEXTSIZE), base_color="black", hovering_color="red")

        POKE_BUTTON.changeColor(TITLE_MOUSE_POS)
        POKE_BUTTON.update(SCREEN)

        for event in pygame.event.get():
            if POKE_BUTTON.checkForInput(TITLE_MOUSE_POS):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    main_menu()
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


        pygame.display.update()

def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

# Function to check if a string contains only numeric characters
def is_numeric(string):
    return all(char.isdigit() for char in string)

def playsound(soundeffect, is_Looping):
        mixer.init()
        mixer.music.load(soundeffect)
        if is_Looping:
            mixer.music.play(-1)
        else:
            mixer.music.play()

# Define a global variable to store the return value of updatebattle function
battle_id = None

def execute_query(query):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Execute the query
        cursor.execute(query)

        # Fetch all rows from the result
        result = cursor.fetchall()

        cursor.close()
        connection.close()

        return result
    except mysql.connector.Error as error:
        print("MySQL Error:", error)
        return []

def start_battle(user1_id, user2_id):
    # Define entry box dimensions
    entry_box_width = 200
    entry_box_height = 30
    entry_box_margin = 20

    # Define the current page variable
    current_page = 'battle'

    while True:
        USER_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("grey")

        if current_page == 'battle':
            # Render the table headers
            header_font = pygame.font.Font(None, 32)
            header_text = header_font.render("BATTLE", True, pygame.Color("black"))
            header_rect = header_text.get_rect(center=(screen_width // 2, 50))
            SCREEN.blit(header_text, header_rect)

            # Get user 1 cards from the battle_cards table
            user1_cards = execute_query(f"SELECT pokeid, name, health_points, attack_points, category FROM battle_cards WHERE userid = {user1_id};")

            # Get user 2 cards from the battle_cards table
            user2_cards = execute_query(f"SELECT pokeid, name, health_points, attack_points, category FROM battle_cards WHERE userid = {user2_id};")

            # Render User 1 table
            display_table("User 1 Cards", user1_cards, (20, 100))

            # Render User 2 table
            display_table("User 2 Cards", user2_cards, (20, 300))

            # Adjusted position of the back button to the bottom-right corner
            BACK_BUTTON = Button(image=None, pos=(screen_width - 200, screen_height - 100),
                                 text_input="BACK", font=get_font(24), base_color="Black",
                                 hovering_color="Green")

            # Render the "Next" button
            NEXT_BUTTON = Button(image=None, pos=(screen_width // 2, screen_height - 100),
                                 text_input="Next", font=get_font(24), base_color="White",
                                 hovering_color="Green")

            BACK_BUTTON.changeColor(USER_MOUSE_POS)
            BACK_BUTTON.update(SCREEN)

            NEXT_BUTTON.changeColor(USER_MOUSE_POS)
            NEXT_BUTTON.update(SCREEN)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if BACK_BUTTON.checkForInput(USER_MOUSE_POS):
                        main_menu()
                    elif NEXT_BUTTON.checkForInput(USER_MOUSE_POS):
                        current_page = 'input'  # Move to the input page

        elif current_page == 'input':
            SCREEN.fill("grey")

            # Render input box labels
            poke_id_1_label = get_font(24).render("Poke ID 1:", True, pygame.Color("white"))
            poke_id_2_label = get_font(24).render("Poke ID 2:", True, pygame.Color("white"))
            poke_id_1_label_rect = poke_id_1_label.get_rect(midright=(screen_width // 2 - 20, screen_height // 2 - 30))
            poke_id_2_label_rect = poke_id_2_label.get_rect(midright=(screen_width // 2 - 20, screen_height // 2 + 30))

            SCREEN.blit(poke_id_1_label, poke_id_1_label_rect)
            SCREEN.blit(poke_id_2_label, poke_id_2_label_rect)

            # Render input boxes for Poke IDs
            entry_box1 = pygame.Rect(screen_width // 2 + 30, screen_height // 2 - 30, entry_box_width, entry_box_height)
            pygame.draw.rect(SCREEN, "white", entry_box1)
            entry_box2 = pygame.Rect(screen_width // 2 + 30, screen_height // 2 + 30, entry_box_width, entry_box_height)
            pygame.draw.rect(SCREEN, "white", entry_box2)

            # Adjusted position of the back button to the bottom-right corner
            BACK_BUTTON = Button(image=None, pos=(screen_width - 200, screen_height - 100),
                                 text_input="BACK", font=get_font(24), base_color="Black",
                                 hovering_color="Green")

            # Render the "Start" button
            START_BUTTON = Button(image=None, pos=(screen_width // 2, screen_height - 100),
                                  text_input="START", font=get_font(24), base_color="White",
                                  hovering_color="Green")

            BACK_BUTTON.changeColor(USER_MOUSE_POS)
            BACK_BUTTON.update(SCREEN)

            START_BUTTON.changeColor(USER_MOUSE_POS)
            START_BUTTON.update(SCREEN)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if BACK_BUTTON.checkForInput(USER_MOUSE_POS):
                        current_page = 'battle'  # Go back to the battle page
                    elif START_BUTTON.checkForInput(USER_MOUSE_POS):
                        # Get input from the input boxes
                        lets_continue_on_terminal()
                        # Process the Poke IDs

        pygame.display.update()

def lets_continue_on_terminal():
    
    # Display the table in the Pygame window
    while True:
        USER_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("light blue")

        # Render the table headers
        header_font = get_font(BACK_BUTTON_TEXTSIZE)
        header_text = header_font.render("NOW!!\n Let's Continue on Terminal!", True, "Black")
        header_rect = header_text.get_rect(center=(screen_width // 2, screen_height // 4))
        SCREEN.blit(header_text, header_rect)


        # Adjusted position of the back button to the bottom-right corner
        BACK_BUTTON = Button(image=None, pos=(screen_width - 200, screen_height - 100),
                            text_input="BACK", font=get_font(BACK_BUTTON_TEXTSIZE), base_color="Black",
                            hovering_color="Green")

        BACK_BUTTON.changeColor(USER_MOUSE_POS)
        BACK_BUTTON.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BACK_BUTTON.checkForInput(USER_MOUSE_POS):
                    main_menu()

        pygame.display.update()
    return
def display_table(title, data, position):
    # Render table title
    title_font = get_font(20)
    title_text = title_font.render(title, True, "black")
    title_rect = title_text.get_rect(topleft=position)
    SCREEN.blit(title_text, title_rect)

    # Create a PrettyTable object
    table = PrettyTable()

    # Define table headers
    headers = ["Poke ID", "Name", "Health Points", "Attack Points", "Category"]
    table.field_names = headers

    # Add rows to the table
    for row in data:
        table.add_row(row)

    # Render the table as a string
    table_text = table.get_string()

    # Render table data
    data_font = get_font(16)
    data_text = data_font.render(table_text, True, "black")
    data_rect = data_text.get_rect(topleft=(position[0], position[1] + 50))
    SCREEN.blit(data_text, data_rect)

def render_cards_table(cards, pos):
    # Define table properties
    table_width = 300
    table_height = 400
    cell_padding = 10
    card_font_size = 20

    # Render table background
    pygame.draw.rect(SCREEN, "white", (pos[0], pos[1], table_width, table_height))

    # Render table title
    title_font = get_font(card_font_size)
    title_text = title_font.render("User Cards", True, "black")
    title_rect = title_text.get_rect(center=(pos[0] + table_width // 2, pos[1] + 50))
    SCREEN.blit(title_text, title_rect)

    # Create a PrettyTable object
    table = PrettyTable()
    table.field_names = ["Poke ID", "Name"]

    # Add cards to the table
    for card in cards:
        table.add_row([card[0], card[1]])

    # Render the table as a string
    table_text = table.get_string(header=True, border=True)
    table_font = get_font(16)
    table_render = table_font.render(table_text, True, "black")
    table_rect = table_render.get_rect(topleft=(pos[0] + cell_padding, pos[1] + 100))
    SCREEN.blit(table_render, table_rect)

def execute_get_user_cards(user_id):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Call the GetUserCards stored procedure to fetch user's Pokémon cards
        cursor.callproc('GetUserCards', (user_id,))
        
        # Fetch the result set from the stored procedure
        for result in cursor.stored_results():
            user_cards = result.fetchall()

        cursor.close()
        connection.close()
        
        return user_cards

    except mysql.connector.Error as error:
        print("MySQL Error:", error)
        return None
    
def insert_battle_card(poke_id):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Call the insertbattlecard procedure
        cursor.callproc('insertbattlecard', (poke_id,))

        # Commit the transaction
        connection.commit()

        cursor.close()
        connection.close()

    except mysql.connector.Error as error:
        print("MySQL Error:", error)

def select_user1_cards(userid_1,userid_2):
    user1_cards = execute_get_user_cards(userid_1)
    selected_cards = []  # List to store the selected card IDs

    while True:
        USER_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.fill("light blue")

        # Display user1's cards as clickable image buttons
        card_width = 150
        card_height = 200
        card_margin = 20
        cards_per_row = 4
        current_row = 0
        current_column = 0
        for card_info in user1_cards:
            card_id, card_name, user_id = card_info  # Extract user_id along with card_id and card_name
            card_image_path = f"cards/{card_name.lower()}.png"
            card_image = pygame.transform.scale(pygame.image.load(card_image_path), (card_width, card_height))
            card_rect = pygame.Rect(card_margin + current_column * (card_width + card_margin), 
                                     card_margin + current_row * (card_height + card_margin),
                                     card_width, card_height)
            pygame.draw.rect(SCREEN, (255, 255, 255), card_rect)
            SCREEN.blit(card_image, card_rect)
            current_column += 1
            if current_column >= cards_per_row:
                current_column = 0
                current_row += 1
                
            button_text = card_name
            button_pos = (card_rect.centerx, card_rect.bottom + 10)
            CARD_BUTTON = Button(image=None, pos=button_pos, text_input=button_text, font=get_font(10),
                                base_color="Black", hovering_color="Green")

            # Check for mouse interaction with the button
            CARD_BUTTON.changeColor(USER_MOUSE_POS)
            CARD_BUTTON.update(SCREEN)
            if CARD_BUTTON.checkForInput(USER_MOUSE_POS) and pygame.mouse.get_pressed()[0]:
                # Add the selected card ID to the list
                selected_cards.append(card_id)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if NEXT_BUTTON.checkForInput(USER_MOUSE_POS):
                    # Proceed to the next step (e.g., select cards for User 2)
                    select_user2_cards(userid_1,userid_2)

        # Display message and buttons
        message_font = get_font(20)
        message_text = message_font.render("Select 4 cards for User 1", True, "black")
        message_rect = message_text.get_rect(midtop=(screen_width // 2, 10))
        SCREEN.blit(message_text, message_rect)

        NEXT_BUTTON = Button(image=None, pos=(screen_width // 2 + 100, screen_height - 50),
                             text_input="Next", font=get_font(20),
                             base_color="white", hovering_color="green")
        NEXT_BUTTON.changeColor(USER_MOUSE_POS)
        NEXT_BUTTON.update(SCREEN)

        pygame.display.update()

        done_button = Button(image=None, pos=(screen_width // 2 - 100, screen_height - 50),
                         text_input="Done", font=get_font(20),
                         base_color="white", hovering_color="green")
        done_button.changeColor(USER_MOUSE_POS)
        done_button.update(SCREEN)

def select_user2_cards(userid_1,userid_2):
    user2_cards = execute_get_user_cards(userid_2)

    while True:
        USER_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.fill("pink")

        # Display user2's cards as clickable image buttons
        card_width = 150
        card_height = 200
        card_margin = 20
        cards_per_row = 4
        current_row = 0
        current_column = 0
        for card_info in user2_cards:
            card_id, card_name = card_info
            card_image_path = f"cards/{card_name.lower()}.png"
            card_image = pygame.transform.scale(pygame.image.load(card_image_path), (card_width, card_height))
            card_rect = pygame.Rect(card_margin + current_column * (card_width + card_margin), 
                                     card_margin + current_row * (card_height + card_margin),
                                     card_width, card_height)
            pygame.draw.rect(SCREEN, (255, 255, 255), card_rect)
            SCREEN.blit(card_image, card_rect)
            current_column += 1
            if current_column >= cards_per_row:
                current_column = 0
                current_row += 1
                
            button_text = card_name
            button_pos = (card_rect.centerx, card_rect.bottom + 10)
            CARD_BUTTON = Button(image=None, pos=button_pos, text_input=button_text, font=get_font(10),
                                base_color="Black", hovering_color="Green")

            # Check for mouse interaction with the button
            CARD_BUTTON.changeColor(USER_MOUSE_POS)
            CARD_BUTTON.update(SCREEN)
            if CARD_BUTTON.checkForInput(USER_MOUSE_POS) and pygame.mouse.get_pressed()[0]:
                # Call the insertbattlecard procedure
                insert_battle_card(card_id)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if done_button.checkForInput(pygame.mouse.get_pos()):
                    start_battle(userid_1,userid_2)  # Exit the function to stop displaying user2's cards

        # Display message and done button
        message_font = get_font(20)
        message_text = message_font.render("Select 4 cards for User 2", True, "black")
        message_rect = message_text.get_rect(midtop=(screen_width // 2, 10))
        SCREEN.blit(message_text, message_rect)

        done_button = Button(image=None, pos=(screen_width // 2, screen_height - 50),
                             text_input="Done", font=get_font(20),
                             base_color="white", hovering_color="green")
        done_button.changeColor(pygame.mouse.get_pos())
        done_button.update(SCREEN)

        pygame.display.update()
        
def handle_events_and_render(screen_width, screen_height):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if done_button.checkForInput(pygame.mouse.get_pos()):
                return  # Exit the function to stop displaying user's cards

    # Display message and done button
    message_font = get_font(20)
    message_text = message_font.render("Select 4 cards", True, "black")
    message_rect = message_text.get_rect(midtop=(screen_width // 2, 10))
    SCREEN.blit(message_text, message_rect)

    done_button = Button(image=None, pos=(screen_width // 2, screen_height - 50),
                         text_input="Done", font=get_font(20),
                         base_color="white", hovering_color="green")
    done_button.changeColor(pygame.mouse.get_pos())
    done_button.update(SCREEN)

    pygame.display.update()

def execute_update_battle(user_id_1, user_id_2):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Call the updatebattle stored procedure
        cursor.callproc('updatebattle', (user_id_1, user_id_2))

        # Fetch the result from the stored procedure
        for result in cursor.stored_results():
            battle_id = result.fetchone()[0]  # Assuming the stored procedure returns a single value

        cursor.close()
        connection.close()

        return battle_id

    except mysql.connector.Error as error:
        print("MySQL Error:", error)
        return None

def start_game(userid_1, userid_2):
    user1_cards = execute_get_user_cards(userid_1)
    selected_cards = set()  # Set to store the selected card IDs
    while True:
        USER_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.fill("light blue")

        # Display user1's cards as clickable image buttons
        card_width = 150
        card_height = 200
        card_margin = 30
        cards_per_row = 4
        current_row = 0
        current_column = 0
        for card_info in user1_cards:
            card_id, card_name = card_info
            card_image_path = f"cards/{card_name.lower()}.png"
            card_image = pygame.transform.scale(pygame.image.load(card_image_path), (card_width, card_height))
            card_rect = pygame.Rect(card_margin + current_column * (card_width + card_margin), 
                                     card_margin + current_row * (card_height + card_margin),
                                     card_width, card_height)
            pygame.draw.rect(SCREEN, (255, 255, 255), card_rect)
            SCREEN.blit(card_image, card_rect)
            current_column += 1
            if current_column >= cards_per_row:
                current_column = 0
                current_row += 1

            button_text = card_name
            button_pos = (card_rect.centerx, card_rect.bottom + 10)
            CARD_BUTTON = Button(image=None, pos=button_pos, text_input=button_text, font=get_font(20),
                                 base_color="Black", hovering_color="Green")

            # Check for mouse interaction with the button
            CARD_BUTTON.changeColor(USER_MOUSE_POS)
            CARD_BUTTON.update(SCREEN)
            if CARD_BUTTON.checkForInput(USER_MOUSE_POS) and pygame.mouse.get_pressed()[0]:
                # Add the selected card ID to the set
                selected_cards.add(card_id)
                print(f"Selected card: {card_name}")

        # Display message and next button
        message_font = get_font(20)
        message_text = message_font.render("Select 4 cards for User 1", True, "black")
        message_rect = message_text.get_rect(midtop=(screen_width // 2, 10))
        SCREEN.blit(message_text, message_rect)

        NEXT_BUTTON = Button(image=None, pos=(screen_width // 2, screen_height - 50),
                             text_input="Next", font=get_font(20),
                             base_color="black", hovering_color="green")
        NEXT_BUTTON.changeColor(pygame.mouse.get_pos())
        NEXT_BUTTON.update(SCREEN)

        # Adjusted position of the back button to the bottom-right corner
        BACK_BUTTON = Button(image=None, pos=(screen_width - 200, screen_height - 100),
                            text_input="BACK", font=get_font(BACK_BUTTON_TEXTSIZE), base_color="Black",
                            hovering_color="Green")

        BACK_BUTTON.changeColor(USER_MOUSE_POS)
        BACK_BUTTON.update(SCREEN)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if NEXT_BUTTON.checkForInput(USER_MOUSE_POS):
                    # Insert the selected cards into battle_cards
                    for card_id in selected_cards:
                        insert_battle_card(card_id)
                    # Call the execute_update_battle function
                    battle_id = execute_update_battle(userid_1, userid_2)
                    if battle_id is not None:
                        print("Battle ID:", battle_id)  # Use the battle_id for further processing
                    else:
                        print("Failed to execute updatebattle function.")
                    select_user2_cards(userid_1, userid_2)
                if BACK_BUTTON.checkForInput(USER_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def play():
    # Create a UI manager for Pygame GUI elements
    manager = pygame_gui.UIManager((screen_width, screen_height))

    # Create text entry boxes for user IDs
    user_id_1_entry = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((350, 275), (300, 50)), manager=manager, object_id='#user_id_1_entry')
    user_id_2_entry = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((350, 350), (300, 50)), manager=manager, object_id='#user_id_2_entry')

    # Variable to track user ID entry completion
    user_id_1_entered = False
    user_id_numeric_constraint_voilation = False
    show_start_button = False

    # Create a back button for the Start page
    BACK_BUTTON = Button(image=None, pos=(screen_width - 200, screen_height - 200),
                               text_input="BACK", font=get_font(BACK_BUTTON_TEXTSIZE), base_color="White",
                               hovering_color="Green")

    # Create a start button
    START_BUTTON = Button(image=None, pos=(screen_width // 2, screen_height - 200),
                          text_input="START", font=get_font(BACK_BUTTON_TEXTSIZE), base_color="White",
                          hovering_color="Green")

    # Render text labels
    user_id_1_label = get_font(BACK_BUTTON_TEXTSIZE).render("User 1 ID:", True, "White")
    user_id_2_label = get_font(BACK_BUTTON_TEXTSIZE).render("User 2 ID:", True, "White")
    user_id_1_label_rect = user_id_1_label.get_rect(
        midright=(user_id_1_entry.rect.left - 10, user_id_1_entry.rect.centery))
    user_id_2_label_rect = user_id_2_label.get_rect(
        midright=(user_id_2_entry.rect.left - 10, user_id_2_entry.rect.centery))

    user_id_1 = ""  # Initialize variables to store user IDs
    user_id_2 = ""

    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")

        # Draw the text entry boxes
        manager.update(8)
        manager.draw_ui(SCREEN)

        # Draw the back button
        BACK_BUTTON.changeColor(PLAY_MOUSE_POS)
        BACK_BUTTON.update(SCREEN)

        # Draw the text labels
        SCREEN.blit(user_id_1_label, user_id_1_label_rect)
        SCREEN.blit(user_id_2_label, user_id_2_label_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Process text input events for user IDs
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if not user_id_1_entered:
                        user_id_1 = user_id_1_entry.get_text()
                        if is_numeric(user_id_1):
                            print("User 1 ID:", user_id_1)  # Display user ID in terminal
                            user_id_1_entered = True
                        else:
                            print("User 1 ID must contain only numeric characters.")
                            user_id_numeric_constraint_voilation = True
                    else:
                        user_id_2 = user_id_2_entry.get_text()
                        if is_numeric(user_id_2):
                            print("User 2 ID:", user_id_2)  # Display user ID in terminal
                            user_id_1_entered = False
                            show_start_button = True
                        else:
                            print("User 2 ID must contain only numeric characters.")
                            user_id_numeric_constraint_voilation = True

            # Check for button click events
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BACK_BUTTON.checkForInput(PLAY_MOUSE_POS):
                    main_menu()  # Go back to the main menu
                elif show_start_button and START_BUTTON.checkForInput(PLAY_MOUSE_POS):
                    # Open a new window or start the game when the start button is clicked
                    start_game(user_id_1, user_id_2)

            # Pass events to the UI manager
            manager.process_events(event)

        # Draw the numeric constraint violation label
        if user_id_numeric_constraint_voilation:
            numeric_constraint_label = get_font(BACK_BUTTON_TEXTSIZE).render(
                "Non-numeric value for User ID. Please enter only numeric characters.",
                True,
                "White")
            numeric_constraint_label_rect = numeric_constraint_label.get_rect(
                midright=(user_id_2_entry.rect.left - 10, user_id_2_entry.rect.centery + screen_height // 8))
            SCREEN.blit(numeric_constraint_label, numeric_constraint_label_rect)

        # Draw the start button if both user IDs are entered correctly
        if show_start_button:
            START_BUTTON.changeColor(PLAY_MOUSE_POS)
            START_BUTTON.update(SCREEN)

        pygame.display.update()

# Function to fetch Pokemon info from the database
def fetch_pokemon_info(pokemon_name):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        
        # Query to fetch Pokemon info based on name (case insensitive)
        query = "SELECT * FROM new_pokemon WHERE LOWER(name) = LOWER(%s)"
        cursor.execute(query, (pokemon_name,))
        pokemon_info = cursor.fetchone()
        
        connection.close()
        return pokemon_info
    except mysql.connector.Error as error:
        print("MySQL Error:", error)

manager = pygame_gui.UIManager((screen_width, screen_height))

text_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((350, 275), (900, 50)), manager=manager,
                                               object_id='#main_text_entry')

clock = pygame.time.Clock()

def show_purchased_card(user_name, pokemon_name):
    SCREEN.fill("black")  # Fill the screen with black background

    # Fetch Pokémon info
    pokemon_info = fetch_pokemon_info(pokemon_name)

    if pokemon_info:
        card_image_path = f"cards/{pokemon_name.lower()}.png"
        card_image = pygame.image.load(card_image_path)

        # Calculate the scaled dimensions to fit within the window
        max_card_width = screen_width // 1.5 # Maximum width allowed
        max_card_height = screen_height // 1.6  # Maximum height allowed
        scale_factor = min(max_card_width / card_image.get_width(), max_card_height / card_image.get_height())
        scaled_width = int(card_image.get_width() * scale_factor * 1.5)  # Increase scale by 1.5 times
        scaled_height = int(card_image.get_height() * scale_factor * 1.5)  # Increase scale by 1.5 times

        # Position the card in the middle of the screen
        card_rect = card_image.get_rect(center=(screen_width // 2, screen_height // 2))
        SCREEN.blit(pygame.transform.scale(card_image, (scaled_width, scaled_height)), card_rect)

        # Display Pokémon name at the left-hand side, upper corner
        pokemon_font = get_font(30)
        pokemon_text = pokemon_font.render(pokemon_name, True, (255, 255, 255))  # White color
        pokemon_rect = pokemon_text.get_rect(topleft=(50, 50))
        SCREEN.blit(pokemon_text, pokemon_rect)

        # Add a button to go back to shop
        button_width = 150
        button_height = 50
        button_margin = 20
        button_font = get_font(20)
        BACK_TO_SHOP_BUTTON = Button(image=None, pos=(screen_width - button_width - button_margin, screen_height - button_height - button_margin),
                                     text_input="Back to Shop", font=button_font, base_color="green", hovering_color="white")
        BACK_TO_SHOP_BUTTON.changeColor(pygame.mouse.get_pos())
        BACK_TO_SHOP_BUTTON.update(SCREEN)

        # Add a button to go back to main menu
        BACK_TO_MENU_BUTTON = Button(image=None, pos=(button_margin, screen_height - button_height - button_margin),
                                     text_input="Back to Main Menu", font=button_font, base_color="green", hovering_color="white")
        BACK_TO_MENU_BUTTON.changeColor(pygame.mouse.get_pos())
        BACK_TO_MENU_BUTTON.update(SCREEN)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if BACK_TO_SHOP_BUTTON.checkForInput(pygame.mouse.get_pos()):
                        shop()  # Go back to the shop screen
                    elif BACK_TO_MENU_BUTTON.checkForInput(pygame.mouse.get_pos()):
                        main_menu()  # Go back to the main menu

            pygame.display.update()

    else:
        # Pokémon info not found
        error_font = get_font(30)
        error_text = error_font.render("Error: Pokémon info not found!", True, (255, 0, 0))  # Red color
        error_rect = error_text.get_rect(center=(screen_width // 2, screen_height // 2))
        SCREEN.blit(error_text, error_rect)
        pygame.display.update()

def buy_pokemon(username, pokemon_name):
    user_id = get_user_id(username)
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Call the PurchaseCard stored procedure
        cursor.callproc('PurchaseCard', (user_id, pokemon_name))

        # Commit the transaction
        connection.commit()

        # Fetch the result of the procedure
        for result in cursor.stored_results():
            message = result.fetchone()[0]
            #print(message)  # Print the message returned by the stored procedure
            show_purchased_card(username,pokemon_name)
            

        cursor.close()
        connection.close()
    except mysql.connector.Error as error:
        print("MySQL Error:", error)
    #print("Buying pokemon")

def show_user_name_to_buy(user_name, pokemon_name):
    # Query the database to check if the user exists
    user_exists = check_user_exists(user_name)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        SCREEN.fill("light blue")  # Fill the screen with white background
        
        # Display a header text
        header_font = get_font(40)
        header_text = header_font.render("Purchase Pokemon Card", True, (0, 0, 0))  # Black color
        header_rect = header_text.get_rect(center=(screen_width // 2, 50))
        SCREEN.blit(header_text, header_rect)

        # Check if the user exists
        if user_exists:
            # Display a welcome message for existing users
            welcome_font = get_font(30)
            welcome_text = welcome_font.render(f"Welcome back, {user_name}!", True, (0, 128, 0))  # Green color
            welcome_rect = welcome_text.get_rect(center=(screen_width // 2, 150))
            SCREEN.blit(welcome_text, welcome_rect)

            # Create and display a 'Buy' button
            buy_button = Button(image=None, pos=(screen_width // 2, 250),
                                text_input="BUY", font=get_font(25),
                                base_color=(0, 128, 0), hovering_color=(0, 255, 0))  # Green button with hover effect
            buy_button.changeColor(pygame.mouse.get_pos())  # Change button color based on mouse position
            buy_button.update(SCREEN)

            # Handle mouse click event for the 'Buy' button
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if buy_button.checkForInput(pygame.mouse.get_pos()):
                        buy_pokemon(user_name, pokemon_name)  # Call buy_pokemon function on button click
        else:
            # Display a registration message for new users
            registration_font = get_font(30)
            registration_text = registration_font.render(f"Hello, {user_name}!", True, (0, 0, 255))  # Blue color
            registration_rect = registration_text.get_rect(center=(screen_width // 2, 150))
            SCREEN.blit(registration_text, registration_rect)

            # Create and display a 'Back' button for new users
            back_button = Button(image=None, pos=(screen_width // 2, 250),
                                 text_input="BACK", font=get_font(25),
                                 base_color=(255, 0, 0), hovering_color=(255, 128, 128))  # Red button with hover effect
            back_button.changeColor(pygame.mouse.get_pos())  # Change button color based on mouse position
            back_button.update(SCREEN)

            # Handle mouse click event for the 'Back' button
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back_button.checkForInput(pygame.mouse.get_pos()):
                        main_menu()  # Return to main menu on button click

        pygame.display.update()  # Update the display

def get_user_name_to_buy(pokemon_name):
    while True:
        UI_REFRESH_RATE = clock.tick(60)/1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if (event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and
                event.ui_object_id == '#main_text_entry'):
                show_user_name_to_buy(event.text,pokemon_name)
            
            manager.process_events(event)
        
        manager.update(UI_REFRESH_RATE)
        
        SCREEN.fill("white")

        manager.draw_ui(SCREEN)
        
        pygame.display.update()

def check_user_exists(user_name):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Query to check if the user exists
        query = "SELECT COUNT(*) FROM new_users WHERE username = %s"
        cursor.execute(query, (user_name,))
        count = cursor.fetchone()[0]

        cursor.close()
        connection.close()
        
        return count > 0  # Return True if count is greater than 0 (user exists), False otherwise

    except mysql.connector.Error as error:
        print("MySQL Error:", error)
        return False  # Return False in case of any error or exception

def get_user_id(username):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Query to check if the user exists
        query = "SELECT userId FROM new_users WHERE username = %s"
        cursor.execute(query, (username,))
        userid = cursor.fetchone()[0]

        cursor.close()
        connection.close()
        
        return userid # Return True if count is greater than 0 (user exists), False otherwise

    except mysql.connector.Error as error:
        print("MySQL Error:", error)
        return False  # Return False in case of any error or exception
 
def fetch_available_pokemon_info():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Call the GetAllRanks stored procedure
        cursor.callproc('availablepoke')

        # Fetch all results
        for result in cursor.stored_results():
            rows = result.fetchall()
 
        cursor.close()
        connection.close()
        return rows

    except mysql.connector.Error as error:
        print("MySQL Error:", error)
        return None
 
def load_card_images(available_pokemon, card_width, card_height):
    card_images = {}
    for pokemon in available_pokemon:
        pokemon_name = pokemon[1]
        card_image_path = f"cards/{pokemon_name.lower()}.png"
        card_images[pokemon_name] = pygame.transform.scale(pygame.image.load(card_image_path), (card_width, card_height))
    return card_images

def shop():
    try:
        available_pokemon = fetch_available_pokemon_info()
    except mysql.connector.Error as error:
        print("MySQL Error:", error)
        return

    card_width = 250
    card_height = 300
    card_margin = 30
    cards_per_row = 4

    total_cards = len(available_pokemon)
    rows = (total_cards + cards_per_row - 1) // cards_per_row
    total_height = rows * (card_height + card_margin) + card_margin

    slider = Slider(screen_width, screen_height, total_height)
    card_images = load_card_images(available_pokemon, card_width, card_height)

    while True:
        SHOP_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.fill("white")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP or event.type == pygame.MOUSEMOTION:
                slider.handle_event(event)  # Pass mouse events to the slider
            elif event.type == pygame.MOUSEWHEEL:
                # Handle mouse wheel scrolling
                if event.y > 0:  # Scroll up
                    slider.slider_handle_pos -= 10  # Adjust the step size as needed
                    slider.slider_handle_pos = max(0, slider.slider_handle_pos)  # Ensure handle doesn't go above track
                elif event.y < 0:  # Scroll down
                    slider.slider_handle_pos += 10  # Adjust the step size as needed
                    slider.slider_handle_pos = min(slider.slider_height - slider.slider_handle_height, slider.slider_handle_pos)  # Ensure handle doesn't go below track

        slider.update_slider()

        current_row = 0
        current_column = 0
        button_font = get_font(19)
        for pokemon in available_pokemon:
            card_y = current_row * (card_height + card_margin) - slider.scroll_position
            pokemon_name = pokemon[1]
            card_image = card_images[pokemon_name]

            card_rect = pygame.Rect(card_margin + current_column * (card_width + card_margin), card_y,
                                     card_width, card_height)

            # Create a Button instance for the text below the card
            button_text = pokemon_name
            button_pos = (card_rect.centerx, card_rect.bottom + 10)
            card_button = Button(image=None, pos=button_pos, text_input=button_text, font=button_font,
                                 base_color="Black", hovering_color="Green")

            # Check for mouse interaction with the button
            card_button.changeColor(SHOP_MOUSE_POS)
            card_button.update(SCREEN)
            if card_button.checkForInput(SHOP_MOUSE_POS) and pygame.mouse.get_pressed()[0]:
                # Perform action when the button is clicked (e.g., select the card)
                # print(f"Clicked on {pokemon_name}")
                get_user_name_to_buy(pokemon_name)

            SCREEN.blit(card_image, card_rect)

            current_column += 1
            if current_column >= cards_per_row:
                current_column = 0
                current_row += 1

        slider.draw_slider(SCREEN)
        button_width = 100
        button_height = 50
        button_margin = 10
        button_font_size = 20
        button_font = get_font(button_font_size)
        BACK_BUTTON = Button(image=None, pos=(screen_width - button_width + 20, screen_height - button_height - button_margin),
                             text_input="BACK", font=button_font, base_color="Black", hovering_color="Green")
        BACK_BUTTON.changeColor(SHOP_MOUSE_POS)
        BACK_BUTTON.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if BACK_BUTTON.checkForInput(SHOP_MOUSE_POS):
                    main_menu()  # Go back to the main menu

        pygame.display.update()
        
def get_all_ranks():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Call the GetAllRanks stored procedure
        cursor.callproc('GetAllRanks')

        # Fetch all results
        for result in cursor.stored_results():
            rows = result.fetchall()

        cursor.close()
        connection.close()
        return rows

    except mysql.connector.Error as error:
        print("MySQL Error:", error)
        return None
    
def ranks():
    try:
        rank_order = get_all_ranks()
    except mysql.connector.Error as error:
        print("MySQL Error:", error)
        # Handle the error as per your application's requirements
        # For example, display an error message to the user or log the error
        return

    # Display the results in a table format using PrettyTable
    table = PrettyTable(["User ID", "Username", "Points", "Rank"])
    for row in rank_order:
        table.add_row(row)

    # Display the table in the Pygame window
    while True:
        RANKS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("light blue")

        # Render the table headers
        header_font = get_font(OPTIONS_BUTTON_TEXTSIZE)
        header_text = header_font.render("RANKS", True, "Black")
        header_rect = header_text.get_rect(center=(screen_width // 2, 50))
        SCREEN.blit(header_text, header_rect)

        # Render each row of the table
        row_font = get_font(25)
        y_offset = screen_height // 6
        for line in str(table).splitlines():
            row_text = row_font.render(line, True, "Black")
            row_rect = row_text.get_rect(center=(screen_width // 2, y_offset))
            SCREEN.blit(row_text, row_rect)
            y_offset += 30  # Increase y_offset for next row

        # Adjusted position of the back button to the bottom-right corner
        RANKS_BACK = Button(image=None, pos=(screen_width - 200, screen_height - 100),
                            text_input="BACK", font=get_font(BACK_BUTTON_TEXTSIZE), base_color="Black",
                            hovering_color="Green")

        RANKS_BACK.changeColor(RANKS_MOUSE_POS)
        RANKS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if RANKS_BACK.checkForInput(RANKS_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def get_battle_data():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        query = "SELECT * FROM new_battle"
        cursor.execute(query)

    # Fetch all rows
        rows = cursor.fetchall()

        cursor.close()
        connection.close()
        return rows

    except mysql.connector.Error as error:
        print("MySQL Error:", error)
        return None

def logs():
    try:
        battle_logs = get_battle_data()
    except mysql.connector.Error as error:
        print("MySQL Error (inlogs):", error)
        # Handle the error as per your application's requirements
        # For example, display an error message to the user or log the error
        return

    # Display the results in a table format using PrettyTable
    table = PrettyTable(["MatchId","UID1","UID2","Winner"])
    for row in battle_logs:
        table.add_row(row)

    # Display the table in the Pygame window
    while True:
        LOGS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("pink")

        # Render the table headers
        header_font = get_font(OPTIONS_BUTTON_TEXTSIZE)
        header_text = header_font.render("LOGS", True, "Black")
        header_rect = header_text.get_rect(center=(screen_width // 2, 50))
        SCREEN.blit(header_text, header_rect)

        # Render each row of the table
        row_font = get_font(25)
        y_offset = screen_height // 6
        for line in str(table).splitlines():
            row_text = row_font.render(line, True, "Black")
            row_rect = row_text.get_rect(center=(screen_width // 2, y_offset))
            SCREEN.blit(row_text, row_rect)
            y_offset += 30  # Increase y_offset for next row

        # Adjusted position of the back button to the bottom-right corner
        LOGS_BACK = Button(image=None, pos=(screen_width - 200, screen_height - 100),
                            text_input="BACK", font=get_font(BACK_BUTTON_TEXTSIZE), base_color="Black",
                            hovering_color="Green")

        LOGS_BACK.changeColor(LOGS_MOUSE_POS)
        LOGS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if LOGS_BACK.checkForInput(LOGS_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def exit_game():
    pygame.quit()
    sys.exit()

def main_menu():
    while True:
        
        MAINMENU_TITLE_SIZE = (int)(screen_height * 0.12)
        SCREEN.blit(BG, (0, 0))
         

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(MAINMENU_TITLE_SIZE).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(screen_width // 2, screen_height // 9))

        BUTTON_Y_OFFSET = screen_height // 7  # Adjust this value to increase or decrease the gap between buttons
        buttons = [
            {"text": "Play", "function": play},
            {"text": "Shop", "function": shop},
            {"text": "Ranks", "function": ranks},  # Changed to call the rank handling function
            {"text": "Logs", "function": logs},
            {"text": "Exit", "function": sys.exit}
        ]

        for i, button_info in enumerate(buttons):
            button_y = screen_height // 3.5 + i * BUTTON_Y_OFFSET
            
            BUTTON_BG = "assets/General Rect.png"
            BUTTON_BASE_COLOR = '#d7fcd4'
            button = Button(image=pygame.image.load(BUTTON_BG), pos=(screen_width // 2, button_y),
                            text_input=button_info["text"], font=get_font(OPTIONS_BUTTON_TEXTSIZE),
                            base_color=BUTTON_BASE_COLOR, hovering_color="White")
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
            if button.checkForInput(MENU_MOUSE_POS):
                if pygame.mouse.get_pressed()[0]:  # Check if left mouse button is pressed
                    button_info["function"]()  # Call the associated function when the button is clicked

        SCREEN.blit(MENU_TEXT, MENU_RECT)
         

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()





title_screen()
main_menu()