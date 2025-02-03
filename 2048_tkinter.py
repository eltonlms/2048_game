import random
from tkinter import Button, Frame, Label, Tk, Toplevel


class Game2048:
    def __init__(self, master):
        self.master = master
        self.master.title("2048 Game")
        self.grid = [[0] * 4 for _ in range(4)]
        self.init_ui()
        self.place_random_tile()
        self.place_random_tile()
        self.update_ui()
        self.master.bind("<Left>", lambda event: self.handle_move("LEFT"))
        self.master.bind("<Right>", lambda event: self.handle_move("RIGHT"))
        self.master.bind("<Up>", lambda event: self.handle_move("UP"))
        self.master.bind("<Down>", lambda event: self.handle_move("DOWN"))

    def init_ui(self):
        self.cells = []
        self.frame = Frame(self.master, bg="gray")
        self.frame.grid()
        for r in range(4):
            row = []
            for c in range(4):
                label = Label(
                    self.frame,
                    text="",
                    width=4,
                    height=2,
                    font=("Arial", 24),
                    fg="white",
                    relief="ridge",
                )
                label.grid(row=r, column=c, padx=5, pady=5)
                row.append(label)
            self.cells.append(row)

    def update_ui(self):
        for r in range(4):
            for c in range(4):
                value = self.grid[r][c]
                self.cells[r][c].config(
                    text=str(value) if value else "",
                    bg="lightblue" if value else "lightgreen",
                )

    def place_random_tile(self):
        empty_cells = [(r, c) for r in range(4) for c in range(4) if self.grid[r][c] == 0]
        if empty_cells:
            r, c = random.choice(empty_cells)
            self.grid[r][c] = 2 if random.random() < 0.9 else 4

    def slide(self, row):
        new_row = [num for num in row if num != 0]
        while len(new_row) < 4:
            new_row.append(0)
        return new_row

    def merge(self, row):
        for i in range(3):
            if row[i] == row[i + 1] and row[i] != 0:
                row[i] *= 2
                row[i + 1] = 0
        return row

    def move(self, direction):
        if direction == "LEFT":
            for r in range(4):
                self.grid[r] = self.slide(self.merge(self.slide(self.grid[r])))
        elif direction == "RIGHT":
            for r in range(4):
                self.grid[r] = list(reversed(self.slide(self.merge(self.slide(reversed(self.grid[r]))))))
        elif direction == "UP":
            for c in range(4):
                col = [self.grid[r][c] for r in range(4)]
                col = self.slide(self.merge(self.slide(col)))
                for r in range(4):
                    self.grid[r][c] = col[r]
        elif direction == "DOWN":
            for c in range(4):
                col = [self.grid[r][c] for r in range(4)]
                col = list(reversed(self.slide(self.merge(self.slide(reversed(col))))))
                for r in range(4):
                    self.grid[r][c] = col[r]

    def handle_move(self, direction):
        old_grid = [row[:] for row in self.grid]
        self.move(direction)
        if old_grid != self.grid:
            self.place_random_tile()
            self.update_ui()
        if self.check_win():
            self.show_message("You win!")
        elif self.check_game_over():
            self.show_message("Game Over!")

    def check_win(self):
        return any(2048 in row for row in self.grid)

    def check_game_over(self):
        if any(0 in row for row in self.grid):
            return False
        for r in range(4):
            for c in range(3):
                if self.grid[r][c] == self.grid[r][c + 1]:
                    return False
        for c in range(4):
            for r in range(3):
                if self.grid[r][c] == self.grid[r + 1][c]:
                    return False
        return True

    def show_message(self, message):
        popup = Toplevel(self.master)
        popup.title("Game Over")
        label = Label(popup, text=message, font=("Arial", 16))
        label.pack(pady=10)
        button = Button(popup, text="OK", command=self.master.quit)
        button.pack(pady=5)


if __name__ == "__main__":
    root = Tk()
    game = Game2048(root)
    root.mainloop()
