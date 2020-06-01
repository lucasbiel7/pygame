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
W_BGCOLOR = GREEN
SPEED = 5  # velocidade de movimento do carrinho do jogador
SPEED1 = [0, 2]  # velocidade de movimento do carrinho oponente 1
SPEED2 = [0, 3]  # velocidade de movimento do carrinho oponente 1
SPEED_LEVEL = 0.1  # Taxa de aumento da velocidade dos carrinhos
# próximo nível (valor sugerido: pode ser alterado conforme a sua lógica)
LEVEL = 10
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

# [TODO] carregar as imagens dos carrinhos [DONE]
car = pygame.image.load("white_car.png")
car_opponet_1 = pygame.image.load("red_car.png")
car_opponet_2 = pygame.image.load("blue_car.png")

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

# define posicoes iniciais para os oponentes (não alterar)
# Repare que a coordenada ``y'' é negativa. Isso permite
# iniciar aos carrinhos em uma posição fora da tela.
oponente_1_rect = car_opponet_1.get_rect()
oponente_2_rect = car_opponet_2.get_rect()

# [DONE] carregar a musica de fundo e deixá-la em execução
pygame.mixer.init()
pygame.mixer.music.load('top-Gear-Soundtrack.mp3')


# Comentei a música para conseguir ouvir música enquanto desenvolve
# pygame.mixer.music.play()

# Funções para o jogo
#


def restart_opponent(rect, x_start, x_end):
    global score
    rect.center = (random.randint(x_start, x_end), random.randint(-5, 0))
    score += 1


restart_opponent(oponente_1_rect, 70, 160)
restart_opponent(oponente_2_rect, 160, 300)


def captura_colisao_oponentes():
    global oponente_1_rect, oponente_2_rect
    """ [TODO] Detectar colisao entre os oponentes ('blocos'). Em caso de colisao,
        afastar um carrinho para o lado sem deixa-lo sair das pistas.
    """


def captura_colisao():
    global SPEED, SPEED1, SPEED2
    """
    [TODO] Detectar colisao entre o carrinho e cada um de seus oponentes ('blocos'). Em caso
    de colisão, retornar True e parar o movimento de todos os elementos. Sem colisão detectada,
    então manter o jogo em execução e retornar False.
    """
    

def out_height_screen(rect):
    return rect.centery > W_HEIGHT


def reinicia_oponente():
    global oponente_1_rect, oponente_2_rect, score
    if out_height_screen(oponente_1_rect):
        restart_opponent(oponente_1_rect, 70, 160)
    if out_height_screen(oponente_2_rect):
        restart_opponent(oponente_2_rect, 160, 290)


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
            pygame.mixer.music.stop();
            pygame.quit()
            sys.exit(0)


def build_tree_scenario():
    global t1, t2
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
def buildCarControls():
    x = 0
    y = 0
    if pygame.key.get_focused():
        key = pygame.key.get_pressed()
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
    car_rect.move_ip(x, y)


def buildScenario():
    pygame.draw.rect(SCREEN, WHITE, (0, 0, W_WIDTH, W_HEIGHT))
    desenhar_area_verde()
    desenhar_pistas()


def build_opponents():
    oponente_1_rect.move_ip(SPEED1)
    oponente_2_rect.move_ip(SPEED2)
    SCREEN.blit(car_opponet_1, oponente_1_rect)
    SCREEN.blit(car_opponet_2, oponente_2_rect)


while True:
    # [DONE] Capturar o evento de fechar o jogo na interface.
    handle_quit_game()
    # [DONE] desenhar a imagem de fundo. Utilize os valores numéricos da tela e das pistas.
    buildScenario()
    # [DONE mover as arvores em 1 pixel. Reposicionar quando as arvores saem da Interface.
    build_tree_scenario()
    # [DONE] Capturar uma tecla pressionada para mover o carrinho. Usar as teclas
    buildCarControls()

    build_car()

    # [DONE] reiniciar oponentes quando
    reinicia_oponente()

    # [DONE] mover os carrinhos oponentes
    build_opponents()
    #
    #
    # [TODO] detectar colisão
    # captura_colisao_oponentes()
    #

    # [TODO] a cada intervalo de pontos a velocidade dos oponentes eh aumentada

    # [TODO] detectar colisao entre o carrinho do jogador e algum carrinho oponente.
    # Em caso de colisão mostrar a mensagem ''Fim de Jogo'' e carregar a imagem
    # de carrinho batido para o carrinho do jogador.
    # if()):
    #    SCREEN.blit(font_score.render(str(game_over), True, RED), (50, W_HEIGHT//4))
    #    car =
    #

    #
    # text_surf_p = font_score.render(str(score), True, BLACK)
    # SCREEN.blit(text_surf_p, (W_WIDTH-100, 20))
    #
    pygame.display.update()
    clock.tick(FPS)
