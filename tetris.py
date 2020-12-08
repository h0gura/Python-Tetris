# -*- coding:utf-8 -*-
import tkinter as tk
import random

BLOCK_SIZE = 25
FIELD_WIDTH = 10
FIELD_HEIGHT = 20

MOVE_LEFT = 0
MOVE_RIGHT = 1
MOVE_DOWN = 2



class TetrisGame():
    def __init__(self):
        self.field = TetrisField()

        self.block = None

        self.canvas = TetrisCanvas()

        self.canvas.update(self.field, self.block)



class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry("400x600")
        self.title("Tetris")

        game = TetrisGame()




def main():
    app = Application()
    app.mainloop()


if __name__ == '__main__':
    main()
