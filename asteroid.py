import pygame
import random
from circleshape import CircleShape
from constants import *

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
    
    def draw(self, screen):
        pygame.draw.circle(screen, "White", (self.position.x, self.position.y), self.radius, 2)
    
    def update(self, dt):
        self.position += self.velocity * dt
    
    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        random_angle = random.uniform(20, 50)
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        a1 = Asteroid(self.position.x, self.position.y, new_radius)
        a2 = Asteroid(self.position.x, self.position.y, new_radius)
        
        speed = self.velocity.length() * 1.2
        forward_a1 = self.velocity.normalize().rotate(random_angle)
        forward_a2 = self.velocity.normalize().rotate(-random_angle)
        a1.velocity = forward_a1 * speed
        a2.velocity = forward_a2 * speed