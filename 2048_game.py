import os
import random


def initialize_game():
    grid = [[0] * 4 for _ in range(4)]
    place_random_tile(grid)
    place_random_tile(grid)
    return grid


def place_random_tile(grid):
    empty_cells = [(r, c) for r in range(4) for c in range(4) if grid[r][c] == 0]
    if empty_cells:
        r, c = random.choice(empty_cells)
        grid[r][c] = 2 if random.random() < 0.9 else 4


def slide(row):
    new_row = [num for num in row if num != 0]  # Remove zeroes
    while len(new_row) < 4:
        new_row.append(0)  # Fill with zeroes
    return new_row


def merge(row):
    for i in range(3):
        if row[i] == row[i + 1] and row[i] != 0:
            row[i] *= 2
            row[i + 1] = 0
    return row


def move(grid, direction):
    if direction == "LEFT":
        for r in range(4):
            grid[r] = slide(merge(slide(grid[r])))
    elif direction == "RIGHT":
        for r in range(4):
            grid[r] = list(reversed(slide(merge(slide(reversed(grid[r]))))))
    elif direction == "UP":
        for c in range(4):
            col = [grid[r][c] for r in range(4)]
            col = slide(merge(slide(col)))
            for r in range(4):
                grid[r][c] = col[r]
    elif direction == "DOWN":
        for c in range(4):
            col = [grid[r][c] for r in range(4)]
            col = list(reversed(slide(merge(slide(reversed(col))))))
            for r in range(4):
                grid[r][c] = col[r]


def check_win(grid):
    return any(2048 in row for row in grid)


def check_game_over(grid):
    if any(0 in row for row in grid):
        return False  # There are empty spaces
    for r in range(4):
        for c in range(3):
            if grid[r][c] == grid[r][c + 1]:
                return False  # Merge possible horizontally
    for c in range(4):
        for r in range(3):
            if grid[r][c] == grid[r + 1][c]:
                return False  # Merge possible vertically
    return True  # No moves left


def display(grid):
    os.system("cls" if os.name == "nt" else "clear")
    for row in grid:
        print("\t".join(str(num) if num != 0 else "." for num in row))
    print()


def main():
    grid = initialize_game()
    while True:
        display(grid)
        if check_win(grid):
            print("You win!")
            break
        if check_game_over(grid):
            print("Game Over!")
            break
        direction = input("Enter move (LEFT, RIGHT, UP, DOWN): ").strip().upper()
        if direction in ["LEFT", "RIGHT", "UP", "DOWN"]:
            old_grid = [row[:] for row in grid]  # Copy grid before move
            move(grid, direction)
            if old_grid != grid:
                place_random_tile(grid)
        else:
            print("Invalid input! Use LEFT, RIGHT, UP, or DOWN.")


if __name__ == "__main__":
    main()
