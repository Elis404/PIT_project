import os
import sys
import pygame
import random

pygame.init()
size = (400, 500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Cosmo Tetris')
clock = pygame.time.Clock()  # инициализация времени
fps = 25  # стандартный фпс
level = 1  # глобальная переменная уровня для доступа из разных функций
pygame.mouse.set_visible(False)  # отключение курсора, т. к. у нас свой курсор

colors = [
    (0, 168, 107),
    (255, 255, 255),
    (29, 97, 140),
    (255, 79, 0),
    (119, 221, 119),
    (0, 128, 0)
]  # Цвета фигур, ВЫБРАТЬ СЛУЧАЙНЫМ ОБРАЗОМ, через рандом


# Функция загрузки изображений (например логотипа, курсора и т. д.)
def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


# Вспомогательная функция для начального экрана:
def terminate():
    pygame.quit()
    sys.exit()


# Фуннкция начального экрана
def start_screen():
    global level

    # Заголовок тетрис:
    title = pygame.sprite.Sprite(sprites)
    title.image = load_image('title.png')
    title.image = pygame.transform.scale(title.image, (260, 210))
    title.rect = title.image.get_rect()
    title.rect.x = 70
    title.rect.y = 0

    x_text, y_text = -400, 280  # Координаты текста

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Если нажали Enter выходим
                    title.rect.y = 500  # КОСТЫЛЬ - смещение логотипа
                    game.state = 'start'
                    game.__init__(20, 10)
                    return  # Выходим из функции
                if event.key == pygame.K_UP:  # Повышение уровня (1 - 5)
                    if level < 5:
                        level += 1
                if event.key == pygame.K_DOWN:  # Понижение уровня (5 - 1)
                    if level > 1:
                        level -= 1
            if event.type == pygame.MOUSEMOTION:  # Для отображения курсора при перемещении
                x, y = event.pos
                cursor.rect.x, cursor.rect.y = x, y
            if event.type == pygame.MOUSEBUTTONDOWN:  # При нажатии курсор меняется
                if event.button == 1:
                    cursor.press(event.pos)
            if event.type == pygame.MOUSEBUTTONUP:  # Отпустили курсор
                cursor.up(event.pos)

        screen.fill(BLACK)  # Мерцание (чтобы не оставлять кучу картинок курсора)
        sprites.draw(screen)  # Отрисовка спрайтов
        font = pygame.font.SysFont('Times New Roman', 20, True, False)  # Шрифт1
        font2 = pygame.font.SysFont('Times New Roman', 22, True, False)  # Шрифт2
        font3 = pygame.font.SysFont('Times New Roman', 18, True, False)  # Шрифт3

        level_text = font.render('Level: ' + str(level), True, WHITE)  # Уровень
        screen.blit(level_text, [60, 200])  # Уровень

        info_text = font.render('--Press up/down arrows to choose level--', True, BLUE)  # Инфо
        screen.blit(info_text, [40, 220])  # Инфо

        start_text = font2.render('~PRESS ENTER TO START GAME~', True, ORANGE)  # Старт
        screen.blit(start_text, [x_text, y_text])  # Старт
        x_text += 3  # Движение текста
        if x_text > 400:
            x_text = -400

        # Правила
        rules_text1 = font.render('Game rules:', True, WHITE)
        rules_text2 = font3.render('1) To lower the figure - press |down arrow|', True, WHITE)
        rules_text3 = font3.render('2) To flip the figure - press |up arrow|', True, WHITE)
        rules_text4 = font3.render('3) To completely lower - press |space|', True, WHITE)
        rules_text5 = font3.render('4) To update game - press |ESC|', True, WHITE)

        screen.blit(rules_text1, [20, 320])
        screen.blit(rules_text2, [20, 355])
        screen.blit(rules_text3, [20, 380])
        screen.blit(rules_text4, [20, 405])
        screen.blit(rules_text5, [20, 430])

        pygame.display.flip()
        clock.tick(fps)


def game_over():
    x_text, y_text = -300, 120  # Координаты текста
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

        screen.fill(BLACK)
        font = pygame.font.SysFont('Times New Roman', 58, True, False)  # Шрифт
        font2 = pygame.font.SysFont('Times New Roman', 25, True, False)  # Шрифт
        game_over_text = font.render('GAME OVER', True, ORANGE)
        esc_text = font2.render('Press ESC to EXIT', True, WHITE)
        score_text = font2.render('Score: ' + str(game.score), True, WHITE)
        screen.blit(game_over_text, [x_text, y_text])
        screen.blit(esc_text, [20, 250])
        screen.blit(score_text, [20, 280])
        x_text += 3  # Движение текста
        if x_text > 400:
            x_text = -300
        pygame.display.flip()
        clock.tick(fps)


# Класс описывающий новый курсор
class Cursor(pygame.sprite.Sprite):
    cursor = load_image('cursor.png')  # загрузка обычного курсора
    press_cursor = load_image('press_cursor.png')  # загрузка курсора в нажатии

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Cursor.cursor
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()

    # Нажатие
    def press(self, pos):
        self.image = Cursor.press_cursor
        self.image = pygame.transform.scale(self.image, (25, 30))
        self.rect = self.image.get_rect()
        x, y = pos
        cursor.rect.x, cursor.rect.y = x, y

    # Отпускание
    def up(self, pos):
        self.image = Cursor.cursor
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        x, y = pos
        cursor.rect.x, cursor.rect.y = x, y


# Класс описывающий фигуры
class Figure:
    x = 0
    y = 0

    # Все фигуры игры:
    figures = [
        [[1, 5, 9, 13], [4, 5, 6, 7]],
        [[4, 5, 9, 10], [2, 6, 5, 9]],
        [[6, 7, 9, 10], [1, 5, 6, 10]],
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
        [[1, 2, 5, 6]],
    ]

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.randint(0, len(self.figures) - 1)  # Рандомный выбор типа фигуры
        self.color = random.randint(1, len(colors) - 1)  # Рандомный выбор цвета
        self.rotation = 0

    # Для отрисовки
    def image(self):
        return self.figures[self.type][self.rotation]

    # Для поворота
    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.figures[self.type])


# Класс самой игры
class Tetris:
    best_score = 0
    state = "start"
    field = []
    height = 0
    width = 0
    x = 100
    y = 60
    zoom = 20
    figure = None

    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.field = []
        self.score = 0
        self.state = "start"
        for i in range(height):
            new_line = []
            for j in range(width):
                new_line.append(0)
            self.field.append(new_line)

    def new_figure(self):
        self.figure = Figure(3, 0)

    def intersects(self):
        intersection = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    if i + self.figure.y > self.height - 1 or \
                            j + self.figure.x > self.width - 1 or \
                            j + self.figure.x < 0 or \
                            self.field[i + self.figure.y][j + self.figure.x] > 0:
                        intersection = True
        return intersection

    def break_lines(self):
        lines = 0
        for i in range(1, self.height):
            zeros = 0
            for j in range(self.width):
                if self.field[i][j] == 0:
                    zeros += 1
            if zeros == 0:
                lines += 1
                for i1 in range(i, 1, -1):
                    for j in range(self.width):
                        self.field[i1][j] = self.field[i1 - 1][j]
        self.score += lines ** 2

    def go_space(self):
        while not self.intersects():
            self.figure.y += 1
        self.figure.y -= 1
        self.freeze()

    def go_down(self):
        self.figure.y += 1
        if self.intersects():
            self.figure.y -= 1
            self.freeze()

    def freeze(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    self.field[i + self.figure.y][j + self.figure.x] = self.figure.color
        self.break_lines()
        self.new_figure()
        if self.intersects():
            self.state = "gameover"

    def go_side(self, dx):
        old_x = self.figure.x
        self.figure.x += dx
        if self.intersects():
            self.figure.x = old_x

    def rotate(self):
        old_rotation = self.figure.rotation
        self.figure.rotate()
        if self.intersects():
            self.figure.rotation = old_rotation


# Спрайты
sprites = pygame.sprite.Group()
cursor = Cursor(sprites)

# Основные цвета (текст, поле и т.д.)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (9, 9, 150)
DARK_BLUE = (9, 9, 80)
ORANGE = (250, 79, 0)

# Создание игры
running = True
game = Tetris(20, 10)
counter = 0

# Начальный экран
start_screen()

pressing_down = False

# Игровой цикл
while running:
    if game.figure is None:
        game.new_figure()
    counter += 1
    if counter > 100000:
        counter = 0

    if counter % (fps // level // 2) == 0 or pressing_down:
        if game.state == "start":
            game.go_down()  # Автоматическое опускание фигуры

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                game.rotate()  # Переворот фигуры
            if event.key == pygame.K_DOWN:
                pressing_down = True  # Вниз
            if event.key == pygame.K_LEFT:
                game.go_side(-1)  # Влево
            if event.key == pygame.K_RIGHT:
                game.go_side(1)  # Вправо
            if event.key == pygame.K_SPACE:
                game.go_space()  # Вниз до конца
            if event.key == pygame.K_ESCAPE:
                game.__init__(20, 10)  # Обновление игры
        # Курсор:
        if event.type == pygame.MOUSEMOTION:
            x, y = event.pos
            cursor.rect.x, cursor.rect.y = x, y
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                cursor.press(event.pos)
        if event.type == pygame.MOUSEBUTTONUP:
            cursor.up(event.pos)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                pressing_down = False

    screen.fill(BLACK)
    sprites.draw(screen)

    # Отрисовка поля
    for i in range(game.height):
        for j in range(game.width):
            pygame.draw.rect(screen, DARK_BLUE,
                             [game.x + game.zoom * j, game.y + game.zoom * i, game.zoom, game.zoom],
                             1)
            if game.field[i][j] > 0:
                pygame.draw.rect(screen, colors[game.field[i][j]],
                                 [game.x + game.zoom * j + 1, game.y + game.zoom * i + 1,
                                  game.zoom - 2, game.zoom - 1])
    # Фигуры
    if game.figure is not None:
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in game.figure.image():
                    pygame.draw.rect(screen, colors[game.figure.color],
                                     [game.x + game.zoom * (j + game.figure.x) + 1,
                                      game.y + game.zoom * (i + game.figure.y) + 1,
                                      game.zoom - 2, game.zoom - 2])

    # Текст
    font = pygame.font.SysFont('Times New Roman', 20, True, False)
    text1 = font.render("Score: " + str(game.score), True, WHITE)
    text2 = font.render("Level: " + str(level), True, WHITE)
    text3 = font.render("Best Score: " + str(game.best_score), True, WHITE)

    screen.blit(text1, [0, 0])
    screen.blit(text2, [300, 0])
    screen.blit(text3, [0, 20])
    if game.state == "gameover":
        game_over()
        if game.score > game.best_score:
            game.best_score = game.score
        start_screen()

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
