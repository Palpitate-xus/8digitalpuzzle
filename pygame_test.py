import sys
import pygame

pygame.init()

screen = pygame.display.set_mode((400,400))
screen.fill((255,255,255))
pygame.display.set_caption('8 digital puzzle')

f = pygame.font.Font('C:/Windows/Fonts/simhei.ttf',50)
# 生成文本信息，第一个参数文本内容；第二个参数，字体是否平滑；
# 第三个参数，RGB模式的字体颜色；第四个参数，RGB模式字体背景颜色；
text0 = pygame.image.load("./digital/0.png").convert()
text1 = pygame.image.load("./digital/1.png").convert()
text2 = f.render("2", False, (0, 0, 0))
text3 = f.render("3", False, (0, 0, 0))
text4 = f.render("4", False, (0, 0, 0))
text5 = f.render("5", False, (0, 0, 0))
text6 = f.render("6", False, (0, 0, 0))
text7 = f.render("7", False, (0, 0, 0))
text8 = f.render("8", False, (0, 0, 0))

#创建一个 50*50 的图像,并优化显示
face = pygame.Surface((90, 90),flags=pygame.HWSURFACE)
#填充颜色
face.fill(color='pink')

# 固定代码段，实现点击"X"号退出界面的功能，几乎所有的pygame都会使用该段代码
while True:
    # 循环获取事件，监听事件状态
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
                face.blit(text1, (0, 0))
            if event.key == pygame.K_DOWN:
                print("down")
                face.fill(color='green')
                face.blit(text3, (2, 0))
            if event.key == pygame.K_RIGHT:
                print("right")
                face.fill(color='purple')
                face.blit(text3, (2, 0))
            if event.key == pygame.K_LEFT:
                print("left")
                face.fill(color='yellow')
                face.blit(text4, (2, 0))
    face.blit(text0, (0, 0))
    screen.blit(face, (25, 25))
    pygame.display.flip() #更新屏幕内容