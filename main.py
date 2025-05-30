import pygame
from constants import *
from vehicle import Vehicle
from environment import Obstacle

def is_lane_clear(vehicle, obstacles, target_lane):
    x = ROAD_LEFT + target_lane * LANE_WIDTH + (LANE_WIDTH - VEHICLE_WIDTH) // 2
    for obs in obstacles:
        obs_lane = (obs.rect.x - ROAD_LEFT) // LANE_WIDTH
        if obs_lane == target_lane:
            if obs.rect.y < vehicle.rect.y and vehicle.rect.y - obs.rect.y < 120:
                return False
    return True

def get_lane(rect):
    return (rect.x - ROAD_LEFT) // LANE_WIDTH

def get_lane_center_x(lane):
    return ROAD_LEFT + lane * LANE_WIDTH + (LANE_WIDTH - VEHICLE_WIDTH) // 2

def check_obstacle_ahead(vehicle, obstacles, lane):
    for obs in obstacles:
        obs_lane = get_lane(obs.rect)
        ahead = obs.rect.y < vehicle.rect.y and vehicle.rect.y - obs.rect.y < 120
        if obs_lane == lane and ahead:
            return True
    return False

def find_clear_lane(vehicle, obstacles, current_lane):
    for offset in range(1, NUM_LANES):
        left_lane = current_lane - offset
        right_lane = current_lane + offset
        if left_lane >= 0 and is_lane_clear(vehicle, obstacles, left_lane):
            return left_lane
        if right_lane < NUM_LANES and is_lane_clear(vehicle, obstacles, right_lane):
            return right_lane
    return None

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Autonomous Driverless Vehicle Simulation")
clock = pygame.time.Clock()

vehicle = Vehicle(get_lane_center_x(0), SCREEN_HEIGHT - 100)
obstacles = [Obstacle() for _ in range(5)]


state = "forward"
target_x = vehicle.rect.x
reverse_frames = 0
MAX_REVERSE_FRAMES = 30
lane_change_speed = 8

running = True
while running:
    screen.fill(GRAY)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    vehicle_lane = get_lane(vehicle.rect)
    obstacle_ahead = check_obstacle_ahead(vehicle, obstacles, vehicle_lane)

    if state == "forward":
        if obstacle_ahead:
            target_lane = find_clear_lane(vehicle, obstacles, vehicle_lane)
            if target_lane is not None:
                target_x = get_lane_center_x(target_lane)
                state = "changing_lane"
            else:
                state = "reversing"
                reverse_frames = 0
        else:
            vehicle.start()
            vehicle.move_forward()

    elif state == "reversing":
        vehicle.stop()
        vehicle.rect.y += VEHICLE_SPEED  
        reverse_frames += 1
        if reverse_frames >= MAX_REVERSE_FRAMES:
            vehicle_lane = get_lane(vehicle.rect)
            target_lane = find_clear_lane(vehicle, obstacles, vehicle_lane)
            if target_lane is not None:
                target_x = get_lane_center_x(target_lane)
                state = "changing_lane"
            else:
                reverse_frames = 0  

    elif state == "changing_lane":
        vehicle.stop()
        if abs(vehicle.rect.x - target_x) <= lane_change_speed:
            vehicle.rect.x = target_x
            state = "forward"
        else:
            if vehicle.rect.x < target_x:
                vehicle.rect.x += lane_change_speed
            else:
                vehicle.rect.x -= lane_change_speed

    pygame.draw.rect(screen, BLACK, (ROAD_LEFT, 0, ROAD_WIDTH, SCREEN_HEIGHT))
    for i in range(1, NUM_LANES):
        x = ROAD_LEFT + i * LANE_WIDTH
        pygame.draw.line(screen, WHITE, (x, 0), (x, SCREEN_HEIGHT), 2)

    vehicle.draw(screen)
    for obs in obstacles:
        obs.draw(screen)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
