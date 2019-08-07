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
        self.num_alive = 0

    def start(self):
        self.game_loop()

    def draw_score(self, score):
        pygame.font.init()
        font = pygame.font.SysFont('Arial', 24)
        text_surface = font.render(f'Score: {score}', True, (255, 255, 255))
        self.screen.blit(text_surface, (10, 10))

    def draw_num_of_alive(self):
        pygame.font.init()
        font = pygame.font.SysFont('Arial', 24)
        text_surface = font.render(f'Alive: {self.num_alive}', True, (255, 255, 255))
        self.screen.blit(text_surface, (100, 10))

    def draw_screen(self, birds, pipes, ground):
        self.screen.blit(self.bg_img, (0, 0))
        [pipe.draw(self.screen) for pipe in pipes]
        [bird.draw(self.screen) for bird in birds]
        ground.draw(self.screen)
        self.draw_score(self.score)
        self.draw_num_of_alive()

        clock.tick(30)
        pygame.display.update()

    def move(self, birds, ground, pipes):
        [bird.move() for bird in birds]
        [pipe.move() for pipe in pipes]
        ground.move()

    def collision(self, birds, pipes):
        to_remove = []
        add_pipe = False

        for pipe in pipes:
            for bird in birds:
                if pipe.collide(bird):
                    birds.remove(bird)

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

        for bird in birds:
            if bird.y + bird.img.get_height() >= self.base or bird.y < 0:
                birds.remove(bird)

    def is_running(self, birds):
        self.num_alive = len(birds)
        if self.num_alive == 0:
            self.run = False

    def restart(self):
        self.score = 0
        self.run = True
        return [Bird(240, 350) for _ in range(50)], Ground(self.base, self.screen_width), [Pipe(700)]

    def game_loop(self):
        birds = [Bird(240, 350) for _ in range(50)]
        ground = Ground(self.base, self.screen_width)
        pipes = [Pipe(700)]
        self.run = True
        self.num_alive = len(birds)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    birds, ground, pipes = self.restart()

            while self.run:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        birds[0].jump()

                self.move(birds, ground, pipes)
                self.collision(birds, pipes)
                self.is_running(birds)
                self.draw_screen(birds, pipes, ground)
