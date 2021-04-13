import pygame
import random
pygame.init()
win_size = (600, 500)
win1 = pygame.display.set_mode(win_size)
white = (255, 255, 255)
black = (0, 0, 0)
run = True
clock = pygame.time.Clock()
myfont = pygame.font.match_font('arial')
num_targets = 0

def main_loop(win1):

    # Initial variable values
    base = Player(win_size[1])
    bouncer = Ball()
    reset_score = True
    run = True
    time_reset = 0
    mobs = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    puck = Puck()
    all_sprites.add(puck)

    for i in range(2):
        m = Mob()
        mobs.add(m)

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


        # Create some targets
        # if score - 10*num_targets > 10:
        new_target = True
        # if keys[pygame.K_SPACE]:

        # Update
        puck.update()

        # Draw/render
        all_sprites.draw(win1)
        base.draw(win1, keys, win_size, 0)
        bouncer.draw(win1, win_size, base, 0, score)
        mobs.draw(win1)
        if run:
            draw_text(win1, str(score), 22, win_size[1] - 5, 0)
        pygame.display.update()

        # Clock
        clock.tick(60)

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
        # Check if a's corners are inside b
        if ((isPointInsideRect(a.left, a.top, b)) or
            (isPointInsideRect(a.left, a.bottom, b)) or
            (isPointInsideRect(a.right, a.top, b)) or
            (isPointInsideRect(a.right, a.bottom, b))):
            return True

    return False


def is_point_inside_rect(x, y, rect):
    if (x > rect.left) and (x < rect.right) and (y > rect.top) and (y < rect.bottom):
        return True
    else:
        return False


def targets(num):
    target_list = [Target() for i in range(num)]

    for i in range(num):
        target_list[i].draw()


class Player(object):

    def __init__(self, win_size_b):
        self.rec_x = 10
        self.rec_y = win_size_b - 20
        self.rec_width = 120
        self.rec_height = 10
        self.vel = 10
        self.bl_colour = (230, 25, 75)
        self.rect = (self.rec_x, self.rec_y, self.rec_width, self.rec_height)

    def draw(self, win1, keys, win_size, v_fact):
        pygame.draw.rect(win1, self.bl_colour, self.rect)

        self.vel += v_fact

        if self.rec_x > 0:
            if keys[pygame.K_LEFT]:
                self.rec_x -= self.vel

        if self.rec_x < win_size[0] - self.rec_width:
            if keys[pygame.K_RIGHT]:
                self.rec_x += self.vel

        self.rect = (self.rec_x, self.rec_y, self.rec_width, self.rec_height)


class Ball(object):
    def __init__(self):
        self.radius = 10
        self.color = (210, 245, 60)
        self.vel_x = 5
        self.vel_y = 5
        self.x_dir = 1
        self.y_dir = 1
        self.x = int(win_size[0]/2)
        self.y = int(win_size[1]/2)
        self.circ = (self.x, self.y, self.radius)

    def draw(self, win1, win_size, block_b, v_fact, score):

        self.vel_x += int(v_fact)
        self.vel_y += int(v_fact)

        pygame.draw.circle(win1, self.color, (self.x, self.y), self.radius)
        if self.x == 0 or self.x == win_size[0] - self.radius:
            self.x_dir = -self.x_dir

        if self.y == 0:
            self.y_dir = -self.y_dir

        if detect_col_block(block_b.rect, self.circ) == 1:
            self.y_dir = -self.y_dir

        if self.y > win_size[1]:
            restart_game()





        self.x += self.vel_x * self.x_dir
        self.y -=self.vel_y * self.y_dir

        self.circ = (self.x, self.y, self.radius)


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

    def update(self):

        self.check_wall()

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

    def check_col(self):
        pygame.sprite.spritecollide(self, )


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



