import pygame
import random
import numpy
pygame.init()
win_size = (600, 500)
win1 = pygame.display.set_mode(win_size)
white = (255, 255, 255)
black = (0, 0, 0)
run = True
clock = pygame.time.Clock()
myfont = pygame.font.match_font('arial')
num_targets = 0
FPS = 60

def main_loop(win1):

    # Initial variable values
    player = Player()
    reset_score = True
    run = True
    time_reset = 0
    mobs = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    puck = Puck()
    all_sprites.add(puck)
    all_sprites.add(player)
    all_blocks = pygame.sprite.Group()
    all_blocks.add(player)

    for i in range(2):
        m = Mob()
        mobs.add(m)
        all_blocks.add(m)
        all_sprites.add(m)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Check to see if a key has been pressed
        keys = pygame.key.get_pressed()

        # Calculate the score
        score, time_reset = calc_score(reset_score, time_reset)
        reset_score = False

        # fill the screen black
        win1.fill(black)

        # Update
        player.update(keys)
        puck.update(all_blocks, all_sprites, mobs)


        # Draw/render
        all_sprites.draw(win1)
        mobs.draw(win1)
        if run:
            draw_text(win1, str(score), 22, win_size[1] - 5, 0)
        pygame.display.update()

        # Clock
        clock.tick(FPS)

    pygame.quit()


def calc_score(reset_score, time_reset):

    if reset_score:
        time_reset = pygame.time.get_ticks()

    el_time = pygame.time.get_ticks() - time_reset

    el_time_s = el_time / 1000
    score = int(el_time_s / 5)
    return score, time_reset


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(myfont, size)
    text_surface = font.render(text, True, white)
    text_rect = text_surface.get_rect()
    text_rect.topright = (x, y)
    surf.blit(text_surface, text_rect)


def restart_game():
    main_loop(win1)


def detect_col_block(rect, circ):
    # returns a flag indicating whether there is a collision between a rect and a circle
    # takes the argument of (x, y, width, height) (x, y, radius)

    # check x coordinate
    if circ[0] + circ[2] >= rect[0] and circ[0] - circ[2] <= rect[0] + rect[2]:
        col_x = 1
    else:
        col_x = 0

    # check y coordinate
    if circ[1] - circ[2] <= rect[1] + rect[3] and circ[1] + circ[2] >= rect[1]:
        col_y = 1
    else:
        col_y = 0

    # Work out which edge the collision happened on


    col = col_x * col_y
    return col


def do_rects_overlap(rect1, rect2):
    for a, b in [(rect1, rect2), (rect2, rect1)]:
        # Check first if there is any overlap
        if ((is_point_inside_rect(a.left, a.top, b)) or
            (is_point_inside_rect(a.left, a.bottom, b)) or
            (is_point_inside_rect(a.right, a.top, b)) or
            (is_point_inside_rect(a.right, a.bottom, b))):

            col = True
        else:
            col = False

    # Check top and bottom points
    if ((is_point_inside_rect(rect1.left, rect1.bottom, rect2)) and
        (is_point_inside_rect(rect1.right, rect1.bottom, rect2)) or
        (is_point_inside_rect(rect1.left, rect1.top, rect2)) and
        (is_point_inside_rect(rect1.right, rect1.top, rect2))):

        y_col = 1
    else:
        y_col = 0

    return col, y_col


def is_point_inside_rect(x, y, rect):
    if (x >= rect.left) and (x <= rect.right) and (y >= rect.top) and (y <= rect.bottom):
        return True
    else:
        return False


class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((120, 40))
        self.image.fill((230, 25, 75))
        self.rect = self.image.get_rect()
        self.rect.centerx = win_size[0]/2
        self.rect.bottom = win_size[1] - 10
        self.vel = 10


    def update(self, keys):


        if self.rect.left > 0:
            if keys[pygame.K_LEFT]:
                self.rect.x -= self.vel

        if self.rect.right < win_size[0]:
            if keys[pygame.K_RIGHT]:
                self.rect.x += self.vel


class Puck(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 10))
        self.image.fill(white)
        self.rect = self.image.get_rect()
        self.rect.centerx = win_size[0]/2
        self.rect.centery = win_size[1]/2
        self.vel_x = 5
        self.vel_y = 5
        self.x_dir = 1
        self.y_dir = -1
        self.col_hist = numpy.array

    def update(self, player, all_sprites, mobs):

        self.check_wall()
        self.check_col(player, all_sprites, mobs)

        self.rect.x += self.vel_x*self.x_dir
        self.rect.y += self.vel_y*self.y_dir

    def check_wall(self):

        # Collision with the vertical walls
        if self.rect.right >=win_size[0] or self.rect.left <= 0:
            self.x_dir = self.x_dir*-1

        # Collision with the top
        if self.rect.top <= 0:
            self.y_dir = self.y_dir*-1

        # Falling off the bottoms
        if self.rect.top >= win_size[1]:
            restart_game()

    def check_col(self, all_blocks, all_sprites, mobs):

        for block in all_blocks:

            col, y_col = do_rects_overlap(self.rect, block.rect)

            if y_col == 1:
                self.y_dir = self.y_dir * -1
            elif col and y_col == 0:
                self.x_dir = self.x_dir * -1

            if col:
                if not isinstance(block, Player):
                    block.kill()
                    m = Mob()
                    all_sprites.add(m)
                    all_blocks.add(m)
                    mobs.add(m)





class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((100, 40))
        self.image.fill(white)
        self.rect = self.image.get_rect()
        self.colours = ((230, 25, 75),  (60, 180, 75),  (255, 225, 25), (0, 130, 200),  (245, 130, 48),
                        (145, 30, 180), (70, 240, 240), (240, 50, 230), (210, 245, 60), (250, 190, 190),
                        (0, 128, 128),  (230, 190, 255),(170, 110, 40), (255, 250, 200), (128, 0, 0), (170, 255, 195), (128, 128, 0),
                        (255, 215, 180), (0, 0, 128), (128, 128, 128), (255, 255, 255), (0, 0, 0))

        self.create(win_size)


    def create(self, win_size):
        self.rect.y = random.randint(0, win_size[1]/2)
        self.rect.x = random.randint(0, win_size[0] - self.rect[2])
        col_i = random.randint(0,20)
        self.image.fill(self.colours[col_i])

main_loop(win1)



