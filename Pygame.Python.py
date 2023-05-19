import pygame, random

WIDTH = 1200
HEIGHT = 600
SPEED = 10
GAME_SPEED = 10
GROUND_WIDTH = 2 * WIDTH
GROUND_HEIGHT = 30

pygame.init()

# Dimensões da tela
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Jogo da Durezah')
background_image = pygame.image.load('Game_01/sprites/fundo.jpg')
background_image = pygame.transform.scale(background_image,[WIDTH, HEIGHT])

# Cor
black = (0, 0, 0)

# Fonte
font = pygame.font.Font(None, 40)

# Textos do menu
text_title = font.render("Desenvolvido por Durezah", True, black)
text_start = font.render("START", True, black )
text_quit = font.render("QUIT", True, black)
text_restart = font.render("RESTART", True, black)

# Som do jogo
pygame.init()
pygame.mixer.music.set_volume(1)
musica_de_fundo = pygame.mixer.music.load('Game_01/sprites/awesomeness.wav')
pygame.mixer.music.play(-1)

# Posições dos textos
title_rect = text_title.get_rect(center=(WIDTH/2, HEIGHT/2 -100))
start_rect = text_start.get_rect(center=(WIDTH/2 ,HEIGHT/2 ))
quit_rect = text_quit.get_rect(center=(WIDTH/2, HEIGHT/2  + 100))
restart_rect = text_restart.get_rect(center=(WIDTH/2, HEIGHT/2 + 200))

# Menu iniciar
start_menu = True
while start_menu:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            start_menu = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            # Verifique se o botão START foi clicado
            if start_rect.collidepoint(mouse_pos):
                som_start = pygame.mixer.Sound('Game_01/sprites/smw_fireball.wav')
                som_start.play()
                start_menu = False
            # Verifique se o botão SAIR foi clicado
            elif quit_rect.collidepoint(mouse_pos):
                start_menu = False
                pygame.quit()
                quit()

    # Desenhe o fundo e os textos
    screen.blit(background_image, (0, 0))
    screen.blit(text_title, title_rect)
    screen.blit(text_start, start_rect)
    screen.blit(text_quit, quit_rect)
    
    pygame.display.update()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_run = [pygame.image.load('Game_01/sprites/Run__000.png').convert_alpha(),
                          pygame.image.load('Game_01/sprites/Run__001.png').convert_alpha(),
                          pygame.image.load('Game_01/sprites/Run__002.png').convert_alpha(),
                          pygame.image.load('Game_01/sprites/Run__003.png').convert_alpha(),
                          pygame.image.load('Game_01/sprites/Run__004.png').convert_alpha(),
                          pygame.image.load('Game_01/sprites/Run__005.png').convert_alpha(),
                          pygame.image.load('Game_01/sprites/Run__006.png').convert_alpha(),
                          pygame.image.load('Game_01/sprites/Run__007.png').convert_alpha(),
                          ]
        self.image_fall = pygame.image.load('Game_01/sprites/Fall.png').convert_alpha()
        self.image = pygame.image.load('Game_01/sprites/shoot.png').convert_alpha()
        self.rect = pygame.Rect(100, 100, 100, 100)
        self.mask = pygame.mask.from_surface(self.image)
        self.current_image = 0

 
    def update(self, *args):
        def move_player(self):
            key = pygame.key.get_pressed()
            if key[pygame.K_d]:
                self.rect[0] += GAME_SPEED
            if key[pygame.K_a]:
                self.rect[0] -= GAME_SPEED
            self.current_image = (self.current_image + 1) % 8
            self.image = self.image_run[self.current_image]
            self.image = pygame.transform.scale(self.image,[100, 100])
        move_player(self)
        self.rect[1] += SPEED

        def fly(self):
            key = pygame.key.get_pressed()
            if key[pygame.K_w]:
                self.rect[1] -= 40
                self.image = pygame.image.load('Game_01/sprites/Fly.png').convert_alpha()
                self.image = pygame.transform.scale(self.image, [100, 100])
                print('fly')
        fly(self)


        def fall(self):
            key = pygame.key.get_pressed()
            if not pygame.sprite.groupcollide(playerGroup, groundGroup, False, False) and not key[pygame.K_w]:
                self.image = self.image_fall
                self.image = pygame.transform.scale(self.image, [100, 100])
                print('falling')
        fall(self)


class Ground(pygame.sprite.Sprite):
    def __init__(self, xpos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Game_01/sprites/ground.png').convert_alpha()
        self.image = pygame.transform.scale(self.image,(GROUND_WIDTH, GROUND_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        self.rect[1] = HEIGHT - GROUND_HEIGHT  

    def update(self, *args):
        self.rect[0] -= GAME_SPEED

class Obstacles(pygame.sprite.Sprite):
    def __init__(self, xpos, ysize):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Game_01/sprites/Box.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, [100, 100])
        self.rect = pygame.Rect(100, 100, 100, 100)
        self.rect[0] = xpos
        self.mask = pygame.mask.from_surface(self.image)
        self.rect[1] = HEIGHT - ysize

    def update(self, *args):
        self.rect[0] -= GAME_SPEED
        print('obstacle')
   

class Coins(pygame.sprite.Sprite):   
    def __init__(self, xpos, ysize):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Game_01/sprites/coin.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, [150, 150])
        self.rect = pygame.Rect(100, 100, 20, 20)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect[0] = xpos
        self.rect[1] = HEIGHT - ysize
        

    def update(self, *args):
        self.rect[0] -= GAME_SPEED
        print('coin')
 

def get_random_obstacles(xpos):
    size = random.randint(120, 600)
    box = Obstacles(xpos, size)
    return box

def get_random_coins(xpos):
    size = random.randint(60, 500)
    coin = Coins(xpos, size)
    return coin

def is_off_screen(sprite):
    return sprite.rect[0] < -(sprite.rect[2])

pygame.init()
game_window = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Jogo da Durezah')
BACKGROUND = pygame.image.load('Game_01/sprites/fundo.jpg')
BACKGROUND = pygame.transform.scale(BACKGROUND,[WIDTH, HEIGHT])

playerGroup = pygame.sprite.Group()
player = Player()
playerGroup.add(player)

pygame.mixer.music.set_volume(1)
musica_de_fundo = pygame.mixer.music.load('Game_01/sprites/awesomeness.wav')
barulho_coin = pygame.mixer.Sound('Game_01/sprites/smw_fireball.wav')
pygame.mixer.music.play(-1)

groundGroup = pygame.sprite.Group()
for i in range(100):
    ground = Ground(WIDTH * i)
    groundGroup.add(ground)

coinsGroup = pygame.sprite.Group()
for i in range(2):
    coin = get_random_coins(WIDTH * i + 1000)
    coinsGroup.add(coin)

obstacleGroup = pygame.sprite.Group()
for i in range(2):
    obstacle = get_random_obstacles(WIDTH * i + 1000)
    obstacleGroup.add(obstacle)

gameloop = True
def draw():
    playerGroup.draw(game_window)
    groundGroup.draw(game_window)
    obstacleGroup.draw(game_window)
    coinsGroup.draw(game_window)
def update():
    groundGroup.update()
    playerGroup.update()
    obstacleGroup.update()
    coinsGroup.update()
clock = pygame.time.Clock()
placar = 0

while gameloop:
    game_window.blit(BACKGROUND, (0, 0))
    font = pygame.font.SysFont('Arial',30)
    text = font.render('Placar', True, [255,255,255])
    game_window.blit(text, [1100, 20])
    contador = font.render(f'{placar}', True, [255,255,255])
    game_window.blit(contador, [1125, 50])
    clock.tick(27)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            break

    if is_off_screen(groundGroup.sprites()[0]):
        groundGroup.remove(groundGroup.sprites()[0])
        newGround = Ground(WIDTH - 40)
        groundGroup.add(newGround)

    if is_off_screen(obstacleGroup.sprites()[0]):
        obstacleGroup.remove(obstacleGroup.sprites()[0])
        newObstacle = get_random_obstacles(WIDTH * 1.5)
        obstacleGroup.add(newObstacle)
        newCoin = get_random_coins(WIDTH * 2)
        newCoin1 = get_random_coins(WIDTH * 2.2)
        newCoin2 = get_random_coins(WIDTH * 2.4)
        newCoin3 = get_random_coins(WIDTH * 2.6)
        newCoin4 = get_random_coins(WIDTH * 2.8)
        coinsGroup.add(newCoin)
        coinsGroup.add(newCoin1)
        coinsGroup.add(newCoin2)
        coinsGroup.add(newCoin3)
        coinsGroup.add(newCoin4)
    def exibe_mensagem(msg, tamanho, cor):
        fonte = pygame.font.sysFont('comicsansms', tamanho, True, False)
        mensagem = f'{msg}'
        texto_formatado = fonte.render(mensagem, True, cor)
        return texto_formatado
    
        if groupcollide == True:
            if pontos % 100 == 0:
                pomtos += 1
            game_over = exibe_mensagem('GAME OVER', 40, (0,0,0))
            tela.blit(game_over, (WIDTH//2, HEIGHT//2))
        
    if pygame.sprite.groupcollide(playerGroup, groundGroup, False, False):
        SPEED = 0
        print('collision')
    else:
        SPEED = 10

    if pygame.sprite.groupcollide(playerGroup, coinsGroup, False, True):
        placar += 1
        barulho_coin.play()

    if placar % 5 == 0 and placar != 0:
        GAME_SPEED += 0.02
        print('GAMESPEED ALTERADA')

    if pygame.sprite.groupcollide(playerGroup, obstacleGroup, False, False):
        break
    
    update()
    draw()
    pygame.display.update()

    # Menu de reinicialização
restart_menu = True
while restart_menu:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            restart_menu = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            # Verifique se o botão REINICIAR foi clicado
            if restart_rect.collidepoint(mouse_pos):
                som_restart = pygame.mixer.Sound('Game_01/sprites/smw_fireball.wav')
                som_restart.play()
                restart_menu = False
            # Check if the QUIT button was clicked
            elif quit_rect.collidepoint(mouse_pos):
                restart_menu = False
                pygame.quit()
                quit()


    # Desenhe o fundo e os textos
    screen.blit(background_image, (0, 0))
    screen.blit(text_title, title_rect)
    screen.blit(text_restart, restart_rect)
    screen.blit(text_quit, quit_rect)

    pygame.display.update()

paused = False
while True:
    # Verifique se o jogo está pausado
    if not paused:
        # Atualize a tela e lide com eventos
        # ...
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused
for event in pygame.event.get():
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_p:
            paused = not paused
if paused:
    # Exibir mensagem de pausa
    font = pygame.font.SysFont(None, 48)
    text = font.render("Jogo Pausado", True, (255, 255, 255))
    screen.blit(text, (SCREEN_WIDTH/2 - text.get_width()/2, SCREEN_HEIGHT/2 - text.get_height()/2))
    
    # Desenhar botões
    continue_button = pygame.draw.rect(screen, (0, 255, 0), (SCREEN_WIDTH/2 - 50, SCREEN_HEIGHT/2 + 50, 100, 50))
    quit_button = pygame.draw.rect(screen, (255, 0, 0), (SCREEN_WIDTH/2 - 50, SCREEN_HEIGHT/2 + 110, 100, 50))
    
    # Verificar se o botão "continuar" foi clicado
    if continue_button.collidepoint(pygame.mouse.get_pos()):
        if pygame.mouse.get_pressed()[0]:
            paused = False
            
    # Verificar se o botão "sair" foi clicado
    if quit_button.collidepoint(pygame.mouse.get_pos()):
        if pygame.mouse.get_pressed()[0]:
            pygame.quit()
            sys.exit()





    

    




    






