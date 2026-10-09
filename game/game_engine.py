import pygame
from game.maze import generate_maze, CELL
from game.entities import Player, Enemy

COLS, ROWS = 13, 11
WIDTH = COLS * CELL
HEIGHT = ROWS * CELL + 50
FPS = 60
SPEEDUP_INTERVAL_MS = 15_000
ENEMY_INTERVAL_STEP = 2
MIN_ENEMY_INTERVAL = 5
POWER_PELLET_FREEZE_MS = 5_000

class GameEngine:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Maze Chase")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("monospace", 22)
        self.hud_font = pygame.font.SysFont("monospace", 17)
        self.exit_font = pygame.font.SysFont("monospace", 14)
        self.big_font = pygame.font.SysFont("monospace", 38, bold=True)
        self.reset()

    def reset(self):
        self.walls = generate_maze(COLS, ROWS)
        self.player = Player(0, 0)
        self.score = 0
        self.enemies = [
            Enemy(ROWS-1, COLS-1),
            Enemy(0, COLS-1),
            Enemy(ROWS-1, 0),
        ]
        self.pellet_rect = pygame.Rect(0, 0, 18, 18)
        self.pellet_rect.center = (
            (COLS//2-2)*CELL + CELL//2,
            (ROWS//2)*CELL + CELL//2,
        )
        self.pellet_collected = False
        self.freeze_started_at = None
        self.initial_enemy_move_interval = self.enemies[0].move_interval
        self.enemy_move_interval = self.initial_enemy_move_interval
        self.speed_tier = 0
        self.difficulty_start_time = pygame.time.get_ticks()
        for enemy in self.enemies:
            enemy.move_interval = self.enemy_move_interval
        self.exit_rect = pygame.Rect((COLS//2)*CELL+5, (ROWS//2)*CELL+5, CELL-10, CELL-10)
        self.caught = False
        self.won = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r: self.reset()
        return True

    def update(self):
        now = pygame.time.get_ticks()
        if (
            self.freeze_started_at is not None
            and now - self.freeze_started_at >= POWER_PELLET_FREEZE_MS
        ):
            self.freeze_started_at = None
            for enemy in self.enemies:
                enemy.frozen = False
        if self.caught or self.won: return
        elapsed_ms = now - self.difficulty_start_time
        max_speed_tier = (
            self.initial_enemy_move_interval - MIN_ENEMY_INTERVAL
            + ENEMY_INTERVAL_STEP - 1
        ) // ENEMY_INTERVAL_STEP
        speed_tier = min(elapsed_ms // SPEEDUP_INTERVAL_MS, max_speed_tier)
        if speed_tier != self.speed_tier:
            self.speed_tier = speed_tier
            self.enemy_move_interval = max(
                MIN_ENEMY_INTERVAL,
                self.initial_enemy_move_interval - ENEMY_INTERVAL_STEP * self.speed_tier,
            )
            for enemy in self.enemies:
                enemy.move_interval = self.enemy_move_interval
        keys = pygame.key.get_pressed()
        self.player.move(keys, self.walls, ROWS, COLS)
        if not self.pellet_collected and self.player.rect.colliderect(self.pellet_rect):
            self.pellet_collected = True
            self.freeze_started_at = now
            for enemy in self.enemies:
                enemy.frozen = True
                enemy.timer = 0
        for enemy in self.enemies:
            enemy.update(self.walls, self.player, ROWS, COLS)
        if any(self.player.rect.colliderect(enemy.rect) for enemy in self.enemies):
            self.caught = True
        if self.player.rect.colliderect(self.exit_rect):
            self.won = True
        if not self.caught and not self.won:
            self.score += 1

    def draw(self):
        self.screen.fill((230, 220, 210))
        wc=(50,40,60)
        for r in range(ROWS):
            for c in range(COLS):
                x,y=c*CELL,r*CELL
                w=self.walls[r][c]
                if w[0]: pygame.draw.line(self.screen,wc,(x,y),(x+CELL,y),3)
                if w[1]: pygame.draw.line(self.screen,wc,(x,y+CELL),(x+CELL,y+CELL),3)
                if w[2]: pygame.draw.line(self.screen,wc,(x+CELL,y),(x+CELL,y+CELL),3)
                if w[3]: pygame.draw.line(self.screen,wc,(x,y),(x,y+CELL),3)
        pygame.draw.rect(self.screen,(80,200,80),self.exit_rect,border_radius=4)
        lbl=self.exit_font.render("EXIT",True,(20,80,20))
        self.screen.blit(lbl,lbl.get_rect(center=self.exit_rect.center))
        if not self.pellet_collected:
            center = self.pellet_rect.center
            pygame.draw.circle(self.screen,(70,55,30),center,10)
            pygame.draw.circle(self.screen,(255,210,45),center,8)
            pygame.draw.circle(self.screen,(255,250,190),(center[0]-3,center[1]-3),2)
        self.player.draw(self.screen)
        for enemy in self.enemies:
            enemy.draw(self.screen)
        hud=pygame.Rect(0,ROWS*CELL,WIDTH,50)
        pygame.draw.rect(self.screen,(30,30,50),hud)
        info=self.hud_font.render("Reach EXIT before the enemy catches you!  R=Restart",True,(200,200,200))
        self.screen.blit(info,(8,ROWS*CELL+3))
        speed_info = self.hud_font.render(
            f"Survived: {self.score // 60}s  Speed tier: {self.speed_tier}  Interval: {self.enemy_move_interval}f",
            True,
            (200,200,200),
        )
        self.screen.blit(speed_info,(8,ROWS*CELL+26))
        if self.caught:
            self._overlay("CAUGHT!", (220,60,60))
        if self.won:
            self._overlay("ESCAPED!", (80,220,80))
        pygame.display.flip()

    def _overlay(self, text, color):
        surf=pygame.Surface((WIDTH,ROWS*CELL),pygame.SRCALPHA)
        surf.fill((0,0,0,140))
        self.screen.blit(surf,(0,0))
        msg=self.big_font.render(text,True,color)
        sub=self.font.render("Press R to Restart",True,(200,200,200))
        score=self.font.render(f"Survived: {self.score // 60}s",True,(200,200,200))
        self.screen.blit(msg,(WIDTH//2-msg.get_width()//2,ROWS*CELL//2-30))
        self.screen.blit(sub,(WIDTH//2-sub.get_width()//2,ROWS*CELL//2+20))
        self.screen.blit(score,(WIDTH//2-score.get_width()//2,ROWS*CELL//2+52))

    def run(self):
        running=True
        while running:
            running=self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()
