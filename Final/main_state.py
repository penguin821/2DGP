import random
from pico2d import *

import game_framework
import title_state



name = "MainState"

tile = None
map = None
starting_point = None
background = None
ball = None
font = None
running = None
lastX = None
lastY = None
lastDirection = None
count = None
i = None


class Background:

    def __init__(self):
        self.image = load_image('background.png')

    def draw(self):
        self.image.draw(200, 300)


class Starting_Point:

    def __init__(self):
        self.x, self.y = 200, 75
        self.image = load_image('starting_point.png')

    def update(self):
        self.y -= 0.5


    def draw(self):
        self.image.clip_draw(0, 0, 250, 150, self.x, self.y)


class Map:

    def __init__(self):
        self.direction = random.randint(0, 1)
        if self.direction == 0:
            self.x, self.y = random.randint(75, 250), 175
            self.image = load_image('map_tile1.png')
        elif self.direction == 1:
            self.x, self.y = random.randint(150, 250), 175
            self.image = load_image('map_tile2.png')


    def update(self):
        self.y -= 0.5


    def draw(self):
        self.image.clip_draw(0, 0, 150, 50, self.x, self.y)


class Tile:

    def __init__(self):
        global lastX, lastY, lastDirection
        self.direction = random.randint(0, 1)
        if lastDirection == 0:
            if self.direction == 0:
                if lastX - 150 < 0:
                    self.x, self.y = lastX, lastY + 50
                    self.image = load_image('map_tile2.png')
                    self.direction = 1
                elif lastX - 150 >= 0:
                    self.x, self.y = lastX - 75, lastY + 50
                    self.image = load_image('map_tile1.png')
            if self.direction == 1:
                self.x, self.y = lastX, lastY + 50
                self.image = load_image('map_tile2.png')
        elif lastDirection == 1:
            if self.direction == 0:
                self.x, self.y = lastX, lastY + 50
                self.image = load_image('map_tile1.png')
            if self.direction == 1:
                if lastX + 150 > 400:
                    self.x, self.y = lastX, lastY + 50
                    self.image = load_image('map_tile1.png')
                    self.direction = 0
                elif lastX + 150 <= 400:
                    self.x, self.y = lastX + 75, lastY + 50
                    self.image = load_image('map_tile2.png')

        lastX, lastY = self.x, self.y
        lastDirection = self.direction




    def update(self):
        self.y -= 0.5


    def draw(self):
        self.image.clip_draw(0, 0, 150, 50, self.x, self.y)


class Ball:

    LEFT_ROLL, RIGHT_ROLL = 0, 1

    def handle_left_roll(self):
        self.x -= 0.7
        if self.x < 0:
            self.state = self.RIGHT_ROLL
            self.x = 0

    def handle_right_roll(self):
        self.x += 0.7
        if self.x > 400:
            self.state = self.LEFT_ROLL
            self.x = 400

    handle_state = {
        LEFT_ROLL: handle_left_roll,
        RIGHT_ROLL: handle_right_roll
    }

    def update(self):
        self.handle_state[self.state](self)

    def __init__(self):
        self.x, self.y = 200, 65
        self.image = load_image('ball.png')
        self.state = self.RIGHT_ROLL

    def draw(self):
        self.image.clip_draw(0, 0, 21, 21, self.x, self.y)


def enter():
    global ball, background, starting_point, map, lastX, lastY, lastDirection, maps
    ball = Ball()
    background = Background()
    starting_point = Starting_Point()
    map = Map()
    lastX, lastY = map.x, map.y
    lastDirection = map.direction
    maps = [Tile() for i in range(100)]

def exit():
    global ball, background, starting_point, map, tile
    del(ball)
    del(background)
    del(starting_point)
    del(map)
    del(tile)


def handle_events():
    global count
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_state(title_state)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            if ball.state == ball.RIGHT_ROLL:
                ball.state = ball.LEFT_ROLL
            elif ball.state == ball.LEFT_ROLL:
                ball.state = ball.RIGHT_ROLL


def update():
    starting_point.update()
    map.update()
    for tile in maps:
        tile.update()
    ball.update()


def draw():
    clear_canvas()
    background.draw()
    starting_point.draw()
    map.draw()
    for tile in maps:
        tile.draw()
    ball.draw()
    update_canvas()