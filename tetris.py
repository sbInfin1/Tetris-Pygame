'''
STATUS: 1) In this version, the all 5 tetrominoes work without any sort of wrong collision
and there exists a 2 dp gap between stacked up tetrominoes (both horizontal and vertical)
2) The glitchy horizontal movement from the previous version is gone
3) The grid backend for the tetrominoes is set up.
4) The row number mismatch is corrected.
5) The logic for clearing a row is ready. Just need to be tested.
6) Glitch overlap fixed.
7) Row vanishing works, but has some glitches when multiple rows need to be vanished at the
   same time.
8) Pause button implemented.
9) Downfall speed control.
10) Mechanism of sprite disappearance changed (blitting the previous image to a new surface).
11) Making a new sprite for above rows.
12) Splitting a sprite into bottom and top parts work with minor bugs.
13) All bugs fixed. Row vanishing works like a charm.

TODO: 1) The tetrominoes still can get overlapped if rotated while it has entered a narrow space,
        and get out of boundary if rotated near the right boundary.
      3) Display the next tetromino.
      4) Display the score.
      5) Start, pause and stop buttons.
'''
# pygame template - skeleton for a new Pygame project
import pygame
import random
import copy

WIDTH = 480
HEIGHT = 640
PLAY_WIDTH = 300 # 30 px width for each cell with 10 columns
PLAY_HEIGHT = 600 # 30 px height for each cell with 20 rows
CELL_EDGE = PLAY_WIDTH / 10
TOP_LEFT_X = (WIDTH - PLAY_WIDTH) // 2
TOP_LEFT_Y = (HEIGHT - PLAY_HEIGHT)
ROWS = 20
COLS = 10
FPS = 60

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PINK = (255,192,203)
ORANGE = (255,165,0)
TURQUOISE = (64,224,208)

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

tetroColors = [PINK, YELLOW, GREEN, ORANGE, TURQUOISE]
e = CELL_EDGE
TTetro = [[(1, e+1), (1, 2*e-1), (e+1, 2*e-1), (e+1, 3*e-1), (2*e-1, 3*e-1), (2*e-1, 1), (e+1, 1), (e+1, e+1), [2, 3]],
            [[1, 2*e-1], [1, e+1], [e+1, e+1], [e+1, 1], [2*e-1, 1], [2*e-1, e+1], [3*e-1, e+1], [3*e-1, 2*e-1], [3, 2]],
            [[1,1], [e-1, 1], [e-1, e+1], [2*e-1, e+1], [2*e-1, 2*e-1], [e-1, 2*e-1], [e-1, 3*e-1], [1, 3*e-1], [2, 3]],
            [[1, 1], [3*e-1, 1], [3*e-1, e-1], [2*e-1, e-1], [2*e-1, 2*e-1], [e+1, 2*e-1], [e+1, e-1], [1, e-1], [3, 2]]]

squareTetro = [[[1, 1], [2*e-1, 1], [2*e-1, 2*e-1], [1, 2*e-1], [2, 2]],
               [[1, 1], [2*e-1, 1], [2*e-1, 2*e-1], [1, 2*e-1], [2, 2]],
               [[1, 1], [2*e-1, 1], [2*e-1, 2*e-1], [1, 2*e-1], [2, 2]],
               [[1, 1], [2*e-1, 1], [2*e-1, 2*e-1], [1, 2*e-1], [2, 2]]]

skewTetro = [[[e+1, 1], [3*e-1, 1], [3*e-1, e-1], [2*e-1, e-1], [2*e-1, 2*e-1], [1, 2*e-1], [1, e+1], [e+1, e+1], [3, 2]],
             [[1, 1], [e-1, 1], [e-1, e+1], [2*e-1, e+1], [2*e-1, 3*e-1], [e+1, 3*e-1], [e+1, 2*e-1], [1, 2*e-1], [2, 3]],
             [[e+1, 1], [3*e-1, 1], [3*e-1, e-1], [2*e-1, e-1], [2*e-1, 2*e-1], [1, 2*e-1], [1, e+1], [e+1, e+1], [3, 2]],
             [[1, 1], [e-1, 1], [e-1, e+1], [2*e-1, e+1], [2*e-1, 3*e-1], [e+1, 3*e-1], [e+1, 2*e-1], [1, 2*e-1], [2, 3]]]

LTetro = [[[1, 1], [e-1, 1], [e-1, 2*e+1], [2*e-1, 2*e+1], [2*e-1, 3*e-1], [1, 3*e-1], [2, 3]],
          [[1, 1], [3*e-1, 1], [3*e-1, e-1], [e-1, e-1], [e-1, 2*e-1], [1, 2*e-1], [3, 2]],
          [[1, 1], [2*e-1, 1], [2*e-1, 3*e-1], [e+1, 3*e-1], [e+1, e-1], [1, e-1], [2, 3]],
          [[1, e+1], [2*e+1, e+1], [2*e+1, 1], [3*e-1, 1], [3*e-1, 2*e-1], [1, 2*e-1], [3, 2]]]

straightTetro = [[[1, 1], [4*e-1, 1], [4*e-1, e-1], [1, e-1], [4, 1]],
                 [[1, 1], [e-1, 1], [e-1, 4*e-1], [1, 4*e-1], [1, 4]],
                 [[1, 1], [4*e-1, 1], [4*e-1, e-1], [1, e-1], [4, 1]],
                 [[1, 1], [e-1, 1], [e-1, 4*e-1], [1, 4*e-1], [1, 4]]]

pointsSet = {0: TTetro, 1: squareTetro, 2: skewTetro, 3: LTetro, 4: straightTetro}

grid = [['#' for i in range(COLS)] for j in range(ROWS)]
# grid = [[-1]*COLS]*(ROWS+1)

class Tetrominoes(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.tetroType = random.randint(0, 4)
        self.rot = random.randint(0, 3)
        randomTetro = pointsSet[self.tetroType][self.rot]
        points = randomTetro[0:-1]
        self.size_cells = [randomTetro[-1][0], randomTetro[-1][1]]
        size = [randomTetro[-1][0]*CELL_EDGE, randomTetro[-1][1]*CELL_EDGE]
        self.image = pygame.Surface(size, pygame.SRCALPHA, 32)
        # self.image.fill(BLUE)
        self.rect = self.image.get_rect()

        self.mask_color = tetroColors[self.tetroType]
        pygame.draw.polygon(self.image, self.mask_color, points)

        # Create the collision mask (anything not transparent)
        self.mask = pygame.mask.from_surface(self.image)
        # self.rect = self.mask.get_rect()

        self.image_orig = self.image

        # this variable will be later replaces with the width of the specific tetromino
        tetromino_rect_width_cells = 2
        random_col = random.randint(0, 9-tetromino_rect_width_cells)
        self.rect.left = TOP_LEFT_X + (random_col * CELL_EDGE)
        self.rect.top = TOP_LEFT_Y
        self.cell_row = 0
        self.cell_col = random_col
        self.isMoving = True
        self.downfall_interval = 500
        # self.rot = 0
        self.prev_y_update = pygame.time.get_ticks()

    def __str__(self):
        return str(self.tetroType)

    def update(self):
        now = pygame.time.get_ticks()

        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_DOWN]:
            self.downfall_interval = 100
        else:
            self.downfall_interval = 500

        if self.isMoving and now > self.prev_y_update + self.downfall_interval:
            self.prev_y_update = now
            self.rect.y += CELL_EDGE
            self.cell_row += 1
            # self.cell_row = (self.cell_row + 1) % 20
            print("cell_row = {}".format(self.cell_row))
            if self.rect.bottom >= TOP_LEFT_Y + PLAY_HEIGHT:
                self.rect.bottom = TOP_LEFT_Y + PLAY_HEIGHT
                self.isMoving = False
                # self.updateGrid()

    def updateGrid(self):
        for i in range(0, self.size_cells[0]):
            for j in range(0, self.size_cells[1]):
                # print("i = {}, j = {}".format(i, j))
                # pixel_x = TOP_LEFT_X + (self.cell_col + i)*CELL_EDGE + 5
                # pixel_y = TOP_LEFT_Y + (self.cell_row + i)*CELL_EDGE + 5
                pixel_x = int(i*CELL_EDGE + 5)
                pixel_y = int(j*CELL_EDGE + 5)
                # print("pixel_x = {}, pixel_y = {}".format(pixel_x, pixel_y))
                # print(tuple(self.image.get_at((pixel_x, pixel_y))))
                # print(self.mask_color)
                if tuple(self.image.get_at((pixel_x, pixel_y)))[0:3] == self.mask_color:
                    # print("color matched!")
                    # print("self.cell_row + j = {}, self.cell_col + i = {}".format(self.cell_row+j, self.cell_col+i))
                    print("BEFORE ASSIGNMENT:")
                    printGrid()
                    grid[self.cell_row+j][self.cell_col+i] = self

                    # print(grid[self.cell_row+j][self.cell_col+i])
                    # print(type(grid[self.cell_row+j][self.cell_col+i]))
                    print("AFTER ASSIGNMENT:")
                    printGrid()

        for i in range(ROWS-1, -1, -1):
            filled = True
            for j in range(0, COLS):
                filled = filled and (grid[i][j] != '#')
            if filled:
                shiftGrid(i)

    def validate_x(self):
        if self.rect.right > TOP_LEFT_X + PLAY_WIDTH:
            self.rect.right = TOP_LEFT_X + PLAY_WIDTH
        elif self.rect.x < TOP_LEFT_X:
            self.rect.x = TOP_LEFT_X

        if self.cell_col > 10-self.size_cells[0]:
            self.cell_col = 10-self.size_cells[0]
        elif self.cell_col < 0:
            self.cell_col = 0


    def rotate(self):
        self.rot = (self.rot + 1) % 4
        points = pointsSet[self.tetroType][self.rot][0:-1]
        self.size_cells = [pointsSet[self.tetroType][self.rot][-1][0],
                            pointsSet[self.tetroType][self.rot][-1][1]]
        size = [pointsSet[self.tetroType][self.rot][-1][0]*CELL_EDGE,
                pointsSet[self.tetroType][self.rot][-1][1]*CELL_EDGE]
        new_image = pygame.Surface(size, pygame.SRCALPHA, 32)
        # self.image.fill(BLUE)
        pygame.draw.polygon(new_image, tetroColors[self.tetroType], points)
        # Create the collision mask (anything not transparent)
        self.mask = pygame.mask.from_surface(new_image)

        self.image = new_image
        self.rect = self.image.get_rect()
        self.rect.left = TOP_LEFT_X + (self.cell_col * CELL_EDGE)
        self.rect.top = TOP_LEFT_Y + (self.cell_row * CELL_EDGE)


# i is the number of vertical cells to keep in the chopped tetromino
def chopOffBottom(tetro, i):
    # if(tetro.size_cells[1] == 1):
    #     tetro.kill()
    all_sprites.remove(tetro)
    # new_tetro = copy.deepcopy(tetro)
    new_tetro = Tetrominoes()
    # new_tetro.size_cells[1] -= 1
    new_tetro.size_cells[0] = tetro.size_cells[0]
    new_tetro.size_cells[1] = i
    new_tetro.cell_col = tetro.cell_col
    new_tetro.cell_row = tetro.cell_row
    size = (new_tetro.size_cells[0]*CELL_EDGE, new_tetro.size_cells[1]*CELL_EDGE)
    new_image = pygame.Surface(size, pygame.SRCALPHA, 32)
    new_image.blit(tetro.image, (0, 0), (0, 0, new_tetro.size_cells[0]*CELL_EDGE, new_tetro.size_cells[1]*CELL_EDGE))

    new_tetro.image = new_image
    new_tetro.rect = new_tetro.image.get_rect()
    new_tetro.rect.left = TOP_LEFT_X + (new_tetro.cell_col * CELL_EDGE)
    new_tetro.rect.top = TOP_LEFT_Y + (new_tetro.cell_row * CELL_EDGE)
    new_tetro.tetroType = tetro.tetroType
    new_tetro.rot = tetro.rot
    new_tetro.mask = pygame.mask.from_surface(new_tetro.image)
    new_tetro.mask_color = tetro.mask_color
    new_tetro.isMoving = False

    all_sprites.add(new_tetro)
    return new_tetro

# i is the number of vertical rows to discard in the chopped tetromino
def chopOffTop(tetro, i):
    # if(tetro.size_cells[1] == 1):
    #     tetro.kill()
    all_sprites.remove(tetro)
    # new_tetro = copy.deepcopy(tetro)
    new_tetro = Tetrominoes()
    # new_tetro.size_cells[1] -= 1
    new_tetro.size_cells[0] = tetro.size_cells[0]
    new_tetro.size_cells[1] = tetro.size_cells[1] - i
    new_tetro.cell_col = tetro.cell_col
    new_tetro.cell_row = tetro.cell_row+i
    size = (new_tetro.size_cells[0]*CELL_EDGE, new_tetro.size_cells[1]*CELL_EDGE)
    new_image = pygame.Surface(size, pygame.SRCALPHA, 32)
    # In the .blit() function the second argument is the coordinate in the destination image
    # where the drawing will start. The third argument gives the edges of the rectangle of
    # the source image to draw on the destination surface.
    new_image.blit(tetro.image, (0, 0), (0, i*CELL_EDGE,
                    new_tetro.size_cells[0]*CELL_EDGE, new_tetro.size_cells[1]*CELL_EDGE))

    new_tetro.image = new_image
    new_tetro.rect = new_tetro.image.get_rect()
    new_tetro.rect.left = TOP_LEFT_X + (new_tetro.cell_col * CELL_EDGE)
    new_tetro.rect.top = TOP_LEFT_Y + (new_tetro.cell_row * CELL_EDGE)
    new_tetro.tetroType = tetro.tetroType
    new_tetro.rot = tetro.rot
    new_tetro.mask = pygame.mask.from_surface(new_tetro.image)
    new_tetro.mask_color = tetro.mask_color
    new_tetro.isMoving = False

    all_sprites.add(new_tetro)
    return new_tetro


def draw_grid(surface, row, col):
    sx = TOP_LEFT_X
    sy = TOP_LEFT_Y
    for i in range(row):
        pygame.draw.line(surface, (128,128,128), (sx, sy+ i*30), (sx + PLAY_WIDTH, sy + i * 30))  # horizontal lines
        for j in range(col):
            pygame.draw.line(surface, (128,128,128), (sx + j * 30, sy), (sx + j * 30, sy + PLAY_HEIGHT))  # vertical lines
    pygame.draw.rect(surface, (255, 0, 0), (TOP_LEFT_X, TOP_LEFT_Y, PLAY_WIDTH, PLAY_HEIGHT), 5)


def printGrid():
    for row in grid:
        for cell in row:
            print("{} ".format(cell), end =" ")
        print("\n")

def shiftGrid(ground):
    # cuttoffSet will contain all the tetrominoes in the cleared row, which are to be chopped off
    cutoffSet = set()
    for cutoffTetro in grid[ground]:
        if cutoffTetro.size_cells[1] == 1:
            all_sprites.remove(cutoffTetro)
            cutoffTetro.kill()
        else:
            cutoffSet.add(cutoffTetro)

    # Go through the row above the cleared row and check for those tetrominoes whose parts were cleared
    map = {}
    for j in range(COLS):
        tetro = grid[ground-1][j]
        if tetro in cutoffSet:
            if tetro not in map:
                map[tetro] = chopOffBottom(tetro, ground-tetro.cell_row)
            grid[ground-1][j] = map[tetro]

    # Replace all occurrences of the replaces tetrominoes above the cleared row
    for i in range(ground-2, ground-4, -1):
        for j in range(COLS):
            if grid[i][j] in map:
                grid[i][j] = map[grid[i][j]]

    if ground != ROWS-1:
        # Go through the row below the cleared row and check for those tetrominoes whose parts were cleared
        map = {}
        for j in range(COLS):
            tetro = grid[ground+1][j]
            if tetro in cutoffSet:
                if tetro not in map:
                    map[tetro] = chopOffTop(tetro, ground-tetro.cell_row+1)
                grid[ground+1][j] = map[tetro]

        # Replace all occurrences of the tetrominoes below the cleared row
        for i in range(ground+2, min(ROWS, ground+4)):
            for j in range(COLS):
                if grid[i][j] in map:
                    grid[i][j] = map[grid[i][j]]

    # Kill all the tetrominoes that existed only in the now cleared row
    # for tetro in cutoffSet:
    #     if tetro.size_cells[1] == 1:
    #         tetro.kill()

    # shiftSet will contain the tetrominoes in the current grid that are above the cleared row
    shiftSet = set()
    for i in range(0, ground):
        for j in range(COLS):
            if(grid[i][j] != '#'):
                shiftSet.add(grid[i][j])

    # Shift all the tetrominoes in the shiftSet down by one row
    for tetro in shiftSet:
        tetro.rect.y += CELL_EDGE
        tetro.cell_row = (tetro.cell_row + 1) % 20

    # Shift all the items in the backend grid down by one row
    for i in range(ground, 0, -1):
        grid[i] = grid[i-1]

all_sprites = pygame.sprite.Group()
tetromino = Tetrominoes()
all_sprites.add(tetromino)
current_tetromino = tetromino

# Game loop
RUNNING, PAUSE, STOP = 0, 1, 2
state = RUNNING
while state != STOP:
    # Process input (events)
    for event in pygame.event.get():
        # check for closing the window
        if event.type == pygame.QUIT:
            state = STOP
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                current_tetromino.rect.x -= CELL_EDGE
                current_tetromino.cell_col -= 1
                current_tetromino.validate_x()
            elif event.key == pygame.K_RIGHT:
                current_tetromino.rect.x += CELL_EDGE
                current_tetromino.cell_col += 1
                current_tetromino.validate_x()
            elif event.key == pygame.K_SPACE:
                current_tetromino.rotate()
            elif event.key == pygame.K_p:
                state = PAUSE
            elif event.key == pygame.K_s:
                state = RUNNING
    else:
        if state == RUNNING:
            # Update
            all_sprites.update()

            # Check for overlap
            restOfTetrominoes = all_sprites.copy()
            restOfTetrominoes.remove(current_tetromino)
            overlap = pygame.sprite.spritecollide(current_tetromino, restOfTetrominoes,
                                                False, pygame.sprite.collide_mask)
            # print(overlap == True)
            if overlap:
                current_tetromino.isMoving = False
                current_tetromino.rect.y -= CELL_EDGE
                current_tetromino.cell_row -= 1
                # current_tetromino.updateGrid()

            if not current_tetromino.isMoving:
                current_tetromino.updateGrid()

            # Check to see if there is a moving Tetromino in the screen or not.
            # In case there isn't one, create a new Tetrominoes object, and
            # add it to the sprite group
            isMoving = False
            movingTetromino = Tetrominoes()
            for tetromino in all_sprites:
                if tetromino.isMoving:
                    isMoving = True
                    movingTetromino = tetromino
                    break

            # If there is a moving sprite, check if it overlaps with any other sprite
            # in the sprite group excluding itself. Note that, the sprite group is copied
            # to another spriteGroup variable using the pygame.sprite.Group.copy() function
            # If it does overlap, then we stop its movement
            if not(isMoving):
                tetromino = Tetrominoes()
                all_sprites.add(tetromino)
                current_tetromino = tetromino


        # Draw / render
        screen.fill(BLACK)
        draw_grid(screen, 20, 10)
        all_sprites.draw(screen)
        # after drawing everything, flip the display
        pygame.display.flip()
        # keep loop running at the right speed
        clock.tick(FPS)

pygame.quit()
