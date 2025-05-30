import pygame
import random
from constants import *

class Obstacle:
    def __init__(self):
        lane = random.choice(range(NUM_LANES))
        x = ROAD_LEFT + lane * LANE_WIDTH + (LANE_WIDTH - 50) // 2
        y = random.randint(100, SCREEN_HEIGHT - 200)
        self.rect = pygame.Rect(x, y, 50, 50)

    def draw(self, screen):
        pygame.draw.rect(screen, RED, self.rect)
