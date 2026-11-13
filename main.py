# Sun-Earth-Moon Simulation using Pygame
import pygame
import math


# -------------------- SETUP --------------------
pygame.init()

WIDTH, HEIGHT = 900, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sun-Earth-Moon Simulation - SNM Project")

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
GREY = (200, 200, 200)
BLACK = (0, 0, 0)

FONT = pygame.font.SysFont("comicsans", 16)
CLOCK = pygame.time.Clock()

# -------------------- PARAMETERS --------------------
# Sun
SUN_X, SUN_Y = WIDTH // 2, HEIGHT // 2
SUN_RADIUS = 30

# Earth
EARTH_RADIUS = 12
 # EARTH_DISTANCE = 200          # distance from Sun in pixels
EARTH_SPEED = 0.01            # radians per frame

# Moon
MOON_RADIUS = 5
MOON_DISTANCE = 50             # distance from Earth in pixels
MOON_SPEED = EARTH_SPEED * 13              

# Initialize angles
earth_angle = 0
moon_angle = 0

# Orbit trails (stores recent positions)
earth_orbit = []
moon_orbit = []

# Simulation speed multiplier
speed_multiplier = 1.0

# -------------------- MAIN LOOP --------------------
run = True
paused = False
while run:
    CLOCK.tick(60)
    WIN.fill(BLACK)

    # -------------------- EVENTS --------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused
            if event.key == pygame.K_UP:
                speed_multiplier *= 1.5
            if event.key == pygame.K_DOWN:
                speed_multiplier /= 1.5

    if not paused:
        # Update angles
        earth_angle += EARTH_SPEED * speed_multiplier
        moon_angle += MOON_SPEED * speed_multiplier

    # -------------------- CALCULATE POSITIONS --------------------
    EARTH_A = 220   # semi-major axis (pixels)
    EARTH_B = 180   # semi-minor axis (pixels)
    earth_x = SUN_X + EARTH_A * math.cos(earth_angle)
    earth_y = SUN_Y + EARTH_B * math.sin(earth_angle)

    moon_x = earth_x + MOON_DISTANCE * math.cos(moon_angle)
    MOON_TILT = 0.2  # fraction to tilt orbit
    moon_y = earth_y + MOON_DISTANCE * math.sin(moon_angle) * (1 + MOON_TILT)

    # Add to orbit trails
    earth_orbit.append((int(earth_x), int(earth_y)))
    moon_orbit.append((int(moon_x), int(moon_y)))

    # Limit trail lengths for smooth effect
    if len(earth_orbit) > 100:
        earth_orbit.pop(0)
    if len(moon_orbit) > 100:
        moon_orbit.pop(0)

    # -------------------- DRAW --------------------
    # Sun
    pygame.draw.circle(WIN, YELLOW, (SUN_X, SUN_Y), SUN_RADIUS)
    sun_label = FONT.render("Sun", True, WHITE)
    WIN.blit(sun_label, (SUN_X - sun_label.get_width()//2, SUN_Y - SUN_RADIUS - 20))

    # Earth orbit trail
    if len(earth_orbit) > 2:
        pygame.draw.lines(WIN, BLUE, False, earth_orbit, 2)
    # Earth
    pygame.draw.circle(WIN, BLUE, (int(earth_x), int(earth_y)), EARTH_RADIUS)
    earth_label = FONT.render("Earth", True, WHITE)
    WIN.blit(earth_label, (int(earth_x) - earth_label.get_width()//2, int(earth_y) - EARTH_RADIUS - 20))

    # Moon orbit trail
    if len(moon_orbit) > 2:
        pygame.draw.lines(WIN, GREY, False, moon_orbit, 2)
    # Moon
    pygame.draw.circle(WIN, GREY, (int(moon_x), int(moon_y)), MOON_RADIUS)
    moon_label = FONT.render("Moon", True, WHITE)
    WIN.blit(moon_label, (int(moon_x) - moon_label.get_width()//2, int(moon_y) - MOON_RADIUS - 20))

    # -------------------- INFO --------------------
    info_label = FONT.render("SPACE: Pause | UP: Faster | DOWN: Slower", True, WHITE)
    WIN.blit(info_label, (10, 10))

    pygame.display.update()

pygame.quit()
