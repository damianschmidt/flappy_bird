import random
import pygame

# Global config
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
BASE = 730

pygame.init()
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Bird')

# Images load
pipe_img = pygame.transform.scale2x(pygame.image.load('src/img/pipe.png').convert_alpha())
bg_img = pygame.transform.scale(pygame.image.load('src/img/background.png').convert_alpha(), (600, 900))
bird_img = [pygame.transform.scale2x(pygame.image.load(f'src/img/bird{str(x)}.png')) for x in range(1, 4)]
ground_img = pygame.transform.scale(pygame.image.load('src/img/ground.png').convert_alpha(), (SCREEN_WIDTH, 300))


class Bird:
    imgs = bird_img
    rotation_velocity = 8
    max_rotation = 25

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity = 0

        self.fall_time = 0
        self.rotation = 0
        self.animation_time = 5
        self.img_count = 0
        self.img = self.imgs[0]

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


class Pipe:
    img = pipe_img
    velocity = 5

    def __init__(self, x):
        self.x = x
        self.height = 0
        self.gap_between = 200

        self.top_position = 0
        self.bottom_position = 0

        self.pipe_top = pygame.transform.flip(self.img, False, True)
        self.pipe_bottom = self.img

        self.passed = False
        self.set_height()

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


class Ground:
    width = SCREEN_WIDTH
    velocity = 5

    def __init__(self, y):
        self.y = y
        self.x_start = 0
        self.x_end = self.width

    def move(self):
        self.x_start -= self.velocity
        self.x_end -= self.velocity

        if self.x_start + self.width < 0:
            self.x_start = self.x_end + self.width

        if self.x_end + self.width < 0:
            self.x_end = self.x_start + self.width

    def draw(self, screen):
        screen.blit(ground_img, (self.x_start, self.y))
        screen.blit(ground_img, (self.x_end, self.y))


def end_screen(screen):
    pass


def draw_screen(screen, bird, pipes, ground, score):
    screen.blit(bg_img, (0, 0))
    for pipe in pipes:
        pipe.draw(screen)

    ground.draw(screen)

    bird.draw(screen)

    draw_score(score, screen)

    pygame.display.update()


def draw_score(score, screen):
    font = pygame.font.SysFont('Arial', 24)
    text_surface = font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(text_surface, (10, 10))


def restart():
    global bird, ground, pipes, score, run
    bird = Bird(240, 350)
    ground = Ground(BASE)
    pipes = [Pipe(700)]
    score = 0
    run = True


if __name__ == '__main__':
    bird = Bird(240, 350)
    ground = Ground(BASE)
    pipes = [Pipe(700)]
    score = 0

    clock = pygame.time.Clock()
    run = True
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                restart()
        while run:
            clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    bird.jump()

            bird.move()
            ground.move()

            to_remove = []
            add_pipe = False
            for pipe in pipes:
                pipe.move()

                # check collision
                if pipe.collide(bird):
                    run = False

                if pipe.x + pipe.pipe_top.get_width() < 0:
                    to_remove.append(pipe)

                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True

            if add_pipe:
                score += 1
                pipes.append(Pipe(SCREEN_WIDTH))

            for item in to_remove:
                pipes.remove(item)

            # collision with sky and ground
            if bird.y + bird.img.get_height() >= BASE or bird.y < 0:
                run = False

            # draw
            draw_screen(SCREEN, bird, pipes, ground, score)
