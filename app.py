import pygame
import random

pygame.init()


class DrawInformation:
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    GREEN = 0, 255, 0
    RED = 255, 0, 0
    BACKGROUND_COLOR = WHITE

    GRADIENTS = [
        (128, 128, 128),
        (160, 160, 160),
        (192, 192, 192)
    ]

    FONT = pygame.font.SysFont('arial', 30)
    LARGE_FONT = pygame.font.SysFont('arial', 45)
    SIDE_PAD = 100
    TOP_PAD = 150

    def __init__(self, width, height, lst):
        self.width = width
        self.height = height

        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Visualização do Sorting")
        self.set_list(lst)

    def set_list(self, lst):
        self.lst = lst
        self.max_val = max(lst)
        self.min_val = min(lst)

        self.largura_bloco = round((self.width - self.SIDE_PAD)/len(lst))
        self.altura_bloco = round(
            (self.height - self.TOP_PAD)/(self.max_val-self.min_val))
        self.start_x = self.SIDE_PAD // 2

# Função de desenhar
# Preenche  a tela com a cor para limpar
# Desenha e manda um update para não ter outros overlays e tal


def desenhar(draw_info):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)
    controles = draw_info.FONT.render(
        "R - Resetar | SPACE - Começar sort | A - Ascendente | D - Descendente", 1, draw_info.BLACK)
    draw_info.window.blit(
        controles, (draw_info.width/2 - controles.get_width()/2, 5))

    algoritmo = draw_info.FONT.render(
        "I - Insertion Sort | B - Bubble Sort | M - Mergesort", 1, draw_info.RED)
    draw_info.window.blit(
        algoritmo, (draw_info.width/2 - algoritmo.get_width()/2, 40))
    desenhar_lista(draw_info)
    pygame.display.update()


def desenhar_lista(draw_info):
    lst = draw_info.lst

    for i, val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.largura_bloco
        y = - 10 + draw_info.height - (val - draw_info.min_val) * \
            draw_info.altura_bloco

        cor = draw_info.GRADIENTS[i % 3]
        pygame.draw.rect(draw_info.window, cor,
                         (x, y, draw_info.largura_bloco, draw_info.height))


def gerador_lista(n, min_val, max_val):
    lst = []
    for _ in range(n):
        valor = random.randint(min_val, max_val)
        lst.append(valor)

    return lst


def main():
    run = True
    clock = pygame.time.Clock()

    n = 50
    min_val = 0
    max_val = 100
    sorting = False
    ascendente = True

    lst = gerador_lista(n, min_val, max_val)

    draw_info = DrawInformation(800, 600, lst)
    while run:
        clock.tick(60)

        desenhar(draw_info=draw_info)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_r:
                lst = gerador_lista(n, min_val, max_val)
                draw_info.set_list(lst=lst)
            elif event.key == pygame.K_SPACE and sorting is False:
                sorting = True
            elif event.key == pygame.K_a and not sorting:
                ascendente = True
            elif event.key == pygame.K_d and not sorting:
                ascendente = False

    pygame.quit()


if __name__ == '__main__':
    main()
