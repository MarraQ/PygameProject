import sys

import pygame

FPS = 60


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
        screen.fill(pygame.Color('black'))
        pygame.draw.rect(screen, pygame.Color("red"), back_rect, border_radius=10)
        pygame.draw.line(screen, pygame.Color("White"), (30, 30), (80, 30))
        pygame.draw.line(screen, pygame.Color("white"), (30, 30), (45, 15))
        pygame.draw.line(screen, pygame.Color("white"), (30, 30), (45, 45))
        pygame.draw.rect(screen, pygame.Color("red"), lvl1_rect, border_radius=20)
        screen.blit(num1, num1_rect)
        pygame.display.flip()
        clock.tick(FPS)


def terminate():
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    pygame.init()
    screen_size = (800, 600)
    screen = pygame.display.set_mode(screen_size)
    clock = pygame.time.Clock()
    while True:
        start_screen()
        level_choose()
