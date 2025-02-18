import pygame
from circleshape import CircleShape
from shot import Shot
from constants import *
from explosion import Explosion

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.timer = 0
        self.lives = PLAYER_LIVES  # Add initial lives
        self.respawn_timer = 0  # Add respawn timer
        self.is_alive = True
        self.death_pause = 0  # Add death pause timer
        self.explosion = None  # Track explosion state
        

    # in the player class
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def draw(self, screen):
        # Flash the player during respawn
        if not self.is_alive:
            if self.death_pause > 0:
                return  # Don't draw player during death pause
            if int(self.respawn_timer * 15) % 2:  # Faster flashing (15 instead of 10)
                return
        
        # Draw the player triangle with a glow effect during respawn
        if not self.is_alive and self.respawn_timer > 0:
            # Draw glow
            points = self.triangle()
            glow_color = (100, 100, 255, 50)  # Blue glow
            pygame.draw.polygon(screen, glow_color, points, 0)  # Filled
        
        # Draw normal triangle
        glow_color = (100, 100, 255, 50)
        pygame.draw.polygon(screen, glow_color, self.triangle(), 2)

    def update(self, dt):
        if self.death_pause > 0:
            self.death_pause -= dt
            if self.death_pause <= 0:
                self.respawn()
            return
            
        if self.respawn_timer > 0:
            self.respawn_timer -= dt
            if self.respawn_timer <= 0:
                self.is_alive = True
        
        # Only process input if alive
        if self.is_alive:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                self.rotate(-dt)
            if keys[pygame.K_d]:
                self.rotate(dt)
            if keys[pygame.K_w]:
                self.move(dt)
            if keys[pygame.K_s]:
                self.move(-dt)
            if keys[pygame.K_SPACE]:
                self.shoot(dt)
        
        self.timer -= dt

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt
    
    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt
    
    def shoot(self, dt):
        if self.timer > 0:
            return
        shot = Shot(self.position.x, self.position.y, SHOT_RADIUS)
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        shot.velocity = forward * PLAYER_SHOT_SPEED
        self.timer = PLAYER_SHOT_COOLDOWN

    def collision(self, other):
        # Get the triangle points
        points = self.triangle()
        
        # Check if the center of the other object is inside our triangle
        center = other.position
        
        def point_in_triangle(px, py, ax, ay, bx, by, cx, cy):
            def sign(x1, y1, x2, y2, x3, y3):
                return (x1 - x3) * (y2 - y3) - (x2 - x3) * (y1 - y3)
            
            d1 = sign(px, py, ax, ay, bx, by)
            d2 = sign(px, py, bx, by, cx, cy)
            d3 = sign(px, py, cx, cy, ax, ay)
            
            has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
            has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)
            
            return not (has_neg and has_pos)
        
        # Check if any point of the other object's circle intersects with our triangle
        for angle in range(0, 360, 30):  # Check 12 points around the circle
            point = other.position + pygame.Vector2(0, other.radius).rotate(angle)
            if point_in_triangle(point.x, point.y, 
                               points[0].x, points[0].y,
                               points[1].x, points[1].y,
                               points[2].x, points[2].y):
                return True
        
        return False

    def lose_life(self):
        self.lives -= 1
        self.is_alive = False
        self.death_pause = 2.0  # 2 second pause before respawn
        # Create enhanced player explosion
        self.explosion = Explosion(self.position.x, self.position.y, self.radius * 4, True)
        if self.lives <= 0:
            return True
        return False
    
    def respawn(self):
        self.position.x = SCREEN_WIDTH / 2
        self.position.y = SCREEN_HEIGHT / 2
        self.rotation = 0
        self.is_alive = False
        self.respawn_timer = 2.0  # 2 seconds of invulnerability
