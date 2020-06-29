import random
import sys

import pygame

# definicao de constantes para o jogo
FPS = 60
W_SIZE = W_WIDTH, W_HEIGHT = 500, 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (20, 255, 140)
GREY = (210, 210, 210)
PURPLE = (97, 52, 219)

SPEED = 5  # velocidade de movimento do carrinho do jogador
SPEED1 = [0, 2]  # velocidade de movimento do carrinho oponente 1
SPEED2 = [0, 3]  # velocidade de movimento do carrinho oponente 1
SPEED_LEVEL = 0.1  # Taxa de aumento da velocidade dos carrinhos
# próximo nível (valor sugerido: pode ser alterado conforme a sua lógica)
LEVEL = 1
# Usar essa quantidade de atualização das velocidades dos carrinhos oponentes.
# Isto é, a cada 10 carrinhos ultrapassados aumentar a velocidade destes.
LEVEL_FREQ = 10
# Tamanho de cada pista (em pixels)
FAIXAS = [[40, 140], [144, 254], [258, 354]]
# Lista contendo as imagens de arvores usadas no jogo
TREES = ["tree_1.png", "tree_2.png", "tree_3.png", "tree_4.png", "tree_5.png"]

# Habilita as funcoes do pygame e configura a Interface (não alterar)
pygame.init()
SCREEN = pygame.display.set_mode(W_SIZE)
pygame.display.set_caption('Car Racing')
pygame.display.set_icon(pygame.image.load('gameicon.png'))
clock = pygame.time.Clock()

# define os textos para 'pontos' e mensagem do 'termino' do jogo (não alterar)
score = 0
game_over = "GAME OVER"
font_score = pygame.font.Font('freesansbold.ttf', 50)
font_restart = pygame.font.Font('freesansbold.ttf', 16)
loser = False
# [DONE] carregar as imagens dos carrinhos
car = pygame.image.load("white_car.png")
car = pygame.transform.scale(car, (50, 100))

cars = ["red_car.png", "blue_car.png", "caminhonete.png", "ferrari.png"]
car_opponent_red = pygame.image.load("red_car.png")
car_opponent_blue = pygame.image.load("blue_car.png")

# define posicoes iniciais para os oponentes (não alterar)
# Repare que a coordenada ``y'' é negativa. Isso permite
# iniciar aos carrinhos em uma posição fora da tela.
oponente_rect_red = car_opponent_red.get_rect()
oponente_blue_rect = car_opponent_blue.get_rect()
# Lista para verificar colisão
LISTA_OPONENTES = [oponente_rect_red, oponente_blue_rect]
# carrega as imagens das árvores, escolhendo-as aleatoriamente. Repare que apenas
# duas árvores são visíveis na tela a cada instante (não alterar).
trees_images = []
trees_images_rect = []
for i in range(0, len(TREES)):
    trees_images.append(pygame.image.load(TREES[i]))
    trees_images_rect.append(trees_images[i].get_rect())
t1 = random.randint(0, 2)
t2 = random.randint(3, 4)

# define posicao inicial para o carrinho (não alterar)
car_rect = car.get_rect()
car_rect.center = (W_WIDTH // 2, W_HEIGHT - 100)

# define posicoes iniciais para as arvores (não alterar)
# Repare que a coordenada ``y'' é negativa. Isso permite
# iniciar as ávores em uma posição fora da tela.
trees_images_rect[t1].center = (450, -1)
trees_images_rect[t2].center = (410, -300)

# [DONE] carregar a musica de fundo e deixá-la em execução
pygame.mixer.init()
pygame.mixer.music.load('top-Gear-Soundtrack.mp3')

# Comentei a música para conseguir ouvir música enquanto desenvolve
# pygame.mixer.music.play()

# Funções para o jogo
#
RANGE_STREET = [70, 300]


def restart_opponent(rect, x_start, x_end, plus_score=True):
    global score
    rect.center = (random.randint(x_start, x_end), random.randint(-5, 0))
    if plus_score:
        score += 1
    return pygame.image.load(cars[random.randint(0, len(cars) - 1)])


def start_game():
    global car_opponent_red, car_opponent_blue, car, loser, score
    pygame.mixer.music.play()
    car_opponent_red = restart_opponent(oponente_rect_red, RANGE_STREET[0], RANGE_STREET[1], False)
    car_opponent_red = pygame.transform.scale(car_opponent_red, (50, 100))
    car_opponent_blue = restart_opponent(oponente_blue_rect, RANGE_STREET[0], RANGE_STREET[1], False)
    car_opponent_blue = pygame.transform.scale(car_opponent_blue, (50, 100))
    car = pygame.image.load("white_car.png")
    car = pygame.transform.scale(car, (50, 100))
    loser = False
    score = 0


start_game()


def calcularDeslocamento(start_x_1, end_x_1, start_x_2, end_x_2):
    pass
    # Valida se o carro 1 está mais a esquerda
    # Caso verdadeiro calcula a quantidade de deslocamento que deve ser realizado para evitar a colisão
    # O calculo leva a seguinte ideia
    #   |  1   |
    #         |    2   |
    #
    if start_x_1 < start_x_2:
        if start_x_1 < RANGE_STREET[0] + 50:
            return end_x_2 - start_x_1 + 1
        return start_x_2 - end_x_1
    else:
        # Caso o carro 2 esteja mais a esquerda que o carro 1
        #                 |  1   |
        #         |    2   |
        result = end_x_2 - start_x_1
        if start_x_1 < RANGE_STREET[0] + 50:
            return end_x_2 - start_x_1 + 1

        return -result if start_x_1 > W_WIDTH / 2 else result


def calcularDistancia(start_y_1, end_y_1, start_y_2, end_y_2):
    pass
    if start_y_1 > start_y_2:
        # Carrinho 1 está mais em baixo
        resultado = start_y_1 - end_y_2
    else:
        resultado = start_y_2 - end_y_1

    if resultado <= 0:
        return 1
    else:
        return resultado


def captura_colisao_oponentes():
    global oponente_rect_red, oponente_blue_rect
    start_x_red = oponente_rect_red.x
    end_x_red = oponente_rect_red.x + oponente_rect_red.width
    start_y_red = oponente_rect_red.y
    end_y_red = oponente_rect_red.y + oponente_rect_red.height
    start_x_blue = oponente_blue_rect.x
    end_x_blue = oponente_blue_rect.x + oponente_blue_rect.width
    start_y_blue = oponente_blue_rect.y
    end_y_blue = oponente_blue_rect.y + oponente_blue_rect.height
    if start_x_red > start_x_blue > RANGE_STREET[0] + oponente_blue_rect.width:
        validar_e_mover(end_x_red, end_x_blue, end_y_red, end_y_blue, oponente_blue_rect, start_x_red, start_x_blue,
                        start_y_red, start_y_blue)
    else:
        validar_e_mover(end_x_blue, end_x_red, end_y_blue, end_y_red, oponente_rect_red, start_x_blue, start_x_red,
                        start_y_blue, start_y_red)


def validar_e_mover(end_x_blue, end_x_red, end_y_blue, end_y_red, rect, start_x_blue, start_x_red,
                    start_y_blue, start_y_red):
    if validar_range(start_x_red, start_x_blue, end_x_blue) or validar_range(end_x_red, start_x_blue, end_x_blue):
        rect.move_ip(
            calcularDeslocamento(start_x_red, end_x_red, start_x_blue, end_x_blue) / calcularDistancia(start_y_red,
                                                                                                       end_y_red,
                                                                                                       start_y_blue,
                                                                                                       end_y_blue),
            0)


# Verifica se o número está entre o outro carro
def validar_range(numero, inicio, fim):
    if inicio <= numero <= fim:
        return True
    return False


def out_height_screen(rect):
    return rect.centery > W_HEIGHT


def reinicia_oponente():
    global oponente_rect_red, oponente_blue_rect, score, car_opponent_blue, car_opponent_red
    if out_height_screen(oponente_rect_red):
        car_opponent_red = restart_opponent(oponente_rect_red, RANGE_STREET[0], RANGE_STREET[1])
        car_opponent_red = pygame.transform.scale(car_opponent_red, (50, 100))
    if out_height_screen(oponente_blue_rect):
        car_opponent_blue = restart_opponent(oponente_blue_rect, RANGE_STREET[0], RANGE_STREET[1])
        car_opponent_blue = pygame.transform.scale(car_opponent_blue, (50, 100))


#
# Desenha as áreas verdes
#
def desenhar_area_verde():
    pygame.draw.rect(SCREEN, GREEN, (0, 0, FAIXAS[0][0], W_HEIGHT))
    pygame.draw.rect(SCREEN, GREEN, (FAIXAS[2][1], 0, W_WIDTH - FAIXAS[2][1], W_HEIGHT))


#
# Desenha as pistas dos carros
#
def desenhar_pistas():
    for pista in FAIXAS:
        pygame.draw.rect(SCREEN, GREY, (pista[0], 0, pista[1] - pista[0], W_HEIGHT))


#
# Código para quando o usuário apertar no botão de fechar quitar do jogo
#
def handle_quit_game():
    # A musica deve ser finalizada antes do fechamento do jogo.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.mixer.music.stop()
            pygame.quit()
            sys.exit(0)


def build_tree_scenario():
    global t1, t2
    if not loser:
        trees_images_rect[t1].move_ip(0, 1)
        trees_images_rect[t2].move_ip(0, 1)
        if out_height_screen(trees_images_rect[t1]):
            t1 = random.randint(0, 2)
            trees_images_rect[t1].center = (450, -1)
        if out_height_screen(trees_images_rect[t2]):
            t2 = random.randint(3, 4)
            trees_images_rect[t2].center = (410, -1)
    # desenha os objetos em posicoes atualizadas (não alterar)
    SCREEN.blit(trees_images[t1], trees_images_rect[t1])
    SCREEN.blit(trees_images[t2], trees_images_rect[t2])


# CODIGO PRINCIPAL
def build_car():
    SCREEN.blit(car, car_rect)


#
# Controles do carro do usuário com validações para ele não sair da tela
#
def build_car_controls():
    x = 0
    y = 0
    key = pygame.key.get_pressed()
    if pygame.key.get_focused() and not loser:
        half_width = car_rect.width / 2
        half_height = car_rect.height / 2
        # [DONE] manter o carrinho do jogador na tela. Use valores numéricos da tela e das pistas.
        if key[pygame.K_UP] and car_rect.centery - SPEED - half_height > 0:
            y -= SPEED
        if key[pygame.K_DOWN] and car_rect.centery - 1 + half_height < W_HEIGHT:
            y += SPEED
        if key[pygame.K_LEFT] and (car_rect.centerx - 1 - half_width) > FAIXAS[0][0]:
            x -= SPEED
        if key[pygame.K_RIGHT] and (car_rect.centerx + 1 + half_width) < FAIXAS[2][1]:
            x += SPEED
    else:
        if key[pygame.K_SPACE]:
            start_game()

    car_rect.move_ip(x, y)


def build_scenario():
    pygame.draw.rect(SCREEN, WHITE, (0, 0, W_WIDTH, W_HEIGHT))
    desenhar_area_verde()
    desenhar_pistas()


def build_opponents():
    if not loser:
        oponente_rect_red.move_ip(SPEED1[0], SPEED1[1] * (SPEED_LEVEL * LEVEL + 1))
        oponente_blue_rect.move_ip(SPEED2[0], SPEED2[1] * (SPEED_LEVEL * LEVEL + 1))
    SCREEN.blit(car_opponent_red, oponente_rect_red)
    SCREEN.blit(car_opponent_blue, oponente_blue_rect)


def build_score():
    text_surf_p = font_score.render(str(score), True, BLACK)
    SCREEN.blit(text_surf_p, (W_WIDTH - 100, 20))


def colisao(meu_carro, oponente):
    pass
    if ((validar_range(meu_carro.x, oponente.x, oponente.x + oponente.width) or
         validar_range(meu_carro.x + meu_carro.width, oponente.x, oponente.x + oponente.width))
            and
            (validar_range(meu_carro.y, oponente.y, oponente.y + oponente.height) or
             validar_range(meu_carro.y + meu_carro.height, oponente.y, oponente.y + oponente.height))
    ):
        return True
    return False


def captura_colisao():
    pass
    for oponente in LISTA_OPONENTES:
        if colisao(car_rect, oponente):
            return True
    return False


while True:
    # [DONE] Capturar o evento de fechar o jogo na interface.
    handle_quit_game()
    # [DONE] desenhar a imagem de fundo. Utilize os valores numéricos da tela e das pistas.
    build_scenario()
    # [DONE mover as arvores em 1 pixel. Reposicionar quando as arvores saem da Interface.
    build_tree_scenario()
    # [DONE] Capturar uma tecla pressionada para mover o carrinho. Usar as teclas
    build_car_controls()

    build_car()

    # [DONE] reiniciar oponentes quando
    reinicia_oponente()

    # [DONE] mover os carrinhos oponentes
    build_opponents()

    #
    #
    # [DONE] detectar colisão entre oponentes e calcula o desvio que deve ser realizado no espaço de tempo
    # que possui
    captura_colisao_oponentes()

    #
    #
    LEVEL = score / LEVEL_FREQ

    # [DONE] detectar colisao entre o carrinho do jogador e algum carrinho oponente.
    # Em caso de colisão mostrar a mensagem ''Fim de Jogo'' e carregar a imagem
    # de carrinho batido para o carrinho do jogador.
    if captura_colisao():
        SCREEN.blit(font_score.render(str(game_over), True, RED), (50, W_HEIGHT // 4))
        font_restart.set_italic(True)
        SCREEN.blit(font_restart.render("Aperte espaço para recomeçar!", True, PURPLE), (80, W_HEIGHT // 4 + 75))
        car = pygame.image.load("white_car_2.png")
        pygame.mixer.music.pause()
        loser = True
    #
    build_score()
    #
    pygame.display.update()
    clock.tick(FPS)
