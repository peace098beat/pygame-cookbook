# -*- coding:utf-8 -*-
"""
タイルベーススクロール

http://aidiary.hatenablog.com/entry/20080607/1275790963


"""
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import sys
import os
 
# ******************************************************** #
# Constant
# ******************************************************** #
SCR_RECT = Rect(0, 0, 640, 480)
ROW,COL = 15,20  # マップサイズ（15マスx20マス）
GS = 32  # マスのサイズ（ピクセル）
DOWN,LEFT,RIGHT,UP = 0,1,2,3
GRASS, WATER = 0, 1
# ******************************************************** #
# Util
# ******************************************************** #
def load_image(filename, colorkey=None):
    filename = os.path.join("data", filename)
    try:
        image = pygame.image.load(filename)
    except pygame.error as message:
        print ("Cannot load image:", filename)
        raise SystemExit(message)
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image

def calc_offset(player):
    """オフセットを計算する"""
    offsetx = player.rect.topleft[0] - SCR_RECT.width/2
    offsety = player.rect.topleft[1] - SCR_RECT.height/2
    return offsetx, offsety
# ******************************************************** #
# MAIN ROOTIN
# ******************************************************** #
def main():
    pygame.init()
    screen = pygame.display.set_mode(SCR_RECT.size)
    pygame.display.set_caption(u"PyRPG 02 マップを作る")
     
    # Map
    Map.images[GRASS] = load_image("grass.png")
    Map.images[WATER] = load_image("water.png")
    map = Map("test2")

    player = Player("Vheicle0_64x32", (1,1), DOWN)

    clock = pygame.time.Clock()

    while True:
        clock.tick(60)
        # Update
        player.update(map)
        # Drawing
        offset = calc_offset(player)
        map.draw(screen, offset)
        player.draw(screen, offset)
        # pygame update
        pygame.display.update()
        # ************************** #
        # Event (update next time)
        # ************************** #
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                sys.exit()


# ******************************************************** #
# Map
# ******************************************************** #
class Map:
    images = [None] * 256 # Image Buffer : 256 is Max Number
    def __init__(self, name="map0"):
        self.name = name
        self.row, self.col = -1, -1
        self.map = []
        # Initialize
        self.load()
    def load(self):
        """ Create Map for **.map file"""
        file = os.path.join("./data", self.name + ".map")
        with open(file) as fp:
            lines = fp.readlines()
            self.row, self.col = map(int, lines[0].split())
            self.default = int(lines[1])  # デフォルト値
            for line in lines[2:]:  # マップデータを読み込む
                line = line.rstrip()  # 改行除去
                self.map.append([int(x) for x in list(line)])

    def draw(self, screen, offset):
        """マップを描画する"""
        offsetx, offsety = offset
        # startx, starty = offset
        startx = int(offsetx / GS)
        starty = int(offsety / GS)
        endx = int(startx + SCR_RECT.width/GS + 1)
        endy = int(starty + SCR_RECT.height/GS + 1)

        for y in range(starty, endy):
            for x in range(startx, endx):
                if x < 0 or y < 0 or x > self.col-1 or y > self.row-1:
                    screen.blit(self.images[self.default],
                                (x*GS-offsetx,y*GS-offsety))
                else:
                    img = self.images[self.map[y][x]]
                    screen.blit(img,
                                (x*GS-offsetx,y*GS-offsety))

    def is_movable(self, x,y):
        """(x,y)は移動可能か？"""
        # マップ範囲内か？
        if x<0 or x>self.col-1 or y<0 or y>self.row-1:
            return False
        # マップチップは移動可能か？
        if self.map[y][x] == 1:  # 水は移動できない
            return False
        return True


# ******************************************************** #
# Player
# ******************************************************** #
class Player:
    speed = 10
    def __init__(self, name, init_pos, dir):
        self.name = name
        self.image = load_image(name+".png", -1)
        self.x, self.y = init_pos[0], init_pos[1]
        self.rect = self.image.get_rect(topleft=(self.x*GS, self.y*GS))
        self.direction = dir #?

    def update(self, map):
        self.image = self.image
        self.direction = None
        self.vx, self.vy = 0, 0

        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_DOWN]:
            self.direction = DOWN
            self.vx, self.vy = 0, self.speed
            self.rect.move_ip(self.vx, self.vy)

        if pressed_keys[K_UP]:
            self.direction = UP
            self.vx, self.vy = 0, -self.speed
            self.rect.move_ip(self.vx, self.vy)

        if pressed_keys[K_LEFT]:
            self.direction = LEFT
            self.vx, self.vy = -self.speed, 0
            self.rect.move_ip(self.vx, self.vy)

        if pressed_keys[K_RIGHT]:
            self.direction = RIGHT
            self.vx, self.vy = self.speed, 0
            self.rect.move_ip(self.vx, self.vy)


    def draw(self, screen, offset):
        offsetx, offsety = offset
        player_x = self.rect.topleft[0]
        player_y = self.rect.topleft[1]
        screen.blit(self.image, (player_x-offsetx, player_y-offsety))
    
    def move(self, dir, map):
        """プレイヤーを移動"""
        if dir == DOWN:
            self.direction = DOWN
            if map.is_movable(self.x, self.y+1):
                self.y += 1
                self.rect.top += GS
        elif dir == LEFT:
            self.direction = LEFT
            if map.is_movable(self.x-1, self.y):
                self.x -= 1
                self.rect.left -= GS
        elif dir == RIGHT:
            self.direction = RIGHT
            if map.is_movable(self.x+1, self.y):
                self.x += 1
                self.rect.left += GS
        elif dir == UP:
            self.direction = UP
            if map.is_movable(self.x, self.y-1):
                self.y -= 1
                self.rect.top -= GS




if __name__ == "__main__":
    main()