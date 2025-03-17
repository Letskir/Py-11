from pygame import *
from random import randint
# Инициализация Pygame
font.init()
mixer.init()

# Настройки окна
window = display.set_mode((1024, 838))
bg = transform.scale(image.load("Background_178.png"), (1024, 838))
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

# Класс игрока
class Player(GameSprite):
    def update(self):
        global anim_r, anim_l
        keys=key.get_pressed()
        napravlenie="right"
        if keys[K_LEFT] and self.rect.x>10:
            if anim_l <=7:
                window.blit(guide_l[anim_l],(self.rect.x, self.rect.y))
                anim_l+=1
            else:
                anim_l=0
                window.blit(guide_l[anim_l],(self.rect.x, self.rect.y))
            self.rect.x-=self.speed
            napravlenie="left"
            if self.check_collision():
                self.rect.x+=self.speed
                music_hurt.play()


        elif keys[K_RIGHT] and self.rect.x<w1-50:
            if anim_r <=7:
                window.blit(guide_r[anim_r],(self.rect.x, self.rect.y))
                anim_r+=1
            else:
                anim_r=0
                window.blit(guide_r[anim_r],(self.rect.x, self.rect.y))
            self.rect.x+=self.speed
            if self.check_collision():
                self.rect.x-=self.speed
                music_hurt.play()
            napravlenie="right"  

        elif keys[K_UP] and self.rect.y>10 and sprite.collide_rect(gg,btn_restart)!=True:
            if napravlenie=="right":
                if anim_r <=7:
                    window.blit(guide_r[anim_r],(self.rect.x, self.rect.y))
                    anim_r+=1
                else:
                    anim_r=0
                    window.blit(guide_r[anim_r],(self.rect.x, self.rect.y))
            if napravlenie=="left":
                if anim_l <=7:
                    window.blit(guide_l[anim_l],(self.rect.x, self.rect.y))
                    anim_l+=1
                else:
                    anim_l=0
                    window.blit(guide_l[anim_l],(self.rect.x, self.rect.y)) 
            self.rect.y-=self.speed
            if self.check_collision():
                self.rect.y+=self.speed
                music_hurt.play()


        elif keys[K_DOWN]and self.rect.y<750:
            if napravlenie=="right":
                if anim_r <=7:
                    window.blit(guide_r[anim_r],(self.rect.x, self.rect.y))
                    anim_r+=1
                else:
                    anim_r=0
                    window.blit(guide_r[anim_r],(self.rect.x, self.rect.y))
            if napravlenie=="left":
                if anim_l <=7:
                    window.blit(guide_l[anim_l],(self.rect.x, self.rect.y))
                    anim_l+=1
                else:
                    anim_l=0
                    window.blit(guide_l[anim_l],(self.rect.x, self.rect.y)) 
            self.rect.y+=self.speed
            if self.check_collision():
                self.rect.y-=self.speed
                music_hurt.play()
            
                
        else:
            self.reset()
    def check_collision(self):
         for wall in walls:
             if sprite.collide_rect(self, wall):
                 return True
         return False


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


monstr = Enemy("l/monstr_anim1l.png", "r/monstr_anim1r.png", 2, 100, 100, 66, 36, 100, 500)
btn_restart=GameSprite("btn.png",0,0,0,150,75)
gg=Player("r/G_right.png",4,50,100,40,56)
# Переменные для жизни игрока
finish=False
x,y=-1,-1
# Создание объектов игры
walls = [Wall(0,0,0,10,755,0,0)]


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
        monstr.reset()
        monstr.update()
        for wall in walls:
            wall.draw_wall() # Отрисовка стен
        display.update() # Обновление экрана
    display.update()
    clock.tick(FPS)

    
quit()