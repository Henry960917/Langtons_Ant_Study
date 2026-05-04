import pygame
import numpy as np
import random

# --- 參數設定 ---
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 10  # 為了方便觀察，格子設大一點
COLS, ROWS = WIDTH // GRID_SIZE, HEIGHT // GRID_SIZE
FPS = 60 # 可以調高來加速學習

# 顏色定義 (0:白, 1:黑, 2:紅, 3:藍)
COLOR_MAP = [
    (255, 255, 255), (50, 50, 50), 
    (255, 100, 100), (100, 100, 255)
]

# Q-Learning 參數
ALPHA = 0.2    # 學習率
GAMMA = 0.9    # 折扣因子
EPSILON = 0.1  # 探索率
ACTIONS = [0, 1, 2, 3] # 0:左轉, 1:右轉, 2:直行, 3:迴轉
# 狀態數 = 顏色數量
q_table = np.zeros((len(COLOR_MAP), len(ACTIONS)))

# --- 螞蟻類別 ---
class Ant:
    def __init__(self):
        self.x = COLS // 2
        self.y = ROWS // 2
        self.dir = 0  # 0:上, 1:右, 2:下, 3:左
        self.last_pos = (self.x, self.y)
        self.steps = 0
        
    def move(self, action):
        # 根據動作改變方向
        if action == 0:   # 左轉
            self.dir = (self.dir - 1) % 4
        elif action == 1: # 右轉
            self.dir = (self.dir + 1) % 4
        elif action == 3: # 迴轉
            self.dir = (self.dir + 2) % 4
            
        # 前進
        if self.dir == 0: self.y -= 1
        elif self.dir == 1: self.x += 1
        elif self.dir == 2: self.y += 1
        elif self.dir == 3: self.x -= 1
        
        # 邊界處理
        self.x %= COLS
        self.y %= ROWS

# --- 初始化 Pygame ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Q-Learning Langton's Ant: Finding Highway")
clock = pygame.time.Clock()

grid = np.zeros((COLS, ROWS), dtype=int)
ant = Ant()

# 為了計算獎勵，記錄每 100 步的起始位置
start_pos_for_reward = (ant.x, ant.y)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 1. 觀察當前狀態 (目前格子的顏色)
    state = grid[ant.x, ant.y]

    # 2. 選擇動作 (Epsilon-Greedy)
    if random.random() < EPSILON:
        action = random.choice(ACTIONS)
    else:
        action = np.argmax(q_table[state])

    # 3. 執行動作並改變環境
    old_x, old_y = ant.x, ant.y
    ant.move(action)
    
    # 蘭頓螞蟻的核心：離開後格子變色 (循環顏色)
    grid[old_x, old_y] = (grid[old_x, old_y] + 1) % len(COLOR_MAP)
    
    # 4. 計算獎勵 (每 50 步結算一次位移)
    reward = 0
    ant.steps += 1
    if ant.steps % 50 == 0:
        dist = np.sqrt((ant.x - start_pos_for_reward[0])**2 + (ant.y - start_pos_for_reward[1])**2)
        reward = dist  # 位移愈遠，獎勵愈高
        start_pos_for_reward = (ant.x, ant.y) # 重置參考點

        # 5. 更新 Q 表
        next_state = grid[ant.x, ant.y]
        old_value = q_table[state, action]
        next_max = np.max(q_table[next_state])
        
        # Q-Learning 公式
        q_table[state, action] = old_value + ALPHA * (reward + GAMMA * next_max - old_value)

    # --- 繪圖 ---
    screen.fill((200, 200, 200))
    
    # 繪製網格 (優化：只繪製非背景色的格子)
    for x in range(COLS):
        for y in range(ROWS):
            if grid[x, y] != 0:
                pygame.draw.rect(screen, COLOR_MAP[grid[x, y]], 
                                 (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
    
    # 繪製螞蟻
    pygame.draw.rect(screen, (255, 0, 255), 
                     (ant.x * GRID_SIZE, ant.y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()