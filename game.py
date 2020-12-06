import pygame, sys, os, random, menu
from maze import Grid, Cell
from utils.spritesheet import Background
from utils.timer import Timer
from camera import Camera
from maze import Player

class Game:

    def __init__(self):
        pygame.init()
        self.wall_base_path = os.getcwd() + '\\images\\'
        self.bg = Background('larger_backdrop.png', (0,0))
        self.width, self.height = 1024, 768
        self.centre = (self.width//2, self.height//2)
        self.surface = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        sysfont = pygame.font.get_default_font()
        self.font = "fonts\\pressstartp2.ttf"
        self.clicking = False
        self.menu_bg = Background("menu.png", (0, 0))
        self.set_maze()
        self.set_player()
        self.main_menu = menu.MainMenu(self)
        self.pause_menu = menu.PauseMenu(self)
        self.running = False
        self.camera = Camera(2160, 1920)
        self.timer = Timer()
        self.timer.countdown(90)
        self.all_sprites = []

        
    def button(self, off_x, off_y):
        return pygame.Rect(tuple(map(lambda i, j: i + j, self.centre, (-100, 200))), (200, 80))

    def draw_text(self, msg, x, y, size=32, colour="purple"):
        char = len(str(msg))
        text = pygame.font.Font(self.font, size)
        image = text.render(str(msg), True, pygame.Color(colour))
        rect = image.get_rect()
        rect.center = x, y
        self.surface.blit(image, rect)
        return rect

    def set_maze(self):
        self.maze = Grid(self.width, self.height, random.randint(0, 90))
        self.maze.create_grid()
        self.maze.generate_maze()
        self.maze.populate("apple", 5)
    
    def set_player(self):
        # self.p1 = Player(self.maze.grid[se].x+25, self.maze.grid[0].y+25, self.maze)
        self.p1 = Player(self.maze, self.maze.starting_cell)
        self.p1.reset_pos(self.maze, self.maze.starting_cell)

    def new_game(self):
        self.set_maze()
        self.set_player()
        self.timer = Timer()
        self.all_sprites = [self.p1, self.maze, self.bg]
        self.run()

    def get_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                return "KEYPRESS"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    return "MOUSE1"

    @staticmethod
    def is_clicked(rect):
        mx, my = pygame.mouse.get_pos()
        if rect.collidepoint((mx, my)):# and self.clicking:
            return True

    def run(self):
        self.running = True
        while self.running:
            self.clock.tick(10)
            self.timer.update()
            

            self.clicking = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                        self.timer.toggle()
                        self.pause_menu.display()
                    elif event.key == pygame.K_t:
                        self.timer.start_time -= 20

            if self.p1.cell == self.maze.longest_path:
                self.set_maze()
                self.set_player()


            
            

            


            self.p1.update(self.camera)
            self.surface.blit(self.bg.image, self.camera.apply(self.bg))
            self.maze.draw(self.surface, self.camera)
            self.p1.draw(self.surface, self.camera)
            
            self.draw_text("Time", self.width//2, self.height//2 - 350)
            self.draw_text(str(self.timer.neg_time), self.width//2, self.height//2 - 300)
            
            for apple, i in zip(range(self.p1.apples_collected), range(10, self.p1.apples_collected * 64, 64)):
                self.surface.blit(pygame.transform.scale2x(Cell.apple), (0 + i, self.height - 64))

            #self.surface.blit(self.maze.image)
            
            pygame.display.flip()