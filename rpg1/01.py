# -*- coding:utf-8 -*-
"""
RPGのマップ作成

http://gamepro.blog.jp/python/pygame/create_map


1「pygame」「sys」モジュールをインポートする。
2 画面のサイズを設定する。(640*480)
3 Pygameを初期化する。[pygame.init]
4 画面（ウィンドウ）を生成する。[pygame.display.set_mode]
5 水、地面の画像(32x32)を読み込む。
6 マップデータに合わせて、画面に画像を貼り付ける。（1なら水、0なら地面）
7 画面を更新する。
8 イベント処理をする。
・画面の閉じるボタンが押されたら終了する。
・Escキーが押されたら終了する。
9 7-8の処理を繰り返す。

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


# ******************************************************** #
# MAIN ROOTIN
# ******************************************************** #
def main():
    pygame.init()
    screen = pygame.display.set_mode(SCR_RECT.size)
    pygame.display.set_caption(u"PyRPG 02 マップを作る")
     
    # イメージロード
    playerImg = load_image("player1.png", -1)  # プレイヤー
    grassImg = load_image("grass.png")         # 草地
    waterImg = load_image("water.png")         # 水
    
    # Map
    Map.images[GRASS] = load_image("grass.png")
    Map.images[WATER] = load_image("water.png")
    map = Map()

    player = Player("player1", (1,1), None)

    clock = pygame.time.Clock()

    while True:
        clock.tick(60)
        # Update
        player.update()
        # Drawing
        map.draw(screen)
        player.draw(screen)
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
            # Player Movin
            if event.type == KEYDOWN and event.key == K_DOWN:
                player.move(DOWN, map)
            if event.type == KEYDOWN and event.key == K_UP:
                player.move(UP, map)
            if event.type == KEYDOWN and event.key == K_RIGHT:
                player.move(RIGHT, map)
            if event.type == KEYDOWN and event.key == K_LEFT:
                player.move(LEFT, map)

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
            for line in lines[1:]:  # マップデータを読み込む
                line = line.rstrip()  # 改行除去
                self.map.append([int(x) for x in list(line)])
    def draw(self, screen):
        """マップを描画する"""
        for r in range(self.row):
            for c in range(self.col):
                img = self.images[self.map[r][c]]
                screen.blit(img, (c*GS,r*GS))

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
    def __init__(self, name, init_pos, dir):
        self.name = name
        self.image = load_image(name+".png", -1)
        self.x, self.y = init_pos[0], init_pos[1]
        self.rect = self.image.get_rect(topleft=(self.x*GS, self.y*GS))
        self.direction = dir #?

    def update(self):
        self.image = self.image
    def draw(self, screen):
        screen.blit(self.image, self.rect)
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