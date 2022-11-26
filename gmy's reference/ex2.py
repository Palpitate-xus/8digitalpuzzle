import random as rd
import pygame as pg
def h(a,b):
    ct=0
    for i in range(9):
        if(a[i]=='0'):continue
        for j in range(9):
            if(a[i]==b[j]):break
        ct+=abs(i//3-j//3)+abs(i%3-j%3)
    return ct
def findpathbutA_star(start):
    end=['123804765',4]
    if(start[0]==end[0]):return [0,0]
    loop=h(start[0],end[0])
    crv={start[0]:[loop,'']}
    dir=((1,0),(-1,0),(0,1),(0,-1))
    while(1):
        stk,td=[start],[0]
        while(len(stk)):
            t,dep=stk.pop(0),td.pop(0)
            for d in dir:
                tem=[t[0],t[1]]
                m=t[1]//3+d[0];n=t[1]%3+d[1];tem[1]=3*m+n
                if(m>=3 or n>=3 or m<0 or n<0):continue
                tem[0]=swcplace(tem[0],tem[1],t[1])
                if(tem[0]==crv[t[0]][1]):continue
                if(not tem[0] in crv):
                    crv[tem[0]]=[h(tem[0],end[0]),t[0]]
                k=crv[tem[0]]
                if(k[0]+dep>=loop):continue
                if(not k[0]):return [crv,loop]
                stk.insert(0,tem),td.insert(0,dep+1)
        loop+=1
        if(loop>50):return [0,-1]
def findpath(start):
    end=["123456780",8]
    if(start[0]==end[0]):return [0,0]
    que=[start,end]
    crv={start[0]:[1,0,''],end[0]:[0,1,'']}
    dir=((1,0),(-1,0),(0,1),(0,-1))
    while(len(que)):
        t=que.pop(0)
        for d in dir:
            tem=[t[0],t[1]]
            m=t[1]//3+d[0];n=t[1]%3+d[1];tem[1]=3*m+n
            if(m>=3 or n>=3 or m<0 or n<0):continue
            tem[0]=swcplace(tem[0],tem[1],t[1])
            if(not tem[0] in crv):
                k=crv[t[0]]
                crv[tem[0]]=[k[0],k[1]+1,t[0]]
                que.append(tem);continue
            if(crv[tem[0]][0]==crv[t[0]][0]):continue
            k,d=[t[0],tem[0]],crv[t[0]][0]
            while(len(k[d^1])):
                temp=crv[k[d^1]][2]
                crv[k[d^1]][2]=k[d];k[d]=k[d^1];k[d^1]=temp
            return [crv,crv[tem[0]][1]+crv[t[0]][1]]
    return [0,-1]
def displaypics(pres):
    for i in range(9):
        mscr.blit(imgs[int(pres[0][i])],((i%3)*182+90,(i//3)*182+40))
        if(pres[0][i]=='0'):pg.draw.rect(mscr,(0,0,0),[(i%3)*182+90,(i//3)*182+40,180,180],3)
def swcplace(str,i,j):
    t=list(str);str=''
    t[i],t[j]=t[j],t[i]
    for c in t:str+=c
    return str
def inside(n,rec):
    return n[0]>=rec[0] and n[0]<=rec[0]+rec[2] and n[1]>=rec[1] and n[1]<=rec[1]+rec[3]
def movefunc(pos):
    for x in recs:
        if(inside(pos,x)):
            pg.draw.rect(mscr,(137,66,196),x,2)
        else:pg.draw.rect(mscr,(255,255,255),x,2)
def newpat():
    pat=['123456780',8]
    dir=((1,0),(-1,0),(0,1),(0,-1))
    for i in range(rd.randint(80,100)):
        d=dir[rd.randint(0,3)]
        m=pat[1]//3+d[0];n=pat[1]%3+d[1]
        if(m>=3 or n>=3 or m<0 or n<0):continue
        pat[0]=swcplace(pat[0],pat[1],3*m+n)
        pat[1]=3*m+n
    return pat
def downfunc(pos):
    global newgame,endgame,autos,pres,cplt
    if(inside(pos,recs[0])):
        pg.draw.rect(mscr,(137,66,196),recs[0],0)
        newgame=basicfont.render('New Game',True,(255,255,255))
        mscr.blit(newgame,(750,250))
        pg.display.flip()
        while(True):
            evt=pg.event.wait()
            if(not evt.type==pg.MOUSEBUTTONUP):continue
            if(inside(evt.pos,recs[0])):
                pres=newpat()
                cplt=0
            pg.draw.rect(mscr,(255,255,255),recs[0],0)
            newgame=basicfont.render('New Game',True,(137,66,196))
            break
    elif(inside(pos,recs[1])):
        pg.draw.rect(mscr,(137,66,196),recs[1],0)
        endgame=basicfont.render('End Game',True,(255,255,255))
        mscr.blit(endgame,(750,350))
        pg.display.flip()
        while(True):
            evt=pg.event.wait()
            if(not evt.type==pg.MOUSEBUTTONUP):continue
            if(inside(evt.pos,recs[1])):
                pg.quit();exit(0)
            pg.draw.rect(mscr,(255,255,255),recs[1],0)
            endgame=basicfont.render('End Game',True,(137,66,196))
            break
    elif(inside(pos,recs[2])):
        pg.draw.rect(mscr,(137,66,196),recs[2],0)
        autos=basicfont.render('auto solve',True,(255,255,255))
        mscr.blit(autos,(740,450))
        pg.display.flip()
        while(True):
            evt=pg.event.wait()
            if(not evt.type==pg.MOUSEBUTTONUP):continue
            if(inside(evt.pos,recs[2])):
                ans=findpath(pres)
                if(ans[1]):
                    t1=pres[0];t2=ans[0][t1][2]
                    while(t2):
                        pres[0]=t2
                        displaypics(pres)
                        pg.display.update()
                        t1=t2;t2=ans[0][t1][2]
                        pg.time.wait(300)
            pg.draw.rect(mscr,(255,255,255),recs[2],0)
            autos=basicfont.render('auto solve',True,(137,66,196))
            cplt=1;break
    elif(not cplt):
        i=(pos[0]-90)//182+(pos[1]-40)//182*3
        rect=((i%3)*182+90,(i//3)*182+40,180,180)
        while(True):
            evt=pg.event.wait()
            if(not evt.type==pg.MOUSEBUTTONUP):continue
            if(inside(evt.pos,rect)):
                dir,m,n=((1,0),(-1,0),(0,1),(0,-1)),-1,-1
                for d in dir:
                    m=i//3+d[0];n=i%3+d[1]
                    if(m<3 and n<3 and m>=0 and n>=0 and 3*m+n==pres[1]):
                        pres=[swcplace(pres[0],i,pres[1]),i];break
                if(pres[0]=='123456780'):cplt=1
                break
    movefunc(pos)
    pg.event.get().clear()
pres=['123456780',8]
cplt=1
pg.init()
mscr=pg.display.set_mode(size=(960,640))
mscr.fill((255,255,255))
imgs=[pg.transform.scale(pg.image.load('pic/'+str(i)+'.png').convert(),(180,180)) for i in range(9)]
basicfont=pg.font.SysFont('consolas',24)
newgame=basicfont.render('New Game',True,(137,66,196))
endgame=basicfont.render('End Game',True,(137,66,196))
autos=basicfont.render('auto solve',True,(137,66,196))
recs=[(720,230,164,64),(720,330,164,64),(720,430,164,64)]
pg.display.set_caption('拼图游戏')
while(True):
    evt=pg.event.wait()
    if(evt.type==pg.QUIT):
        pg.quit();exit(0)
    if(evt.type==pg.MOUSEMOTION):
        movefunc(evt.pos)
    if(evt.type==pg.MOUSEBUTTONDOWN):
        downfunc(evt.pos)
    displaypics(pres)
    mscr.blit(newgame,(750,250))
    mscr.blit(endgame,(750,350))
    mscr.blit(autos,(740,450))
    pg.display.update()