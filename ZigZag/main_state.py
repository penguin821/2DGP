import random
from pico2d import *

import game_framework
import gameover_state

current_time = get_time()
frame_time = get_time() - current_time

PIXEL_PER_METER = (10.0 / 0.3)           # 10 pixel 30 cm
MOVING_SPEED_KMPH = 20.0                    # Km / Hour
MOVING_SPEED_MPM = (MOVING_SPEED_KMPH * 1000.0 / 60.0)
MOVING_SPEED_MPS = (MOVING_SPEED_MPM / 60.0)
MOVING_SPEED_PPS = (MOVING_SPEED_MPS * PIXEL_PER_METER)
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 3

name = "MainState"

tile = None
map = None
starting_point = None
background = None
ball = None
jewel = None
font = None
running = None
lastX = None
lastY = None
lastDirection = None
count = None
i = None
font = None
point = 0

BALL_SPEED = 1.5
MAP_SPEED = 1.1

class Background:
    global point

    def __init__(self):
        self.image = load_image('background.png')
        self.bgm = load_music('Marble Machine.mp3')
        self.bgm.set_volume(64)
        self.bgm.repeat_play()

    def draw(self):
        self.image.draw(200, 300)


class Starting_Point:

    def __init__(self):
        self.x, self.y = 200, 75
        self.image = load_image('starting_point.png')

    def update(self):
        if point < 100:
            self.y -= MAP_SPEED
        elif point >= 100 and point < 400:
            self.y -= MAP_SPEED * 3/2
        elif point >= 400 and point < 650:
            self.y -= MAP_SPEED * 2
        elif point >= 750:
            self.y -= MAP_SPEED * 2.5


    def draw(self):
        self.image.draw(self.x, self.y)

    def get_bb1(self):
        return self.x - 125, self.y - 75, self.x + 125, self.y + 75

    def draw_bb(self):
        draw_rectangle(*self.get_bb1())

class Finish:

    def __init__(self):
        self.x, self.y = 200, 5215
        self.image = load_image('finish.png')

    def update(self):
        if point < 100:
            self.y -= MAP_SPEED
        elif point >= 100 and point < 400:
            self.y -= MAP_SPEED * 3/2
        elif point >= 400 and point < 650:
            self.y -= MAP_SPEED * 2
        elif point >= 750:
            self.y -= MAP_SPEED * 2.5


    def draw(self):
        self.image.draw(self.x, self.y)

    def get_bb1(self):
        return self.x - 200, self.y - 15, self.x + 200, self.y + 15

    def draw_bb(self):
        draw_rectangle(*self.get_bb1())

class Map:

    def __init__(self):
        self.direction = random.randint(0, 1)
        if self.direction == 0:
            self.x, self.y = random.randint(75, 250), 175
            self.image = load_image('map_tile1.png')
        elif self.direction == 1:
            self.x, self.y = random.randint(150, 250), 175
            self.image = load_image('map_tile2.png')

    def get_bb(self):
        return self.x + 75, self.y + 25, self.x - 75, self.y - 25

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def get_bb1(self):
        if self.direction == 1:
            return self.x - 10, self.y + 15, self.x + 70, self.y + 25
        if self.direction == 0:
            return self.x - 70, self.y + 15, self.x + 10, self.y + 25

    def get_bb2(self):
        if self.direction == 1:
            return self.x - 25, self.y + 5, self.x + 55, self.y + 15
        if self.direction == 0:
            return self.x - 55, self.y + 5, self.x + 25, self.y + 15

    def get_bb3(self):
        if self.direction == 1:
            return self.x - 40, self.y - 5, self.x + 40, self.y + 5
        if self.direction == 0:
            return self.x - 40, self.y - 5, self.x + 40, self.y + 5

    def get_bb4(self):
        if self.direction == 1:
            return self.x - 55, self.y - 15, self.x + 25, self.y - 5
        if self.direction == 0:
            return self.x - 25, self.y - 15, self.x + 55, self.y - 5

    def get_bb5(self):
        if self.direction == 1:
            return self.x - 70, self.y - 25, self.x + 10, self.y - 15
        if self.direction == 0:
            return self.x - 10, self.y - 25, self.x + 70, self.y - 15

    def draw_bb(self):
        draw_rectangle(*self.get_bb1())
        draw_rectangle(*self.get_bb2())
        draw_rectangle(*self.get_bb3())
        draw_rectangle(*self.get_bb4())
        draw_rectangle(*self.get_bb5())


    def update(self):
        if point < 100:
            self.y -= MAP_SPEED
        elif point >= 100 and point < 400:
            self.y -= MAP_SPEED * 3/2
        elif point >= 400 and point < 650:
            self.y -= MAP_SPEED * 2
        elif point >= 750:
            self.y -= MAP_SPEED * 2.5


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

    def get_bb1(self):

        if self.direction == 1:
            return self.x - 10, self.y + 15, self.x + 70, self.y + 25
        if self.direction == 0:
            return self.x - 70, self.y + 15, self.x + 10, self.y + 25

    def get_bb2(self):
        if self.direction == 1:
            return self.x - 25, self.y + 5, self.x + 55, self.y + 15
        if self.direction == 0:
            return self.x - 55, self.y + 5, self.x + 25, self.y + 15

    def get_bb3(self):
        if self.direction == 1:
            return self.x - 40, self.y - 5, self.x + 40, self.y + 5
        if self.direction == 0:
            return self.x - 40, self.y - 5, self.x + 40, self.y + 5

    def get_bb4(self):
        if self.direction == 1:
            return self.x - 55, self.y - 15, self.x + 25, self.y - 5
        if self.direction == 0:
            return self.x - 25, self.y - 15, self.x + 55, self.y - 5

    def get_bb5(self):
        if self.direction == 1:
            return self.x - 70, self.y - 25, self.x + 10, self.y - 15
        if self.direction == 0:
            return self.x - 10, self.y - 25, self.x + 70, self.y - 15

    def draw_bb(self):
        draw_rectangle(*self.get_bb1())
        draw_rectangle(*self.get_bb2())
        draw_rectangle(*self.get_bb3())
        draw_rectangle(*self.get_bb4())
        draw_rectangle(*self.get_bb5())

    def update(self):
        if point < 100:
            self.y -= MAP_SPEED
        elif point >= 100 and point < 400:
            self.y -= MAP_SPEED * 3/2
        elif point >= 400 and point < 650:
            self.y -= MAP_SPEED * 2
        elif point >= 750:
            self.y -= MAP_SPEED * 2.5

    def draw(self):
        self.image.draw(self.x, self.y)


class Ball:

    LEFT_ROLL, RIGHT_ROLL = 0, 1

    def handle_left_roll(self):
        if point < 100:
            self.x -= BALL_SPEED
        elif point >= 100 and point < 400:
            self.x -= BALL_SPEED * 3/2
        elif point >= 400 and point < 650:
            self.x -= BALL_SPEED * 2
        elif point >= 750:
            self.x -= BALL_SPEED * 2.5

        if self.x < 0:
            self.state = self.RIGHT_ROLL
            self.x = 0

    def handle_right_roll(self):
        if point < 100:
            self.x += BALL_SPEED
        elif point >= 100 and point < 400:
            self.x += BALL_SPEED * 1.5
        elif point >= 400 and point < 650:
            self.x += BALL_SPEED * 2
        elif point >= 750:
            self.x += BALL_SPEED * 2.5


        if self.x > 400:
            self.state = self.LEFT_ROLL
            self.x = 400

    handle_state = {
        LEFT_ROLL: handle_left_roll,
        RIGHT_ROLL: handle_right_roll
    }

    def update(self):
        self.handle_state[self.state](self)

    def remove(self):
        self.x, self.y = 0, 0

    def __init__(self):
        self.x, self.y = 200, 65
        self.image = load_image('ball.png')
        self.state = self.RIGHT_ROLL

    def get_bb(self):
        return self.x-4, self.y-3, self.x+4, self.y+3

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def draw(self):
        self.image.draw(self.x, self.y)


class Jewel:

    def __init__(self):
        self.x, self.y = random.randint(100, 400), random.randint(500, 5200)
        self.falling_speed = random.randint(1, 2)
        self.frame = 0
        self.image = load_image('jewel_animation.png')

    def update(self):
        self.frame = (self.frame + 1) % FRAMES_PER_ACTION
        self.y -= self.falling_speed

    def remove(self):
        self.x, self.y = -100, -100

    def get_bb1(self):
        return self.x-4, self.y-4, self.x+4, self.y+4

    def draw_bb(self):
        draw_rectangle(*self.get_bb1())

    def draw(self):
        self.image.clip_draw(self.frame*60, 0, 30, 30, self.x, self.y)


def collide_tile(a, b, n):
    if n == 1:
        left_a, bottom_a, right_a, top_a = a.get_bb1()
        left_b, bottom_b, right_b, top_b = b.get_bb()
    elif n == 2:
        left_a, bottom_a, right_a, top_a = a.get_bb2()
        left_b, bottom_b, right_b, top_b = b.get_bb()
    elif n == 3:
        left_a, bottom_a, right_a, top_a = a.get_bb3()
        left_b, bottom_b, right_b, top_b = b.get_bb()
    elif n == 4:
        left_a, bottom_a, right_a, top_a = a.get_bb4()
        left_b, bottom_b, right_b, top_b = b.get_bb()
    elif n == 5:
        left_a, bottom_a, right_a, top_a = a.get_bb5()
        left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True


def enter():
    global ball, background, starting_point, map, lastX, lastY, lastDirection, maps, font, jewels, finish
    font = load_font('ENCR10B.TTF')
    ball = Ball()
    background = Background()
    starting_point = Starting_Point()
    finish = Finish()
    map = Map()
    lastX, lastY = map.x, map.y
    lastDirection = map.direction
    maps = [Tile() for i in range(100)]
    jewels = [Jewel() for i in range(160)]


def exit():
    global ball, background, starting_point, map, tile, jewel, font, finish
    del(ball)
    del(background)
    del(starting_point)
    del(map)
    del(tile)
    del(jewel)
    del(font)
    del(finish)


def handle_events():
    global count
    global point
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            if ball.state == ball.RIGHT_ROLL:
                ball.state = ball.LEFT_ROLL
                point += 1
            elif ball.state == ball.LEFT_ROLL:
                ball.state = ball.RIGHT_ROLL
                point += 1


def update():
    global point
    count = 0
    starting_point.update()
    finish.update()
    map.update()

    for jewel in jewels:
        if collide_tile(jewel, ball, 1):
            point += 30
            jewel.remove()

    for i in range(5):
        if collide_tile(map, ball, i + 1):
            count = 1
            point += 0.1
    for tile in maps:
        tile.update()
        for i in range(5):
            if collide_tile(tile, ball, i+1):
                count = 1
                point += 0.1
    if collide_tile(starting_point, ball, 1):
        count = 1
    if count == 0:
        print("Your Score is %d!" % point)
        point = 0
        game_framework.push_state(gameover_state)

    ball.update()
    for jewel in jewels:
        jewel.update()


def draw():
    clear_canvas()
    background.draw()
    starting_point.draw()
    finish.draw()
    map.draw()
    for tile in maps:
        tile.draw()

    for jewel in jewels:
        jewel.draw()

    ball.draw()
    font.draw(350, 550, '%d' % point)

    update_canvas()

def pause():
    pass

def resume():
    pass
