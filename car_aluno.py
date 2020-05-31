import random

import pygame

# definicao de constantes para o jogo
FPS = 80
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
bloco1 = car_opponet_1.get_rect()
bloco2 = car_opponet_2.get_rect()

bloco1.center = (random.randint(70, 160), random.randint(-5, 0))
bloco2.center = (random.randint(160, 290), random.randint(-5, 0))

# [TODO] carregar a musica de fundo e deixá-la em execução
pygame.mixer.init();
pygame.mixer.music.load('top-Gear-Soundtrack.mp3')
pygame.mixer.music.play()


# Funções para o jogo
#

def captura_colisao_oponentes():
    global bloco1, bloco2
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


def reinicia_oponente():
    global bloco1, bloco2, score
    """
    [TODO] Se um oponente sai da tela, renicia-se a sua posicao aleatoriamente na tela
    """


#
# Desenha as áreas verdes
#
def desenharAreaVerde():
    pygame.draw.rect(SCREEN, GREEN, (0, 0, FAIXAS[0][0], W_HEIGHT))
    pygame.draw.rect(SCREEN, GREEN, (FAIXAS[2][1], 0, W_WIDTH - FAIXAS[2][1], W_HEIGHT))


def desenharPistas():
    for pista in FAIXAS:
        pygame.draw.rect(SCREEN, GREY, (pista[0], 0, pista[1] - pista[0], W_HEIGHT))


#
# Código para quando o usuário apertar no botão de fechar quitar do jogo
#
def handleQuitGame():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()


# CODIGO PRINCIPAL
while True:
    handleQuitGame()
    # [TODO] desenhar a imagem de fundo. Utilize os valores numéricos da tela e das pistas.
    desenharAreaVerde()
    desenharPistas()
    # [TODO mover as arvores em 1 pixel. Reposicionar quando as arvores saem da Interface.
    # trees_images_rect[t1].move_ip(t1., 2)
    # trees_images_rect[t2].move_ip()
    # if():
    #    t1 = random.randint(0, 2)
    #    trees_images_rect[t1].center = (450, -1)
    # if():
    #    t2 = random.randint(3, 4)
    #    trees_images_rect[t2].center = (410, -300)
    #
    # # [TODO] Capturar o evento de fechar o jogo na interface.
    # # A musica deve ser finalizada antes do fechamento do jogo.
    # for event in pygame.event.get():
    #    if event.type == pygame.QUIT:
    #
    #       pygame.quit()
    #       sys.exit()
    #
    # # [TODO] Capturar uma tecla pressionada para mover o carrinho. Usar as teclas
    # # UP, DOWN, LEFT e RIGHT (setinhas). Para mover o carrinho use a velocidade na
    # # coordenada correta.
    # if pygame.key.get_focused():
    #    key = pygame.key.get_pressed()
    #
    #
    # # [TODO] mover os carrinhos oponentes
    #
    #
    # # [TODO] detectar colisão
    # captura_colisao_oponentes()
    #
    # # [TODO] reiniciar oponentes quando
    # reinicia_oponente()

    # [TODO] a cada intervalo de pontos a velocidade dos oponentes eh aumentada

    # [TODO] manter o carrinho do jogador na tela. Use valores numéricos da tela e das pistas.

    # [TODO] detectar colisao entre o carrinho do jogador e algum carrinho oponente.
    # Em caso de colisão mostrar a mensagem ''Fim de Jogo'' e carregar a imagem
    # de carrinho batido para o carrinho do jogador.
    # if()):
    #    SCREEN.blit(font_score.render(str(game_over), True, RED), (50, W_HEIGHT//4))
    #    car =
    #
    # # desenha os objetos em posicoes atualizadas (não alterar)
    # SCREEN.blit(trees_images[t1], trees_images_rect[t1])
    # SCREEN.blit(trees_images[t2], trees_images_rect[t2])
    #
    # text_surf_p = font_score.render(str(score), True, BLACK)
    # SCREEN.blit(text_surf_p, (W_WIDTH-100, 20))
    #
    # SCREEN.blit(car_opponet_1, bloco1)
    # SCREEN.blit(car_opponet_2, bloco2)
    #
    # SCREEN.blit(car, car_rect)
    pygame.display.update()
    clock.tick(FPS)
