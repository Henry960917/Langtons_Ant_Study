---
title: 蘭頓螞蟻 Langton's Ant

---

# 蘭頓螞蟻 Langton's Ant

## 簡介
蘭頓螞蟻是一種由數學家Christopher Langton在1986年提出的二維圖靈機，是細胞自動機的例子，具簡單的規則與複雜的表現。可被想像成一隻在格子世界中移動的小螞蟻，而每個格子只有黑白二色，螞蟻會根據目前格子的顏色決定轉向。

## 規則
設白格為0、黑格為1。
* 若螞蟻在白格，則右轉90度，將該格改為黑格，向前走一步。
* 若螞蟻在黑格，則左轉90度，將該格改為白格，向前走一步。

此規則記為==RL==。

## 現象
蘭頓螞蟻的演化會經歷三階段：簡單(Simplicity)、渾沌(Chaos)、湧現(Emergence)

一開始會出現許多重複或對稱的簡單形狀，接著螞蟻會進入偽隨機(pseudo-random)、雜亂的行走，而經過約10000步後，螞蟻幾乎一定會形成固定結構：「==高速公路(Highway)==」。以週期性方式前進、留下斜向重複圖案
、持續無限延伸。在目前測試過的所有起始型態，最終都收斂到相同的重複模式，表明了「高速公路」是蘭頓螞蟻的吸引子(attractor)，但尚無法證明這是無論任何起始狀態都會導致的必然結果。

<div style="text-align: center;"><img src="https://hackmd.io/_uploads/Hk4jna8kGe.png"></div>

([圖片來源](https://en.wikipedia.org/wiki/Langton%27s_ant))

## 實作
可以用==pygame==來簡單呈現蘭頓螞蟻。

### 完整程式碼
```python
import pygame
import random

W = 400
H = 250
ants = 1
cellSize = 4
cnt = 0
dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1] #urdl
grid = [[0 for _ in range(W)] for _ in range(H)]

pygame.init()
screen = pygame.display.set_mode((W*cellSize, H*cellSize))
pygame.display.set_caption("原汁原味蘭頓螞蟻")

class Ant:
    def __init__(self):
        self.x = random.randint(0, H-1)
        self.y = random.randint(0, W-1)
        self.dir = random.randint(0, 3) #0:u, 1:r, 2:d, 3:l

manyAnts = []
for i in range(ants):
    manyAnts.append(Ant())

run = True

while run:
    pygame.time.Clock().tick(60)

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run = False

    cnt+=1
    if(cnt%100==0):
        print("目前步數:", cnt)

    for i in manyAnts:
        x = i.x
        y = i.y
        d = i.dir
        if (grid[x][y] == 0): #white
            d = (d + 1) % 4
            grid[x][y] = 1
        else: #black
            d = (d + 3) % 4
            grid[x][y] = 0
        x = (x + dx[d] + H) % H
        y = (y + dy[d] + W) % W
        i.x = x
        i.y = y
        i.dir = d

    screen.fill((255,255,255))
    for i in range(H):
        for j in range(W):
            if grid[i][j] == 1:
                pygame.draw.rect(
                    screen,
                    (0, 0, 0),
                    (j*cellSize, i*cellSize, cellSize, cellSize)
                )

    for i in manyAnts:
        pygame.draw.rect(
            screen,
            (255, 0, 0),
            (i.y*cellSize, i.x*cellSize, cellSize, cellSize)
        )

    pygame.display.flip()

pygame.quit()
```

## 推廣_多色蘭頓螞蟻
將蘭頓螞蟻模型擴展成==多色蘭頓螞蟻==，不再使用兩種顏色，而是使用更多顏色，表示方法是用L和R表示各顏色是左轉還是右轉。

多色螞蟻比原始蘭頓螞蟻更加複雜，可能呈現:

* 高速公路
* 不規則混亂軌跡
* 對稱圖形
* 內部循環
* 其他軌跡...

由於存在一些重複(e.g., RRL與LLR之軌跡相同)、無用(e.g., RRR,LLL)之規則，可以稍微Dedupe一下，此處用C++。固定第一個元素為R，利用二進制進位之概念產生所有排列，如下所示：

### 完整程式碼
```cpp
//我把相同軌跡的去除(保留R開頭的組合，L開頭的組合去除掉)、全為R或全為L的也去除
//請輸入n
#include <iostream>
#include <cmath>
#include <vector>
using namespace std;

int main(){
    int n;
    cin >> n;
    int total = pow(2, n);
    vector<int> v(n, 1);
    for(int i = 1; i<n; i++){
        v[i] = -1;
    }
    while(true){
        bool all_one = true;
        for(int i = 0; i<v.size(); i++){
            if(v[i]!=1){
                all_one = false;
            }
        }
        if(!all_one){
            for(int i = 0; i<v.size(); i++){
                cout << v[i] << " ";
            }
            cout << endl;
        }
        int idx = n-1;
        while(idx>=1){
            if(v[idx]==-1){
                v[idx] = 1;
                break;
            }
            else{
                v[idx] = -1;
                idx--;
            }
        }
        if(idx<1){
            break;
        }
    }
}
```

### 範例

|規則 | 圖形  |  軌跡  | 步數(大約) |
|--- | :---: | ------ | --- |
|RLL |![RLL_40000](https://hackmd.io/_uploads/S1vxBE7eMl.png =45%x)|不規則|40000|
|RLR |![RLR_30000](https://hackmd.io/_uploads/B1nlvN7xzx.png =45%x)|不規則|30000|
|RRL |![RRL_10000](https://hackmd.io/_uploads/rkNovNQgfl.png)|高速公路|10000|
|RLLL|![RLLL_40000](https://hackmd.io/_uploads/BJJ4jE7eze.png)|不規則|40000|
|RLLR|![RLLR_40000](https://hackmd.io/_uploads/HyNEvvVgzx.png)|對稱、內部循環|40000|
|RLRL|![RLRL_20000](https://hackmd.io/_uploads/rkSRMuEgMl.png)|高速公路|20000|
|RLRR|![RLRR_20000](https://hackmd.io/_uploads/BJh-7uExzg.png)|不規則|20000|
|RRLL|![RRLL_30000](https://hackmd.io/_uploads/r1zy4dNgMl.png)|對稱|30000|
|RRLR|![RRLR_20000](https://hackmd.io/_uploads/SyMWHK4eGg.png)|不規則|20000|
|RRRL|![RRRL_10000](https://hackmd.io/_uploads/HyT_HFNlze.png)|高速公路|10000|
|RLLLL|![RLLLL_20000](https://hackmd.io/_uploads/B16TBYVgMg.png)|不規則|20000|
|RLLLR|![RLLLR_30000](https://hackmd.io/_uploads/By9MUYEefe.png)|內部循環|30000|
|RLLRL|![RLLRL_20000](https://hackmd.io/_uploads/SJeOLtNxMg.png)|不規則|20000|
|RLLRR|![RLLRR_20000](https://hackmd.io/_uploads/HJ5cUF4lzg.png)|內部循環|20000|
|RRLLLRLLLRRR |![螢幕擷取畫面 2026-05-27 230512](https://hackmd.io/_uploads/rJrh_tNxfg.png)|逐漸形成三角形|50000|
|LLRRRLRLRLLR |![螢幕擷取畫面 2026-05-30 140429](https://hackmd.io/_uploads/Bkoen4_gGx.png)|曲折高速公路|40000|
|LRRRRRLLR |![螢幕擷取畫面 2026-05-30 183413](https://hackmd.io/_uploads/rk6UaV_lGl.png)|填滿的正方形|80000|
|LLRRRLRL |![螢幕擷取畫面 2026-05-30 202905](https://hackmd.io/_uploads/S1JV_Iuezg.png)|高速公路|80000|

## 推廣_六角形蘭頓螞蟻
除了使用方格，我們也能使用六邊形的格子，產生更複雜的行為。六邊形網格有六種轉向規則，分別為:**N**(不變)、**R1**(順時針旋轉60度)、**R2**(順時針旋轉120度)、**U**(旋轉180度)、**L1**(逆時針旋轉60度)、**L2**(逆時針旋轉120度)。

### 想法

建立一個hex map來模擬，為了讓六邊形緊密貼合，我採用==Odd-q Vertical Layout==，即奇數欄下沉，如下圖左半所示。

![下載5555](https://hackmd.io/_uploads/ryPID6yWfx.jpg =800x)([圖片來源](http://www.lvesu.com/blog/main/cms-947.html))

為了把六邊形畫出來，我們必須知道它的6個頂點座標。先建立一個半徑為1，中心(0,0)的單位圓，六邊形就可以內接在其中，利用數學公式 $(x, y) = (\cos\theta, \sin\theta)$，就能依序算出這 6 個頂點在單位圓上的座標。

有了這個骨架後，接著要畫grid[i][j]，透過幾何推理一下可知這格在螢幕上的實際像素中心點(cx, cy)，再把骨架的6頂點乘以r(放大)、再加到中心點上(平移)。

最後丟給pygame進行渲染即可。

而為了提升效能，我們可以加上這段程式(如下)。
```python
if grid[i][j] == 0:
    continue
```
若沒有加這行，即使大部分格子為背景色，每次刷新時電腦都要畫 W*H(本程式為400000) 個六邊形，會消耗極大的CPU算力，電腦會非常卡頓。


### 完整程式碼
```python
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
```

### 範例

|規則 | 圖形   |  軌跡   | 步數(大約) |
|--- | :---: | ------ | --- |
|L2NNL1L2L1 |![螢幕擷取畫面 2026-06-03 233235](https://hackmd.io/_uploads/SkZPFTaxMg.png)|循環生長|82000|
|L1L2NUL2L1R2 |![螢幕擷取畫面 2026-06-05 120150](https://hackmd.io/_uploads/B1gLqpkZfx.png)|螺旋生長|60000|
|L1R1L1R1 |![R1L1R1L1](https://hackmd.io/_uploads/rkD7sll-Mx.png)|對稱|100000|
|NR1 |![NR1](https://hackmd.io/_uploads/H1w2seeWzx.png)|類高速公路|40000|
|L1L2L2L2UNL1R1 |![L1L2L2L2UNL1R1](https://hackmd.io/_uploads/Sk72xWe-zl.png)|高速公路|80000|
|R2L1L2R1R1UR1 |![螢幕擷取畫面 2026-06-05 160209](https://hackmd.io/_uploads/SJt5MWgbfg.png)|高速公路|100000|
|UNL2UL1R2N |![螢幕擷取畫面 2026-06-05 160455](https://hackmd.io/_uploads/ByQr7WgWGx.png)|矩形擴張|60000|
|R2L2UL2R2 |![螢幕擷取畫面 2026-06-05 160711](https://hackmd.io/_uploads/HkxRmbgWGl.png)|高速公路|60000|
|L2R1L2R1L2UL1R1 |![螢幕擷取畫面 2026-06-05 161158](https://hackmd.io/_uploads/SJ-KH-gWfl.png)|螺旋生長|60000|

## 參考資料
* [Langton's ant - Wikipedia](https://en.wikipedia.org/wiki/Langton%27s_ant)
* [Langton's Ant on a hexagonal grid - YouTube](https://www.youtube.com/watch?v=sneXM3jzcIg)
* [細胞自動機 - 維基百科](https://zh.wikipedia.org/zh-tw/%E7%B4%B0%E8%83%9E%E8%87%AA%E5%8B%95%E6%A9%9F)
* [正六边形网格化(Hexagonal Grids)原理与实现 - lvesu](http://www.lvesu.com/blog/main/cms-947.html)
* [Turmite - Wikipedia](https://en.wikipedia.org/wiki/Turmite)