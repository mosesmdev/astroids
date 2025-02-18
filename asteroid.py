import pygame
import random
from circleshape import CircleShape
from constants import *

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        # Generate random vertices for the asteroid shape
        self.vertices = []
        num_vertices = random.randint(8, 12)  # Random number of vertices
        for i in range(num_vertices):
            angle = i * (360 / num_vertices)
            # Vary the radius by up to 30% to create irregular shape
            distance = self.radius * random.uniform(0.7, 1.0)
            point = pygame.Vector2(0, distance).rotate(angle)
            self.vertices.append(point)
        
        # Create texture surface
        size = int(radius * 2.2)  # Make slightly larger than asteroid
        self.texture = pygame.Surface((size, size), pygame.SRCALPHA)
        
        # Generate noise pattern
        for x in range(size):
            for y in range(size):
                # Create noisy pattern
                noise = random.uniform(0, 1)
                if noise > 0.6:  # Adjust threshold for more/less texture
                    alpha = random.randint(30, 80)
                    pygame.draw.circle(self.texture, (150, 150, 150, alpha), (x, y), 1)
    
    def draw(self, screen):
        # Create a mask surface for the asteroid shape
        size = int(self.radius * 2.2)
        mask = pygame.Surface((size, size), pygame.SRCALPHA)
        
        # Draw the polygon on the mask
        local_points = [(vertex.x + size/2, vertex.y + size/2) for vertex in self.vertices]
        pygame.draw.polygon(mask, (255, 255, 255, 255), local_points)
        
        # Create base surface with solid dark gray color
        base = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.polygon(base, (50, 50, 50, 255), local_points)
        
        # Create textured surface
        textured = self.texture.copy()
        textured.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        
        # Combine base and texture
        base.blit(textured, (0, 0))
        
        # Draw the final textured asteroid
        texture_pos = (self.position.x - size/2, self.position.y - size/2)
        screen.blit(base, texture_pos)
        
        # Draw outline
        points = [(self.position.x + vertex.x, self.position.y + vertex.y) 
                 for vertex in self.vertices]
        pygame.draw.polygon(screen, "White", points, 2)
    
    def update(self, dt):
        self.position += self.velocity * dt
        
        # Wrap around screen edges
        if self.position.x < -self.radius:
            self.position.x = SCREEN_WIDTH + self.radius
        elif self.position.x > SCREEN_WIDTH + self.radius:
            self.position.x = -self.radius
            
        if self.position.y < -self.radius:
            self.position.y = SCREEN_HEIGHT + self.radius
        elif self.position.y > SCREEN_HEIGHT + self.radius:
            self.position.y = -self.radius
    
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