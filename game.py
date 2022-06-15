#подключение модулей, переменные (Делает Чекерес Владислав)
from random import randint
from pygame import*
font.init()

font1 = font.Font(None, 72)
font2 = font.Font(None, 72)
win_width = 800
win_height = 600
left_bound = win_width / 40
right_bound = win_width - 8 * left_bound
shift = 0

x_start = 20
y_start = 10

img_file_back = 'bg.jpg'
img_file_hero = 'player.png'
img_file_enemy = 'sprite.png' 
img_file_bomb = 'bomb.png'
img_file_door = 'door.png'
img_wall = 'wall.png'
img_key='key.png'
img_button_start='play.png'
img_file_back_start = "bgmenu.png"
FPS = 60

C_WHITE = (255, 255, 255)
C_DARK = (48, 48, 0)
C_YELLOW = (255, 255, 87)
C_GREEN = (32, 128, 32)
C_RED = (255, 0, 0)
C_BLACK = (0, 0, 0)

#music
mixer.init()
mixer.music.load('music.ogg')
mixer.music.play()

#финальный спрайт (Делает Ширяев Андрей)
class FinalSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        sprite.Sprite.__init__ (self)
        self.image = transform.scale(image.load(player_image), (100, 100)) 
        self.speed = player_speed 
        self.rect = self.image.get_rect() 
        self.rect.x = player_x 
        self.rect.y = player_y
        
#главный герой свойтва (Делает Кривша Анатолий)
class Hero(sprite.Sprite):
	def __init__(self, filename, x_speed = 0, y_speed = 0, x=x_start,y=y_start, width = 60, height = 60):
		sprite.Sprite.__init__(self)
		self.image = transform.scale(image.load(filename), (width, height)).convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.x_speed = x_speed
		self.y_speed = y_speed
		self.stands_on = False

	#главный герой методы (Делает Кривша Анатолий)
	def gravitate(self):
	    self.y_speed += 0.25

	def jump(self, y):
	    if self.stands_on:
		    self.y_speed = y

	def update(self):
	    self.rect.x += self.x_speed
	    platforms_touched = sprite.spritecollide(self, barriers, False)
	    if self.x_speed > 0:
		    for p in platforms_touched:
		        self.rect.right - min(self.rect.right, p.rect.left)
	    elif self.x_speed < 0:
		    for p in platforms_touched:
		        self.rect.left = max(self.rect.left, p.rect.right)

	    self.gravitate()
	    self.rect.y += self.y_speed
	    platforms_touched = sprite.spritecollide(self, barriers, False)
	    if self.y_speed > 0:
		    for p in platforms_touched:
		        self.y_speed = 0
		        if p.rect.top < self.rect.bottom:
			        self.rect.bottom = p.rect.top
			        self.stands_on = p
	    elif self.y_speed < 0:
		    self.stands_on = False
		    for p in platforms_touched:
		        self.y_speed = 0
		        self.rect.top = max(self.rect.top, p.rect.bottom)

#класс стен (Делает Сьомкин Владислав)
class Wall(sprite.Sprite):
	def __init__(self,filename,x=20,y=0,width=100,height=100):
		sprite.Sprite.__init__(self)
		self.image = transform.scale(image.load(filename),(width,height)).convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
	
#Класс врагов
class Enemy(sprite.Sprite): # - враг
    def __init__(self, x=20, y=0, filename=img_file_enemy, width=60, height=60):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(filename), (width, height)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        '''перемещает персонажа, применяя текущюу горизонтаьную и вертикальную скорость'''
    def update(self):
        if self.rect.x <= 300:
            self.side = 'right'
        if self.rect.x >= 600:
            self.side = 'left'
        if self.side == "left":
            self.rect.x -= 5
        else:
            self.rect.x += 5

class CoinSprite(sprite.Sprite):
  # конструктор класса
  def __init__(self, filename, player_x, player_y, width=50, height=50):
        # Вызываем конструктор класса (Sprite):
        sprite.Sprite.__init__(self)

        # каждый спрайт должен хранить свойство image - изображение
        # картинка загружается из файла и умещается в прямоугольник нужных размеров:
        self.image = transform.scale(image.load(filename), (width, height)).convert_alpha() 
                        # используем convert_alpha, нам надо сохранять прозрачность

            # каждый спрайт должен хранить свойство rect - прямоугольник. Это свойство нужно для определения касаний спрайтов.         

        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
#Класс кнопок
class Button(sprite.Sprite):
    def __init__(self,player_image,player_x,player_y):
        sprite.Sprite.__init__(self)

        self.image = transform.scale(image.load(player_image),(200,100))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def collidepoint(self,x,y):
        return self.rect.collidepoint(x,y)

#список кнопок
buttons=sprite.Group()
button1=Button(img_button_start,300,250)
buttons.add(button1)

#запуск игры (Делает Лущик Артем)
display.set_caption("ARCADA")
window = display.set_mode([win_width, win_height])
back = transform.scale(image.load(img_file_back).convert(), (win_width, win_height))
all_sprites = sprite.Group()
back_start = transform.scale(image.load(img_file_back_start).convert(), (win_width, win_height))
barriers = sprite.Group()
enemies = sprite.Group()
bombs = sprite.Group()
# список ключей:
keys = sprite.Group()
key=FinalSprite(img_key, 500,  130, 0)
keys.add(key)
all_sprites.add(key)
robin = Hero(img_file_hero)
all_sprites.add(robin)
count_k=0
#создаем стены, добавляем их:
list_blocks=['1100100010001111','00110100000','000011110000111','0011111111111111111111111111','00111111111111111111111111111']
for i in range(len(list_blocks)):
    for j in range(len(list_blocks[i])):
        if list_blocks[i][j]=='1':
            #print(i,j)
            w = Wall(img_wall,(j)*80,(i+1)*130,100,50)
            barriers.add(w)
            all_sprites.add(w)

#создаем врагов, добавлям их:'1100100010001111','00110100000','000011110000111','0011111111111111111111111111','00111111111111111111111111111'
en = Enemy(300, 330)
all_sprites.add(en)
enemies.add(en)


#создаем мины, добавляем их:
bomb = Enemy(250, 200, img_file_bomb, 60, 60)
bombs.add(bomb) #в список всех спрайтов бомбы не добавляем, будем рисовать их отдельной командой
                #так легко сможем подрывать бомбы, а также делаем их неподвижными, update() не вызывается

#создаем финальный спрайт, добавляем его:
door = FinalSprite(img_file_door, win_width + 500, win_height - 150, 0)
all_sprites.add(door)

#основной цикл игры, управление (Делает --)
run = True
finished = False

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_LEFT:
                robin.x_speed = -5
            elif e.key == K_RIGHT:
                robin.x_speed = 5
            elif e.key == K_UP:
                robin.jump(-7)

        elif e.type == KEYUP:
            if e.key == K_LEFT:
                robin.x_speed = 0
            elif e.key == K_RIGHT:
                robin.x_speed = 0
        if e.type == MOUSEBUTTONDOWN and e.button == 1:
            x,y = e.pos
            if button1.collidepoint(x,y):
                finished = False
                button1.kill(   )
                robin.kill()
                for key in keys:
                    key.kill()
                for bomb in bombs:
                    bomb.kill()
                robin = Hero(img_file_hero)
                all_sprites.add(robin)
                key=CoinSprite(img_key,randint(300,500),100,100)
                keys.add(key)
                all_sprites.add(key)
                bomb=Enemy(randint(50,500),200,img_file_bomb,60,60)
                bombs.add(bomb)
                count_k=0
    window.blit(back_start,(0,0))
    buttons.draw(window)

    if not finished:
        all_sprites.update()
        sprite.groupcollide(bombs, all_sprites, True, True)
        if sprite.spritecollide(robin, enemies, False):
            robin.kill()
        if sprite.spritecollide(robin, keys, False):
            key.kill() # метод kill убирает спрайт из всех групп, в которых он числится
            count_k+=1
            count_keys = font2.render("Количество ключей: "+str(count_k), 1, C_BLACK)

        if (
            robin.rect.x > right_bound and robin.x_speed > 0
            or
            robin.rect.x < left_bound and robin.x_speed < 0
        ):
            shift -= robin.x_speed
            for s in all_sprites:
                s.rect.x -= robin.x_speed
            for s in bombs:
                s.rect.x -= robin.x_speed
            for s in enemies:
                s.rect.x -= robin.x_speed

        #Конец игры (Делает ---)
        local_shift = shift % win_width 
        window.blit(back, (local_shift, 0 )) 
        if local_shift != 0:
            window.blit(back, (local_shift - win_width, 0 ))
        all_sprites.draw(window)
        bombs.draw(window)
        if sprite.collide_rect(robin, door):
            finished = True
            # window.fill ( c_BLACK ) 
            text = font1.render("YOU WIN!", 1, C_RED) 
            window.blit(text, (250,250))

        if robin not in all_sprites or robin.rect.top > win_height:
            finished = True
            text = font1.render('GAME OVER', 1, C_RED)
            window.blit(text, (250, 250))
    
    display.update()

    #пауза
    time.delay(20)
display.update()
