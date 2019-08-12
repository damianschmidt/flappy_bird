import pygame
import neat
import visualize

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
        self.generation = 0

    def start(self):
        self.game_loop()

    def draw_score(self):
        pygame.font.init()
        font = pygame.font.SysFont('Arial', 24)
        score_surface = font.render(f'Score: {self.score}', True, (255, 255, 255))
        gen_surface = font.render(f'Generation: {self.generation}', True, (255, 255, 255))
        self.screen.blit(gen_surface, (10, 10))
        self.screen.blit(score_surface, (10, 60))

    def draw_num_of_alive(self, alive):
        pygame.font.init()
        font = pygame.font.SysFont('Arial', 24)
        text_surface = font.render(f'Alive: {alive}', True, (255, 255, 255))
        self.screen.blit(text_surface, (10, 110))

    def draw_screen(self, birds, pipes, ground, pipe_ind, draw_line=False):
        self.screen.blit(self.bg_img, (0, 0))
        [pipe.draw(self.screen) for pipe in pipes]
        [bird.draw(self.screen) for bird in birds]
        ground.draw(self.screen)
        self.draw_score()
        self.draw_num_of_alive(len(birds))

        if draw_line:
            for bird in birds:
                try:
                    pygame.draw.line(self.screen, (255, 0, 0),
                                     (bird.x + bird.img.get_width() / 2, bird.y + bird.img.get_height() / 2),
                                     (pipes[pipe_ind].x + pipes[pipe_ind].pipe_top.get_width() / 2,
                                      pipes[pipe_ind].height),
                                     5)
                    pygame.draw.line(self.screen, (255, 0, 0),
                                     (bird.x + bird.img.get_width() / 2, bird.y + bird.img.get_height() / 2), (
                                         pipes[pipe_ind].x + pipes[pipe_ind].pipe_bottom.get_width() / 2,
                                         pipes[pipe_ind].bottom_position), 5)
                except:
                    pass

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
        if len(birds) == 0:
            self.run = False

    def restart(self):
        self.score = 0
        self.run = True
        return [Bird(240, 350) for _ in range(50)], Ground(self.base, self.screen_width), [Pipe(700)]

    def game_loop(self):
        birds = [Bird(240, 350)]
        ground = Ground(self.base, self.screen_width)
        pipes = [Pipe(700)]
        self.run = True

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
                self.draw_screen(birds, pipes, ground, 0)

    def eval_genomes(self, genomes, config):
        self.generation += 1

        nets = []
        birds = []
        genomes_list = []

        for genome_id, genome in genomes:
            genome.fitness = 0
            net = neat.nn.FeedForwardNetwork.create(genome, config)

            nets.append(net)
            birds.append(Bird(230, 350))
            genomes_list.append(genome)

        # Build game
        ground = Ground(self.base, self.screen_width)
        pipes = [Pipe(700)]
        self.score = 0
        self.run = True

        while self.run and len(birds) > 0:
            clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                    pygame.quit()
                    quit()

            # On which pipe NEAT should take care of
            pipe_index = 0
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].pipe_top.get_width():
                pipe_index = 1

            for i, bird in enumerate(birds):
                genomes_list[i].fitness += 0.1
                bird.move()

                # give bird, top pipe and bottom pipe height to make jump decision
                output = nets[i].activate(
                    (bird.y, abs(bird.y - pipes[pipe_index].height), abs(bird.y - pipes[pipe_index].bottom_position)))

                if output[0] > 0.5:
                    bird.jump()

            ground.move()
            [pipe.move() for pipe in pipes]

            pipes_to_remove = []
            add_pipe = False

            for pipe in pipes:
                for i, bird in enumerate(birds):
                    if pipe.collide(bird):
                        genomes_list[i].fitness -= 1
                        birds.remove(bird)

                if pipe.x + pipe.pipe_top.get_width() < 0:
                    pipes_to_remove.append(pipe)

                if not pipe.passed and pipe.x < bird.x:
                    # genomes_list[i].fitness += 5
                    pipe.passed = True
                    add_pipe = True

            if add_pipe:
                self.score += 1
                pipes.append(Pipe(self.screen_width))

            for item in pipes_to_remove:
                pipes.remove(item)

            to_remove = []
            for i, bird in enumerate(birds):
                if bird.y + bird.img.get_height() >= self.base or bird.y < 0:
                    to_remove.append((bird, nets[i], genomes_list[i]))

            for item in to_remove:
                birds.remove(item[0])
                nets.remove(item[1])
                genomes_list.remove(item[2])

            self.draw_screen(birds, pipes, ground, pipe_index, True)

    def run_neat(self, config_file):
        # Load configuration.
        config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                             neat.DefaultStagnation, config_file)

        # Create the population, which is the top-level object for a NEAT run.
        p = neat.Population(config)

        # Add a stdout reporter to show progress in the terminal.
        p.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        p.add_reporter(stats)
        # p.add_reporter(neat.Checkpointer(5))

        # Run for up to 50 generations.
        winner = p.run(self.eval_genomes, 20)

        # Show final stats
        print('\nBest genome:\n{!s}'.format(winner))
        node_names = {-1: 'BIRD_Y', -2: 'TOP_PIPE_Y', -3: 'BOTTOM_PIPE_Y', 0: 'JUMP'}
        visualize.draw_net(config, winner, True, node_names=node_names)
        visualize.plot_stats(stats, ylog=False, view=True)
        visualize.plot_species(stats, view=True)
