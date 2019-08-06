import pygame
import random


class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = 0
        self.gap_between = 200

        self.top_position = 0
        self.bottom_position = 0

        self.img = pygame.transform.scale2x(pygame.image.load('src/img/pipe.png').convert_alpha())
        self.pipe_top = pygame.transform.flip(self.img, False, True)
        self.pipe_bottom = self.img

        self.passed = False
        self.set_height()
        self.velocity = 5

    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top_position = self.height - self.pipe_top.get_height()
        self.bottom_position = self.height + self.gap_between

    def move(self):
        self.x -= self.velocity

    def draw(self, screen):
        # draw top pipe
        screen.blit(self.pipe_top, (self.x, self.top_position))

        # draw bottom pipe
        screen.blit(self.pipe_bottom, (self.x, self.bottom_position))

    def collide(self, bird):
        bird_mask = pygame.mask.from_surface(bird.img)
        top_mask = pygame.mask.from_surface(self.pipe_top)
        bottom_mask = pygame.mask.from_surface(self.pipe_bottom)
        top_offset = (self.x - bird.x, self.top_position - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom_position - round(bird.y))

        bottom_collision = bird_mask.overlap(bottom_mask, bottom_offset)
        top_collision = bird_mask.overlap(top_mask, top_offset)

        if top_collision or bottom_collision:
            return True
        return False
