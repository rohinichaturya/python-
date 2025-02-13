import pygame
import math
import random

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Carrom Board Game")

# Colors
BOARD_COLOR = (255, 204, 153)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# Game settings
POCKET_RADIUS = 30
COIN_RADIUS = 15
STRIKER_RADIUS = 20
FRICTION = 0.98  # Slows down movement

# Define pocket positions (four corners)
pockets = [(50, 50), (WIDTH - 50, 50), (50, HEIGHT - 50), (WIDTH - 50, HEIGHT - 50)]

# Define Striker
striker = {
    "x": WIDTH // 2,
    "y": HEIGHT - 100,
    "dx": 0,
    "dy": 0,
    "speed": 0,
    "angle": 0,
    "power": 0,
    "max_power": 10
}

# Define Coins
coins = []
for i in range(9):
    coins.append({
        "x": WIDTH // 2 + random.randint(-50, 50),
        "y": HEIGHT // 2 + random.randint(-50, 50),
        "dx": 0,
        "dy": 0,
        "color": RED if i == 0 else BLACK
    })

# Move objects with friction
def move_objects():
    # Move striker
    striker["x"] += striker["dx"]
    striker["y"] += striker["dy"]
    striker["dx"] *= FRICTION
    striker["dy"] *= FRICTION

    # Move coins
    for coin in coins:
        coin["x"] += coin["dx"]
        coin["y"] += coin["dy"]
        coin["dx"] *= FRICTION
        coin["dy"] *= FRICTION

# Handle collisions between striker and coins
def check_collisions():
    for coin in coins:
        dx = coin["x"] - striker["x"]
        dy = coin["y"] - striker["y"]
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance < COIN_RADIUS + STRIKER_RADIUS:
            coin["dx"], coin["dy"] = striker["dx"], striker["dy"]
            striker["dx"], striker["dy"] = -striker["dx"], -striker["dy"]

# Check if coins fall into pockets
def check_pockets():
    global coins
    new_coins = []
    for coin in coins:
        pocketed = False
        for pocket in pockets:
            if math.sqrt((coin["x"] - pocket[0]) ** 2 + (coin["y"] - pocket[1]) ** 2) < POCKET_RADIUS:
                pocketed = True
                break
        if not pocketed:
            new_coins.append(coin)
    coins = new_coins

# Game Loop
running = True
while running:
    screen.fill(BOARD_COLOR)

    # Draw Pockets
    for pocket in pockets:
        pygame.draw.circle(screen, WHITE, pocket, POCKET_RADIUS)

    # Draw Striker
    pygame.draw.circle(screen, BLUE, (int(striker["x"]), int(striker["y"])), STRIKER_RADIUS)

    # Draw Coins
    for coin in coins:
        pygame.draw.circle(screen, coin["color"], (int(coin["x"]), int(coin["y"])), COIN_RADIUS)

    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                striker["angle"] -= 5
            elif event.key == pygame.K_RIGHT:
                striker["angle"] += 5
            elif event.key == pygame.K_SPACE:
                striker["power"] += 1
                if striker["power"] > striker["max_power"]:
                    striker["power"] = striker["max_power"]
            elif event.key == pygame.K_RETURN:
                striker["dx"] = math.cos(math.radians(striker["angle"])) * striker["power"]
                striker["dy"] = -math.sin(math.radians(striker["angle"])) * striker["power"]
                striker["power"] = 0

    # Update Positions
    move_objects()
    check_collisions()
    check_pockets()

    pygame.display.flip()
    pygame.time.delay(30)

pygame.quit()
