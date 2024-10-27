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
        self.start_shuffle = False
        self.start_solution = False
        self.previous_choice = ""
        self.start_game = False
        self.start_timer = False
        self.elapsed_time = 0
        self.directions = []
        self.high_score = float(self.get_high_scores()[0])
        # Starting the mixer 
        mixer.init() 
        
        # Loading the song 
        mixer.music.load("Tick.mp3") 
        
        # Setting the volume 
        mixer.music.set_volume(0.7) 

    def get_high_scores(self):
        with open("high_score.txt", "r") as file:
            scores = file.read().splitlines()
        return scores

    def save_score(self):
        with open("high_score.txt", "w") as file:
            file.write(str("%.3f\n" % self.high_score))

    def create_game(self):
        # grid = [[x + y * GAME_SIZE for x in range(1, GAME_SIZE + 1)] for y in range(GAME_SIZE)]
        # grid[-1][-1] = 0
        grid = copy.deepcopy(initial_state)
        return grid

    def shuffle(self):
        possible_moves = []
        for row, tiles in enumerate(self.tiles):
            for col, tile in enumerate(tiles):
                if tile.text == "empty":
                    if tile.right():
                        possible_moves.append("right")
                    if tile.left():
                        possible_moves.append("left")
                    if tile.up():
                        possible_moves.append("up")
                    if tile.down():
                        possible_moves.append("down")
                    break
            if len(possible_moves) > 0:
                break

        if self.previous_choice == "right":
            possible_moves.remove("left") if "left" in possible_moves else possible_moves
        elif self.previous_choice == "left":
            possible_moves.remove("right") if "right" in possible_moves else possible_moves
        elif self.previous_choice == "up":
            possible_moves.remove("down") if "down" in possible_moves else possible_moves
        elif self.previous_choice == "down":
            possible_moves.remove("up") if "up" in possible_moves else possible_moves

        choice = random.choice(possible_moves)
        self.previous_choice = choice
        if choice == "right":
            self.tiles_grid[row][col], self.tiles_grid[row][col + 1] = self.tiles_grid[row][col + 1], \
                                                                       self.tiles_grid[row][col]
        elif choice == "left":
            self.tiles_grid[row][col], self.tiles_grid[row][col - 1] = self.tiles_grid[row][col - 1], \
                                                                       self.tiles_grid[row][col]
        elif choice == "up":
            self.tiles_grid[row][col], self.tiles_grid[row - 1][col] = self.tiles_grid[row - 1][col], \
                                                                       self.tiles_grid[row][col]
        elif choice == "down":
            self.tiles_grid[row][col], self.tiles_grid[row + 1][col] = self.tiles_grid[row + 1][col], \
                                                                       self.tiles_grid[row][col]
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
        print(row, col)
        direction = self.directions[self.solving_time]
        if direction.lower() == "right":
            print(row, col)
            self.tiles_grid[row][col], self.tiles_grid[row][col + 1] = self.tiles_grid[row][col + 1], \
                                                                    self.tiles_grid[row][col]
            print("right")
        elif direction.lower() == "left":
            print(row, col)
            self.tiles_grid[row][col], self.tiles_grid[row][col - 1] = self.tiles_grid[row][col - 1], \
                                                                        self.tiles_grid[row][col]
            print("left")
        elif direction.lower() == "up":
            print(row, col)
            self.tiles_grid[row][col], self.tiles_grid[row - 1][col] = self.tiles_grid[row - 1][col], \
                                                                        self.tiles_grid[row][col]
            print("down")
        elif direction.lower() == "down":
            print(row, col)
            self.tiles_grid[row][col], self.tiles_grid[row + 1][col] = self.tiles_grid[row + 1][col], \
                                                                       self.tiles_grid[row][col]
            print("up")
        
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
        self.buttons_list = []
        self.buttons_list.append(Button(500, 100, 200, 50, "BFS", WHITE, BLACK))
        self.buttons_list.append(Button(500, 170, 200, 50, "DFS", WHITE, BLACK))
        self.buttons_list.append(Button(500, 240, 200, 50, "IDFS", WHITE, BLACK))
        self.buttons_list.append(Button(500, 310, 200, 50, "A*", WHITE, BLACK))
        self.buttons_list.append(Button(500, 380, 200, 50, "PAUSE", YELLOW, WHITE))
        self.buttons_list.append(Button(500, 450, 200, 50, "RESET", RED, WHITE))
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
        # UIElement(550, 35, "%.3f" % self.elapsed_time).draw(self.screen)
        # UIElement(430, 300, "High Score - %.3f" % (self.high_score if self.high_score > 0 else 0)).draw(self.screen)
        pygame.display.flip()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for row, tiles in enumerate(self.tiles):
                    for col, tile in enumerate(tiles):
                        if tile.click(mouse_x, mouse_y):
                            if tile.right() and self.tiles_grid[row][col + 1] == 0:
                                self.tiles_grid[row][col], self.tiles_grid[row][col + 1] = self.tiles_grid[row][col + 1], self.tiles_grid[row][col]

                            if tile.left() and self.tiles_grid[row][col - 1] == 0:
                                self.tiles_grid[row][col], self.tiles_grid[row][col - 1] = self.tiles_grid[row][col - 1], self.tiles_grid[row][col]

                            if tile.up() and self.tiles_grid[row - 1][col] == 0:
                                self.tiles_grid[row][col], self.tiles_grid[row - 1][col] = self.tiles_grid[row - 1][col], self.tiles_grid[row][col]

                            if tile.down() and self.tiles_grid[row + 1][col] == 0:
                                self.tiles_grid[row][col], self.tiles_grid[row + 1][col] = self.tiles_grid[row + 1][col], self.tiles_grid[row][col]

                            self.draw_tiles()

                for button in self.buttons_list:
                    if button.click(mouse_x, mouse_y):
                        if button.text == "BFS":
                            self.solving_time = 0
                            self.tiles_grid = self.create_game()
                            self.solving_time = 0
                            self.start_solution = True
                            self.buttons_list = []
                            self.buttons_list.append(Button(500, 100, 200, 50, "PAUSE", YELLOW, WHITE))
                            self.buttons_list.append(Button(500, 170, 200, 50, "RESET", RED, WHITE))
                            self.draw()
                            self.directions = bfs(initial_state)
                            print(initial_state)
                        if button.text == "DFS":
                            self.solving_time = 0
                            self.tiles_grid = self.create_game()
                            self.start_solution = True
                            self.buttons_list = []
                            self.buttons_list.append(Button(500, 100, 200, 50, "PAUSE", YELLOW, WHITE))
                            self.buttons_list.append(Button(500, 170, 200, 50, "RESET", RED, WHITE))
                            self.directions = dfs(initial_state)
                        if button.text == 'IDFS':
                            self.solving_time = 0
                            self.tiles_grid = self.create_game()
                            self.start_solution = True
                            self.buttons_list = []
                            self.buttons_list.append(Button(500, 100, 200, 50, "PAUSE", YELLOW, WHITE))
                            self.buttons_list.append(Button(500, 170, 200, 50, "RESET", RED, WHITE))
                            self.directions = iddfs(initial_state)
                        if button.text == 'A*':
                            self.solving_time = 0
                            self.tiles_grid = self.create_game()
                            self.start_solution = True
                            self.buttons_list = []
                            self.buttons_list.append(Button(500, 100, 200, 50, "PAUSE", YELLOW, WHITE))
                            self.buttons_list.append(Button(500, 170, 200, 50, "RESET", RED, WHITE))
                            self.directions, self.path_cost, self.nodes_expanded, self.path_length, self.running_time = A_star(initial_state, euclideane)
                            self.directions, self.path_cost, self.nodes_expanded, self.path_length, self.running_time = A_star(initial_state, manhattan)
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
