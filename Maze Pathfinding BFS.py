import numpy as np
import matplotlib.pyplot as plt
import random
from collections import deque

# Generate a random maze (without start/goal restrictions)
def generate_maze(size=10, wall_prob=0.2):
    maze = np.zeros((size, size), dtype=int)
    for i in range(size):
        for j in range(size):
            if random.random() < wall_prob:
                maze[i][j] = 1  # Wall
    return maze


def bfs(maze, start, goal):
    size = len(maze)
    queue = deque([(start, [start])])
    visited = set([start])
    moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    while queue:
        (x, y), path = queue.popleft()
        if (x, y) == goal:
            return path  

        for dx, dy in moves:
            nx, ny = x + dx, y + dy
            if 0 <= nx < size and 0 <= ny < size and maze[nx][ny] == 0 and (nx, ny) not in visited:
                queue.append(((nx, ny), path + [(nx, ny)]))
                visited.add((nx, ny))
    return None  

# Plot the maze (without path initially)
def plot_maze(maze, start=None, goal=None, path=None):
    size = len(maze)
    fig, ax = plt.subplots(figsize=(8, 8))

   
    for i in range(size):
        for j in range(size):
            color = "black" if maze[i, j] == 1 else "white"
            ax.add_patch(plt.Rectangle((j, i), 1, 1, color=color, ec="gray", lw=1))

    
    if path:
        
        px = [x + 0.5 for (x, y) in path]
        py = [y + 0.5 for (x, y) in path]
        ax.plot(py, px, color="red", linestyle="-", lw=3, label="Path")

  
    if start:
        ax.scatter(start[1] + 0.5, start[0] + 0.5, color="gold", marker="*", s=200, 
                   edgecolors="black", linewidth=1.5, label="Start")
        ax.text(start[1] + 0.5, start[0] - 0.2, "Start", fontsize=12, ha="center", va="top", color="black")
    if goal:
        ax.scatter(goal[1] + 0.5, goal[0] + 0.5, color="blue", marker="P", s=200, 
                   edgecolors="black", linewidth=1.5, label="Goal")
        ax.text(goal[1] + 0.5, goal[0] + 1.2, "Goal", fontsize=12, ha="center", va="bottom", color="black")

    ax.set_xlim(0, size)
    ax.set_ylim(0, size)
    ax.set_xticks(range(size))
    ax.set_yticks(range(size))
    ax.grid(True, color="lightgray", linestyle="--", linewidth=0.5)
    ax.set_aspect("equal")
    plt.legend()
    plt.show()


def get_valid_coordinate(maze, prompt):
    size = len(maze)
    while True:
        try:
            y, x = map(int, input(prompt).split())
            if 0 <= x < size and 0 <= y < size:
                if maze[x][y] == 0:
                    return (x, y)
                else:
                    print("Error: That position is a wall. Try again.")
            else:
                print(f"Error: Coordinates must be between 0 and {size-1}. Try again.")
        except ValueError:
            print("Error: Please enter two integers separated by a space (e.g., '3 5').")


def main():
    
    maze_size = int(input("Enter maze size (e.g., 10 for 10x10): "))
    wall_density = float(input("Enter wall density (0.1 to 0.4 recommended): "))
    
    
    maze = generate_maze(maze_size, wall_density)
    print("\nGenerated Maze (Black = Wall, White = Pathable)")
    plot_maze(maze)
    
    
    print("\nEnter coordinates (row column) between 0 and", maze_size-1)
    start = get_valid_coordinate(maze, "Enter start position (e.g., '0 0'): ")
    goal = get_valid_coordinate(maze, "Enter goal position (e.g., '9 9'): ")
    
   
    shortest_path = bfs(maze, start, goal)
    if shortest_path:
        print("\nPath found! Displaying maze with solution...")
        plot_maze(maze, start, goal, shortest_path)
    else:
        print("\nNo path exists between start and goal!")
        plot_maze(maze, start, goal) 

if __name__ == "__main__":
    main()