import pygame
import random
from constants import *

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, size, is_player=False):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.position = pygame.Vector2(x, y)
        self.particles = []
        self.lifetime = 1.5 if is_player else 1.0  # Longer lifetime for player explosion
        
        # Create particles
        num_particles = size if is_player else size // 2  # More particles for player
        for _ in range(num_particles):
            angle = random.uniform(0, 360)
            speed = random.uniform(100, 300) if is_player else random.uniform(50, 200)  # Faster for player
            size = random.uniform(2, 4) if is_player else random.uniform(1, 3)  # Bigger for player
            lifetime = random.uniform(0.8, 1.5) if is_player else random.uniform(0.5, 1.0)
            color = random.choice([(255, 255, 255), (255, 200, 50), (255, 50, 50)]) if is_player else (255, 255, 255)
            self.particles.append({
                'velocity': pygame.Vector2(0, speed).rotate(angle),
                'pos': pygame.Vector2(self.position),
                'size': size,
                'lifetime': lifetime,
                'max_lifetime': lifetime,
                'color': color  # Add color to particles
            })
    
    def update(self, dt):
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.kill()
            return
        
        # Update particles
        for particle in self.particles:
            particle['lifetime'] -= dt
            particle['pos'] += particle['velocity'] * dt
    
    def draw(self, screen):
        for particle in self.particles:
            if particle['lifetime'] > 0:
                # Fade out particle
                alpha = int((particle['lifetime'] / particle['max_lifetime']) * 255)
                color = (*particle['color'], alpha)  # Use particle's color
                
                # Draw particle
                surf = pygame.Surface((particle['size'] * 2, particle['size'] * 2), pygame.SRCALPHA)
                pygame.draw.circle(surf, color, 
                                (particle['size'], particle['size']), 
                                particle['size'])
                screen.blit(surf, particle['pos'] - pygame.Vector2(particle['size'], particle['size'])) 