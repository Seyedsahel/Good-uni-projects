import tkinter as tk
from tkinter import messagebox
import time
import heapq

class Puzzle:
    def __init__(self, board, parent=None, move="", depth=0):
        self.board = board
        self.parent = parent
        self.move = move
        self.depth = depth
        self.cost = self.depth + self.manhattan_distance()

    def manhattan_distance(self):
        distance = 0
        for i in range(3):
            for j in range(3):
                if self.board[i][j] != 0:
                    target_x = (self.board[i][j] - 1) // 3
                    target_y = (self.board[i][j] - 1) % 3
                    distance += abs(i - target_x) + abs(j - target_y)
        return distance

    def is_goal(self):
        goal = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
        return self.board == goal

    def generate_children(self):
        children = []
        x, y = [(i, row.index(0)) for i, row in enumerate(self.board) if 0 in row][0]
        directions = [(0, -1, "Left"), (0, 1, "Right"), (-1, 0, "Up"), (1, 0, "Down")]

        for dx, dy, move in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 3 and 0 <= ny < 3:
                new_board = [row[:] for row in self.board]
                new_board[x][y], new_board[nx][ny] = new_board[nx][ny], new_board[x][y]
                children.append(Puzzle(new_board, self, move, self.depth + 1))

        return children

    def __lt__(self, other):
        return self.cost < other.cost


def branch_and_bound(initial):
    open_set = []
    heapq.heappush(open_set, Puzzle(initial))
    closed_set = set()

    while open_set:
        current = heapq.heappop(open_set)

        if current.is_goal():
            path = []
            while current.parent:
                path.append(current.move)
                current = current.parent
            return path[::-1]

        closed_set.add(tuple(tuple(row) for row in current.board))

        for child in current.generate_children():
            if tuple(tuple(row) for row in child.board) not in closed_set:
                heapq.heappush(open_set, child)

    return None


class PuzzleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("8 Puzzle Game")

        self.frame = tk.Frame(self.root)
        self.frame.pack()

        self.board = [[3, 4, 5], [2, 7, 6], [1, 8, 0]]
        self.buttons = []
        self.create_board()

        self.mode_var = tk.StringVar(value="Manual")
        self.delay_var = tk.DoubleVar(value=0.5)

        self.create_controls()

    def create_board(self):
        for i in range(3):
            row = []
            for j in range(3):
                button = tk.Button(self.frame, text=str(self.board[i][j]) if self.board[i][j] != 0 else "", 
                                    font=("Helvetica", 20), height=2, width=4, 
                                    command=lambda x=i, y=j: self.manual_move(x, y))
                button.grid(row=i, column=j)
                row.append(button)
            self.buttons.append(row)

    def update_board(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text=str(self.board[i][j]) if self.board[i][j] != 0 else "")

    def create_controls(self):
        controls = tk.Frame(self.root)
        controls.pack()

        tk.Label(controls, text="Mode:").grid(row=0, column=0)
        tk.Radiobutton(controls, text="Manual", variable=self.mode_var, value="Manual").grid(row=0, column=1)
        tk.Radiobutton(controls, text="Auto", variable=self.mode_var, value="Auto").grid(row=0, column=2)

        tk.Label(controls, text="Delay (s):").grid(row=1, column=0)
        tk.Entry(controls, textvariable=self.delay_var, width=5).grid(row=1, column=1)

        tk.Button(controls, text="Start", command=self.start_game).grid(row=1, column=2)

    def manual_move(self, x, y):
        if self.mode_var.get() == "Manual":
            zero_x, zero_y = [(i, row.index(0)) for i, row in enumerate(self.board) if 0 in row][0]
            if abs(zero_x - x) + abs(zero_y - y) == 1:
                self.board[zero_x][zero_y], self.board[x][y] = self.board[x][y], self.board[zero_x][zero_y]
                self.update_board()

                if self.check_win():
                    messagebox.showinfo("Congratulations", "You solved the puzzle!")

    def check_win(self):
        return self.board == [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

    def start_game(self):
        if self.mode_var.get() == "Auto":
            self.auto_solve()

    def auto_solve(self):
        initial = [row[:] for row in self.board]
        solution = branch_and_bound(initial)

        if solution:
            for move in solution:
                self.make_move(move)
                time.sleep(self.delay_var.get())
                self.update_board()
                self.root.update()

            messagebox.showinfo("Done", "Puzzle solved automatically!")
        else:
            messagebox.showerror("Error", "No solution found!")

    def make_move(self, move):
        zero_x, zero_y = [(i, row.index(0)) for i, row in enumerate(self.board) if 0 in row][0]
        if move == "Up":
            self.board[zero_x][zero_y], self.board[zero_x - 1][zero_y] = self.board[zero_x - 1][zero_y], self.board[zero_x][zero_y]
        elif move == "Down":
            self.board[zero_x][zero_y], self.board[zero_x + 1][zero_y] = self.board[zero_x + 1][zero_y], self.board[zero_x][zero_y]
        elif move == "Left":
            self.board[zero_x][zero_y], self.board[zero_x][zero_y - 1] = self.board[zero_x][zero_y - 1], self.board[zero_x][zero_y]
        elif move == "Right":
            self.board[zero_x][zero_y], self.board[zero_x][zero_y + 1] = self.board[zero_x][zero_y + 1], self.board[zero_x][zero_y]

if __name__ == "__main__":
    root = tk.Tk()
    gui = PuzzleGUI(root)
    root.mainloop()
