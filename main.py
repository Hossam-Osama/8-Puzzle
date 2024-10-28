import pygame
from pygame import mixer
import random
import time
from sprite import *
from settings import *
from app import *
import copy

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.solving_time = 0
        self.paused = False
        self.start_solution = False
        self.previous_choice = ""
        self.start_game = False
        self.start_timer = False
        self.elapsed_time = 0
        self.directions = []
        self.statistics = {"path_cost": 0, "nodes_expanded": 0, "running_time": 0}
        self.statistics_manhaten = {"path_cost": 0, "nodes_expanded": 0, "running_time": 0}
        self.a_star = False
        self.high_score = float(self.get_high_scores()[0])
        # Starting the mixer 
        mixer.init() 
        
        # Loading the song 
        mixer.music.load("Tick.mp3") 
        
        # Setting the volume 
        mixer.music.set_volume(0.7) 

    def create_game(self):
        grid = copy.deepcopy(initial_state)
        return grid

    def solve(self):
        for row, tiles in enumerate(self.tiles):
            flag = 0
            for col, tile in enumerate(tiles):
                if tile.text == "empty":
                    flag = 1
                    break
            if flag == 1:
                flag = 0
                break
        direction = self.directions[self.solving_time]
        if direction.lower() == "right":
            self.tiles_grid[row][col], self.tiles_grid[row][col + 1] = self.tiles_grid[row][col + 1], \
                                                                    self.tiles_grid[row][col]
        elif direction.lower() == "left":
            self.tiles_grid[row][col], self.tiles_grid[row][col - 1] = self.tiles_grid[row][col - 1], \
                                                                        self.tiles_grid[row][col]
        elif direction.lower() == "up":
            self.tiles_grid[row][col], self.tiles_grid[row - 1][col] = self.tiles_grid[row - 1][col], \
                                                                        self.tiles_grid[row][col]
        elif direction.lower() == "down":
            self.tiles_grid[row][col], self.tiles_grid[row + 1][col] = self.tiles_grid[row + 1][col], \
                                                                       self.tiles_grid[row][col]
        
    def draw_tiles(self):
        self.tiles = []
        for row, x in enumerate(self.tiles_grid):
            self.tiles.append([])
            for col, tile in enumerate(x):
                if tile != 0:
                    self.tiles[row].append(Tile(self, col, row, str(tile)))
                else:
                    self.tiles[row].append(Tile(self, col, row, "empty"))

    def new(self):
        self.all_sprites = pygame.sprite.Group()
        self.tiles_grid = self.create_game()
        self.tiles_grid_completed = self.create_game()
        self.elapsed_time = 0
        self.start_timer = False
        self.start_game = False
        self.start_solution = False
        self.a_star = False
        self.buttons_list = []
        self.buttons_list.append(Button(500, 100, 200, 50, "BFS", WHITE, BLACK))
        self.buttons_list.append(Button(500, 170, 200, 50, "DFS", WHITE, BLACK))
        self.buttons_list.append(Button(500, 240, 200, 50, "IDFS", WHITE, BLACK))
        self.buttons_list.append(Button(500, 310, 200, 50, "A*", WHITE, BLACK))
        self.statistics = {"path_cost": 0, "nodes_expanded": 0, "running_time": 0}
        self.draw_tiles()

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        if self.start_game:
            if self.tiles_grid == self.tiles_grid_completed:
                self.start_game = False
                if self.high_score > 0:
                    self.high_score = self.elapsed_time if self.elapsed_time < self.high_score else self.high_score
                else:
                    self.high_score = self.elapsed_time
                self.save_score()

            if self.start_timer:
                self.timer = time.time()
                self.start_timer = False
            self.elapsed_time = time.time() - self.timer

        if self.start_solution:
            self.solve()
            self.draw_tiles()
            self.solving_time += 1
            
            if self.solving_time >= len(self.directions):
                self.start_solution = False
                self.start_game = True
                self.start_timer = True
            pygame.time.wait(500)
            mixer.music.play() 
            
        self.all_sprites.update()
        

    def draw_grid(self):
        for row in range(-1, GAME_SIZE * TILESIZE, TILESIZE):
            pygame.draw.line(self.screen, LIGHTGREY, (row, 0), (row, GAME_SIZE * TILESIZE))
        for col in range(-1, GAME_SIZE * TILESIZE, TILESIZE):
            pygame.draw.line(self.screen, LIGHTGREY, (0, col), (GAME_SIZE * TILESIZE, col))

    def draw(self):
        self.screen.fill(BGCOLOUR)
        self.all_sprites.draw(self.screen)
        self.draw_grid()
        for button in self.buttons_list:
            button.draw(self.screen)
        
        UIElement(35, 400, "Path Cost - %d" % (self.statistics["path_cost"])).draw(self.screen)
        UIElement(35, 450, "Nodes Expanded - %d" % (self.statistics["nodes_expanded"])).draw(self.screen)
        UIElement(35, 500, "Running Time - %.4f" % (self.statistics["running_time"])).draw(self.screen)
        if self.a_star:
            UIElement(435, 400, "Path Cost - %d" % (self.statistics["path_cost"])).draw(self.screen)
            UIElement(435, 450, "Nodes Expanded - %d" % (self.statistics_manhaten["nodes_expanded"])).draw(self.screen)
            UIElement(435, 500, "Running Time - %.4f" % (self.statistics_manhaten["running_time"])).draw(self.screen)
            UIElement(50, 600, "EUCLIDEAN").draw(self.screen)
            UIElement(450, 600, "MANHATEN").draw(self.screen)
        pygame.display.flip()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                for button in self.buttons_list:
                    if button.click(mouse_x, mouse_y):
                        self.solving_time = 0
                        self.tiles_grid = self.create_game()
                        self.start_solution = True
                        self.buttons_list = []
                        self.buttons_list.append(Button(500, 100, 200, 50, "PAUSE", YELLOW, WHITE))
                        self.buttons_list.append(Button(500, 170, 200, 50, "RESET", RED, WHITE))
                        if button.text == "BFS":
                            self.directions = bfs(initial_state)
                            print(initial_state)
                        if button.text == "DFS":
                            self.directions = dfs(initial_state)
                        if button.text == 'IDFS':
                            self.directions = iddfs(initial_state)
                        if button.text == 'A*':
                            self.directions, self.statistics["path_cost"], self.statistics["nodes_expanded"], _, self.statistics["running_time"] = A_star(initial_state, euclideane)
                            self.directions, self.statistics_manhaten["path_cost"], self.statistics_manhaten["nodes_expanded"], _, self.statistics_manhaten["running_time"] = A_star(initial_state, manhattan)
                            self.a_star = True
                        if button.text == "RESET":
                            self.new()
                        if button.text == "PAUSE":
                            is_paused = True
                            button.text = "CONTINUE"
                            self.draw()
                            while is_paused:
                                for event in pygame.event.get():
                                    if event.type == pygame.MOUSEBUTTONDOWN:
                                        for button in self.buttons_list:
                                            if button.text == "CONTINUE":
                                                is_paused = False
                                                button.text = "PAUSE"
                                                self.draw()

game = Game()
while True:
    game.new()
    game.run()
