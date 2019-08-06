import pygame


class Ground:
    def __init__(self, y, width):
        self.width = width
        self.y = y
        self.x_start = 0
        self.x_end = self.width
        self.img = pygame.transform.scale(pygame.image.load('src/img/ground.png').convert_alpha(), (self.width, 300))
        self.velocity = 5

    def move(self):
        self.x_start -= self.velocity
        self.x_end -= self.velocity

        if self.x_start + self.width < 0:
            self.x_start = self.x_end + self.width

        if self.x_end + self.width < 0:
            self.x_end = self.x_start + self.width

    def draw(self, screen):
        screen.blit(self.img, (self.x_start, self.y))
        screen.blit(self.img, (self.x_end, self.y))
