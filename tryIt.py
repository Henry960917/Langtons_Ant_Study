import pygame
import random

W = 400
H = 250
ants = 1
cellSize = 4
cnt = 0
dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]
grid = [[0 for _ in range(W)] for _ in range(H)]
Q = [[0.0 for _ in range(2)] for _ in range(8)]
alpha = 0.1
gamma = 0.9
epsilon = 0.05

pygame.init()
screen = pygame.display.set_mode((W*cellSize, H*cellSize))
pygame.display.set_caption("AI蘭頓螞蟻")

class Ant:
    def __init__(self):
        self.x = random.randint(0, H-1)
        self.y = random.randint(0, W-1)
        self.dir = random.randint(0, 3) #0:u, 1:r, 2:d, 3:l

manyAnts = []
for i in range(ants):
    manyAnts.append(Ant())

def get_state(color, d):
    return color * 4 + d

def choose_action(state):
    if random.random() < epsilon:
        return random.randint(0, 1)
    return max(range(2), key=lambda a: Q[state][a])

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
        color = grid[x][y]
        state = get_state(color, d)

        action = choose_action(state)
        if color == 0:
            correct_action = 1  # 右轉
        else:
            correct_action = 0  # 左轉
        if action == correct_action:
            reward = 1
        else:
            reward = -1

    # ===== 執行動作 =====
        if action == 0:
            d = (d + 3) % 4  # 左轉
        else:
            d = (d + 1) % 4  # 右轉
        if (grid[x][y] == 0): #white
            d = (d + 1) % 4
            grid[x][y] = 1
        else: #black
            d = (d + 3) % 4
            grid[x][y] = 0
        nx = (x + dx[d] + H) % H
        ny = (y + dy[d] + W) % W

        new_color = grid[nx][ny]
        new_state = get_state(new_color, d)

        # ===== Q-learning 更新 =====
        maxQ = max(Q[new_state])
        Q[state][action] += alpha * (reward + gamma * maxQ - Q[state][action])
        i.x = nx
        i.y = ny
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