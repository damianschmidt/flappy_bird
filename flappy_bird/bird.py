import pygame


class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity = 0
        self.fall_time = 0
        self.rotation = 0
        self.animation_time = 5
        self.img_count = 0
        self.imgs = [pygame.transform.scale2x(pygame.image.load(f'src/img/bird{str(x)}.png')) for x in range(1, 4)]
        self.img = self.imgs[0]
        self.rotation_velocity = 5
        self.max_rotation = 25

    def jump(self):
        self.fall_time = 0
        self.velocity = -10

    def move(self):
        self.fall_time += 1

        up_force = self.velocity * self.fall_time
        down_force = 1.5 * self.fall_time ** 2

        fall_down = up_force + down_force

        if fall_down >= 16:
            fall_down = (fall_down / abs(fall_down)) * 16

        if fall_down < 0:
            fall_down -= 2

        self.y = self.y + fall_down

        if fall_down < 0:
            if self.rotation < self.max_rotation:
                self.rotation = self.max_rotation
        else:
            if self.rotation > -90:
                self.rotation -= self.rotation_velocity

    def draw(self, screen):
        self.img_count += 1

        if self.img_count <= self.animation_time:
            self.img = self.imgs[0]
        elif self.img_count <= 2 * self.animation_time:
            self.img = self.imgs[1]
        elif self.img_count <= 3 * self.animation_time:
            self.img = self.imgs[2]
        elif self.img_count <= 4 * self.animation_time + 1:
            self.img = self.imgs[0]
            self.img_count = 0

        rotated_bird = pygame.transform.rotate(self.img, self.rotation)
        new_rect = rotated_bird.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)

        screen.blit(rotated_bird, new_rect)
