# Maze Chase

Escape a maze while being hunted by three AI enemies that navigate using BFS pathfinding.

## Setup

```bash
pip install -r requirements.txt
python main.py
```

## Controls

| Key | Action |
|-----|--------|
| W/A/S/D or Arrows | Move |
| R | Restart |

## Tasks to Complete

### Task 1: Multiple Enemies
> Add 2 more enemies starting at different corners. Each chases the player independently.

**Quick Start Prompt:**
```
In my maze-chase pygame game, I have one Enemy that uses BFS to chase the player. Add two more Enemy instances starting at different maze corners. Each should independently call bfs() on every update. List them in a self.enemies list and loop over them.
```

### Task 2: Speed Up Over Time
> Every 15 seconds the enemy move interval decreases, making it faster.

**Quick Start Prompt:**
```
Add a difficulty ramp to my maze-chase game. Track elapsed time with pygame.time.get_ticks(). Every 15 seconds, reduce enemy.move_interval by 2 (minimum 5). Show current enemy speed tier in the HUD.
```

### Task 3: Power Pellet (Freeze Enemy)
> Place a power pellet in the maze. Collecting it freezes the enemy for 5 seconds.

**Quick Start Prompt:**
```
Add a power pellet to my maze-chase game — a yellow circle somewhere in the maze. When the player rect collides with it, set enemy.frozen = True and start a 300-frame countdown. While frozen, enemy.update() does nothing. Show a frozen indicator on the enemy.
```

### Task 4: Score by Distance
> Score increases every frame the player stays alive. Show a survival score.

**Quick Start Prompt:**
```
Add a survival score to maze-chase. Increment self.score by 1 each frame the player is alive. Display it in the HUD as "Survived: Xs" where X is score // 60. On game over, show the final score on the overlay.
```

## Folder Structure

```
maze-chase/
├── main.py
├── requirements.txt
├── game/
│   ├── __init__.py
│   ├── game_engine.py
│   ├── maze.py
│   └── entities.py
└── README.md
```

## Submission Checklist

- [x] All 4 tasks completed
- [x] Multiple enemies work independently
- [x] Power pellet freezes enemy correctly
- [x] Speed ramp increases difficulty over time
- [x] Score increases while alive and appears on game over
- [ ] Code reviewed with LLM (include chat link)
