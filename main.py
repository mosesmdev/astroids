# this allows us to use code from
# the open-source pygame library
# throughout this file
import pygame
from constants import *
from asteroidfield import *
from player import Player
from asteroid import Asteroid
from shot import Shot
from starfield import Starfield
from score import Score

def main():
    pygame.init()
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    Shot.containers = (shots, updatable, drawable)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    clock = pygame.time.Clock()
    dt = 0
    running = True
    playerx = SCREEN_WIDTH / 2
    playery = SCREEN_HEIGHT / 2
    player = Player(playerx, playery)
    asteroidfield = AsteroidField()
    starfield = Starfield(150)  # Create 150 stars
    score = Score()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill((0, 0, 0))
        starfield.draw(screen)   # Draw stars before other elements
        updatable.update(dt)
        for asteroid in asteroids:
            if asteroid.collision(player):
                print("Game Over!")
                running = False
            for bullet in shots:
                if bullet.collision(asteroid):
                    score.add_points(asteroid.radius, ASTEROID_MIN_RADIUS)
                    asteroid.split()
                    bullet.kill()
        for item in drawable:
            item.draw(screen)
        score.draw(screen)  # Draw score last so it's on top
        pygame.display.flip()
        dt = clock.tick(60) / 1000

    pygame.quit()

if __name__ == "__main__":
    main()