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
import pygame
from easygui import *
global username
username = 'анонимус'
username_max_length = 8
spd = 1
mode = 1
mode_name = 'червяк'
square_size = 10 #ширина змейки
background_color = (230, 230, 230) #светло-серый
snake_colors = [(0, 0, 0), (150, 75, 0), (255, 128, 0), (102, 255, 0), (0, 0, 0)] #цвета червя, удава, гадюки и питона соответственно, нумерация с 1
fruit_color = (252, 15, 192)
snake_speeds = [100, 2, 5, 8, 10] #cкорость в каждом режиме
modes = {'червяк': 1, 'удав': 2, 'гадюка': 3, 'питон': 4}
screen_width = 500
screen_height = 500
window_size = (screen_width, screen_height)
score = 0


class body_part(pygame.sprite.Sprite):
    def __init__(self, x, y, v):
        self.x = x
        self.y = y
        self.v = v



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
    #корректируем очки чтобы не были слишком большими и чтобы были круглыми, можно будет в конце подкорректировать
    score //= 100
    score *= 5
    score *= mode
    save_highscore()
    menu()


#менюшка где можно поменять имя, сложность, начать играть, посмотреть таблицу лидеров и выйти
#запускается только после игры
def menu():
    message = 'Отличная игра, '+username+'! Вы набрали '+str(score)+' очков!'
    choice = buttonbox(msg=message, title='змейка', choices=('играть заново', 'переименоваться', 'выбор сложности', 'посмотреть таблицу лидеров', 'выйти'))
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


#собственно игра
def play():
    global score
    score = 0
    v = (spd, 0) #вектор скорости
    col = snake_colors[mode]
    pygame.init()
    pygame.display.set_caption('супер-' + mode_name)
    screen = pygame.display.set_mode(window_size)
    screen.fill(background_color)
    pygame.display.flip()
    running = True
    snake = [body_part(250, 250, v)]
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                game_over()
                return 0
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_DOWN]:
                    v = (0, spd)
                if keys[pygame.K_UP]:
                    v = (0, -1*spd)
                if keys[pygame.K_LEFT]:
                    v = (-1*spd, 0)
                if keys[pygame.K_RIGHT]:
                    v = (spd, 0)
        screen.fill(background_color)
        for p in snake:
            p.v = v
            pygame.draw.rect(screen, col, (p.x, p.y, square_size, square_size))
            p.x += p.v[0]
            p.y += p.v[1]
        pygame.display.update()
        score += 1
        pygame.time.Clock().tick(30)



if __name__ == '__main__':
    enter_username()
    choose_level()
    play()
