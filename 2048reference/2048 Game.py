#2048 Game.py
import pygame
import sys
import traceback
import random
from pygame.locals import *
from copy import deepcopy

board = [[0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0]]

pygame.init()
pygame.mixer.init()

block_size = 100
block_gap  = 16
top_screen = 185
left_screen = 272
bg_size = width,height = 1024, 700
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption('2048 GAME ----Kyle')
score = 0

#背景图
background = pygame.image.load('images/background.png').convert()
button_best = pygame.image.load('images/button_best.png').convert()
button_score = pygame.image.load('images/button_score.png').convert()
button_step = pygame.image.load('images/button_step.png').convert()
words = pygame.image.load('images/words.png').convert()

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
YELLOW4 = (242, 242, 10)

#载入游戏音乐
pygame.mixer.music.load('sound/game_music.wav')
pygame.mixer.music.set_volume(0.2)
vc_sound = pygame.mixer.Sound('sound/Victory.wav')
vc_sound.set_volume(0.3)
df_sound = pygame.mixer.Sound('sound/Defeat.wav')
df_sound.set_volume(0.3)
move_sound = pygame.mixer.Sound('sound/Move.wav')
move_sound.set_volume(0.5)


def draw_block():
    global board
    colors = {0:GREY, 2:FLESH1, 4:FLESH2, 8:RED1, 16:RED2, 32:RED3, 64:RED4, \
              128:RED5, 256:YELLOW1,512:YELLOW2, 1024:YELLOW3, 2048:YELLOW4}
    x, y = left_screen, top_screen
    size = block_size * 4 + block_gap * 5
    pygame.draw.rect(screen, DEEPGREY, (x, y, size, size))
    x, y = x + block_gap, y + block_gap
    for i in range(4):
        for j in range(4):
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
                    font = pygame.font.Font("font/arial black.ttf", number_height)
                    if num <= 4:
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


#在地图中随机产生2或4,有1/4几率产生4
def add():
    add = []
    for i in range(4):
        for j in range(4):
            if board[i][j] == 0:
                add.append((i, j))
    x = random.choice(add)
    add.remove(x)
    num = random.randint(0, 3)
    if num < 1:
        num = 4
    else:
        num = 2
    board[x[0]][x[1]] = num
    

#将地图内部数字向左靠拢进行合并
def move_to_left(K):
    global score
    answer = [0, 0, 0, 0]
    num = []
    for i in K:
        if i != 0:
            num.append(i)
    if len(num) == 4:
        if num[0] == num[1]:
            answer[0] = num[0] + num[1]
            score += answer[0]
            if num[2] == num[3]:
                answer[1] = num[2] + num[3]
                score += answer[1]
            else:
                answer[1] = num[2]
                answer[2] = num[3]
        elif num[1] == num[2]:
            answer[0] = num[0]
            answer[1] = num[1] + num[2]
            answer[2] = num[3]
            score += answer[1]
        elif num[2] == num[3]:
            answer[0] = num[0]
            answer[1] = num[1]
            answer[2] = num[2] + num[3]
            score += answer[2]
        else:
            for i in range(len(num)):
                answer[i] = num[i]
    elif len(num) == 3:
        if num[0] == num[1]:
            answer[0] = num[0] + num[1]
            answer[1] = num[2]
            score += answer[0]
        elif num[1] == num[2]:
            answer[0] = num[0]
            answer[1] = num[1] + num[2]
            score += answer[1]
        else:
            for i in range(len(num)):
                answer[i] = num[i]
    elif len(num) == 2:
        if num[0] == num[1]:
            answer[0] = num[0] + num[1]
            score += answer[0]
        else:
            for i in range(len(num)):
                answer[i] = num[i]
    elif len(num) == 1:
        answer[0] = num[0]
    else:
        pass
    return answer


#向上移动
def up():
    for i in range(4):
        z = []
        for j in range(4):
            z.append(board[j][i])
        l = move_to_left(z)
        for k in range(4):
            board[k][i] = l[k]
           

#向下移动
def down():
    for i in range(4):
        z = []
        for j in range(4):
            z.append(board[3-j][i])
        l = move_to_left(z)
        for k in range(4):
            board[3-k][i] = l[k]
            

#向左移动
def left():
    for i in range(4):
        l = move_to_left(board[i])
        for j in range(4):
            board[i][j] = l[j]

    
#向右移动
def right():
    for i in range(4):
        l = move_to_left(board[i][::-1])
        for j in range(4):
            board[i][3-j] = l[j]
            

#输入法1
def write1(msg, color, height):
    myfont = pygame.font.Font("font/mvboli.ttf", height)
    mytext = myfont.render(msg, True, color)
    mytext = mytext.convert_alpha()
    return mytext


#输入法2
def write2(msg, color, height):
    myfont = pygame.font.Font("font/arial black.ttf", height)
    mytext = myfont.render(msg, True, color)
    mytext = mytext.convert_alpha()
    return mytext


def over():
    for i in range(4):
        for j in range(4):
            if board[i][j] == 0:
                return False

    for i in range(4):
        for j in range(3):
            if board[i][j] == board[i][j+1]:
                return False

    for i in range(3):
        for j in range(4):
            if board[i][j] == board[i+1][j]:
                return False

    return True


def read_best():
    try:
        f = open('record.rec', 'r')
        best = int(f.read())
        f.close()
    except:
        best = 0
    return best


def write_best(best):
    try:
        f = open('record.rec', 'w')
        f.write(str(best))
        f.close()
    except IOError:
        pass


def main():
    global score
    #绘制背景
    pygame.mixer.music.play(-1)
    screen.blit(background, (0, 0))
    screen.blit(button_best, (30,201))
    screen.blit(button_score, (30,317))
    screen.blit(button_step, (30,433))
    screen.blit(words,(30,549))
    add()
    add()

    newboard = deepcopy(board)
    gameover = over()
    draw_block()

    
    best = read_best()
    step = 0
    running = True
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                write_best(best)
                pygame.quit()
                sys.exit()
            elif not gameover:
                #检测玩家键盘操作
                key_pressed = pygame.key.get_pressed()
                        
                #处理玩家键盘操作  
                if key_pressed[K_w] or key_pressed[K_UP]:
                    up()
                    step += 1
                    move_sound.play()
                elif key_pressed[K_s] or key_pressed[K_DOWN]:
                    down()
                    step += 1
                    move_sound.play()
                elif key_pressed[K_a] or key_pressed[K_LEFT]:
                    left()
                    step += 1
                    move_sound.play()
                elif key_pressed[K_d] or key_pressed[K_RIGHT]:
                    right()
                    step += 1
                    move_sound.play()
                if newboard != board:
                    add()
                    newboard = deepcopy(board)
                    draw_block()
                gameover = over()

                #绘制玩家得分
                score_text = write1(str(score), height=40, color=WHITE)
                score_text_rect = score_text.get_rect()
                score_text_rect.center = (272 // 2, 384)
                screen.blit(score_text, score_text_rect)
                #绘制历史最高
                if best < score:
                    best = score
                best_text = write1(str(best), height=40, color=WHITE)
                best_text_rect = best_text.get_rect()
                best_text_rect.center = (272 // 2, 269)
                screen.blit(best_text, best_text_rect)
                #绘制步数
                step_text = write1(str(step), height=40, color=WHITE)
                step_text_rect = step_text.get_rect()
                step_text_rect.center = (272 // 2, 501)
                screen.blit(step_text, step_text_rect)

            else:
                write_best(best)
                #停止背景音乐
                pygame.mixer.music.stop()

                #停止全部音效
                pygame.mixer.stop()

                #绘制游戏结束画面
                screen.blit(write2('Game over !', height = 100, color = BLACK), (210, 300))
                df_sound.play()
            break

            
            
        pygame.display.update()

if __name__ == "__main__":
    main()
