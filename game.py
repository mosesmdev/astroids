import pygame
from constants import *
from asteroidfield import *
from player import Player
from asteroid import Asteroid
from shot import Shot
from starfield import Starfield
from score import Score

class Game:
    def __init__(self):
        pygame.init()
        self.setup_groups()
        self.setup_screen()
        self.setup_game_objects()
        self.clock = pygame.time.Clock()
        self.running = True
        self.dt = 0
        
    def setup_groups(self):
        self.updatable = pygame.sprite.Group()
        self.drawable = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()
        self.shots = pygame.sprite.Group()
        
        # Set up sprite containers
        Player.containers = (self.updatable, self.drawable)
        Asteroid.containers = (self.asteroids, self.updatable, self.drawable)
        AsteroidField.containers = (self.updatable,)
        Shot.containers = (self.shots, self.updatable, self.drawable)
    
    def setup_screen(self):
        self.screen = pygame.display.set_mode(
            (SCREEN_WIDTH, SCREEN_HEIGHT), 
            pygame.SRCALPHA
        )
    
    def setup_game_objects(self):
        player_pos = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.player = Player(*player_pos)
        self.asteroid_field = AsteroidField()
        self.starfield = Starfield(150)
        self.score = Score()
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
    
    def check_collisions(self):
        for asteroid in self.asteroids:
            if asteroid.collision(self.player):
                print("Game Over!")
                self.running = False
                return
                
            for bullet in self.shots:
                if bullet.collision(asteroid):
                    self.score.add_points(asteroid.radius, ASTEROID_MIN_RADIUS)
                    asteroid.split()
                    bullet.kill()
    
    def update(self):
        self.updatable.update(self.dt)
        self.check_collisions()
    
    def draw(self):
        self.screen.fill((0, 0, 0))
        self.starfield.draw(self.screen)
        for item in self.drawable:
            item.draw(self.screen)
        self.score.draw(self.screen)
        pygame.display.flip()
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.dt = self.clock.tick(60) / 1000
        
        pygame.quit()
