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
import json
import pygame
from easygui import *
global username
username = 'анонимус'
username_max_length = 8
spd = 3
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
fruit = 0
prep = [pygame.Rect(200, 200, square_size, square_size), pygame.Rect(200 + square_size, 200, square_size, square_size), pygame.Rect(200 + 2 * square_size, 200, square_size, square_size)]
colprep = (34, 65, 33)
coleda = (255, 0, 255)
coledaset = [(255, 0, 255), (102, 0, 153), (204, 6, 5), (102, 255, 0), (0, 168, 107)]
liders = {}
achievement = ""

class body_part():
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
        self.rect = pygame.Rect(self.x, self.y, square_size, square_size)

    def pr(self):
        print(self.x, self.y, self.v, self.turns)



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
    pass
def show_leaderboard(first):
    if os.path.exists("liders.json"):
        file_size = os.path.getsize("liders.json")

        if file_size > 0:
            f = open("liders.json", "r")
            liders = json.load(f)
            liders["A"] = (0, 0)
            liders["B"] = (0, 0)
            liders["C"] = (0, 0)
        else:
            liders = {}
            liders["A"] = (0, 0)
            liders["B"] = (0, 0)
            liders["C"] = (0, 0)
    else:
        liders = {}
        liders["A"] = (0, 0)
        liders["B"] = (0, 0)
        liders["C"] = (0, 0)
    liders_sorted = dict(sorted(liders.items(), key=lambda x: (-x[1][0], x[0])))
    message = 'Те, кем мы гордимся: \n\n 1. ' + str(list(liders_sorted.keys())[0]) + ' со счетом: ' + str(list(liders_sorted.values())[0][0]) + \
              '\n 2. ' + str(list(liders_sorted.keys())[1]) + ' со счетом: ' + str(list(liders_sorted.values())[1][0]) + \
              '\n 3. ' + str(list(liders_sorted.keys())[2]) + ' со счетом: ' + str(list(liders_sorted.values())[2][0])
    choice = buttonbox(msg=message, title='змейка', choices=('выйти', 'меню'))
    if choice == 'выйти':
        exit()
    if choice == 'меню':
        if first==0:
            menu_start()
        else:
            menu()

#обновляет json с таблицей лидеров
def save_highscore():
    if os.path.exists("liders.json"):
        file_size = os.path.getsize("liders.json")

        if file_size > 0:
            f = open("liders.json", "r")
            liders = json.load(f)
            liders["A"] = (0, 0)
            liders["B"] = (0, 0)
            liders["C"] = (0, 0)
        else:
            liders = {}
            liders["A"] = (0, 0)
            liders["B"] = (0, 0)
            liders["C"] = (0, 0)
    else:
        liders = {}
        liders["A"] = (0, 0)
        liders["B"] = (0, 0)
        liders["C"] = (0, 0)
    if username in liders.keys():
        if liders[username][0] < score:
            liders[username][0] = score

        if liders[username][1] < fruit:
            liders[username][1] = fruit
    else:
        liders[username] = (score, fruit)
    with open('liders.json', 'w') as f_liders:
        json.dump(liders, f_liders)
    pass



def game_over():
    save_highscore()
    menu()


    # корректируем очки чтобы не были слишком большими и чтобы были круглыми, можно будет в конце подкорректировать
def real_score(sc):
    sc //= 100
    sc *= 5
    sc *= mode
    return sc


def RickRoll():
    webbrowser.open_new('https://www.youtube.com/watch?v=hvL1339luv0')
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
        first=1
        show_leaderboard(first)
        menu()
    if choice == 'выйти':
        exit()
    if choice == 'эротический режим':
        RickRoll()

def setprep():
    global prep
    if mode == 1:
        prep = []
    if mode == 2:
        prep = [pygame.Rect(200, 140, 15 * square_size, square_size), pygame.Rect(200, 240, square_size, 8 * square_size)]
    if mode == 3:
        prep = [pygame.Rect(200, 140, 15 * square_size, square_size), pygame.Rect(80, 200,  square_size, 15 * square_size), pygame.Rect(80, 300, 10 * square_size, square_size)]
    if mode == 4:
        prep = [pygame.Rect(200, 140, 15 * square_size, square_size), pygame.Rect(80, 200,  square_size, 15 * square_size), pygame.Rect(80, 300, 10 * square_size, square_size), pygame.Rect(270, 420, 10 * square_size, square_size), pygame.Rect(270 + 10 * square_size, 420 - 9 * square_size, square_size, 10 * square_size)]




def achiev():
    global achievement
    global score
    achievement = ""
    if os.path.exists("liders.json"):
        file_size = os.path.getsize("liders.json")
        if file_size > 0:
            f = open("liders.json", "r")
            liders = json.load(f)
            liders["A"] = (0, 0)
            liders["B"] = (0, 0)
            liders["C"] = (0, 0)
        else:
            liders = {}
            liders["A"] = (0, 0)
            liders["B"] = (0, 0)
            liders["C"] = (0, 0)
    else:
        liders = {}
        liders["A"] = (0, 0)
        liders["B"] = (0, 0)
        liders["C"] = (0, 0)
    if username in liders.keys():
        if fruit == 3 and liders[username][1] < 3:
            achievement = "Поздравляю! 3 фрукта съедены."
            score+=5000
        if fruit == 5 and liders[username][1] < 5:
            achievement = "Поздравляю! 5 фруктов съедены."
            score+=5000
    else:
        if fruit == 3:
            achievement = "Поздравляю! 3 фрукта съедены."
            score+=5000
        if fruit == 5:
            achievement = "Поздравляю! 5 фруктов съедены."
            score+=5000


def eda():
    global e
    global fruit
    e = pygame.Rect(random.randint(25, screen_width - 25), random.randint(90, screen_height - 25), square_size, square_size)
    for b in snake:
        if b.rect.colliderect(e):
            eda()
    for p in prep:
        if p.colliderect(e):
            eda()

#собственно игра
def play():
    global coleda
    global score
    global fruit
    global snake
    global achievement
    achievement = ""
    setprep()
    score = 0
    fruit = 0
    v = (spd, 0) #вектор скорости
    new_v = (spd, 0)
    col = snake_colors[mode]
    pygame.init()
    # добавляет музыку на фон, но не ломается если у игрока не скачан файл
    try:
        pygame.mixer.music.load("nyeh.wav")
        pygame.mixer.music.play(loops=100)
    except:
        pass

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
    eda()
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
        for p in prep:
            pygame.draw.rect(screen, colprep, p)
        for b in snake:
            b.move()
            pygame.draw.rect(screen, col, b.rect)
        for p in prep:
            if snake[0].rect.colliderect(p):
                pygame.quit()
                game_over()
                return 0
        if snake[0].rect.colliderect(e):
            score += 1000*mode
            eda()
            col = coleda
            coleda = coledaset[random.randint(0, 4)]
            snake.append(body_part(snake[-1].x - (snake[-1].v[0]//spd)*square_size, snake[-1].y - (snake[-1].v[1]//spd)*square_size, snake[-1].v, snake[-1].turns.copy()))
            fruit+=1
            achiev()
        pygame.draw.rect(screen, coleda, e)
        # проверка столкновения со стенами

        if snake[0].x < 0 or snake[0].y < 75 or snake[0].x > screen_width - square_size or snake[0].y > screen_height - square_size:
            pygame.quit()
            game_over()
            return 0
        for b in snake[2:]:
            if snake[0].rect.colliderect(b.rect):
                pygame.quit()
                game_over()
                return 0
        s = font.render("Score: " + str(score) , 1, (0, 0, 0))
        screen.blit(s, (10, 10))
        s_achiev = font.render(achievement, 1, (255, 0, 0))
        screen.blit(s_achiev, (10, 40))

        pygame.draw.line(screen, (0, 0, 0), (0, 70), (500, 70), 5)
        pygame.display.update()
        score += 5*mode
        pygame.time.Clock().tick(30)

def menu_start():

    message = 'Добро пожаловать, '+username+'!'
    choice = buttonbox(msg=message, title='змейка', choices=('играть', 'переименоваться', 'выбор сложности', 'посмотреть таблицу лидеров', 'выйти', 'эротический режим'))
    if choice == 'играть':
        play()
    if choice == 'переименоваться':
        enter_username()
        menu_start()
    if choice == 'выбор сложности':
        choose_level()
        menu_start()
    if choice == 'посмотреть таблицу лидеров':
        first=0
        show_leaderboard(first)
        menu_start()
    if choice == 'выйти':
        exit()
    if choice == 'эротический режим':
        RickRoll()

enter_username()
menu_start()
