import tkinter as tk
from tkinter import font
import random

class MineGrid(object):

    FLAG_CHAR = u"\u2691"
    MAYBE_CHAR = "?"
    MINE_CHAR = u"\u2739"
    NOMINE_CHAR = "X"
    NEIGHBOURS_OFFSETS = (
        (1, 0),
        (1, -1),
        (0, -1),
        (-1, -1),
        (-1, 0),
        (-1, 1),
        (0, 1),
        (1, 1)
        )
    BASE_CLR = "#dcedf2"
    PRESSED_CLR = "#efefff"
    MARKED_CLR = "#90c0e0"
    MINE_CLR = "#ffac1c"
    MINEPRESS_CLR = "#ff5330"
    CORRECT_CLR = "#67e843"

    def __init__(self, root, width, height, mines):
        self.root = root
        self.width = width
        self.height = height
        self.mines = mines

        n = width * height
        self.mine_slots = [False for _ in range(n)]
        self.pressed = [False for _ in range(n)]
        self.mark_slots = ["" for _ in range(n)]
        self.buttons = list(range(n))
        
        self.outer_frame = tk.Frame(root)
        self.outer_frame.pack()

        for i in range(width):
            for j in range(height):
                btn = tk.Label(
                    self.outer_frame, text="",
                    relief=tk.RAISED,
                    width=2, height=1,
                    jus="center",
                    padx=0, pady=0,
                    font=font.Font(root, font=("Arial", 16)),
                    bg=self.BASE_CLR)

                handle_m1_event = lambda _, x=i, y=j: self.left_click(x, y)
                handle_m2_event = lambda _, x=i, y=j: self.right_click(x, y)
                btn.bind("<ButtonRelease-1>", handle_m1_event, add=False)
                btn.bind("<ButtonRelease-3>", handle_m2_event, add=False)

                btn.grid(column=i, row=j)
                
                idx = self.to_idx(i, j)
                self.buttons[idx] = btn

        idx_list = list(range(n))
        random.shuffle(idx_list)
        for mine_num, idx in enumerate(idx_list):
            if mine_num > mines:
                break
            self.mine_slots[idx] = True

    def left_click(self, i, j):
        mine = self.press(i, j)
        complete = self.check_complete()
        if mine or complete:
            self.end()

    def right_click(self, i, j):
        self.mark(i, j)  
        complete = self.check_complete()
        if complete:
            self.end()

    def check_complete(self):
        for pressed, mark in zip(self.pressed, self.mark_slots):
            if pressed or mark == self.FLAG_CHAR:
                continue
            else:
                return False
        return True

    def count_mine_neighbours(self, i, j):
        neighbours = 0
        for i_off, j_off in self.NEIGHBOURS_OFFSETS:
            i_neighb = i + i_off
            j_neighb = j + j_off
            if self.in_bounds(i_neighb, j_neighb):
                if self.mine_slots[self.to_idx(i_neighb, j_neighb)]:
                    neighbours += 1
        return neighbours

    def press_neighbours(self, i, j):
        for i_off, j_off in self.NEIGHBOURS_OFFSETS:
            i_neighb = i + i_off
            j_neighb = j + j_off
            if self.in_bounds(i_neighb, j_neighb):
                if not self.pressed[self.to_idx(i_neighb, j_neighb)]:
                    self.press(i_neighb, j_neighb)

    def end(self):
        win = True
        for btn, mine, pressed, mark in zip(self.buttons, self.mine_slots, self.pressed, self.mark_slots):
            btn.bind("<ButtonRelease-1>", lambda _: None)
            btn.bind("<ButtonRelease-3>", lambda _: None)
            if mine:
                flag = mark == self.FLAG_CHAR
                if not flag:
                    win = False
                btn.config(text=self.MINE_CHAR)
                if pressed:
                    continue
                btn.config(bg=self.CORRECT_CLR if flag else self.MINE_CLR)
        
        popup = tk.Toplevel()
        popup.wm_title("Minesweeper.py")
        popup.geometry("200x100")
        l = tk.Label(popup, text="You win!" if win else "You lose!")
        l.pack(fill=tk.BOTH, expand=1)
        b = tk.Button(popup, text="OK", command=popup.destroy)
        b.pack(fill=tk.BOTH, expand=1)

    def to_idx(self, i, j):
        return i * self.width + j

    def in_bounds(self, i, j):
        return i >= 0 and i < self.width and j >= 0 and j < self.height

    def press(self, i, j):
        idx = self.to_idx(i, j)
        self.pressed[idx] = True

        btn = self.buttons[idx]
        mine = self.mine_slots[idx]
        if mine:
            btn.config(bg=self.MINEPRESS_CLR)
            print("Boom!")
            return True
        
        neighbours = self.count_mine_neighbours(i, j)
        btn.bind("<ButtonRelease-1>", lambda _: None)
        btn.bind("<ButtonRelease-3>", lambda _: None)
        btn.config(
            text=str(neighbours) if neighbours > 0 else "",
            relief=tk.SUNKEN,
            bg=self.PRESSED_CLR
            )
        if neighbours == 0:
            self.press_neighbours(i, j)
        return False

    def mark(self, i, j):
        idx = self.to_idx(i, j)
        current_mark = self.mark_slots[idx]
        
        if current_mark == "":
            new_mark = self.FLAG_CHAR
        elif current_mark == self.FLAG_CHAR: 
            new_mark = self.MAYBE_CHAR
        else:
            new_mark = ""

        self.mark_slots[idx] = new_mark
        btn = self.buttons[idx]
        btn.config(
            text=new_mark,
            bg=self.BASE_CLR if new_mark == "" else self.MARKED_CLR
        )  

    def restart(self):
        self.outer_frame.destroy()
        self.__init__(self.root, self.width, self.height, self.mines)


def start(width, height, n_mines):
    root = tk.Tk()
    root.wm_title("Minespeeper.py")
    restart_btn = tk.Button(root, text="Restart")
    restart_btn.pack(fill=tk.BOTH, expand=1)
    minegrid = MineGrid(root, width, height, n_mines)
    restart_btn.config(command=minegrid.restart)
    root.mainloop()


if __name__ == "__main__":
    start(8, 8, 12)
