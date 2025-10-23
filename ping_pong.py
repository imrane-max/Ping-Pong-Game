import pygame
import sys

pygame.init()

# Screen setup
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Ping Pong Game")

# Background image
background = pygame.image.load("pong_table.png")
background = pygame.transform.scale(background, (screen_width, screen_height))

# Colors
white = (255, 255, 255)

# Game area
margin_top = 100
margin_left = 50
player_area = pygame.Rect(
    margin_left,
    margin_top,
    screen_width - 2 * margin_left,
    screen_height - 2 * margin_top,
)

# Game objects
ball_speed = [4, 4]
ball = pygame.Rect(player_area.centerx - 10, player_area.centery - 10, 20, 20)
player1 = pygame.Rect(player_area.left + 25, player_area.centery - 40, 15, 80)
player2 = pygame.Rect(player_area.right - 40, player_area.centery - 40, 15, 80)

# Speed
player1_speed = 0
player2_speed = 0

# Font
font = pygame.font.Font(None, 74)
font_title = pygame.font.Font(None, 34)
game_title = font_title.render("Ping Pong Game", True, white)

# Scores
player1_score = 0
player2_score = 0

# Clock
clock = pygame.time.Clock()

def ball_restart():
    global ball_speed
    ball.center = player_area.center
    ball_speed[0] = -ball_speed[0]

def ball_animation():
    global ball_speed, player1_score, player2_score
    ball.x += ball_speed[0]
    ball.y += ball_speed[1]

    if ball.top <= player_area.top or ball.bottom >= player_area.bottom:
        ball_speed[1] = -ball_speed[1]
    if ball.left <= player_area.left:
        player2_score += 1
        ball_restart()
    if ball.right >= player_area.right:
        player1_score += 1
        ball_restart()
    if ball.colliderect(player1) or ball.colliderect(player2):
        ball_speed[0] = -ball_speed[0]
        # Increase speed by 10% on paddle hit, with a maximum speed of 15
        ball_speed[0] = max(min(ball_speed[0] * 1.1, 15), -15)

def player1_animation():
    player1.y += player1_speed
    if player1.top <= player_area.top:
        player1.top = player_area.top
    if player1.bottom >= player_area.bottom:
        player1.bottom = player_area.bottom

def player2_animation():
    player2.y += player2_speed
    if player2.top <= player_area.top:
        player2.top = player_area.top
    if player2.bottom >= player_area.bottom:
        player2.bottom = player_area.bottom

# Main loop
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                player1_speed = -7
            if event.key == pygame.K_s:
                player1_speed = 7
            if event.key == pygame.K_UP:
                player2_speed = -7
            if event.key == pygame.K_DOWN:
                player2_speed = 7
        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_w, pygame.K_s):
                player1_speed = 0
            if event.key in (pygame.K_UP, pygame.K_DOWN):
                player2_speed = 0
        
        # Mouse control for player1
        if event.type == pygame.MOUSEMOTION:
            mouse_y = event.pos[1]
            if player_area.top <= mouse_y <= player_area.bottom:
                player1.centery = mouse_y


    # Update objects
    ball_animation()
    player1_animation()
    player2_animation()

    # Draw everything
    screen.blit(background, (0, 0))
    pygame.draw.rect(screen, white, player_area, 2)
    pygame.draw.ellipse(screen, white, ball)
    pygame.draw.rect(screen, white, player1)
    pygame.draw.rect(screen, white, player2)
    screen.blit(game_title, (screen_width // 2 - 80, 20))

    # Draw scores
    score1_text = font.render(str(player1_score), True, white)
    score2_text = font.render(str(player2_score), True, white)
    screen.blit(score1_text, (screen_width // 4, 20))
    screen.blit(score2_text, (screen_width * 3 // 4, 20))

    pygame.display.flip()
    clock.tick(60)

