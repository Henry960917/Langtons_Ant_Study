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