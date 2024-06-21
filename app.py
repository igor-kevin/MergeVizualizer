import pygame
import random

pygame.init()


class DrawInformation:
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    GREEN = 0, 255, 0
    RED = 255, 0, 0
    GREY = 128, 128, 128
    BACKGROUND_COLOR = WHITE

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

 lst = gerador_lista(n, min_val, max_val)

  draw_info = DrawInformation(800, 600, lst)
   while run:
        clock.tick(60)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    pygame.quit()


if __name__ == '__main__':
    main()
