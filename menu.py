import sys
import random
import pygame
import pygame.mixer

from tkinter import messagebox
from classes.constants import WIDTH, HEIGHT,BLUE, RED, BLACK, WHITESMOKE

def animate_screen():
    for i in range(0, 20):
        screen.blit(mainmenu_img, (0, 0))
        pygame.display.flip()
        pygame.time.wait(10)
        screen.blit(mainmenu_img, (random.randint(-5, 5), random.randint(-5, 5)))
        pygame.display.flip()
        pygame.time.wait(10)

#Music for the Main Menu
pygame.mixer.init()
pygame.init()
pygame.mixer.music.load('game_sounds/menu.mp3')
pygame.mixer.music.set_volume(0.25)
pygame.mixer.music.play(-1)
pygame.mixer.set_num_channels(20)

for i in range(20):
    channel = pygame.mixer.Channel(i)
    channel.set_volume(0.25)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("FEFU Summer Practice::MiniGame")
clock = pygame.time.Clock()

mainmenu_img = pygame.image.load('images/mainmenu.jpg').convert()
mainmenu_img = pygame.transform.scale(mainmenu_img, (WIDTH, HEIGHT))

logo_img = pygame.image.load('images/logo.png').convert_alpha()
logo_x = (WIDTH - logo_img.get_width()) // 2 + 14
logo_y = 50

play_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 25, 205, 39)
help_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 40, 205, 39)
quit_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 105, 205, 39)


pygame.mixer.music.load('game_sounds/menu.mp3')
pygame.mixer.music.play(-1)
explosion_sound = pygame.mixer.Sound('game_sounds/explosions/explosion1.wav')
explosion_sound.set_volume(0.25)
selected_button = 0
show_menu = True

joystick = None
if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()


while show_menu:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if play_button_rect.collidepoint(x, y):
                explosion_sound.play()
                animate_screen()
                show_menu = False
                import main
                main.main()
                break
            elif quit_button_rect.collidepoint(x, y):
                pygame.quit()
                sys.exit()
            elif help_button_rect.collidepoint(x, y):
                messagebox.showinfo("About","This game is an academic shooting game Created by Abraham Chileshe as a project for the 2023 Summer Practice")

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                selected_button = 0
            elif event.key == pygame.K_DOWN:
                selected_button = 1
            elif event.key == pygame.K_RETURN:
                if selected_button == 0:
                    explosion_sound.play()
                    animate_screen()
                    show_menu = False
                    screen.fill(BLACK)
                    import main
                    main.main()
                    break
                elif selected_button == 1:
                    pygame.quit()
                    sys.exit()

        if joystick:
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 0:
                    if selected_button == 0:
                        explosion_sound.play()
                        animate_screen()
                        show_menu = False
                        screen.fill(BLACK)
                        import game
                        game.main()
                        break
                    elif selected_button == 1:
                        pygame.quit()
                        sys.exit()
            elif event.type == pygame.JOYHATMOTION:
                if event.value[1] == 1:
                    selected_button = 0
                elif event.value[1] == -1:
                    selected_button = 1

    screen.blit(mainmenu_img, (0, 0))

    screen.blit(logo_img, (logo_x, logo_y))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if play_button_rect.collidepoint(event.pos):
                selected_button = 0
            elif help_button_rect.collidepoint(event.pos):
                selected_button = 2
            elif quit_button_rect.collidepoint(event.pos):
                selected_button = 1

        # Mouse hover effect
    mouse_pos = pygame.mouse.get_pos()
    play_hover_color = (192, 192, 192) if play_button_rect.collidepoint(mouse_pos) else WHITESMOKE
    help_hover_color = (0, 0, 0) if help_button_rect.collidepoint(mouse_pos) else BLUE
    quit_hover_color = (255, 100, 100) if quit_button_rect.collidepoint(mouse_pos) else RED

    # Draw buttons
    font = pygame.font.SysFont('Arial Black', 14)

    # Play button
    pygame.draw.rect(screen, play_hover_color, play_button_rect, border_radius=10)
    if selected_button == 0:
        pygame.draw.rect(screen, WHITESMOKE, play_button_rect, border_radius=10, width=3)
    text = font.render("Start", True, BLACK)
    text_rect = text.get_rect()
    text_rect.center = play_button_rect.center
    screen.blit(text, text_rect)

    # Help button
    pygame.draw.rect(screen, help_hover_color, help_button_rect, border_radius=10)
    if selected_button == 2:
        pygame.draw.rect(screen, BLUE, help_button_rect, border_radius=10, width=3)
    text = font.render("About", True, WHITESMOKE)
    text_rect = text.get_rect()
    text_rect.center = help_button_rect.center
    screen.blit(text, text_rect)

    # Quit button
    pygame.draw.rect(screen, quit_hover_color, quit_button_rect, border_radius=10)
    if selected_button == 1:
        pygame.draw.rect(screen, BLACK, quit_button_rect, border_radius=10, width=3)
    text = font.render("Exit", True, BLACK)
    text_rect = text.get_rect()
    text_rect.center = quit_button_rect.center
    screen.blit(text, text_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()