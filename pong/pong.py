'''A Game of Pong'''
import pygame

pygame.init()
WIN_SIZE = (800, 500)
win1 = pygame.display.set_mode(WIN_SIZE)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
clock = pygame.time.Clock()
myfont = pygame.font.match_font('arial')
num_targets = 0
FPS = 100


def main_loop():

    # Initial variable values
    run = True
    player1 = Player(location='left')
    player2 = Player(location='right')
    reset_score = True
    time_reset = 0

    all_sprites = pygame.sprite.Group()
    puck = Puck()
    all_sprites.add(puck)
    all_sprites.add(player1)
    all_sprites.add(player2)

    # Add players to player group
    all_players = pygame.sprite.Group()
    all_players.add(player1)
    all_players.add(player2)

    # for _ in range(2):
    #     m = Mob()
    #     mobs.add(m)
    #     all_blocks.add(m)
    #     all_sprites.add(m)

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
        win1.fill(BLACK)

        # Update
        player1.update(keys)
        player2.update(keys)
        puck.update(all_players)

        # Draw/render
        all_sprites.draw(win1)
        if run:
            draw_text(win1, str(score), 22, WIN_SIZE[1] - 5, 0)
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
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.topright = (x, y)
    surf.blit(text_surface, text_rect)


def restart_game():
    main_loop()


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
        if col:
            if ((is_point_inside_rect(rect1.left, rect1.bottom, rect2)) and
                    (is_point_inside_rect(rect1.right, rect1.bottom, rect2)) or
                    (is_point_inside_rect(rect1.left, rect1.top, rect2)) and
                    (is_point_inside_rect(rect1.right, rect1.top, rect2))):

                y_col = 1
            else:
                y_col = 0
        else:
            y_col = 0

    return col, y_col


def is_point_inside_rect(x, y, rect):
    if ((x >= rect.left) and
            (x <= rect.right) and
            (y >= rect.top) and
            (y <= rect.bottom)):
        return True
    else:
        return False


class Player(pygame.sprite.Sprite):

    def __init__(self, location='left'):
        pygame.sprite.Sprite.__init__(self)
        self.location = location
        self.image = pygame.Surface((20, 120))
        self.image.fill((230, 25, 75))
        self.rect = self.image.get_rect()
        if self.location == 'left':
            self.rect.centerx = 10
            self.move_up = pygame.K_w
            self.move_down = pygame.K_s
        elif self.location == 'right':
            self.rect.centerx = WIN_SIZE[0] - 10
            self.move_up = pygame.K_UP
            self.move_down = pygame.K_DOWN
        self.rect.bottom = WIN_SIZE[1] / 2
        self.vel = 10

    def update(self, keys):
        if self.rect.top > 0:
            if keys[self.move_up]:
                self.rect.y -= self.vel

        if self.rect.bottom < WIN_SIZE[1]:
            if keys[self.move_down]:
                self.rect.y += self.vel


class Puck(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIN_SIZE[0]/2
        self.rect.centery = WIN_SIZE[1]/2
        self.vel_x = 5
        self.vel_y = 5
        self.x_dir = 1
        self.y_dir = -1
        # self.col_hist = numpy.array

    def update(self, all_players):

        self.check_wall()
        self.check_col(all_players)

        self.rect.x += self.vel_x*self.x_dir
        self.rect.y += self.vel_y*self.y_dir

    def check_wall(self):

        # Collision with the vertical walls
        if self.rect.right >= WIN_SIZE[0] or self.rect.left <= 0:
            restart_game()

        # Collision with the top
        if self.rect.top <= 0:
            print('collision with top')
            self.y_dir = self.y_dir*-1

        # Collision with the bottom
        if self.rect.bottom >= WIN_SIZE[1]:
            print('collision with bottom')
            self.y_dir = self.y_dir*-1

    def check_col(self, all_players):

        for block in all_players:

            col, y_col = do_rects_overlap(self.rect, block.rect)

            if y_col == 1:
                print('y collision')
                self.y_dir = self.y_dir * -1
            elif col:
                print('x collision')
                self.x_dir = self.x_dir * -1


main_loop()
