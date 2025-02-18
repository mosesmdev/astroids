import pygame
import random
from constants import *

class Starfield:
    def __init__(self, num_stars=100):
        self.stars = []
        for _ in range(num_stars):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            brightness = random.randint(50, 255)
            size = random.randint(1, 3)
            self.stars.append({
                'pos': (x, y),
                'color': (brightness, brightness, brightness),
                'size': size
            })
    
    def draw(self, screen):
        for star in self.stars:
            pygame.draw.circle(screen, star['color'], star['pos'], star['size']) 