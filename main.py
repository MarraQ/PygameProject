import sys

import pygame

FPS = 60


# Класс мяча
class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y, ):
        super().__init__()
        self.radius = 20
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA, 32)
        self.image.fill(pygame.Color('black'))
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
        # Функция отрисовки мяча
        pygame.draw.circle(screen, pygame.Color('red'), (self.x, self.y), self.radius)

    def update(self):
        if pygame.sprite.spritecollideany(self, horiz_borders):
            self.vy = -self.vy

        # При столкновении меняет скорость по оси
        if pygame.sprite.spritecollideany(self, vert_borders):
            self.vx = -self.vx
        if self.moving:
            self.x += self.vx
            self.y += self.vy
            self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)
        if self.dragging:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if (mouse_x >= self.start_x - 50 and mouse_x <= self.start_x + 50 and mouse_y >= self.start_y - 50 and
                    mouse_y <= self.start_y + 50):
                self.x = mouse_x
                self.y = mouse_y


# Класс монеток
class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.add(coins)
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color('yellow'), (10, 10), 10)
        self.rect = pygame.Rect(x, y, 20, 20)
        self.collected = False


# Класс стенок
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


# Класс выхода
class Exit(pygame.sprite.Sprite):
    def __init__(self, x1, y1, w, h):
        super().__init__(all_sprites)
        self.add(exits)
        self.image = pygame.Surface((w, h))
        pygame.draw.rect(self.image, pygame.Color('green'), (0, 0, w, h))
        self.rect = pygame.Rect(x1, y1, w, h)


# Функция стартового экрана
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
            # При нажатии на F6 вызывает меню сброса очков
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F6:
                    reset_verification()
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:  # Проверяет нажатие на текст
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


def reset_verification():
    # Подтверждение сброса очков
    text_font = pygame.font.Font(None, 45)
    text = text_font.render('Вы уверены, что хотите сбросить результаты?', True, pygame.Color('red'))
    text_rect = text.get_rect(center=(400, 200))
    answer_font = pygame.font.Font(None, 26)
    yes_var = answer_font.render('Да', None, pygame.Color('red'))
    yes_rect = yes_var.get_rect(center=(450, 300))
    no_var = answer_font.render('Нет', None, pygame.Color('red'))
    no_rect = no_var.get_rect(center=(350, 300))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if yes_rect.collidepoint(event.pos):
                    reset_score()
                    return
                if no_rect.collidepoint(event.pos):
                    return
        screen.blit(text, text_rect)
        screen.blit(yes_var, yes_rect)
        screen.blit(no_var, no_rect)
        pygame.display.flip()


def reset_score():
    # Сброс очков
    global score
    with open("current_score.txt", "w", encoding='utf-8') as f:
        f.write('0')
    with open("data/level1/score.txt", 'w', encoding='utf-8') as f:
        f.write('0')
    with open("data/level2/score.txt", 'w', encoding='utf-8') as f:
        f.write('0')
    score = 0


def level_choose():
    # Функция окна выбора уровня
    global score
    score_font = pygame.font.Font(None, 38)
    lvl_font = pygame.font.Font(None, 40)
    num1 = lvl_font.render("1", True, pygame.Color('white'))
    num1_rect = num1.get_rect(center=(95, 85))
    lvl1_rect = pygame.Rect(65, 55, 60, 60)
    back_rect = pygame.Rect(10, 10, 80, 40)
    num2 = lvl_font.render('2', True, pygame.Color('white'))
    num2_rect = num2.get_rect(center=(175, 85))
    lvl2_rect = pygame.Rect(145, 55, 60, 60)
    while True:
        score_text = score_font.render(f"{score}", True, pygame.Color('yellow'))
        score_rect = score_text.get_rect(center=(750, 40))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if back_rect.collidepoint(mouse_pos):
                    return
                if lvl1_rect.collidepoint(mouse_pos):
                    code = level_initialisation("level1")
                    while code not in [0, 1, 3]:
                        code = level_initialisation("level1")
                    if code == 1:
                        successful_completion("level1")
                if lvl2_rect.collidepoint(mouse_pos):
                    code = level_initialisation("level2")
                    while code not in [0, 1, 3]:
                        code = level_initialisation("level2")
                    if code == 1:
                        successful_completion("level2")
        screen.fill(pygame.Color('black'))
        pygame.draw.rect(screen, pygame.Color("red"), back_rect, border_radius=10)
        pygame.draw.line(screen, pygame.Color("White"), (30, 30), (80, 30))
        pygame.draw.line(screen, pygame.Color("white"), (30, 30), (45, 15))
        pygame.draw.line(screen, pygame.Color("white"), (30, 30), (45, 45))
        pygame.draw.rect(screen, pygame.Color("red"), lvl1_rect, border_radius=20)
        pygame.draw.rect(screen, pygame.Color("red"), lvl2_rect, border_radius=20)
        screen.blit(score_text, score_rect)
        screen.blit(num1, num1_rect)
        screen.blit(num2, num2_rect)
        pygame.display.flip()
        clock.tick(FPS)


# Функция инициализации уровня
def level_initialisation(level_name):
    global score
    global all_sprites
    global horiz_borders
    global vert_borders
    global exits
    global coins
    all_sprites = pygame.sprite.Group()
    horiz_borders = pygame.sprite.Group()
    vert_borders = pygame.sprite.Group()
    exits = pygame.sprite.Group()
    coins = pygame.sprite.Group()
    rects = [(0, 0, 20, height), (0, 0, width, 20), (width - 20, 0, 20, height), (0, height - 20, width, 20)]
    # Загрузка данных уровня из файлов
    with open(f"data/{level_name}/barrier.txt", 'r', encoding='utf-8') as f:
        for el in f.readlines():
            Border(*tuple(map(int, el.split())))
    with open(f"data/{level_name}/rects.txt", 'r', encoding='utf-8') as f:
        for el in f.readlines():
            rects.append(tuple(map(int, el.split())))
    with open(f"data/{level_name}/exit.txt", 'r', encoding='utf-8') as f:
        Exit(*tuple(map(int, f.readline().split())))
    Border(20, 20, width - 20, 20)
    Border(20, height - 20, width - 20, height - 20)
    Border(20, 20, 20, height - 20)
    Border(width - 20, 20, width - 20, height - 20)
    with open(f"data/{level_name}/ball.txt", 'r', encoding='utf-8') as f:
        start_x, start_y = map(int, f.readline().split())
    ball = Ball(start_x, start_y)
    level_score = 0
    score_font = pygame.font.Font(None, 25)
    with open(f"data/{level_name}/coins.txt", 'r', encoding='utf-8') as f:
        Coin(*tuple(map(int, f.readline().split())))
        Coin(*tuple(map(int, f.readline().split())))
    with open(f"data/{level_name}/score.txt", 'r', encoding='utf-8') as f:
        prev_score = int(f.readline().strip())

    # Игровой цикл
    while True:
        score_text = score_font.render(f'{level_score}', True, pygame.Color('yellow'))
        score_rect = score_text.get_rect(center=(760, 40))
        if pygame.sprite.spritecollideany(ball, exits):
            level_score += 100
            if prev_score < level_score:
                with open(f"data/{level_name}/score.txt", 'w', encoding='utf-8') as f:
                    f.write(f'{level_score}')
                    score = score - prev_score + level_score
            return 1
        if pygame.sprite.spritecollide(ball, coins, True):
            level_score += 100

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return 2
                if event.key == pygame.K_ESCAPE:
                    return 3
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if ball.rect.collidepoint(mouse_pos) and not ball.moving:
                    ball.dragging = True
            if event.type == pygame.MOUSEBUTTONUP and ball.dragging:  # Запуск мяча
                ball.dragging = False
                ball.moving = True
                end_pos = event.pos
                dx = ball.start_x - end_pos[0]
                dy = ball.start_y - end_pos[1]
                if abs(dx) * 0.003 > 0.140:
                    ball.vx = 0.140 * (dx / abs(dx)) + dx * 0.003 % 0.01
                else:
                    ball.vx = dx * 0.003
                if abs(dy) * 0.003 > 0.140:
                    ball.vy = 0.140 * (dy / abs(dy)) + dy * 0.003 % 0.01
                else:
                    ball.vy = dy * 0.003
            if event.type == pygame.QUIT:
                terminate()
        screen.fill(pygame.Color('black'))
        if ball.vx == 0 and ball.vy == 0:
            pygame.draw.line(screen, pygame.Color('red'), (start_x - 40, start_y), (ball.x, ball.y), 5)
            pygame.draw.line(screen, pygame.Color('red'), (start_x + 40, start_y), (ball.x, ball.y), 5)
        all_sprites.draw(screen)
        for el in rects:
            pygame.draw.rect(screen, pygame.Color('red'), el)
        all_sprites.update()
        ball.draw()
        ball.update()
        screen.blit(score_text, score_rect)
        pygame.display.flip()


# Окно успешного прохождения уровня
def successful_completion(level_name):
    win_font = pygame.font.Font(None, 40)
    win_text = win_font.render("Вы прошли уровень!", True, pygame.Color("red"))
    win_rect = win_text.get_rect(center=(400, 200))
    next_font = pygame.font.Font(None, 35)
    next_text = next_font.render("Далее", True, pygame.Color("red"))
    next_rect = next_text.get_rect(center=(400, 400))
    with open(f"data/{level_name}/score.txt", 'r', encoding='utf-8') as f:
        level_score = f.readline().strip()
    score_font = pygame.font.Font(None, 30)
    score_text = score_font.render(f'Кол-во очков: {level_score}', True, pygame.Color("yellow"))
    score_rect = score_text.get_rect(center=(400, 300))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if next_rect.collidepoint(event.pos):
                    return
            if event.type == pygame.QUIT:
                terminate()
        screen.fill(pygame.Color('black'))
        screen.blit(score_text, score_rect)
        screen.blit(win_text, win_rect)
        screen.blit(next_text, next_rect)
        pygame.display.flip()


# Функция отключения игры
def terminate():
    global score
    with open("current_score.txt", 'w', encoding='utf-8') as f:
        f.write(str(score))  # Сохраняет очки
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    pygame.init()
    width, height = 800, 600
    screen_size = (width, height)
    all_sprites = pygame.sprite.Group()
    horiz_borders = pygame.sprite.Group()
    vert_borders = pygame.sprite.Group()
    exits = pygame.sprite.Group()
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("Bounce ball game")
    with open("current_score.txt", "r", encoding='utf-8') as f:
        score = int(f.readline().strip())
    coins = pygame.sprite.Group()
    clock = pygame.time.Clock()
    while True:
        start_screen()
        level_choose()
