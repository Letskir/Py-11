from pygame import *
from random import randint
# Инициализация Pygame
font.init()
mixer.init()

# Настройки окна
window = display.set_mode((1020, 700))
bg = transform.scale(image.load("Background_178.png"), (1020, 700))
w1, h1 = window.get_size()
mixer.music.load("Terraria.ogg")
mixer.music.play()

# Шрифты
font1 = font.Font("Comic Sans MS.ttf", 70)
font2 = font.Font("Comic Sans MS.ttf", 30)
lose=font1.render("You were slain...", False, (187,22,43))
lose2=font1.render("You were slain...", False, (0,0,0))
lose3=font1.render("You were slain...", False, (0,0,0))
win=font1.render("You win", False, (22,187,43))

  
music_hurt=mixer.Sound("hurt.mp3")
music_hurt.set_volume(0.1)
# Переменные  
game = True
clock = time.Clock()
FPS = 60
game_started = False

# Лор игры
ready_text = font2.render("Нажмите 'Готово' для начала!", True, (187,22,43))
#для анимации персонажа
guide_r=[transform.scale(image.load("r/G_right.png"),(40,56)),
         transform.scale(image.load("r/G_right1.png"),(40,56)),
         transform.scale(image.load("r/G_right2.png"),(40,56)),
         transform.scale(image.load("r/G_right3.png"),(40,56)),
         transform.scale(image.load("r/G_right4.png"),(40,56)),
         transform.scale(image.load("r/G_right5.png"),(40,56)),
         transform.scale(image.load("r/G_right6.png"),(40,56)),
         transform.scale(image.load("r/G_right7.png"),(40,56))]
anim_r=0
guide_l=[transform.scale(image.load("l/G_left.png"),(40,56)),
         transform.scale(image.load("l/G_left1.png"),(40,56)),
         transform.scale(image.load("l/G_left2.png"),(40,56)),
         transform.scale(image.load("l/G_left3.png"),(40,56)),
         transform.scale(image.load("l/G_left4.png"),(40,56)),
         transform.scale(image.load("l/G_left5.png"),(40,56)),
         transform.scale(image.load("l/G_left6.png"),(40,56)),
         transform.scale(image.load("l/G_left7.png"),(40,56))]
anim_l=0

# Класс для спрайтов

class GameSprite(sprite.Sprite):    
    def __init__(self,im, speed,x,y,w,h):
        super().__init__()           
        self.image=transform.scale(image.load(im),(w,h))
        self.speed=speed
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))
jump=False
gravity=0
jump_num=10
# Класс стен

class Wall(sprite.Sprite):
    def __init__(self, color_1,color_2,color_3,wall_width,wall_height,x,y):
        super().__init__()
        self.color_1=color_1
        self.width=wall_width
        self.height=wall_height
        self.image=Surface((self.width,self.height))
        self.image.fill((color_1,color_2,color_3))
        self.rect=self.image.get_rect()
        self.rect.x=x 
        self.rect.y=y
    def draw_wall(self):
        window.blit(self.image,(self.rect.x,self.rect.y))

walls_group=sprite.Group()
wall1=Wall(0,0,100,200,50,50,600)
wall2=Wall(0,0,100,200,50,320,420)
wall3=Wall(0,0,100,200,50,650,600)
walls_group.add(wall1)
walls_group.add(wall2)
walls_group.add(wall3)
# Класс игрока
class Player(GameSprite):
    def __init__(self, im, speed, x, y, w, h):
        super().__init__(im, speed, x, y, w, h)
        self.napravlenie = "right"  # Начальное направление
        self.anim_count = 0  # Счетчик для замедления анимации
        self.anim_speed = 5  # Скорость смены кадров
        
        # Загрузка спрайтов анимации
        self.guide_r = [
            transform.scale(image.load("r/G_right.png"), (40, 56)),
            transform.scale(image.load("r/G_right1.png"), (40, 56)),
            transform.scale(image.load("r/G_right2.png"), (40, 56)),
            transform.scale(image.load("r/G_right3.png"), (40, 56)),
            transform.scale(image.load("r/G_right4.png"), (40, 56)),
            transform.scale(image.load("r/G_right5.png"), (40, 56)),
            transform.scale(image.load("r/G_right6.png"), (40, 56)),
            transform.scale(image.load("r/G_right7.png"), (40, 56))
        ]
        
        self.guide_l = [
            transform.scale(image.load("l/G_left.png"), (40, 56)),
            transform.scale(image.load("l/G_left1.png"), (40, 56)),
            transform.scale(image.load("l/G_left2.png"), (40, 56)),
            transform.scale(image.load("l/G_left3.png"), (40, 56)),
            transform.scale(image.load("l/G_left4.png"), (40, 56)),
            transform.scale(image.load("l/G_left5.png"), (40, 56)),
            transform.scale(image.load("l/G_left6.png"), (40, 56)),
            transform.scale(image.load("l/G_left7.png"), (40, 56))
        ]
        
        self.current_frame = 0
        self.is_moving = False
    
    def update(self):
        global jump,jump_num
        keys = key.get_pressed()
        self.is_moving = False
        
        # Движение влево
        if keys[K_LEFT] and self.rect.x > 10:
            self.is_moving = True
            self.napravlenie = "left"
            self.rect.x -= self.speed
            
            # Проверка столкновения
            if self.check_collision():
                self.rect.x += self.speed
                
        
        # Движение вправо
        elif keys[K_RIGHT] and self.rect.x < w1 - 50:
            self.is_moving = True
            self.napravlenie = "right"
            self.rect.x += self.speed
            
            # Проверка столкновения
            if self.check_collision():
                self.rect.x -= self.speed
            
        if keys[K_UP] and gravity==False:
                jump=True
        # # Движение вверх
        # elif keys[K_UP] and self.rect.y > 10 and sprite.spritecollide(self,walls_group,False):
        #     self.is_moving = True

        #     jump=True
                
        #     # Проверка столкновения
        #     if self.check_collision():
        #         self.rect.y += self.speed
        #         music_hurt.play()
        
        # Обновление анимации
        self.anim_count += 1
        if self.is_moving:
            # Замедление анимации
            if self.anim_count >= self.anim_speed:
                self.anim_count = 0
                self.current_frame = (self.current_frame + 1) % 8
                
                # Выбор спрайтов в зависимости от направления
                if self.napravlenie == "right":
                    self.image = self.guide_r[self.current_frame]
                else:
                    self.image = self.guide_l[self.current_frame]
        else:
            # Статичное изображение
            if self.napravlenie == "right":
                self.image = self.guide_r[0]
            else:
                self.image = self.guide_l[0]
        

        # def jump_def():
        #     global jump,jump_num
        #     if jump_num>0:
        #         self.rect.y-=5    
        #         jump_num-=1
        #     else:
        #         jump=False
        #         jump_num=40    
        # if jump==True:
        #     jump_def()
    def check_collision(self):
            global gravity
            # Проверка столкновения с стенами
            if self.rect.y + self.rect.height >= h1:
                gravity=False
                self.rect.y = h1 - self.rect.height
            elif self.rect.y <= 0:
                gravity=False
                self.rect.y = 0
            if sprite.spritecollide(self, walls_group, False):
                gravity= False
            else:
                gravity=True
            try:
                w = sprite.spritecollideany(self, walls_group)
                if self.rect.y + self.rect.height >= w.rect.y and self.rect.x + self.rect.width > w.rect.x and self.rect.x < w.rect.x + w.rect.width:
                    self.rect.y = w.rect.y - self.rect.height
            except:
                pass
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

# Класс врагов


class Enemy(GameSprite):
    def __init__(self, lim, rim, speed, x, y, w, h,x_start, x_end):
        super().__init__(lim, speed, x, y, w, h)
        self.picl = transform.scale(image.load(lim), (w, h))
        self.picr = transform.scale(image.load(rim), (w, h))
        self.image = self.picl  # Начальное изображение
        self.direction = "l"
        self.x_start = x_start
        self.x_end = x_end

    def update(self):
        if self.direction == "l":
            self.rect.x -= self.speed
            self.image = self.picl  # Устанавливаем изображение для движения влево
        else:
            self.rect.x += self.speed
            self.image = self.picr  # Устанавливаем изображение для движения вправо

        # Проверка границ и изменение направления
        if self.rect.x >= self.x_end:
            self.direction = "l"
        elif self.rect.x <= self.x_start:
            self.direction = "r"

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))  # Отображаем текущее изображение врага


monstr = Enemy("l/monstr_anim1l.png", "r/monstr_anim1r.png", 2, 100, 100, 66, 36, 100, 500)
btn_restart=GameSprite("btn.png",0,0,0,150,75)
gg=Player("r/G_right.png",4,50,505,40,56)
# Переменные для жизни игрока
finish=False
x,y=-1,-1
# Создание объектов игры

def start_menu():
    while True:
        window.fill((0, 0, 0))  # Чёрный фон

        # Отображение текста лора
        font_start = font.Font(None, 36)
        lore_text = [
            "Вы - последний житель мира Terraria.",
            "Ваш мир атакован Марсианами.",
            "Вам нужно пройти в комнату от управления НЛО.",
            "Чтобы остановить их и спасти мир.",
            "Нажмите 'Готово', чтобы начать."
        ]
        
        for i, line in enumerate(lore_text):
            text_surface = font_start.render(line, True, (255, 255, 255))
            window.blit(text_surface, (50, 50 + i * 30))

        # Кнопка "Готово"
        btn_ready = font_start.render("Готово", True, (255, 0, 0))
        btn_rect = btn_ready.get_rect(center=(360, 400))
        window.blit(btn_ready, btn_rect)

        for ev in event.get():
            if ev.type == QUIT:
                quit()
            if ev.type == MOUSEBUTTONDOWN:
                if btn_rect.collidepoint(ev.pos):
                    return  # Переход к игре

        display.update()
gravity=True
start_menu()
# Основной игровой цикл
while game:
    for ev in event.get():
        if ev.type == QUIT:
            game=False
        if ev.type==MOUSEBUTTONDOWN:
            x,y=ev.pos
        if btn_restart.rect.collidepoint(x, y):
            finish = False
            x, y = -1, -1  # Сбрасываем координаты клика
            gg.rect.x = 50  # Начальные координаты игрока
            gg.rect.y = 100
            mixer.music.load("Terraria.ogg")  # Перезапускаем музыку
            mixer.music.play()
        if ev.type==KEYDOWN:
            if ev.key==K_ESCAPE:
                game=False
            

    if sprite.collide_rect(gg,monstr):
        finish=True

        window.blit(lose2,(w1/3-2,h1/3+2))
        window.blit(lose2,(w1/3+2, h1/3-2))
        window.blit(lose,(w1/3,h1/3))
        
        mixer.music.play()

    if finish!=True :
        window.fill((0, 0, 100))
        window.blit(bg,(0,0))
        btn_restart.reset()
        gg.update()
        gg.check_collision()
        monstr.reset()
        monstr.update()
        walls_group.draw(window)
        if jump:
            if jump_num>0:
                gg.rect.y-=10
                jump_num-=1
            else:
                jump=False
                jump_num=20
        if gravity:
            gg.rect.y+=4
        display.update() # Обновление экрана
    display.update()
    clock.tick(FPS)

    
quit()