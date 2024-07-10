import pygame, sys
from button import Button

pygame.init()

# SCREEN = pygame.display.set_mode((1280, 720))
# pygame.display.set_caption("Menu")

SCREEN = pygame.display.Info()
screen_width = SCREEN.current_w
screen_height = SCREEN.current_h

pygame.display.set_caption("Menu")
SCREEN = pygame.display.set_mode((screen_width, screen_height))
BG = pygame.transform.scale(pygame.image.load("assets/Background.png"), (screen_width, screen_height))


def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

def play():
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")

        PLAY_TEXT = get_font(45).render("This is the PLAY screen.", True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        PLAY_BACK = Button(image=None, pos=(640, 460), 
                            text_input="BACK", font=get_font(75), base_color="White", hovering_color="Green")

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()

        pygame.display.update()
    
def shop():
    while True:
        SHOP_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")

        SHOP_TEXT = get_font(45).render("This is the SHOP screen.", True, "Black")
        SHOP_RECT = SHOP_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(SHOP_TEXT, SHOP_RECT)

        SHOP_BACK = Button(image=None, pos=(640, 460), 
                            text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        SHOP_BACK.changeColor(SHOP_MOUSE_POS)
        SHOP_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if SHOP_BACK.checkForInput(SHOP_MOUSE_POS):
                    main_menu()

        pygame.display.update()
        
def match_data():
    while True:
        MATCHDATA_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("yellow")

        MATCHDATA_TEXT = get_font(45).render("This is the MATCHDATA screen.", True, "Black")
        MATCHDATA_RECT = MATCHDATA_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(MATCHDATA_TEXT, MATCHDATA_RECT)

        MATCHDATA_BACK = Button(image=None, pos=(640, 460), 
                            text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        MATCHDATA_BACK.changeColor(MATCHDATA_MOUSE_POS)
        MATCHDATA_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if MATCHDATA_BACK.checkForInput(MATCHDATA_MOUSE_POS):
                    main_menu()

        pygame.display.update()
        
def ranks():
    while True:
        RANKS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("pink")

        RANKS_TEXT = get_font(45).render("This is the RANKS screen.", True, "Black")
        RANKS_RECT = RANKS_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(RANKS_TEXT, RANKS_RECT)

        RANKS_BACK = Button(image=None, pos=(640, 460), 
                            text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

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

# def main_menu():
#     while True:
#         SCREEN.blit(BG, (0, 0))

#         MENU_MOUSE_POS = pygame.mouse.get_pos()

#         MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
#         MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

#         PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250), 
#                             text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
#         OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 400), 
#                             text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
#         QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 550), 
#                             text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

#         SCREEN.blit(MENU_TEXT, MENU_RECT)

#         for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
#             button.changeColor(MENU_MOUSE_POS)
#             button.update(SCREEN)
        
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()
#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
#                     play()
#                 if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
#                     options()
#                 if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
#                     pygame.quit()
#                     sys.exit()

#         pygame.display.update()

def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        GENERAL_BG = "assets/General Rect.png"
        
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pygame.image.load(GENERAL_BG), pos=(640, 150), 
                            text_input="Start", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        SHOP_BUTTON = Button(image=pygame.image.load(GENERAL_BG), pos=(640, 250), 
                            text_input="Shop", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        RANKS_BUTTON = Button(image=pygame.image.load(GENERAL_BG), pos=(640, 350), 
                            text_input="Ranks", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        HISTORY_BUTTON = Button(image=pygame.image.load("assets/MatchData Rect.png"), pos=(640, 450), 
                            text_input="History", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 550), 
                            text_input="Exit", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, SHOP_BUTTON, RANKS_BUTTON, HISTORY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    # Call function to handle play screen
                    play()
                    
                if SHOP_BUTTON.checkForInput(MENU_MOUSE_POS):
                    # Call function to handle shop screen
                    shop()
                    
                if RANKS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    # Call function to handle ranks screen
                    ranks()
                
                if HISTORY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    # Call function to handle match data screen
                    match_data()
                    
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


main_menu()


main_menu()