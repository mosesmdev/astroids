import pygame

class Score:
    def __init__(self):
        self.value = 0
        self.font = pygame.font.Font(None, 36)
        self.high_score = 0  # Add high score tracking
        
    def add_points(self, asteroid_radius, min_radius):
        # Calculate size multiplier (how many times bigger than minimum)
        size = asteroid_radius // min_radius
        if size == 1:  # Small
            self.value += 25
        elif size == 2:  # Medium
            self.value += 100
        else:  # Large
            self.value += 250
    
    def reset(self):
        self.high_score = max(self.high_score, self.value)
        self.value = 0
    
    def draw(self, screen):
        score_text = self.font.render(f"Score: {self.value}", True, (255, 255, 255))
        score_rect = score_text.get_rect()
        score_rect.topright = (screen.get_width() - 20, 20)
        screen.blit(score_text, score_rect) 