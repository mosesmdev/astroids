import pygame
from constants import *

class GameOver:
    def __init__(self, screen, score):
        self.screen = screen
        self.score = score
        self.font_large = pygame.font.Font(None, 74)
        self.font_small = pygame.font.Font(None, 36)
        self.selected_option = 0
        self.options = ["Play Again", "Quit"]
        
    def draw(self):
        # Draw semi-transparent background
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)
        self.screen.blit(overlay, (0, 0))
        
        # Draw Game Over text
        game_over = self.font_large.render("GAME OVER", True, (255, 0, 0))
        game_over_rect = game_over.get_rect(centerx=SCREEN_WIDTH/2, centery=SCREEN_HEIGHT/3)
        self.screen.blit(game_over, game_over_rect)
        
        # Draw score
        score_text = self.font_small.render(f"Final Score: {self.score.value}", True, (255, 255, 255))
        score_rect = score_text.get_rect(centerx=SCREEN_WIDTH/2, centery=SCREEN_HEIGHT/2)
        self.screen.blit(score_text, score_rect)
        
        # Draw menu options
        for i, option in enumerate(self.options):
            color = (255, 255, 0) if i == self.selected_option else (255, 255, 255)
            text = self.font_small.render(option, True, color)
            rect = text.get_rect(centerx=SCREEN_WIDTH/2, 
                               centery=SCREEN_HEIGHT*2/3 + i*50)
            self.screen.blit(text, rect)
    
    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_option = (self.selected_option - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    if self.selected_option == 0:
                        return "restart"
                    else:
                        return "quit"
        return None 