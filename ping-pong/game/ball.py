import pygame
import random

class Ball:
    def __init__(self, x, y, width, height, screen_width, screen_height,
                 sound_paddle=None, sound_wall=None, sound_score=None):
        self.original_x = x 
        self.original_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.velocity_x = random.choice([-5, 5])
        self.velocity_y = random.choice([-3, 3])

        # Optional sound hooks
        self.sound_paddle = sound_paddle
        self.sound_wall = sound_wall
        self.sound_score = sound_score

    def move(self):
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Wall bounce
        if self.y <= 0 or self.y + self.height >= self.screen_height:
            self.velocity_y *= -1
            if self.sound_wall:
                self.sound_wall.play()

    def check_collision(self, player, ai):
        player_rect = player.rect()
        ai_rect = ai.rect()
        ball_rect = self.rect()

        # Player paddle hit
        if ball_rect.colliderect(player_rect) and self.velocity_x < 0:
            self.x = player_rect.right
            self.velocity_x *= -1
            if self.sound_paddle:
                self.sound_paddle.play()

        # AI paddle hit
        elif ball_rect.colliderect(ai_rect) and self.velocity_x > 0:
            self.x = ai_rect.left - self.width
            self.velocity_x *= -1
            if self.sound_paddle:
                self.sound_paddle.play()

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.velocity_x *= -1
        self.velocity_y = random.choice([-3, 3])
        if self.sound_score:
            self.sound_score.play()

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
