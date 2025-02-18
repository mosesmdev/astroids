import pygame
from constants import *
from asteroidfield import *
from player import Player
from asteroid import Asteroid
from shot import Shot
from starfield import Starfield
from score import Score
from gameover import GameOver
from explosion import Explosion

class Game:
    def __init__(self, score=None):
        pygame.init()
        self.setup_groups()
        self.setup_screen()
        self.score = score if score else Score()
        self.setup_game_objects()
        self.clock = pygame.time.Clock()
        self.running = True
        self.dt = 0
        self.game_over_menu = None
        
    def setup_groups(self):
        self.updatable = pygame.sprite.Group()
        self.drawable = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()
        self.shots = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()
        
        # Set up sprite containers
        Player.containers = (self.updatable, self.drawable)
        Asteroid.containers = (self.asteroids, self.updatable, self.drawable)
        AsteroidField.containers = (self.updatable,)
        Shot.containers = (self.shots, self.updatable, self.drawable)
        Explosion.containers = (self.explosions, self.updatable, self.drawable)
    
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
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
    
    def check_collisions(self):
        for asteroid in self.asteroids:
            if asteroid.collision(self.player) and self.player.is_alive:
                if self.player.lose_life():
                    self.game_over_menu = GameOver(self.screen, self.score)
                return
            
            for bullet in self.shots:
                if bullet.collision(asteroid):
                    Explosion(asteroid.position.x, asteroid.position.y, asteroid.radius)
                    self.score.add_points(asteroid.radius, ASTEROID_MIN_RADIUS)
                    asteroid.split()
                    bullet.kill()
    
    def update(self):
        self.updatable.update(self.dt)
        self.check_collisions()
    
    def draw_lives(self):
        life_x = 20
        life_y = 20
        for i in range(self.player.lives):
            pygame.draw.polygon(self.screen, "white", [
                (life_x + 20, life_y),
                (life_x, life_y + 30),
                (life_x + 40, life_y + 30)
            ], 2)
            life_x += 50
    
    def draw(self):
        self.screen.fill((0, 0, 0))
        self.starfield.draw(self.screen)
        for item in self.drawable:
            item.draw(self.screen)
        self.score.draw(self.screen)
        self.draw_lives()
        pygame.display.flip()
    
    def run(self):
        while self.running:
            if self.game_over_menu:
                action = self.game_over_menu.handle_input()
                if action == "restart":
                    self.score.reset()  # Reset score before creating new game
                    self.__init__(self.score)  # Pass existing score object
                elif action == "quit":
                    self.running = False
                else:
                    self.game_over_menu.draw()
                    pygame.display.flip()
            else:
                self.handle_events()
                self.update()
                self.draw()
                self.dt = self.clock.tick(60) / 1000
        
        pygame.quit()
