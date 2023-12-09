def install_and_import(package):          #https://stackoverflow.com/questions/12332975/how-can-i-install-a-python-module-within-code
    import importlib
    try:
        importlib.import_module(package)
    except ImportError:
        import pip
        pip.main(['install', package])
    finally:
        globals()[package] = importlib.import_module(package)

install_and_import('pygame')
import os
import random
install_and_import('easygui')
install_and_import('webbrowser')
import webbrowser
import pygame
from easygui import *
global username
username = 'анонимус'
username_max_length = 8
spd = 1
mode = 1
mode_name = 'червяк'
square_size = 12 #ширина змейки
spawn_len = 5
background_color = (230, 230, 230) #светло-серый
snake_colors = [(0, 0, 0), (150, 75, 0), (255, 128, 0), (102, 255, 0), (0, 0, 0)] #цвета червя, удава, гадюки и питона соответственно, нумерация с 1
fruit_color = (252, 15, 192)
snake_speeds = [100, 2, 3, 6, 12] #cкорость в каждом режиме; они должны быть делителями square_size чтобы квадратики попадали точно в точки поворота
modes = {'червяк': 1, 'удав': 2, 'гадюка': 3, 'питон': 4}
screen_width = 500
screen_height = 520
window_size = (screen_width, screen_height)
score = 0


class body_part(pygame.sprite.Sprite):
    # в переменной turns хранится массив из будущих поворотов, turns[0] - вектор следующего поворота turns[i] = ((x, y), (dx, dy))
    def __init__(self, x, y, v, turns):
        self.x = x
        self.y = y
        self.v = v
        self.turns = turns
        self.rect = pygame.Rect(self.x, self.y, square_size, square_size)

    def move(self):
        #проверяем нужно ли повернуть
        if len(self.turns):
            if self.x == self.turns[0][0][0] and self.y == self.turns[0][0][1]:
                self.v = self.turns[0][1]
                self.turns.pop(0)
        self.x += self.v[0]
        self.y += self.v[1]



#делает окошко для ввода имени, сохраняет в переменную username и обрезает до 8 символов
def enter_username():
    global username
    msg = "Введите имя"
    title = "Добро пожаловать"
    var1 = enterbox(msg, title)
    if var1:                        #если пользователь нажмет на cancel, то установится дефолтный юзернейм
        username = var1
    if len(username) > username_max_length:
        username = username[:username_max_length]


#делает окошко с выбором сложности, пока что сложность влияет только на скорость
def choose_level():
    global spd
    global mode
    global mode_name
    mode_name = buttonbox(msg='выберите уровень сложности', title='змейка', choices=('червяк', 'удав', 'гадюка', 'питон'))
    mode = modes[mode_name]
    spd = snake_speeds[mode]


#выводит доску лидеров, пока пустая
def show_leaderboard():
    pass


#обновляет json с таблицей лидеров, пока пустая
def save_highscore():
    pass


def game_over():
    global score
    score = real_score(score)
    save_highscore()
    menu()


    # корректируем очки чтобы не были слишком большими и чтобы были круглыми, можно будет в конце подкорректировать
def real_score(sc):
    sc //= 100
    sc *= 5
    sc *= mode
    return sc


def RickRoll():
    webbrowser.open_new('https://youtu.be/dQw4w9WgXcQ')


#менюшка где можно поменять имя, сложность, начать играть, посмотреть таблицу лидеров, выйти и зарикроллиться
#запускается только после игры
def menu():
    message = 'Отличная игра, '+username+'! Вы набрали '+str(score)+' очков!'
    choice = buttonbox(msg=message, title='змейка', choices=('играть заново', 'переименоваться', 'выбор сложности', 'посмотреть таблицу лидеров', 'выйти', 'эротический режим'))
    if choice == 'играть заново':
        play()
    if choice == 'переименоваться':
        enter_username()
        menu()
    if choice == 'выбор сложности':
        choose_level()
        menu()
    if choice == 'посмотреть таблицу лидеров':
        show_leaderboard()
        menu()
    if choice == 'выйти':
        exit()
    if choice == 'эротический режим':
        RickRoll()


#собственно игра
def play():
    global score
    score = 0
    v = (spd, 0) #вектор скорости
    new_v = (spd, 0)
    col = snake_colors[mode]
    pygame.init()
    pygame.mixer.music.load("nyeh.wav")
    pygame.mixer.music.play(loops=100)

    pygame.display.set_caption('супер-' + mode_name)
    screen = pygame.display.set_mode(window_size)
    screen.fill(background_color)
    pygame.display.flip()
    font = pygame.font.Font(None, 30)
    running = True
    snake = []
    for i in range(spawn_len):
        snake.append(body_part(screen_width//2 - i*square_size, screen_height//2, v, []))
    #snake = [body_part(250, 250, v, []), body_part(250-square_size, 250, v, []), body_part(250-2*square_size, 250, v, [])]

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                game_over()
                return 0
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                    new_v = (0, spd)
                if keys[pygame.K_UP] or keys[pygame.K_w]:
                    new_v = (0, -1*spd)
                if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                    new_v = (-1*spd, 0)
                if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                    new_v = (spd, 0)
                if new_v != v:
                    v = new_v
                    for p in snake:
                        p.turns.append(((snake[0].x, snake[0].y), v))

        screen.fill(background_color)
        for p in snake:
            p.move()
            pygame.draw.rect(screen, col, (p.x, p.y, square_size, square_size))
        # проверка столкновения со стенами
        if snake[0].x < 0 or snake[0].y < 45 or snake[0].x > screen_width - square_size or snake[0].y > screen_height - square_size:
            pygame.quit()
            game_over()
            return 0
        s = font.render("Score: " + str(real_score(score)), 1, (0, 0, 0))
        screen.blit(s, (10, 10))
        pygame.draw.line(screen, (0, 0, 0), (0, 40), (500, 40), 5)
        pygame.display.update()
        score += 1
        pygame.time.Clock().tick(30)


if __name__ == '__main__':
    enter_username()
    choose_level()
    play()
