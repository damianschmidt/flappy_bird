import pygame
from flappy_bird.bird import Bird
from flappy_bird.pipe import Pipe
from flappy_bird.ground import Ground

pygame.init()
pygame.display.set_caption('Flappy Bird')
clock = pygame.time.Clock()


class Game:
    def __init__(self):
        self.screen_width = 600
        self.screen_height = 800
        self.base = 730
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.bg_img = pygame.transform.scale(pygame.image.load('src/img/background.png').convert_alpha(), (600, 900))
        self.score = 0
        self.run = False

    def start(self):
        self.game_loop()

    def draw_score(self, score):
        pygame.font.init()
        font = pygame.font.SysFont('Arial', 24)
        text_surface = font.render(f'Score: {score}', True, (255, 255, 255))
        self.screen.blit(text_surface, (10, 10))

    def draw_screen(self, bird, pipes, ground):
        self.screen.blit(self.bg_img, (0, 0))
        for pipe in pipes:
            pipe.draw(self.screen)
        ground.draw(self.screen)
        bird.draw(self.screen)
        self.draw_score(self.score)

        clock.tick(30)
        pygame.display.update()

    def move(self, bird, ground, pipes):
        bird.move()
        ground.move()
        for pipe in pipes:
            pipe.move()

    def collision(self, bird, pipes):
        to_remove = []
        add_pipe = False

        for pipe in pipes:
            if pipe.collide(bird):
                self.run = False

            if pipe.x + pipe.pipe_top.get_width() < 0:
                to_remove.append(pipe)

            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True

            if add_pipe:
                add_pipe = False
                self.score += 1
                pipes.append(Pipe(self.screen_width))

        for item in to_remove:
            pipes.remove(item)

        if bird.y + bird.img.get_height() >= self.base or bird.y < 0:
            self.run = False

    def restart(self):
        self.score = 0
        self.run = True
        return Bird(240, 350), Ground(self.base, self.screen_width), [Pipe(700)]

    def game_loop(self):
        bird = Bird(240, 350)
        ground = Ground(self.base, self.screen_width)
        pipes = [Pipe(700)]
        self.run = True

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    bird, ground, pipes = self.restart()

            while self.run:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.run = False
                        pygame.quit()
                        quit()
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        bird.jump()

                self.move(bird, ground, pipes)
                self.collision(bird, pipes)
                self.draw_screen(bird, pipes, ground)
