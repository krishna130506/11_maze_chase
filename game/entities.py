import pygame
from game.maze import CELL

SPEED = 2

class Player:
    def __init__(self, r, c):
        self.r, self.c = r, c
        cx, cy = c*CELL+CELL//2, r*CELL+CELL//2
        self.rect = pygame.Rect(cx-10, cy-10, 20, 20)
        self.color = (60, 120, 220)

    def move(self, keys, walls, rows, cols):
        dx=dy=0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]: dx=-SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: dx=SPEED
        if keys[pygame.K_UP] or keys[pygame.K_w]: dy=-SPEED
        if keys[pygame.K_DOWN] or keys[pygame.K_s]: dy=SPEED
        nr = self.rect.move(dx,0)
        if self._valid(nr, walls, rows, cols): self.rect=nr
        nr = self.rect.move(0,dy)
        if self._valid(nr, walls, rows, cols): self.rect=nr

    def _valid(self, rect, walls, rows, cols):
        for px,py in [(rect.left,rect.top),(rect.right-1,rect.top),(rect.left,rect.bottom-1),(rect.right-1,rect.bottom-1)]:
            cr,cc=py//CELL,px//CELL
            if not(0<=cr<rows and 0<=cc<cols): return False
        left_col, right_col = rect.left//CELL, (rect.right-1)//CELL
        top_row, bottom_row = rect.top//CELL, (rect.bottom-1)//CELL
        for row in range(top_row, bottom_row+1):
            for col in range(left_col, right_col):
                if walls[row][col][2]: return False
        for row in range(top_row, bottom_row):
            for col in range(left_col, right_col+1):
                if walls[row][col][1]: return False
        return True

    def draw(self, screen):
        pygame.draw.ellipse(screen, self.color, self.rect)

class Enemy:
    def __init__(self, r, c):
        self.r, self.c = r, c
        cx, cy = c*CELL+CELL//2, r*CELL+CELL//2
        self.rect = pygame.Rect(cx-12, cy-12, 24, 24)
        self.color = (220, 60, 60)
        self.timer = 0
        self.move_interval = 20  # frames between cell moves
        self.frozen = False

    def update(self, walls, player, rows, cols):
        if self.frozen: return
        from game.maze import bfs
        self.timer += 1
        if self.timer >= self.move_interval:
            self.timer = 0
            pr, pc = player.rect.centery//CELL, player.rect.centerx//CELL
            step = bfs(walls, (self.r, self.c), (pr, pc), rows, cols)
            if step:
                dr, dc = step
                self.r += dr; self.c += dc
                cx, cy = self.c*CELL+CELL//2, self.r*CELL+CELL//2
                self.rect.center = (cx, cy)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=5)
        if self.frozen:
            pygame.draw.rect(screen, (100,220,255), self.rect.inflate(6,6), 2, border_radius=7)
        # eyes
        for ex in [self.rect.x+4, self.rect.x+14]:
            pygame.draw.circle(screen, (255,255,255), (ex, self.rect.y+8), 4)
            pygame.draw.circle(screen, (0,0,0), (ex+1, self.rect.y+8), 2)
