import pygame
import random
import math

W = 800
H = 500
ants = 1
cellSize = 2
cnt = 0
#d:0上、1右上、2右下、3下、4左下、5左上
dxOdd = [-1,0,1,1,1,0] #垂直 when odd(兩邊較高)
dxEven = [-1,-1,0,1,0,-1] #垂直 when even(兩邊較低)
dy = [0,1,1,0,-1,-1] #水平

N = 0
R1 = 1
R2 = 2
U = 3
L2 = -2
L1 = -1


grid = [[0 for _ in range(W)] for _ in range(H)]
rule = [L1,L2,N,U,L2,L1,R2]

colors = [
    (255,255,255),   # 0 白
    (0,0,0),         # 1 黑
    (255,0,0),       # 2 紅
    (0,255,0),       # 3 綠
    (0,0,255),       # 4 藍
    (255,0,255),     # 5 洋紅
    (255,255,0),     # 6 黃
    (0,255,255),     # 7 青
    (255,128,0),     # 8 橘
    (128,0,255),     # 9 紫
    (128,128,128),   # 10 灰
    (255,192,203),   # 11 粉紅
    (139,69,19),     # 12 棕
    (0,128,128),     # 13 深青
    (128,255,0),     # 14 黃綠
    (75,0,130),      # 15 靛
    (255,215,0),     # 16 金
    (173,216,230),   # 17 淺藍
    (240,230,140),   # 18 卡其
    (220,20,60),     # 19 深紅
    (50,205,50),     # 20 萊姆綠
    (70,130,180),    # 21 鋼藍
    (210,105,30),    # 22 巧克力
    (255,140,0),     # 23 深橘
    (199,21,133),    # 24 紫紅
    (154,205,50),    # 25 黃綠2
    (0,191,255),     # 26 天藍
    (186,85,211),    # 27 中紫
    (255,99,71),     # 28 番茄紅
    (46,139,87),     # 29 海綠
]

r = cellSize
window_w = (int((W-1)*r*1.5 + r*2))
window_h = int(H * r * math.sqrt(3) + (r * math.sqrt(3) / 2) + r)

pygame.init()
screen = pygame.display.set_mode((window_w, window_h))
pygame.display.set_caption("蘭頓螞蟻")

hex_shape = []
for i in range(6):
    theta = math.pi / 3 * i
    hex_shape.append((math.cos(theta), math.sin(theta)))

class Ant:
    def __init__(self):
        self.x = H//2
        self.y = W//2
        self.dir = random.randint(0, 5) #朝向哪

manyAnts = []
for i in range(ants):
    manyAnts.append(Ant())

def gridToPx(row,col):
    cx = col*1.5*r + r
    cy = row*r*math.sqrt(3)+(col%2)*(r*math.sqrt(3)/2)+r #odd要下沉
    return cx,cy #中心座標

run = True
screen.fill((255,255,255))
while run:
    pygame.time.Clock().tick(60)

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run = False

    cnt+=1
    
    print("目前回合數:", cnt)
    for _ in range(1000): #加速用，先設個20好了
        for i in manyAnts:
            x = i.x
            y = i.y
            d = i.dir
            c = grid[x][y]    #目前顏色
            d = (d + rule[c] + 6) % 6
            grid[x][y] = (c + 1) % len(rule)
            if y % 2 == 0:
                x = (x + dxEven[d] + H) % H
            else:
                x = (x + dxOdd[d] + H) % H
            y = (y + dy[d] + W) % W
            i.x = x
            i.y = y
            i.dir = d

    
    for i in range(H):
        for j in range(W):
            c = grid[i][j]
            if c == 0:
                continue
            cx, cy = gridToPx(i, j)
            points=[]
            for k,l in hex_shape:
                points.append((cx+r*k, cy+r*l))
            
            pygame.draw.polygon(screen, colors[c % len(colors)], points)

    pygame.display.flip()

pygame.quit()