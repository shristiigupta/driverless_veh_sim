import pygame
from constants import *

class Vehicle:
    def __init__(self, x, y):
        self.image = pygame.image.load("assets/car.png")
        self.image = pygame.transform.scale(self.image, (VEHICLE_WIDTH, VEHICLE_HEIGHT))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = VEHICLE_SPEED

    def move_forward(self):
        self.rect.y -= self.speed

    def move_left(self):
        if self.rect.left > ROAD_LEFT:
            self.rect.x -= LANE_WIDTH

    def move_right(self):
        if self.rect.right < ROAD_RIGHT - VEHICLE_WIDTH:
            self.rect.x += LANE_WIDTH

    def stop(self):
        self.speed = 0

    def start(self):
        self.speed = VEHICLE_SPEED

    def draw(self, screen):
        screen.blit(self.image, self.rect)
