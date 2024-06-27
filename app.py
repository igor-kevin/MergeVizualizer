import pygame
import random
import math
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
        self.altura_bloco = math.floor(
            (self.height - self.TOP_PAD)/(self.max_val-self.min_val))
        self.start_x = self.SIDE_PAD // 2

# Função de desenhar
# Preenche  a tela com a cor para limpar
# Desenha e manda um update para não ter outros overlays e tal


def desenhar(draw_info, nome_algoritmo, ascendendo):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)

    titulo = draw_info.LARGE_FONT.render(
        f"Atual: {nome_algoritmo} - {'Ascendente' if ascendendo else 'Descendente'}", 1, draw_info.RED)
    draw_info.window.blit(
        titulo, (draw_info.width/2 - titulo.get_width()/2, 10))

    controles = draw_info.FONT.render(
        "R - Resetar | SPACE - Começar sort | A - Ascendente | D - Descendente", 1, draw_info.BLACK)
    draw_info.window.blit(
        controles, (draw_info.width/2 - controles.get_width()/2, 48))

    algoritmo = draw_info.FONT.render(
        "I - Insertion Sort | B - Bubble Sort | M - Mergesort | J - Miracle Sort | , - Random Sort", 1, draw_info.BLACK)
    draw_info.window.blit(
        algoritmo, (draw_info.width/2 - algoritmo.get_width()/2, 80))

    desenhar_lista(draw_info)

    pygame.display.update()


def desenhar_lista(draw_info, posicao_cores={}, limpa_bg=False):
    lst = draw_info.lst
    if limpa_bg:
        limpa_retangulo = (draw_info.SIDE_PAD//2, draw_info.TOP_PAD, draw_info.width -
                           draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
        pygame.draw.rect(draw_info.window,
                         draw_info.BACKGROUND_COLOR, limpa_retangulo)

    for i, val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.largura_bloco
        y = - 10 + draw_info.height - (val - draw_info.min_val) * \
            draw_info.altura_bloco

        cor = draw_info.GRADIENTS[i % 3]

        if i in posicao_cores:
            cor = posicao_cores[i]

        pygame.draw.rect(draw_info.window, cor,
                         (x, y, draw_info.largura_bloco, draw_info.height))
    if limpa_bg:
        pygame.display.update()


def gerador_lista(n, min_val, max_val):
    lst = []
    for _ in range(n):
        valor = random.randint(min_val, max_val)
        lst.append(valor)

    return lst


def bubble_sort(draw_info, ascendendo=True):
    desordenado = draw_info.lst
    for i in range(len(desordenado)):
        for j in range(len(desordenado)):
            if (desordenado[i] < desordenado[j] and ascendendo) or (desordenado[i] > desordenado[j] and not ascendendo):
                desordenado[i], desordenado[j] = desordenado[j], desordenado[i]
                desenhar_lista(
                    draw_info, {j: draw_info.GREEN, i: draw_info.RED}, True)
                yield True
    # Agora ordenada na verdade
    return desordenado


def insert_sort(draw_info, ascendendo=True):
    desordenado = draw_info.lst
    tamanho: int = len(desordenado)
    comparando: int
    for proximo in range(1, tamanho):
        comparando = desordenado[proximo]
        index_vetor: int = proximo

        # Enquanto estiver dentro do vetor e os valores forem maior do que o atual volta um no index
        while (index_vetor > 0 and desordenado[index_vetor-1] > comparando and ascendendo) or (index_vetor > 0 and desordenado[index_vetor-1] < comparando and not ascendendo):
            desordenado[index_vetor] = desordenado[index_vetor-1]
            index_vetor -= 1
            desenhar_lista(
                draw_info, {index_vetor: draw_info.GREEN, proximo: draw_info.RED}, True)
            yield True

        desordenado[index_vetor] = comparando


def merge_sort(draw_info, ascendendo=True):
    desordenado = draw_info.lst
    n = len(desordenado)
    current_size = 1

    while current_size < n:
        for left_start in range(0, n, 2 * current_size):
            mid = min(n - 1, left_start + current_size - 1)
            right_end = min((left_start + 2 * current_size - 1), (n - 1))

            left = desordenado[left_start:mid + 1]
            right = desordenado[mid + 1:right_end + 1]

            i = j = 0
            k = left_start

            while i < len(left) and j < len(right):
                if (left[i] <= right[j] and ascendendo) or (left[i] >= right[j] and not ascendendo):
                    desordenado[k] = left[i]
                    desenhar_lista(
                        draw_info, {k: draw_info.GREEN, left_start + i: draw_info.RED}, True)
                    i += 1
                else:
                    desordenado[k] = right[j]
                    desenhar_lista(
                        draw_info, {k: draw_info.GREEN, mid + 1 + j: draw_info.RED}, True)
                    j += 1
                k += 1
                yield True

            while i < len(left):
                desordenado[k] = left[i]
                desenhar_lista(
                    draw_info, {k: draw_info.GREEN, left_start + i: draw_info.RED}, True)
                i += 1
                k += 1
                yield True

            while j < len(right):
                desordenado[k] = right[j]
                desenhar_lista(
                    draw_info, {k: draw_info.GREEN, mid + 1 + j: draw_info.RED}, True)
                j += 1
                k += 1
                yield True

        current_size *= 2
    return desordenado


def miracle_sort(draw_info, asdf,  ascendente=True):
    lst = draw_info.lst
    if sorted(lst) != lst:
        random.shuffle(lst)
        desenhar_lista(draw_info, {}, True)
        yield True
    return lst


def is_sorted(arr):
    """Função auxiliar para verificar se a lista está ordenada"""
    for i in range(len(arr) - 1):
        if arr[i] > arr[i + 1]:
            return False
    return True


def random_sort(draw_info, ascending=True):
    """Implementação do Random Sort (Bogo Sort) com visualização Pygame"""
    lst = draw_info.lst
    while not is_sorted(lst):
        # Seleciona dois índices aleatórios para troca
        i, j = random.sample(range(len(lst)), 2)
        # Troca os elementos
        lst[i], lst[j] = lst[j], lst[i]

        # Desenha a lista atualizada no Pygame
        desenhar_lista(draw_info, {i: draw_info.RED, j: draw_info.GREEN}, True)

        yield True


def main():
    run = True
    clock = pygame.time.Clock()

    n = 100
    min_val = 10
    max_val = 400
    sorting = False
    ascendente = True

    lst = gerador_lista(n, min_val, max_val)

    algoritmo_escolhido = bubble_sort
    nome_algoritmo_escolhido = "Bubble Sort"
    gerador_algoritmo_sort = None

    draw_info = DrawInformation(1100, 700, lst)
    while run:
        clock.tick(20)
        if sorting:
            try:
                next(gerador_algoritmo_sort)
            except StopIteration:
                sorting = False
        else:
            desenhar(draw_info, nome_algoritmo_escolhido, ascendente)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_r and not sorting:
                lst = gerador_lista(n, min_val, max_val)
                draw_info.set_list(lst=lst)
            elif event.key == pygame.K_SPACE and sorting is False:
                sorting = True
                gerador_algoritmo_sort = algoritmo_escolhido(
                    draw_info, ascendente)
            elif event.key == pygame.K_a and not sorting:
                ascendente = True
            elif event.key == pygame.K_d and not sorting:
                ascendente = False
            elif event.key == pygame.K_i and not sorting:
                algoritmo_escolhido = insert_sort
                nome_algoritmo_escolhido = "Insert Sort"
            elif event.key == pygame.K_b and not sorting:
                algoritmo_escolhido = bubble_sort
                nome_algoritmo_escolhido = "Bubble Sort"
            elif event.key == pygame.K_m and not sorting:
                algoritmo_escolhido = merge_sort
                nome_algoritmo_escolhido = "Merge Sort"
            elif event.key == pygame.K_j and not sorting:
                algoritmo_escolhido = miracle_sort
                nome_algoritmo_escolhido = "Miracle Sort"
            elif event.key == pygame.K_COMMA and not sorting:
                algoritmo_escolhido = random_sort
                nome_algoritmo_escolhido = "Random Sort (aperte Q para sair)"
            elif event.key == pygame.K_q:
                pygame.quit()

    pygame.quit()


if __name__ == '__main__':
    main()
