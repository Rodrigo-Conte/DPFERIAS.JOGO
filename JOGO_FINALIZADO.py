from re import M
from threading import Timer
from tkinter import EventType, Image
import pygame
from pygame.locals import *
import random 
from pygame import mixer
import time

pygame.init()

##MUSICA
mixer.init() 
mixer.music.load("muscia_dualipa.mp3") 
mixer.music.set_volume(0.3)
mixer.music.play()

### TELA\EXIBICAO JOGO
tamanho_tela = (600, 600)
pixel = 10

tela_game_over = pygame.image.load('foto_gameover.jpeg')

tela = pygame.display.set_mode(tamanho_tela)
pygame.display.set_caption('COBRINHA')

imagem_fundo = pygame.image.load('fundos.jpeg')
imagem_maca = pygame.image.load('apple.png').convert_alpha()

imagem_maca_escala = pygame.transform.scale(imagem_maca, (20,20))

###FUNCOES 

def colisao(pos1, pos2):
    return pos1 == pos2

def colisaooo(pos1, pos2, limiar = 5):
    xp1 = pos1[0] + pixel//2
    yp1 = pos1[1] + pixel//2
    xp2 = pos2[0] 
    yp2 = pos2[1] 

    return xp1 > xp2 - limiar and xp1 < xp2 + limiar and yp1 > yp2 - limiar and yp1 < yp2 + limiar
    
    

def random_on_grid():
    x = random.randint(0, tamanho_tela[0])
    y = random.randint(0, tamanho_tela[1])
    return x // pixel * pixel, y // pixel * pixel

def limite(pos):
    if 0 <= pos[0] < tamanho_tela[0] and 0 <= pos[1] < tamanho_tela[1]:
        return False
    else:
        return True


contador = 0


#CORES
vermelho = (255, 0, 0)
azul = (0, 0, 255)
preto = (0, 0, 0)
verde = (0 ,255, 0)


#COBRA
pos_cobra =[(250, 50), (260, 50), (270, 50)] 
superficie_cobra = pygame.Surface((pixel, pixel))
superficie_cobra.fill(azul)
snake_direction = K_LEFT

pos_cobra_x = 220
pos_cobra_y = 50

#MAÇA
superficie_maca = pygame.Surface((10, 10))
pos_maca = random_on_grid()

velocidade = 15


##EXIBIR TEXTO
 
pygame.display.set_caption('ANACONDA GAME')

fonte = pygame.font.Font('freesansbold.ttf', 40)

text = fonte.render(f'{contador}', True, preto)

textRect = text.get_rect()
 
textRect.center = (540, 50)


tecla_inicio = pygame.event.get()

while True:
    
    pygame.time.Clock().tick(velocidade)
    tela.blit(imagem_fundo, (0,0))
    
    for event in pygame.event.get():
        if event.type == QUIT:
            mixer.music.stop()
            tela.blit(tela_game_over, (0,0))
            time.sleep(4)
            pygame.quit()
            quit()

        elif event.type == KEYDOWN :
            if event.key in [K_UP, K_DOWN, K_LEFT, K_RIGHT]:
                snake_direction = event.key

    tela.blit(imagem_maca_escala, pos_maca)
    tela.blit(text, textRect)


##QUANDO COMER MAÇÃ
    if colisaooo(pos_maca, pos_cobra[0], limiar = 14):
        pos_maca = random_on_grid()
        pos_cobra.append((-20, -20))
        contador += 1
        text = fonte.render(f'{contador}', True, preto)
        
##DIFICULDADES
        if contador % 3 == 0:
            velocidade += 7
            
    cobra_grupo = pygame.sprite.Group()

    for pos in pos_cobra:
        tela.blit(superficie_cobra, pos)
        pedaco = pygame.sprite.Sprite()
        pedaco.image = superficie_cobra
        pedaco.rect = superficie_cobra.get_rect()
        pedaco.rect.x = pos[0]
        pedaco.rect.y = pos[1]
        cobra_grupo.add(pedaco)
    
    smaca = pygame.sprite.Sprite()
    smaca.image = superficie_maca
    smaca.rect = superficie_maca.get_rect()
    smaca.rect.x = pos_maca[0]
    smaca.rect.y = pos_maca[1] 

    col = pygame.sprite.spritecollide(smaca, cobra_grupo, dokill = True)
    

    for i in range(len(pos_cobra)-1, 0, -1):
       
##COLISAO
        if colisao(pos_cobra[0], pos_cobra[i]):
            tela.blit(tela_game_over, (0,0))
            mixer.music.stop()
            pygame.quit()
            quit()

        pos_cobra[i] = pos_cobra[i - 1]
        

    if limite(pos_cobra[0]):
        mixer.music.stop()
        tela.blit(tela_game_over, (0,0))
        

        
### MOVIMENTOS COBRA
    if snake_direction == K_UP:
        pos_cobra[0] = (pos_cobra[0][0], pos_cobra[0][1] - pixel)
    elif snake_direction == K_DOWN:
        pos_cobra[0] = (pos_cobra[0][0], pos_cobra[0][1] + pixel)
    elif snake_direction == K_LEFT:
        pos_cobra[0] = (pos_cobra[0][0] - pixel, pos_cobra[0][1])
    elif snake_direction == K_RIGHT:
        pos_cobra[0] = (pos_cobra[0][0] + pixel, pos_cobra[0][1])

    pygame.display.update()
