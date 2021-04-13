import pygame
import random

pygame.init()
clock = pygame.time.Clock()
FPS = 7


# Screen Size
WIDTH = 400
HEIGHT = WIDTH
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")
ROWS = 20
grid_size = WIDTH / ROWS

# Colour definitions
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (40, 40, 40)
RED = (255, 0, 0)
LIGHT_GREY = (170, 170, 170)


class Food(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((grid_size, grid_size))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(1, ROWS-1) * grid_size
        self.rect.y = random.randint(1, ROWS-1) * grid_size


class Cube(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((grid_size, grid_size))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.pos = (self.rect.x, self.rect.y)

    def update_cube(self, x, y):
        self.rect.x = x
        self.rect.y = y
        self.pos = (self.rect.x, self.rect.y)


class Snake(Cube):
    body = []
    turns = {}

    def __init__(self):
        super().__init__(WIDTH//2, WIDTH//2)
        self.vel = self.rect.width
        self.dir_x = 1
        self.dir_y = 0
        self.length = 1
        self.body = []
        self.head = Cube(WIDTH // 2, WIDTH // 2)

    def update(self):

        keys = pygame.key.get_pressed()

        if self.rect.left >= 0:
            if keys[pygame.K_LEFT]:
                if self.dir_x != 1:
                    self.dir_x = -1
                    self.dir_y = 0
                    self.turns[self.head.pos[:]] = [self.dir_x, self.dir_y]

        if self.rect.right <= WIDTH:
            if keys[pygame.K_RIGHT]:
                if self.dir_x != -1:
                    self.dir_x = 1
                    self.dir_y = 0
                    self.turns[self.head.pos[:]] = [self.dir_x, self.dir_y]

        if self.rect.top > 0:
            if keys[pygame.K_UP]:
                if self.dir_y != 1:
                    self.dir_y = -1
                    self.dir_x = 0
                    self.turns[self.head.pos[:]] = [self.dir_x, self.dir_y]

        if self.rect.bottom <= HEIGHT:
            if keys[pygame.K_DOWN]:
                if self.dir_y != -1:
                    self.dir_y = 1
                    self.dir_x = 0
                    self.turns[self.head.pos[:]] = [self.dir_x, self.dir_y]

        self.body.insert(0, self.rect[:])

        self.rect.x += self.vel * self.dir_x
        self.rect.y += self.vel * self.dir_y

        if self.check_col():
            global running
            running = False

        for food in all_food:
            if pygame.sprite.collide_rect(self, food):
                food.kill()
                f = Food()
                all_food.add(f)
                all_sprites.add(f)
                self.eat_food()

        # This section maintains a list with the previous positions in it
        l_body = len(self.body)
        if l_body > self.length + 1:
            self.body.pop(l_body - 1)
        # Update positions of the bodies
        i = 0
        for cu in snake_body:
            pos = self.body[i]
            cu.update_cube(pos[0], pos[1])
            i += 1

    def eat_food(self):
        self.length += 1
        pos = self.body[self.length-1]
        cu = Cube(pos[0], pos[1])
        snake_body.add(cu)
        all_sprites.add(cu)

    def check_col(self):
        if pygame.sprite.spritecollide(self, snake_body, False):
            col = True
        else:
            col = False

        if (self.rect.right > WIDTH or
                self.rect.left < 0 or
                self.rect.top < 0 or
                self.rect.bottom > HEIGHT):
            col = True

        return col


def redraw_window():
    screen.fill(GREY)
    all_sprites.draw(screen)
    draw_grid()
    pygame.display.update()


def draw_grid():
    size_between = WIDTH // ROWS

    x = 0
    y = 0

    for l in range(int(ROWS)):
        x = x + size_between
        y = y + size_between

        pygame.draw.line(screen, LIGHT_GREY, (x, 0), (x, HEIGHT))
        pygame.draw.line(screen, LIGHT_GREY, (0, y), (WIDTH, y))


# Initialise sprites
all_sprites = pygame.sprite.Group()
all_food = pygame.sprite.Group()
snake_body = pygame.sprite.Group()
for i in range(2):
    food = Food()
    all_food.add(food)
    all_sprites.add(food)

snake = Snake()
all_sprites.add(snake)

# Game Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update
    all_sprites.update()

    # Draw
    redraw_window()

    # Tick the clock
    clock.tick(FPS)
    # pygame.time.delay()
