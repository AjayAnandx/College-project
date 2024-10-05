import pygame
import speedtest
import threading
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Internet Speed Test")

# Fonts
font = pygame.font.SysFont(None, 55)
small_font = pygame.font.SysFont(None, 35)

# Speed test results
download_speed = 0
upload_speed = 0

# Function to perform the speed test
def perform_speed_test():
    global download_speed, upload_speed
    st = speedtest.Speedtest()
    st.download()
    st.upload()

    download_speed = st.results.dict()["download"] / 1_000_000  # Convert to Mbps
    upload_speed = st.results.dict()["upload"] / 1_000_000  # Convert to Mbps

# Function to draw the needle
def draw_needle(angle, length, color, center, width=5):
    end_x = center[0] + length * math.cos(math.radians(angle))
    end_y = center[1] + length * math.sin(math.radians(angle))
    pygame.draw.line(screen, color, center, (end_x, end_y), width)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                threading.Thread(target=perform_speed_test).start()

    screen.fill(WHITE)

    # Draw the speedometer backgrounds
    pygame.draw.circle(screen, BLACK, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2), 150, 5)
    pygame.draw.circle(screen, BLACK, (3 * SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2), 150, 5)

    # Draw the needles
    download_angle = -90 + (download_speed / 100) * 180  # Map download speed to angle
    upload_angle = -90 + (upload_speed / 100) * 180  # Map upload speed to angle

    draw_needle(download_angle, 130, RED, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2))
    draw_needle(upload_angle, 130, GREEN, (3 * SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2))

    # Display the speeds
    download_text = font.render(f"Download: {download_speed:.2f} Mbps", True, BLACK)
    upload_text = font.render(f"Upload: {upload_speed:.2f} Mbps", True, BLACK)
    screen.blit(download_text, (SCREEN_WIDTH // 4 - 100, SCREEN_HEIGHT // 2 + 160))
    screen.blit(upload_text, (3 * SCREEN_WIDTH // 4 - 100, SCREEN_HEIGHT // 2 + 160))

    # Instructions
    instructions_text = small_font.render("Press SPACE to test speed", True, BLACK)
    screen.blit(instructions_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT - 50))

    pygame.display.flip()

pygame.quit()
