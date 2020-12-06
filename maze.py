import pygame, random, os, sys, time
from camera import Camera
from utils.timer import Timer
import menu

class Player(pygame.sprite.Sprite):

    def __init__(self, grid, initial_cell):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images\\tortoise.png")
        #self.image.fill(pygame.Color('red'))
        self.rect = self.image.get_rect()
        self.cells = grid.grid
        self.cell_index = initial_cell
        self.cell = self.cells[self.cell_index]
        self.cols = grid.cols
        self.apples_collected = 0
        self.rect.center = self.cell.rect.center
    
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

        if self.cell.contents == "apple":
            self.cell.contents = None
            self.apples_collected += 1

    def reset_pos(self, grid, cell):
        self.cells = grid.grid
        self.cell = self.cells[cell]
        self.cell_index = cell
        

    def draw(self, s):
        s.blit(self.image, self.rect)


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

    off_x, off_y = 195, 380

    wall =  pygame.image.load("images\\wall2.png")
    apple = pygame.image.load("images\\apple.png")
    portal = pygame.image.load("images\\portal.png")

    def __init__(self, i, j, w, is_wall=False):
        # self.hedges = Spritesheet('images\\Hedge1.png').load_strip((0, 0, 64, 64), 17, pygame.Color('black'))
        self.i = i
        self.j = j
        self.visited = False
        self.width = w
                    # top, right, bottom, left
        self.walls = [True, True, True, True]
        self.x = self.i*self.width+self.off_x
        self.y = self.j*self.width+self.off_y
        self.rect = pygame.Rect(self.x, self.y, self.width, self.width)
        # self.image = self.hedges[0]
        self.contents = None

    @classmethod
    def move_cells(cls):
        cls.off_x += 20
        cls.off_y += 20

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
        if self.contents == None:
            self.contents = item
            return True
        else:
            return False


    def draw(self, s, dd=False):
        line = self.width // 8
        # dd is a debugging variable that will draw in walls around the players current cell
        # This was used to check that collision was working properly
        x = self.x - 10
        y = self.y - 10
        if self.walls[0]:
            s.blit(pygame.transform.rotate(self.wall, -90), (x, y))
            
        if self.walls[1]:
            s.blit(pygame.transform.flip(self.wall, True, False), (x, y))
            
        if self.walls[2]:
            s.blit(pygame.transform.rotate(self.wall, 90), (x, y))
            
        if self.walls[3]:
            s.blit(self.wall, (x, y))

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

       
            
        if self.contents == "apple":
            s.blit(self.apple, (self.x+16, self.y+16))
        elif self.contents == "exit":
            s.blit(self.portal, (self.x+16, self.y+16))
            pass
    
    def draw_camera(self, s, dd=False):
        line = self.width // 8
        # dd is a debugging variable that will draw in walls around the players current cell
        # This was used to check that collision was working properly
        x = self.x - 10
        y = self.y - 10
        if self.walls[0]:
            s.blit(pygame.transform.rotate(self.wall, -90), (x, y))
            
        if self.walls[1]:
            s.blit(pygame.transform.flip(self.wall, True, False), (x, y))
            
        if self.walls[2]:
            s.blit(pygame.transform.rotate(self.wall, 90), (x, y))
            
        if self.walls[3]:
            s.blit(self.wall, (x, y))

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

       
            
        if self.contents == "apple":
            s.blit(self.apple, (self.x+16, self.y+16))
        elif self.contents == "exit":
            s.blit(self.portal, (self.x+16, self.y+16))
            pass


class Grid:

    def __init__(self, s_width, s_height, initial_cell):
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
        self.starting_cell = initial_cell
    
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
        for j in range(0, self.rows):
            for i in range(0, self.cols):
                cell = Cell(i, j, self.width)
                self.grid.append(cell)

    def index_cell(self, i, j):
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

        t = self.index_cell(cell.i, cell.j-1)
        if t or t is 0:
            top = self.grid[t]
            if top.visited == False:
                neighbours.append(top)

        r = self.index_cell(cell.i+1, cell.j)
        if r:
            right = self.grid[r]
            if right.visited == False:
                neighbours.append(right)

        b = self.index_cell(cell.i, cell.j+1)
        if b:
            bottom = self.grid[b]
            if bottom.visited == False:
                neighbours.append(bottom)

        l = self.index_cell(cell.i-1, cell.j)
        if l or l is 0:
            left = self.grid[l]
            if left.visited == False:
                neighbours.append(left)

        # This function will randomly select a cell from neighbours, hence the maze is random
        if len(neighbours) > 0:
            r = random.choice(neighbours)
            return r
        else:
            return False

    def generate_maze(self, random_edge=False):
        for c in self.grid:
            # This will reset the grid that the maze is being generated on
            c.walls = [True, True, True, True]
            c.visited = False
        stack = []
        maze_done = False
        # edges = [(i, j) for i, j in]
        current = self.grid[self.starting_cell]
        current.visited = True
        max_pos = current
        longest_pathed_cells = []
        max_stack = 0
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
                max_stack = max(max_stack, len(stack))
                if max_stack == len(stack):
                    longest_pathed_cells.append(max_pos)
                    max_pos.colour = pygame.Color('cyan')
                    max_pos = current
                # Otherwise there are no valid neighbouring cells so take the top one off the stack
                current = stack.pop()
            else:
                # If the stack is 0 then the maze is solved
                self.longest_path = max_pos
                self.longest_path.populate_cell("exit")
                maze_done = True
    
    def populate(self, item, num):
        for _ in range(num):
            if not self.grid[random.randint(0, 90)].populate_cell(item):
                num += 1

    def draw(self, surface):
        """Draws the maze onto the screen"""
        for i in range(len(self.grid)):
                self.grid[i].draw(surface)

