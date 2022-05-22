#подключение модулей, переменные (Делает Чекерес Владислав)
from random import randint
from pygame import*
font.init()

font = font.Font(None, 72)
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
    def _init_(self, player_image, player_x, player_y, player_speed):
        sprite.Sprite._init_ (self)
        self.image = transform.scale(image.load(player_image), (100, 100)) 
        self.speed = player_speed 
        self.rect = self.image.get_rect() 
        self.rect.x = player_x 
        self.rect.y = player_y
        
#главный герой свойтва (Делает Кривша Анатолий)
class Hero(sprite.Sprite):
	def __init__(self, filename, x_speed = 0, y_speed = 0, x = x_start, width = 60, height = 60):
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
		    self.y_speed = y_speed

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
	    platforms_touched = spritecollide(self, barriers, False)
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

#запуск игры (Делает Лущик Артем)
display.set_caption("ARCADA")
window = display.set_mode([win_width, win_height])
back = transform.scale(image.load(img_file_back).convert(), (win_width, win_height))
all_sprites = sprite.Group()
barriers = sprite.Group()
enemies = sprite.Group()
bombs = sprite.Group()
robin = Hero(img_file_hero)
all_sprites.add(robin)

#создаем стены, добавляем их:
list_blocks=['1100100010001111','00110100000','000011110000111','0011111111111111111111111111','00111111111111111111111111111']
for i in range(len(list_blocks)):
    for j in range(len(list_blocks[i])):
        print(i,j)
        w = wall(img_wall,(j)*80,(i+1)*130,100,50)
        barriers.add(w)
        all_sprites.add(w)







#создаем врагов, добавлям их:
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

#В цикле пока не финиш (Делает -Артем)



























        #Конец игры (Делает ---)
        local_shift - shift % win_width 
        window.blit(back, (local_shift, 0 )) 
        if local_shift != 0:
            window.blit(back, (local_shift - win_width, 0 ))
        all_sprites.draw(window)
        bombs.draw(window)
        if sprite.collide_rect(robin, door):
            finished = True
            # window.fill ( c_BLACK ) 
            text = font.render("YOU WIN!", 1, C_RED) 
            window.blit(text, (250,250))

        if robin not in all_sprites or robin.rect.top > win_height:
            finished = True
            text = font.render('GAME OVER', 1, C_RED)
            window.blit(text, (250, 250))
    
    display.update()

    #пауза
    time.delay(20)
display.update()
