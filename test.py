import pygame
from sys import exit

# --- Initialize Pygame ---
pygame.init()
pygame.mixer.init()

# --- Screen Setup ---
screen = pygame.display.set_mode((800, 400))
clock = pygame.time.Clock()

# --- Font Setup ---
txtFont = pygame.font.Font("Media/font/Pixeltype.ttf", 50)
txt = txtFont.render("Runner game", False, "Black")
txtRect = txt.get_rect(topleft=(300, 50))

# --- Global variables for score text ---
scoretxt = None
scoreRect = None

# --- Function to update score text (no return, uses global) ---
def updateScore(score):
    global scoretxt, scoreRect
    scoreStr = "Score = " + str(score)
    scoretxt = txtFont.render(scoreStr, False, "red")
    scoreRect = scoretxt.get_rect(topleft=(10, 10))

# --- Load Assets ---
pygame.mixer.music.load("Media/audio/music.wav")
pygame.mixer.music.play(-1)
jumpSound = pygame.mixer.Sound("Media/audio/jump.mp3")


sky = pygame.image.load("Media/graphics/Sky.png")
ground = pygame.image.load("Media/graphics/ground.png")
player = pygame.image.load("Media/graphics/Player/player_stand.png")
snail = pygame.image.load("Media/graphics/snail/snail1.png")

# --- Set Rectangles (Positions) ---
skyRect = sky.get_rect(topleft=(0, 0))
groundRect = ground.get_rect(topleft=(0, 300))
playerRect = player.get_rect(midbottom=(100, 300))
snailRect = snail.get_rect(midbottom=(650, 300))

# --- Player Physics ---
player_gravity = 0
jump_power = -20

# --- Score Initialization ---
score = 0
updateScore(score)  # Initialize the score text

# --- Game Modes ---
game_mode = "start"  # modes: "start", "playing", "game_over"

# --- Main Game Loop ---
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and game_mode=="start":
            game_mode = "playing"

       
            
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and game_mode=="playing" and playerRect.bottom >= 300:
            player_gravity = jump_power
            jumpSound.play()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and game_mode == "game_over":
                # Reset game state to start playing again
                score = 0
                updateScore(score)
                playerRect.midbottom = (100, 300)
                player_gravity = 0
                snailRect.left = 800
                game_mode = "playing"

    # --- Game logic only runs in playing mode ---
    if game_mode == "playing":
        # Gravity effect
        player_gravity += 1
        playerRect.top += player_gravity

        # Stop at ground
        if playerRect.bottom >= 300:
            playerRect.bottom = 300
            player_gravity = 0

        # Move snail left
        snailRect.left -= 5
        if snailRect.right < 0:
            snailRect.left = 800
            score += 1
            updateScore(score)

        # Collision detection
        if snailRect.colliderect(playerRect):
            game_mode = "game_over"

    # --- Drawing ---
    screen.blit(sky, skyRect)
    screen.blit(ground, groundRect)

    if game_mode == "start":
        start_text = txtFont.render("Press SPACE to start", False, "Black")
        start_rect = start_text.get_rect(center=(400, 200))
        screen.blit(start_text, start_rect)

    elif game_mode == "playing":
        screen.blit(player, playerRect)
        screen.blit(snail, snailRect)
        screen.blit(scoretxt, scoreRect)

    elif game_mode == "game_over":
        screen.blit(player, playerRect)
        screen.blit(snail, snailRect)
        game_over_text = txtFont.render("Game Over! Press space to restart", False, "Red")
        game_over_rect = game_over_text.get_rect(center=(400, 200))
        screen.blit(game_over_text, game_over_rect)
        screen.blit(scoretxt, scoreRect)

    screen.blit(txt, txtRect)

    pygame.display.update()
    clock.tick(60)
