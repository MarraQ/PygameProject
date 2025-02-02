import sys

import pygame

FPS = 60
all_sprites = pygame.sprite.Group()
horiz_borders = pygame.sprite.Group()
vert_borders = pygame.sprite.Group()
exits = pygame.sprite.Group()

class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.radius = 20
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color('red'), (self.radius, self.radius), self.radius)
        self.start_x, self.start_y = x, y
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.rect = pygame.Rect(x - self.radius, y - self.radius, self.radius * 2, self.radius * 2)
        self.dragging = False
        self.moving = False

    def draw(self):
        pygame.draw.circle(screen, pygame.Color('red'), (self.x, self.y), self.radius)
        pygame.draw.circle(self.image, pygame.Color('red'), (self.radius, self.radius), self.radius)

    def update(self):
        if pygame.sprite.spritecollideany(self, horiz_borders):
            self.vy = -self.vy
        # if pygame.sprite.spritecollideany(self, exits):
        #     successful_completion()
        if pygame.sprite.spritecollideany(self, vert_borders):
            self.vx = -self.vx
        if self.moving:
            self.x += self.vx
            self.y += self.vy
            self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)
        if self.dragging:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if mouse_x >= self.start_x - 100 and mouse_x <= self.start_x + 100 and mouse_y >= self.start_y - 100 and mouse_y <= self.start_y + 100:
                self.x = mouse_x
                self.y = mouse_y


class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.add(coins)
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color('yellow'), (10, 10), 10)
        self.rect = pygame.Rect(x, y, 20, 20)
        self.collected = False


class Border(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:  # вертикальная стенка
            self.add(vert_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:  # горизонтальная стенка
            self.add(horiz_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


class Exit(pygame.sprite.Sprite):
    def __init__(self, x1, y1):
        super().__init__(all_sprites)
        self.add(exits)
        self.image = pygame.Surface((200, 10), pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, pygame.Color('green'), (0, 0, 400, 50))
        self.rect = pygame.Rect(x1, y1, x1 + 400, y1 + 50)

def start_screen():
    font = pygame.font.Font(None, 30)
    start = font.render("Начать игру", True, pygame.Color('red'))
    start_rect = start.get_rect(center=(400, 300))
    exit = font.render("Выйти", True, pygame.Color('red'))
    exit_rect = exit.get_rect(center=(400, 400))
    font_name = pygame.font.Font(None, 38)
    name = font_name.render("Bounce ball game", True, pygame.Color('red'))
    name_rect = name.get_rect(center=(400, 200))
    while True:
        screen.fill(pygame.Color('black'))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if start_rect.collidepoint(mouse_pos):
                    return
                if exit_rect.collidepoint(mouse_pos):
                    terminate()
        screen.blit(start, start_rect)
        screen.blit(exit, exit_rect)
        screen.blit(name, name_rect)
        pygame.display.flip()
        clock.tick(FPS)


def level_choose():
    lvl_font = pygame.font.Font(None, 40)
    num1 = lvl_font.render("1", True, pygame.Color('white'))
    num1_rect = num1.get_rect(center=(95, 85))
    lvl1_rect = pygame.Rect(65, 55, 60, 60)
    back_rect = pygame.Rect(10, 10, 80, 40)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if back_rect.collidepoint(mouse_pos):
                    return
                if lvl1_rect.collidepoint(mouse_pos):
                    lvl1()
        screen.fill(pygame.Color('black'))
        pygame.draw.rect(screen, pygame.Color("red"), back_rect, border_radius=10)
        pygame.draw.line(screen, pygame.Color("White"), (30, 30), (80, 30))
        pygame.draw.line(screen, pygame.Color("white"), (30, 30), (45, 15))
        pygame.draw.line(screen, pygame.Color("white"), (30, 30), (45, 45))
        pygame.draw.rect(screen, pygame.Color("red"), lvl1_rect, border_radius=20)
        screen.blit(num1, num1_rect)
        pygame.display.flip()
        clock.tick(FPS)


def lvl1():
    exit_x, exit_y = 300, 300
    Exit(exit_x, exit_y)
    Border(5, 5, width - 5, 5)
    Border(5, height - 5, width - 5, height - 5)
    Border(5, 5, 5, height - 5)
    Border(width - 5, 5, width - 5, height - 5)
    start_x, start_y = 450, 450
    ball = Ball(start_x, start_y)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if ball.rect.collidepoint(mouse_pos):
                    ball.dragging = True
            if event.type == pygame.MOUSEBUTTONUP and ball.dragging:
                ball.dragging = False
                ball.moving = True
                end_pos = event.pos
                dx = ball.start_x - end_pos[0]
                dy = ball.start_y - end_pos[1]
                ball.vx = dx * 0.003
                ball.vy = dy * 0.003
            if event.type == pygame.QUIT:
                terminate()
        screen.fill(pygame.Color('black'))
        if ball.vx == 0 and ball.vy == 0:
            pygame.draw.line(screen, pygame.Color('red'), (start_x - 40, start_y), (ball.x, ball.y), 5)
            pygame.draw.line(screen, pygame.Color('red'), (start_x + 40, start_y), (ball.x, ball.y), 5)
        all_sprites.draw(screen)
        all_sprites.update()
        ball.draw()
        ball.update()
        pygame.display.flip()
def successful_completion():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        screen.fill(pygame.Color('black'))


def terminate():
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    pygame.init()
    width, height = 800, 600
    screen_size = (width, height)
    screen = pygame.display.set_mode(screen_size)
    with open("current_session.txt", "r", encoding='utf-8') as f:
        score = int(f.readline().strip())

    coins = pygame.sprite.Group()
    clock = pygame.time.Clock()
    while True:
        start_screen()
        level_choose()
