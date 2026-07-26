import random
import time
from collections import deque


class GridEnvironment:


    def __init__(self, width=10, height=8, wall_prob=0.2, seed=None):
        self.width = width
        self.height = height
        if seed is not None:
            random.seed(seed)


        self.grid = [
            [1 if random.random() < wall_prob else 0 for _ in range(width)]
            for _ in range(height)
        ]

    def is_valid(self, pos):
        x, y = pos
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x] == 0
        return False

    def get_neighbors(self, pos):

        x, y = pos
        candidates = [(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)]
        return [c for c in candidates if self.is_valid(c)]

    def ensure_path_cells(self, *cells):

        for (x, y) in cells:
            self.grid[y][x] = 0

    def is_reachable(self, start, goal):

        seen = {start}
        queue = deque([start])
        while queue:
            pos = queue.popleft()
            if pos == goal:
                return True
            for n in self.get_neighbors(pos):
                if n not in seen:
                    seen.add(n)
                    queue.append(n)
        return False


class BlindDog:

    def __init__(self, env: GridEnvironment, start, goal):
        self.env = env
        self.start = start
        self.goal = goal
        self.current = start

        self.visited = set()          
        self.path_stack = [start]     
        self.full_history = [start]   
        self.steps = 0
        self.backtracks = 0

    def choose_next(self, unvisited_neighbors):
   
        def dist_to_goal(p):
            return abs(p[0] - self.goal[0]) + abs(p[1] - self.goal[1])

        min_dist = min(dist_to_goal(p) for p in unvisited_neighbors)
        best = [p for p in unvisited_neighbors if dist_to_goal(p) == min_dist]
        return random.choice(best)

    def step(self):

        self.visited.add(self.current)

        if self.current == self.goal:
            return "GOAL"

        neighbors = self.env.get_neighbors(self.current)
        unvisited = [n for n in neighbors if n not in self.visited]

        if unvisited:
            next_pos = self.choose_next(unvisited)
            self.path_stack.append(next_pos)
            self.current = next_pos
            self.full_history.append(next_pos)
            self.steps += 1
            return "MOVE"
        else:
  
            if len(self.path_stack) <= 1:
                return "STUCK"  
            self.path_stack.pop()
            self.current = self.path_stack[-1]
            self.full_history.append(self.current)
            self.backtracks += 1
            self.steps += 1
            return "BACKTRACK"

    def run(self, max_steps=2000, verbose=True):
        result = "MOVE"
        while result not in ("GOAL", "STUCK") and self.steps < max_steps:
            result = self.step()
            if verbose:
                print(f"Step {self.steps:4d} | action: {result:9s} | pos: {self.current}")

        if result == "GOAL":
            print(f"\n🐶 ถึงเป้าหมายแล้ว! ใช้ทั้งหมด {self.steps} steps "
                  f"({self.backtracks} ครั้งที่ backtrack)")
        elif result == "STUCK":
            print(f"\n🚧 สำรวจครบทุกช่องที่เดินได้แล้ว แต่ไปไม่ถึงเป้าหมาย "
                  f"(ใช้ {self.steps} steps)")
        else:
            print(f"\n⏱️ ครบ max_steps ({max_steps}) ก่อนเจอคำตอบ")

        return result


def print_grid(env: GridEnvironment, dog: BlindDog):
  
    for y in range(env.height):
        row = ""
        for x in range(env.width):
            pos = (x, y)
            if env.grid[y][x] == 1:
                row += "# "
            elif pos == dog.current:
                row += "D "
            elif pos == dog.goal:
                row += "G "
            elif pos in dog.visited:
                row += "* "
            else:
                row += ". "
        print(row)
    print()


def animate_run(env: GridEnvironment, dog: BlindDog, delay=0.15, max_steps=2000):

    import os

    result = "MOVE"
    while result not in ("GOAL", "STUCK") and dog.steps < max_steps:
        os.system("cls" if os.name == "nt" else "clear")
        print(f"Step: {dog.steps} | Backtracks: {dog.backtracks}\n")
        print_grid(env, dog)
        result = dog.step()
        time.sleep(delay)

    os.system("cls" if os.name == "nt" else "clear")
    print_grid(env, dog)
    if result == "GOAL":
        print(f"🐶 ถึงเป้าหมายแล้ว! ใช้ {dog.steps} steps ({dog.backtracks} backtracks)")
    elif result == "STUCK":
        print(f"🚧 สำรวจครบทุกช่องแล้ว แต่ไปไม่ถึงเป้าหมาย ({dog.steps} steps)")


if __name__ == "__main__":
    WIDTH, HEIGHT = 12, 10
    START = (0, 0)
    GOAL = (WIDTH - 1, HEIGHT - 1)

    seed = 42
    env = GridEnvironment(width=WIDTH, height=HEIGHT, wall_prob=0.22, seed=seed)
    env.ensure_path_cells(START, GOAL)

    while not env.is_reachable(START, GOAL):
        seed += 1
        env = GridEnvironment(width=WIDTH, height=HEIGHT, wall_prob=0.22, seed=seed)
        env.ensure_path_cells(START, GOAL)

    dog = BlindDog(env, start=START, goal=GOAL)

    print("=== Smart BlindDog ===")
    print(f"Grid size: {WIDTH} x {HEIGHT} | Start: {START} | Goal: {GOAL}\n")


    dog.run(verbose=True)
    print("\n--- แผนที่สุดท้าย ---")
    print_grid(env, dog)
