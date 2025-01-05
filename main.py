import sys

import pygame

FPS = 60


def start_screen():
    screen.fill(pygame.Color('black'))
    font = pygame.font.Font(None, 30)
    start = font.render("Начать игру", True, pygame.Color('red'))
    start_rect = start.get_rect(center=(400, 300))
    exit = font.render("Выйти", True, pygame.Color('red'))
    exit_rect = exit.get_rect(center=(400, 400))
    font_name = pygame.font.Font(None, 38)
    name = font_name.render("Bounce ball game", True, pygame.Color('red'))
    name_rect = name.get_rect(center=(400, 200))
    running = True
    while running:
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


def terminate():
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    pygame.init()
    screen_size = (800, 600)
    screen = pygame.display.set_mode(screen_size)
    clock = pygame.time.Clock()
    start_screen()
    print('Start game button')
