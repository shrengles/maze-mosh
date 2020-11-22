import pygame, random, os, sys, time
from camera import GameCamera

class Player(pygame.sprite.Sprite):

    def __init__(self, x, y, grid):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images\\tortoise.png")
        #self.image.fill(pygame.Color('red'))
        self.rect = self.image.get_rect()
        self.rect.topleft = x, y
        self.cells = grid.grid
        self.cell = self.cells[0]
        self.cell_index = 0
        self.cols = grid.cols
    
    def update(self):

        """
        The player cannot move through walls so this checks if a
        wall is present by tracking what cell a player is in.
        """
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            if self.cell.walls[0] == False:
                self.rect.y -= 64
                self.cell_index -= self.cols
                self.cell = self.cells[self.cell_index]
        elif keys[pygame.K_s]:
            if self.cell.walls[2] == False:
                self.rect.y += 64
                self.cell_index += self.cols
                self.cell = self.cells[self.cell_index]
        elif keys[pygame.K_d]:
            if self.cell.walls[1] == False:
                self.rect.x += 64
                self.cell_index += 1
                self.cell = self.cells[self.cell_index]
        elif keys[pygame.K_a]:
            if self.cell.walls[3] == False:
                self.rect.x -= 64
                self.cell_index -= 1
                self.cell = self.cells[self.cell_index]

    def reset_pos(self, grid):
        self.cells = grid.grid
        self.cell = self.cells[0]
        self.cell_index = 0
        

    def draw(self, s):
        s.blit(self.image, self.rect)
        self.cell.draw(s, dd=True)


class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        img_base_path = os.getcwd() + '\\images\\'
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(img_base_path+image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


class Cell(pygame.sprite.Sprite):

    """
    This is the class that is responsible for making the cells
    that the grid is comprised of. Each cell will have walls
    that are marked by the algorithm to either be true or false.
    This will determine whether they are visible to the player
    or not.
    """

    def __init__(self, i, j, w, off_x=0, off_y=0, is_wall=False):
        # self.hedges = Spritesheet('images\\Hedge1.png').load_strip((0, 0, 64, 64), 17, pygame.Color('black'))
        self.i = i
        self.j = j
        self.visited = False
        self.width = w
                    # top, right, bottom, left
        self.walls = [True, True, True, True]
        self.x = self.i*self.width+off_x
        self.y = self.j*self.width+off_y
        # self.image = self.hedges[0]
        self.wall =  pygame.image.load("images\\wall2.png")
        self.apple = pygame.image.load("images\\apple.png")
        self.contents = None

    @staticmethod
    def parse_walls(array):
        """
        This method will take the walls attribute from cells and
        translate them into the keys that the hedge_dict will
        understand and be able to assign a digit that will then
        give the corresponding sprite.
        """
        string = ""
        for i in array:
            j = str(i)[0].lower()
            string += j
        return string

    def populate_cell(self, item):
        self.contents = item


    def draw(self, s, dd=False):
        line = self.width // 8
        #self.image = self.hedges[self.hedge_dict[self.parse_walls(self.walls)]]
        # dd is a debugging variable that will draw in walls around the players current cell
        # This was used to check that collision was working properly
        if self.walls[0]:
            s.blit(pygame.transform.rotate(self.wall, -90), (self.x, self.y))
            
        if self.walls[1]:
            s.blit(pygame.transform.flip(self.wall, True, False), (self.x, self.y))
            
        if self.walls[2]:
            s.blit(pygame.transform.rotate(self.wall, 90), (self.x, self.y))
            
        if self.walls[3]:
            s.blit(self.wall, (self.x, self.y))

        if dd:
            if self.walls[0]:
                pygame.draw.line(s, pygame.Color('blue'),
                                 (self.x, self.y), (self.x+self.width, self.y), line)
            if self.walls[1]:
                pygame.draw.line(s, pygame.Color('blue'),
                                 (self.x+self.width, self.y), (self.x+self.width, self.y+self.width), line)
            if self.walls[2]:
                pygame.draw.line(s, pygame.Color('blue'),
                                 (self.x+self.width, self.y+self.width), (self.x, self.y+self.width), line)
            if self.walls[3]:
                pygame.draw.line(s, pygame.Color('blue'),
                                 (self.x, self.y+self.width), (self.x, self.y), line)
        #s.blit(self.image, (self.x, self.y))
        if self.contents == "apple":
            s.blit(self.apple, (self.x+25, self.y+25))


class Grid:

    def __init__(self, s_width, s_height, fill = True):
        self.s_width = s_width
        self.s_height = s_height
        self.grid = []
        self.width = 64
        self.rows = 7
        self.cols = 13
        # self.rows = s_height // self.width - 2*self.margin
        # if fill:
        #     self.cols = s_width // self.width - 2*self.margin
        # else:
        #     self.cols = self.rows
    
    @staticmethod
    def remove_walls(a, b):
        """Takes two cells objects and removes the wall between them"""
        x = a.i - b.i
        if x == 1:
            a.walls[3] = False
            b.walls[1] = False
        elif x == -1:
            a.walls[1] = False
            b.walls[3] = False

        y = a.j - b.j
        if y == 1:
            a.walls[0] = False
            b.walls[2] = False
        elif y == -1:
            a.walls[2] = False
            b.walls[0] = False


    def create_grid(self):
        """Iterates through the rows and colums and generates a corresponding grid of cells"""
        for j in range(self.rows):
            for i in range(self.cols):
                cell = Cell(i, j, self.width, 195, 390)
                self.grid.append(cell)

    def index(self, i, j):
        if i < 0 or j < 0 or i > self.cols-1 or j > self.rows-1:
            return False
        else:
            return i + j * self.cols

    def check_neighbours(self, cell):
        """
        This function will check the cells immediatley
        next to it and see if it has been visited.
        If it hasn't been visited, it is added to the
        array neighbours as it is eligible to be
        selected as the next cell.
        """
        neighbours = []

        t = self.index(cell.i, cell.j-1)
        if t:
            top = self.grid[t]
            if top.visited == False:
                neighbours.append(top)

        r = self.index(cell.i+1, cell.j)
        if r:
            right = self.grid[r]
            if right.visited == False:
                neighbours.append(right)

        b = self.index(cell.i, cell.j+1)
        if b:
            bottom = self.grid[b]
            if bottom.visited == False:
                neighbours.append(bottom)

        l = self.index(cell.i-1, cell.j)
        if l:
            left = self.grid[l]
            if left.visited == False:
                neighbours.append(left)

        # This function will randomly select a cell from neighbours, hence the maze is random
        if len(neighbours) > 0:
            r = random.choice(neighbours)
            return r
        else:
            return False

    def generate_maze(self):
        for c in self.grid:
            # This will reset the grid that the maze is being generated on
            c.walls = [True, True, True, True]
            c.visited = False
        stack = []
        maze_done = False
        current = self.grid[0]
        current.visited = True
        while not maze_done:
            # Next cell is checked from valid neighbours
            next_cell = self.check_neighbours(current)
            if next_cell:
                next_cell.visited = True
                # If that next cell is valid then mark it as visited
                stack.append(current)
                # Put the current cell on the stack
                self.remove_walls(current, next_cell)
                # Remove the walls between the current cell and the next cell
                current = next_cell
            elif len(stack) > 0:
                # Otherwise there are no valid neighbouring cells so take the top one off the stack
                current = stack.pop()
            else:
                # If the stack is 0 then the maze is solved
                maze_done = True
    
    def populate(self, item, num):
        for i in range(num):
            self.grid[random.randint(0, 90)].populate_cell(item)

                    
    
    def draw(self, surface):
        """Draws the maze onto the screen"""
        for i in range(len(self.grid)):
                self.grid[i].draw(surface)

class Game:

    def __init__(self):
        pygame.init()
        self.wall_base_path = os.getcwd() + '\\images\\'
        self.bg = Background('backdrop.png', (0,0))
        self.width, self.height = 1200, 900
        self.centre = (self.width//2, self.height//2)
        self.surface = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.set_maze()
        self.set_player()
        sysfont = pygame.font.get_default_font()
        self.font_size = 32
        self.text = pygame.font.Font("fonts\\pressstartp2.ttf", self.font_size)
        self.clicking = False
        self.menu_bg = Background("menu.png", (0, 0))
        self.time_start = None
        self.pause_time = 0

    @staticmethod
    def timer(t1, t2):
        return t2 - t1
        
    def button(self, off_x, off_y):
        return pygame.Rect(tuple(map(lambda i, j: i + j, self.centre, (-100, 200))), (200, 80))

    def draw_text(self, msg, x, y, colour="black"):
        char = len(str(msg))
        image = self.text.render(str(msg), True, pygame.Color(colour))
        self.surface.blit(image, (x - (char//2)*(self.font_size), y))
    
    def set_maze(self):
        self.maze = Grid(self.width, self.height)
        self.maze.create_grid()
        self.maze.generate_maze()
        self.maze.populate("apple", 5)
    
    def set_player(self):
        self.p1 = Player(self.maze.grid[0].x+25, self.maze.grid[0].y+25, self.maze)
        self.p1.reset_pos(self.maze)

    def main_menu(self):
        main_menu = True
        while main_menu:
            self.clock.tick(5)
            self.surface.fill(pygame.Color('white'))
            self.surface.blit(self.menu_bg.image, self.menu_bg.rect)
            mx, my = pygame.mouse.get_pos()
            start_button = self.button(-100, 200)
            if start_button.collidepoint((mx, my)) and self.clicking:
                self.time_start = time.time()
                self.run()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    main_menu = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        main_menu = False
                        pygame.quit()
                        sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.clicking = True

            pygame.draw.rect(self.surface, (200, 0, 0), start_button)
            self.draw_text("Main Menu", self.width//2, self.height//2, colour="purple")
            pygame.display.flip()
    
    def pause(self):
        paused = True
        while paused:
            self.clock.tick(5)
            self.surface.fill(pygame.Color('white'))
            self.surface.blit(self.menu_bg.image, self.menu_bg.rect)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    paused = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.time_start = time.time()
                        self.time_start -= self.pause_time
                        self.run()
            self.draw_text("Pause Menu", self.width//2, self.height//2)
            pygame.display.flip()

    def run(self):
        run = True
        while run:
            self.clock.tick(10)
            self.surface.fill(pygame.Color('black'))
            self.surface.blit(self.bg.image, self.bg.rect)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.pause_time = self.time_now
                        self.pause()

            if self.p1.cell == self.maze.grid[-1]:
                print("You win!")
                self.set_maze()
                self.set_player()


            self.maze.draw(self.surface)
            self.time_now = round(time.time() - self.time_start, 1)
            self.draw_text(self.time_now, self.width//2, self.height//2 - 300, colour="purple")
            self.draw_text("Time", self.width//2, self.height//2 - 350, colour="purple")

            self.p1.update()
            self.p1.draw(self.surface)

            pygame.display.flip()
