import sys
import pygame
import random
import numpy as np
import traceback
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load('game_music.wav')
pygame.mixer.music.set_volume(0.4)
move_sound = pygame.mixer.Sound('Move.wav')
move_sound.set_volume(0.5)
def compareNum(state):
    return state.f

class State:
    def __init__(self, state, originState=None, directionFlag=None, parent=None, f=0):
        self.state = state
        self.originState = originState
        self.direction = ['up', 'down', 'right', 'left']
        if directionFlag:
            self.direction.remove(directionFlag)
        self.parent = parent
        self.f = f

    def getDirection(self):
        return self.direction

    def setF(self, f):
        self.f = f
        return

    # 打印结果
    def showInfo(self):
        for i in range(len(self.state)):
            for j in range(len(self.state)):
                print(self.state[i, j], end='  ')
            print("\n")
        print('->')
        return

    # 获取0点
    def getZeroPos(self):
        postion = np.where(self.state == 0)
        return postion

    # 曼哈顿距离  f = g + h，g=1，如果用宽度优先的评估函数可以不调用该函数
    def getFunctionValue(self):
        cur_node = self.state.copy()
        fin_node = self.answer.copy()
        dist = 0
        N = len(cur_node)

        for i in range(N):
            for j in range(N):
                if cur_node[i][j] != fin_node[i][j]:
                    index = np.argwhere(fin_node == cur_node[i][j])
                    x = index[0][0]  # 最终x距离
                    y = index[0][1]  # 最终y距离
                    dist += (abs(x - i) + abs(y - j))
        return dist + 1

    def nextStep(self):
        if not self.direction:
            return []
        subStates = []
        boarder = len(self.state) - 1
        # 获取0点位置
        x, y = self.getZeroPos()
        # 向左
        if 'left' in self.direction and y > 0:
            s = self.state.copy()
            tmp = s[x, y - 1]
            s[x, y - 1] = s[x, y]
            s[x, y] = tmp
            news = State(s, directionFlag='right', parent=self)
            news.setF(news.getFunctionValue())
            subStates.append(news)
            move(0)
        # 向上
        if 'up' in self.direction and x > 0:
            # it can move to upper place
            s = self.state.copy()
            tmp = s[x - 1, y]
            s[x - 1, y] = s[x, y]
            s[x, y] = tmp
            news = State(s, directionFlag='down', parent=self)
            news.setF(news.getFunctionValue())
            subStates.append(news)
            move(2)
        # 向下
        if 'down' in self.direction and x < boarder:
            # it can move to down place
            s = self.state.copy()
            tmp = s[x + 1, y]
            s[x + 1, y] = s[x, y]
            s[x, y] = tmp
            news = State(s, directionFlag='up', parent=self)
            news.setF(news.getFunctionValue())
            subStates.append(news)
            move(3)
        # 向右
        if self.direction.count('right') and y < boarder:
            # it can move to right place
            s = self.state.copy()
            tmp = s[x, y + 1]
            s[x, y + 1] = s[x, y]
            s[x, y] = tmp
            news = State(s, directionFlag='left', parent=self)
            news.setF(news.getFunctionValue())
            subStates.append(news)
            move(1)
        # 返回F值最小的下一个点
        subStates.sort(key=compareNum)
        return subStates[0]

    # A* 迭代
    def solve(self):
        # openList
        openTable = []
        # closeList
        closeTable = []
        openTable.append(self)
        while len(openTable) > 0:
            # 下一步的点移除open
            n = openTable.pop(0)
            # 加入close
            closeTable.append(n)
            # 确定下一步点
            subStates = n.nextStep()
            path = []
            # 判断是否和最终结果相同
            if (subStates.state == subStates.answer).all():
                while subStates.parent and subStates.parent != self.originState:
                    path.append(subStates.parent)
                    subStates = subStates.parent
                path.reverse()
                return path
            openTable.append(subStates)
        else:
            return None, None


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


board = [[0, 0, 0],
         [0, 0, 0],
         [0, 0, 0]]

def autosolve():
    global board
    State.answer = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
    originState = State(np.array(board))
    print(board)
    s1 = State(state=originState.state, originState=originState)
    path = s1.solve()
    if path:
        for node in path:
            node.showInfo()
        print(State.answer)
        print("Total steps is %d" % len(path))

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


def init():
    global board
    while True:
        data = random.sample(range(9), 9)
        template = [1, 2, 3, 4, 5, 6, 7, 8, 0]
        if inversions(data)[1] % 2 == inversions(template)[1] % 2:  #判断是否有解
            break
    print(data)
    count = 0
    for i in range(3):
        for j in range(3):
            board[i][j] = data[count]
            count+=1
    print(board)
init()

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
        move_sound.play()
    except:
        traceback.print_exc()

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
                move(2)
            if event.key == pygame.K_DOWN:
                print("down")
                move(3)
            if event.key == pygame.K_LEFT:
                print("left")
                move(0)
            if event.key == pygame.K_RIGHT:
                print("right")
                move(1)
            if event.key == pygame.K_a:
                print("autosolve")
                autosolve()
            if event.key == pygame.K_i:
                print("initial")
                init()
            if board == [[1, 2, 3], [4, 5, 6], [7, 8, 0]]:
                print("success!")
    pygame.display.flip() #更新屏幕内容

