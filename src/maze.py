import pygame, random, os

class Player(pygame.sprite.Sprite):

    def __init__(self, x, y, grid):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((32, 32))
        self.image.fill(pygame.Color('red'))
        self.rect = self.image.get_rect()
        self.rect.topleft = x, y
        self.cells = grid.grid
        self.cell = self.cells[0]
        self.cell_index = 0
    
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            if self.cell.walls[0] == False:
                self.rect.y -= 64
                self.cell_index -= 13
                self.cell = self.cells[self.cell_index]
        elif keys[pygame.K_s]:
            if self.cell.walls[2] == False:
                self.rect.y += 64
                self.cell_index += 13
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
        

    
    def draw(self, s):
        s.blit(self.image, self.rect)
        self.cell.draw(s, dd=True)


class Spritesheet:

    def __init__(self, filename):
        """Load the sheet."""
        try:
            self.sheet = pygame.image.load(filename).convert()
        except pygame.error as e:
            print(f"Unable to load spritesheet image: {filename}")
            raise SystemExit(e)


    def image_at(self, rectangle, colorkey = None):
        """Load a specific image from a specific rectangle."""
        # Loads image from x, y, x+offset, y+offset.
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

    def images_at(self, rects, colorkey = None):
        """Load a whole bunch of images and return them as a list."""
        return [self.image_at(rect, colorkey) for rect in rects]

    def load_strip(self, rect, image_count, colorkey = None):
        """Load a whole strip of images, and return them as a list."""
        tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colorkey)

class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(img_base_path+image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


class Cell(pygame.sprite.Sprite):

    hedge_dict = {
        'tttt': 0,
        'fttt': 1,
        'tftt': 2,
        'ttft': 3,
        'tttf': 4,
        'tfft': 5,
        'ttff': 6,
        'fttf': 7,
        'fftt': 8,
        'tftf': 9,
        'ftft': 10,
        'ftff': 11,
        'fftf': 12,
        'ffft': 13,
        'tfff': 14, 
        'ffff': 16}


    def __init__(self, i, j, w, off_x=0, off_y=0, is_wall=False):
        self.hedges = Spritesheet('img\\Hedge1.png').load_strip((0, 0, 64, 64), 17, pygame.Color('black'))
        self.i = i
        self.j = j
        self.visited = False
        self.width = w
        # top, right, bottom, left
        self.walls = [True, True, True, True]
        self.x = self.i*self.width+off_x
        self.y = self.j*self.width+off_y
        self.image = self.hedges[0]

    @staticmethod
    def parse_walls(array):
        string = ""
        for i in array:
            j = str(i)[0].lower()
            string += j
        return string


    def draw(self, s, dd=False):
        line = self.width // 8
        self.image = self.hedges[self.hedge_dict[self.parse_walls(self.walls)]]
        if dd:
            if self.walls[0]:
                pygame.draw.line(s, pygame.Color('blue'), (self.x, self.y), (self.x+self.width, self.y), line)
            if self.walls[1]:
                pygame.draw.line(s, pygame.Color('blue'), (self.x+self.width, self.y), (self.x+self.width, self.y+self.width), line)
            if self.walls[2]:
                pygame.draw.line(s, pygame.Color('blue'), (self.x+self.width, self.y+self.width), (self.x, self.y+self.width), line)
            if self.walls[3]:
                pygame.draw.line(s, pygame.Color('blue'), (self.x, self.y+self.width), (self.x, self.y), line)
        s.blit(self.image, (self.x, self.y))


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
        '''
        This function will check the cells immediatley next to it and see if it has been visited.
        If it hasn't been visited, it is added to the array neighbours as it is eligible to be selected as the
        next cell.
        '''
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

        if len(neighbours) > 0:
            r = random.choice(neighbours)
            return r
        else:
            return False

    def generate_maze(self):
        for c in self.grid:
            c.walls = [True, True, True, True]
            c.visited = False
        stack = []
        maze_done = False
        current = self.grid[0]
        current.visited = True
        while not maze_done:
            # 1
            next_cell = self.check_neighbours(current)
            if next_cell:
                next_cell.visited = True
                # 2
                stack.append(current)
                # 3
                self.remove_walls(current, next_cell)
                # 4
                current = next_cell
            elif len(stack) > 0:
                current = stack.pop()
            else:
                maze_done = True
    
    def draw(self, surface):
        for i in range(len(self.grid)):
                self.grid[i].draw(surface)
            
                
if __name__ == "__main__":
    img_base_path = os.getcwd() + '\\img\\'
    bg = Background('backdrop1.png', (0,0))
    run = True
    width, height = 1200, 900
    surface = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    maze = Grid(width, height)
    maze.create_grid()
    draw_out = False
    maze.generate_maze()
    p1 = Player(maze.grid[0].x+16, maze.grid[0].y+16, maze)

    while run:
        clock.tick(10)
        surface.fill(pygame.Color('black'))
        surface.blit(bg.image, bg.rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False



        
        maze.draw(surface)

        p1.update()
        p1.draw(surface)

        pygame.display.flip()
