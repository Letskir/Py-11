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
jump_num=40
is_on_ground = False  # Новая переменная для отслеживания контакта с землей

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

walls_group = sprite.Group()

# (R, G, B, width, height, x, y)
platforms_data = [
    # Нижний уровень
    (0,100,0,170,20,50,600),

    (0,100,0,130,20,300,600),       
    (0,100,0,130,20,550,600),
    (0,100,0,130,20,800,600),
    
    #Ступенька на средний уровень справа экрана
    (0,100,0, 50, 20, 980, 500),
    
    # Средний уровень 
    
    (0,100,0,40,20,830,400),

    
    (0,100,0,40,20,80,400),
    #Ступенька на верхний уровень слева экрана
    (0,100,0, 50, 20, 0, 270),
 
    # Верхний уровень с трёмя платформами по 150 пикселей шириной на 200 высоте с расстоянием между ними
    
    (0,100,0,150,20,150,200),
    (0,100,0,150,20,400,200),
    (0,100,0,150,20,650,200), 


    # Платформы у скалы

    (255, 128, 0, 150, 20, 900, 150),
]

for data in platforms_data:
    wall = Wall(*data)
    walls_group.add(wall)

class MovingPlatform(Wall):
    def __init__(self, color_1, color_2, color_3, wall_width, wall_height, x, y, x_start, x_end, speed):
        super().__init__(color_1, color_2, color_3, wall_width, wall_height, x, y)
        self.x_start = x_start
        self.x_end = x_end
        self.speed = speed
        self.direction = 1  # 1 = вправо, -1 = влево

    def update(self):
        self.rect.x += self.speed * self.direction

        if self.rect.x < self.x_start:
            self.rect.x = self.x_start
            self.direction = 1
        elif self.rect.x + self.width > self.x_end:
            self.rect.x = self.x_end - self.width
            self.direction = -1

    def is_player_on(self, player):
        return (
            player.rect.bottom <= self.rect.top + 10 and
            player.rect.bottom >= self.rect.top - 10 and
            player.rect.right > self.rect.left and
            player.rect.left < self.rect.right
        )

moving_platform = MovingPlatform(0, 100, 0, 40,20, 750, 400, 150, 750, 2)
walls_group.add(moving_platform)

# Класс игрока
class Player(GameSprite):
    def __init__(self, im, speed, x, y, w, h):
        super().__init__(im, speed, x, y, w, h)
        self.napravlenie = "right"  # Начальное направление
        self.anim_count = 0  # Счетчик для замедления анимации
        self.anim_speed = 5  # Скорость смены кадров
        self.is_on_ground = False  # Флаг для определения, стоит ли персонаж на земле
        self.y_velocity = 0  # Скорость по вертикали
        
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
        global jump, jump_num
        keys = key.get_pressed()
        self.is_moving = False
        
        # Движение влево
        if keys[K_LEFT] and self.rect.x > 10:
            self.is_moving = True
            self.napravlenie = "left"
            self.rect.x -= self.speed
            
            # Проверка столкновения
            if self.check_collision_horizontal():
                self.rect.x += self.speed
        
        # Движение вправо
        elif keys[K_RIGHT] and self.rect.x < w1 - 50:
            self.is_moving = True
            self.napravlenie = "right"
            self.rect.x += self.speed
            
            # Проверка столкновения
            if self.check_collision_horizontal():
                self.rect.x -= self.speed
            
        # Прыжок
        if keys[K_UP] and self.is_on_ground:
            jump = True
            self.is_on_ground = False
            self.y_velocity = -20  # Начальная скорость прыжка
        
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
        
        # Принудительная отрисовка персонажа
        self.reset()

    # Проверка горизонтальных столкновений
    def check_collision_horizontal(self):
        for wall in walls_group:
            if sprite.collide_rect(self, wall):
                return True
        return False
        
    # Проверка вертикальных столкновений и гравитация
    def check_collision_vertical(self):
        self.is_on_ground = False
        
        if self.rect.y + self.rect.height >= h1:
            self.rect.x = 50
            self.rect.y = 505
            self.y_velocity = 0
            return True  # чтобы прекратить дальнейшие проверки
        
        # Проверка столкновения с платформами
        platform_collision = False
        for wall in walls_group:
            if sprite.collide_rect(self, wall):
                # Если персонаж находится над платформой (приземляется)
                if self.rect.y + self.rect.height <= wall.rect.y + 10 and self.y_velocity >= 0:
                    self.is_on_ground = True
                    self.rect.y = wall.rect.y - self.rect.height
                    self.y_velocity = 0
                    platform_collision = True
                # Если персонаж ударяется о платформу снизу
                elif self.rect.y >= wall.rect.y + wall.rect.height - 10 and self.y_velocity < 0:
                    self.rect.y = wall.rect.y + wall.rect.height
                    self.y_velocity = 0
                    platform_collision = True
        
        return platform_collision
    
    # Применение гравитации и перемещение по вертикали
    def apply_gravity(self):
        # Обработка прыжка
        if jump and self.y_velocity <= 0:
            self.y_velocity = min(self.y_velocity + 0.8, 10)  # Постепенное уменьшение высоты прыжка
            
        # Применение гравитации
        if not self.is_on_ground:
            self.y_velocity += 0.5  # Ускорение свободного падения
            if self.y_velocity > 10:  # Максимальная скорость падения
                self.y_velocity = 10
        
        # Применение вертикальной скорости
        self.rect.y += int(self.y_velocity)
        
        # Проверка столкновений после перемещения
        self.check_collision_vertical()

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

# Класс врагов
class Enemy(GameSprite):
    def __init__(self, left_imgs, right_imgs, speed, x, y, w, h, x_start, x_end):
        super().__init__(left_imgs[0], speed, x, y, w, h)
        # Анимационные кадры
        self.frames_l = [transform.scale(image.load(img), (w, h)) for img in left_imgs]
        self.frames_r = [transform.scale(image.load(img), (w, h)) for img in right_imgs]

        self.image = self.frames_l[0]  # Начальное изображение
        self.direction = "l"
        self.x_start = x_start
        self.x_end = x_end

        self.anim_index = 0
        self.anim_timer = 0
        self.anim_speed = 10  # Каждые 10 тиков

    def update(self):
        # Движение
        if self.direction == "l":
            self.rect.x -= self.speed
            current_frames = self.frames_l
        else:
            self.rect.x += self.speed
            current_frames = self.frames_r

        # Переключение кадров анимации
        self.anim_timer += 1
        if self.anim_timer >= self.anim_speed:
            self.anim_timer = 0
            self.anim_index = (self.anim_index + 1) % len(current_frames)

        self.image = current_frames[self.anim_index]

        # Изменение направления
        if self.rect.x >= self.x_end:
            self.direction = "l"
        elif self.rect.x <= self.x_start:
            self.direction = "r"  # ← вот тут было забыто присваивание

monstr = Enemy(
    ["l/monstr_anim1l.png", "l/monstr_anim2l.png"],  # Кадры влево
    ["r/monstr_anim1r.png", "r/monstr_anim2r.png"],  # Кадры вправо
    7, 100, 150, 66, 36, 100, 800  # Начальные координаты и размеры
)


btn_restart = GameSprite("btn.png", 0, 0, 0, 150, 75)
gg = Player("r/G_right.png", 4, 50, 505, 40, 56)

# Переменные для жизни игрока
finish = False
x, y = -1, -1

# Функция для начального меню
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

# Запуск начального меню
start_menu()

# Основной игровой цикл
while game:
    for ev in event.get():
        if ev.type == QUIT:
            game = False
        if ev.type == MOUSEBUTTONDOWN:
            x, y = ev.pos
        if btn_restart.rect.collidepoint(x, y):
            finish = False
            x, y = -1, -1  # Сбрасываем координаты клика
            gg.rect.x = 50  # Начальные координаты игрока
            gg.rect.y = 505
            mixer.music.load("Terraria.ogg")  # Перезапускаем музыку
            mixer.music.play()
        if ev.type == KEYDOWN:
            if ev.key == K_ESCAPE:
                game = False

    if sprite.collide_rect(gg, monstr):
        finish = True
        window.blit(lose2, (w1/3-2, h1/3+2))
        window.blit(lose2, (w1/3+2, h1/3-2))
        window.blit(lose, (w1/3, h1/3))
        mixer.music.play()

    if finish != True:
        window.fill((0, 0, 100))
        window.blit(bg, (0, 0))
        btn_restart.reset()
        gg.update()
        gg.apply_gravity()

        # Телепорт на спавн если упал вниз
        if gg.rect.y > h1:
            gg.rect.x = 50
            gg.rect.y = 505

        if gg.rect.x > 900 and gg.rect.y < 150:
            finish = True

            window.blit(font1.render("You win", False, (0, 0, 0)), (w1/3+2, h1/3-2))  # тень
            window.blit(font1.render("You win", False, (0, 0, 0)), (w1/3-2, h1/3-2))  # тень
            window.blit(font1.render("You win", False, (0, 0, 0)), (w1/3+2, h1/3+2))  # тень
            window.blit(font1.render("You win", False, (0, 0, 0)), (w1/3-2, h1/3+2))  # тень
            window.blit(font1.render("You win", False, (0, 100, 0)),(w1/3, h1/3))  # основной текст

        moving_platform.update()

        # Перемещение игрока вместе с платформой
        if moving_platform.is_player_on(gg):
            gg.rect.x += moving_platform.speed * moving_platform.direction 

        monstr.reset()
        monstr.update()
        walls_group.draw(window)

    display.update()
    clock.tick(FPS)
    
quit()