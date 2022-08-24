import pygame
from pygame.locals import *
from sys import exit
import os
from random import randrange, choice

pygame.init()
pygame.mixer.init()

# criação de tela
cor_tela = (100, 255, 255)
largura = 640
altura = 480
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('cube jump')

# caminho da pasta
diretorio_principal = os.path.dirname(__file__)
diretorio_imagens = os.path.join(diretorio_principal, 'imagens')
diretorio_sons = os.path.join(diretorio_principal, 'sons')

# carregando sprites para o codigo
sprite_sheet = pygame.image.load(os.path.join(diretorio_imagens, 'sprites.png')).convert_alpha()

som_colisao = pygame.mixer.Sound(os.path.join(diretorio_sons, 'sons_death_sound.wav'))
som_colisao.set_volume(1)

colidiu = False
obstaculo = choice([1, 2])
obstaculo1 = choice([1, 2])


def exibe_mensagem(msg, tamanho, cor):
    fonte = pygame.font.SysFont('comicsansms', tamanho, True, False)
    mensagem = f'{msg}'
    texto_formatado = fonte.render(mensagem, True, cor)
    return texto_formatado


class Cubo(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.som_pulo = pygame.mixer.Sound(os.path.join(diretorio_sons, 'som_jump.wav'))
        self.som_pulo.set_volume(1)
        self.imagens_cubo = []
        for i in range(3):
            img = sprite_sheet.subsurface((i * 32, 0), (32, 32))
            img = pygame.transform.scale(img, (32 * 4, 32 * 4))
            self.imagens_cubo.append(img)
        self.index_lista = 0  # primeira imagem a se exibir = primeiro parametro da lista
        self.image = self.imagens_cubo[self.index_lista]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.pos_y_inicial = 366
        self.rect.center = (50, 440)
        self.pulo = False

    def pular(self):
        self.pulo = True
        self.som_pulo.play()

    def update(self):
        if self.pulo == True:
            if self.rect.y <= 270:  # pulo
                self.pulo = False
            self.rect.y -= 20  # subida pulo
        else:
            if self.rect.y < self.pos_y_inicial:
                self.rect.y += 20  # descida pulo
            else:
                self.rect.y = self.pos_y_inicial
        if self.index_lista > 2:
            self.index_lista = 0
        self.index_lista += 0.25
        self.image = self.imagens_cubo[int(self.index_lista)]


class Solo(pygame.sprite.Sprite):
    def __init__(self, posicao_x):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((7 * 32, 0), (32, 32))
        self.image = pygame.transform.scale(self.image, (32 * 4, 32 * 3))
        self.rect = self.image.get_rect()
        self.rect.y = altura - 64
        self.rect.x = posicao_x * 64

    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.x = largura
        self.rect.x -= 10
        # sempre que o canto superior direito do chao for -0


class Triangulo_inf(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((3 * 32, 0), (32, 32))
        self.image = pygame.transform.scale(self.image, (32 * 4, 32 * 4))
        self.rect = self.image.get_rect()  # retangulo ao redor da sprite
        # retangulo n vai ser utilizado para colisão, apenas para enquadramento na tela
        self.mask = pygame.mask.from_surface(self.image)  # mascara em volta da sprite(ppc)
        self.vez_obstaculo = obstaculo
        self.rect.center = (largura + 200, altura - 58)
        self.rect.x = largura

    def update(self):
        if self.vez_obstaculo == 1:
            if self.rect.topright[0] < 0:
                self.rect.x = largura
            self.rect.x -= 10


class Triangulo_duplo(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((6 * 32, 0), (32, 32))
        self.image = pygame.transform.scale(self.image, (32 * 4, 32 * 4))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.vez_obstaculo = obstaculo
        self.rect.center = (largura, altura - 53)
        self.rect.x = largura

    def update(self):
        if self.vez_obstaculo == 2:
            if self.rect.topright[0] < 0:
                self.rect.x = largura
            self.rect.x -= 10


class Triangulo_sup(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((4 * 32, 0), (32, 32))
        self.image = pygame.transform.scale(self.image, (32 * 4, 32 * 4))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.vez_obstaculo1 = obstaculo1
        self.rect.center = (largura + 150, altura - 140)
        self.rect.x = largura + 150

    def update(self):
        if self.vez_obstaculo1 == 2:
            if self.rect.topright[0] < 0:
                self.rect.x = largura
            self.rect.x -= 10


class Quadrado(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((5 * 32, 0), (32, 32))
        self.image = pygame.transform.scale(self.image, (32 * 4, 32 * 4))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.vez_obstaculo1 = obstaculo1
        self.rect.center = (largura + 500, altura - 56)
        self.rect.x = largura + 500

    def update(self):
        if self.vez_obstaculo1 == 1:
            if self.rect.topright[0] < 0:
                self.rect.x = largura
            self.rect.x -= 10


# grupo de sprites
todas_sprites = pygame.sprite.Group()
# (cubo)
cubo = Cubo()
todas_sprites.add(cubo)

# loop solo
for i in range(12):
    solo = Solo(i)
    todas_sprites.add(solo)

# instanciando objeto
triangulo_inf = Triangulo_inf()
todas_sprites.add(triangulo_inf)

triangulo_duplo = Triangulo_duplo()
todas_sprites.add(triangulo_duplo)

triangulo_sup = Triangulo_sup()
todas_sprites.add(triangulo_sup)

quadrado = Quadrado()
todas_sprites.add(quadrado)

# grupo obstaculos
grupo_obstaculos = pygame.sprite.Group()
grupo_obstaculos.add(triangulo_inf)
grupo_obstaculos.add(quadrado)
grupo_obstaculos.add(triangulo_sup)
grupo_obstaculos.add(triangulo_duplo)

# loop principal
relogio = pygame.time.Clock()
while True:
    relogio.tick(20)  # velocidade dos frames
    tela.fill((cor_tela))
    for event in pygame.event.get():  # definindo eventos
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                if cubo.rect.y != cubo.pos_y_inicial:  # bug do espaço
                    pass
                else:
                    cubo.pular()

    if triangulo_inf.rect.topright[0] <= 0 or triangulo_duplo.rect.topright[0] <= 0:
        obstaculo = choice([1, 2])
        triangulo_inf.rect.x = largura
        triangulo_duplo.rect.x = largura
        triangulo_inf.vez_obstaculo = obstaculo
        triangulo_duplo.vez_obstaculo = obstaculo

    if triangulo_sup.rect.topright[0] <= 0 or quadrado.rect.topright[0] <= 0:
        obstaculo1 = choice([1, 2])
        triangulo_sup.rect.x = largura
        quadrado.rect.x = largura
        triangulo_sup.vez_obstaculo1 = obstaculo1
        quadrado.vez_obstaculo1 = obstaculo1

    colisoes = pygame.sprite.spritecollide(cubo, grupo_obstaculos, False, pygame.sprite.collide_mask)
    if colisoes and colidiu == False:
        som_colisao.play()
        colidiu = True

    if colidiu == True:
        game_over = exibe_mensagem('GAME OVER', 40, (0, 0, 0))
        tela.blit(game_over, (largura // 2, altura // 2))


    else:
        todas_sprites.update()

    # inserção das sprites na tela
    todas_sprites.draw(tela)
    pygame.display.flip()
