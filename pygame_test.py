import sys
import pygame
import random
import numpy as np
import traceback
import time
from test import *
from main import main

current_date = time.strftime("%Y-%m-%d", time.localtime())
filename = "LOG_" + current_date + ".txt"
log_file = open(filename, 'a+')

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load('game_music.wav')
pygame.mixer.music.set_volume(0.4)
move_sound = pygame.mixer.Sound('Move.wav')
move_sound.set_volume(0.5)
def compareNum(state):
    return state.f

screen = pygame.display.set_mode((380, 380))
screen.fill((255,255,255))
pygame.display.set_caption('8 digital puzzle')

block_size = 100
block_gap  = 25
top_screen = 0
left_screen = 0

#颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (127, 127, 127)
DEEPGREY = (89, 89, 89)
FLESH1 = (255, 255, 229)
FLESH2 = (255, 255, 204)
RED1 = (255, 170, 128)
RED2 = (255, 136, 77)
RED3 = (255, 119, 51)
RED4 = (255, 102, 26)
RED5 = (255, 85, 0)
YELLOW1 = (255, 255, 102)
YELLOW2 = (255, 255, 51)
YELLOW3 = (255, 255, 0)
YELLOW4 = (232, 232, 10)


board = [[2, 8, 3], [1, 6, 4], [7, 0 ,5]]
def merge(l1, l2):
    i, j = 0, 0
    res, inv = [], 0
    length1, length2 = len(l1), len(l2)
    while i < length1 and j < length2:
        if l1[i] <= l2[j]:
            res.append(l1[i])
            i += 1
        else:
            res.append(l2[j])
            j += 1
            inv += length1 - i
    if i < len(l1):
        res.extend(l1[i:])
    else:
        res.extend(l2[j:])
    return res, inv

def inversions(l :list):
    if len(l) <= 1:
        return l, 0
    elif len(l) == 2:
        return [min(l), max(l)], 0 if l[0]<=l[1] else 1
    mid = len(l) // 2
    left,a=inversions(l[:mid])
    right,b=inversions(l[mid:])
    r, inv = merge(left, right)
    return r, inv + a + b

def autosolve():
    global board
    data = board[0] + board[1] + board[2]
    # template = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    # if inversions(data)[1] % 2 != inversions(template)[1] % 2:  #判断是否有解
    #     print("无解")
    #     return 0
    print("pygame", board)
    # main_solve(board)
    main(data)

def draw_block():
    global board
    colors = {0:GREY, 1:FLESH1, 2:FLESH2, 3:RED1, 4:RED2, 5:RED3, 6:RED4, \
              7:RED5, 8:YELLOW4}
    x, y = left_screen, top_screen
    size = block_size * 3 + block_gap * 4
    pygame.draw.rect(screen, DEEPGREY, (x, y, size, size))
    x, y = x + block_gap, y + block_gap
    for i in range(3):
        for j in range(3):
            num = board[i][j]
            if num == 0:
                number = ""
            else:
                number = str(num)
            color = colors[num]
            class Block:
                def __init__(self, topleft, number, color):
                    self.topleft = topleft
                    self.number = number
                    self.color = color
                def render(self, surface):
                    x, y = self.topleft
                    pygame.draw.rect(surface, self.color, (x, y, block_size, block_size))
                    number_height  = int(block_size * 0.5)
                    font = pygame.font.Font("arial black.ttf", number_height)
                    if num <= 3:
                        number_surface = font.render(self.number, True, DEEPGREY)
                    else:
                        number_surface = font.render(self.number, True, WHITE)
                    number_rect = number_surface.get_rect()
                    number_rect.center = (x + block_size / 2, y + block_size / 2)
                    surface.blit(number_surface, number_rect)
            block = Block((x, y), number, color)
            block.render(screen)
            x += block_size + block_gap
        x = left_screen + block_gap
        y += block_size + block_gap

def swap(a = [0, 0], b = [0, 0]):
    global board
    board[a[0]][a[1]], board[b[0]][b[1]] = board[b[0]][b[1]], board[a[0]][a[1]]
    print(a, " --> ", b)


def move(direct = 0):
    global board
    x, y = 0, 0
    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                x, y = i, j
    try:
        if direct == 0:
            swap([x, y], [x, y+1])
        elif direct == 1 and y > 0:
            swap([x, y], [x, y-1])
        elif direct == 2:
            swap([x, y], [x+1, y])
        elif direct == 3 and x > 0:
            swap([x, y], [x-1, y])
    except:
        traceback.print_exc()
    draw_block()

def detect():
    global board

    data = board[0] + board[1] + board[2]
    template = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    if inversions(data)[1] % 2 != inversions(template)[1] % 2:  #判断是否有解
        print("无解")
        return 0

def init():
    global board
    for i in range(random.randint(1, 1)):  # 随机次数交换位置，生成随机矩阵，并保证有解
        move(random.randint(0, 3))
    print(board)
    log_file.write(str(board))
    log_file.write('\n')
init()


pygame.mixer.music.play()  # 播放音乐

# 固定代码段，实现点击"X"号退出界面的功能
while True:
    # 循环获取事件，监听事件状态
    draw_block()

    for event in pygame.event.get():
        # 判断用户是否点了"X"关闭按钮,并执行if代码段
        if event.type == pygame.QUIT:
            #卸载所有模块
            pygame.quit()
            #终止程序，确保退出程序
            sys.exit()
        elif event.type == pygame.KEYDOWN :
            if event.key == pygame.K_UP:
                print("up")
                log_file.write("up\n")
                move(3)
                move_sound.play()
            if event.key == pygame.K_DOWN:
                print("down")
                log_file.write("down\n")
                move(2)
                move_sound.play()
            if event.key == pygame.K_LEFT:
                print("left")
                log_file.write("left\n")
                move(1)
                move_sound.play()
            if event.key == pygame.K_RIGHT:
                print("right")
                log_file.write("right\n")
                move(0)
                move_sound.play()
            if event.key == pygame.K_a:
                print("autosolve")
                log_file.write("autosolve\n")
                autosolve()
            if event.key == pygame.K_i:
                print("initial")
                log_file.write("initial\n")
                init()
            if event.key == pygame.K_d:
                print("detect")
                log_file.write("detect\n")
                detect()
            if board == [[1, 2, 3], [4, 5, 6], [7, 8, 0]]:
                print("success!")
    pygame.display.flip() #更新屏幕内容

