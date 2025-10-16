import pygame
from .paddle import Paddle
from .ball import Ball

# Game Engine
 
WHITE = (255, 255, 255)

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        # Sound effects
        self.sound_paddle = pygame.mixer.Sound("game/paddle_hit.wav")
        self.sound_wall = pygame.mixer.Sound("game/wall_bounce.wav")
        self.sound_score = pygame.mixer.Sound("game/score.wav")

        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(
            width // 2, height // 2, 7, 7, width, height,
            sound_paddle=self.sound_paddle,
            sound_wall=self.sound_wall,
            sound_score=self.sound_score
        )


        self.player_score = 0
        self.ai_score = 0
        self.font = pygame.font.SysFont("Arial", 30)
        self.winning_score = 5  # default target
        self.game_over = False

        



    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-10, self.height)
        if keys[pygame.K_s]:
            self.player.move(10, self.height)

    def update(self):
        if self.game_over:
            return  # freeze gameplay updates until replay menu handled

        self.ball.move()
        self.ball.check_collision(self.player, self.ai)

        if self.ball.x <= 0:
            self.ai_score += 1
            self.ball.reset()
        elif self.ball.x >= self.width:
            self.player_score += 1
            self.ball.reset()

        self.ai.auto_track(self.ball, self.height)

        # Check for win condition
        self.check_game_over(pygame.display.get_surface())



    def render(self, screen):
        # Draw paddles and ball
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(screen, WHITE, (self.width//2, 0), (self.width//2, self.height))

        # Draw score
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width//4, 20))
        screen.blit(ai_text, (self.width * 3//4, 20))

    def check_game_over(self, screen):
        if self.player_score >= self.winning_score or self.ai_score >= self.winning_score:
            self.game_over = True
            winner_text = "Player Wins!" if self.player_score >= self.winning_score else "AI Wins!"

            # Display winner
            screen.fill((0, 0, 0))
            text_surface = self.font.render(winner_text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(self.width // 2, self.height // 2 - 50))
            screen.blit(text_surface, text_rect)

            # Display replay menu
            menu_lines = [
                "Press 3 for Best of 3",
                "Press 5 for Best of 5",
                "Press 7 for Best of 7",
                "Press ESC to Exit"
            ]
            for i, line in enumerate(menu_lines):
                option_text = self.font.render(line, True, (200, 200, 200))
                screen.blit(option_text, (self.width // 2 - 150, self.height // 2 + i * 40))

            pygame.display.flip()

            self.show_replay_menu()

    def show_replay_menu(self):
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_3:
                        self.winning_score = 2  # best of 3 → first to 2
                        waiting = False
                    elif event.key == pygame.K_5:
                        self.winning_score = 3  # best of 5 → first to 3
                        waiting = False
                    elif event.key == pygame.K_7:
                        self.winning_score = 4  # best of 7 → first to 4
                        waiting = False
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()

            # Limit menu FPS to avoid 100% CPU
            pygame.time.wait(100)

        # Reset for new game
        self.player_score = 0
        self.ai_score = 0
        self.ball.reset()
        self.game_over = False
