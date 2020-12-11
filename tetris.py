# -*- coding:utf-8 -*-
import tkinter as tk
import random
from enum import Enum, auto

FIELD_WIDTH = 10
FIELD_HEIGHT = 20
SQUARE_SIZE = 25


class MoveCmd(Enum):
    LEFT = 0
    RIGHT = auto()
    DOWN = auto()


class BlockType(Enum):
    I = 0
    J = auto()
    L = auto()
    O = auto()
    S = auto()
    T = auto()
    Z = auto()


class TetrisSquare():
    def __init__(self, x=0, y=0, color="gray"):
        self.x = x
        self.y = y
        self.color = color

    def set_pos(self, x, y):
        self.x = x
        self.y = y

    def get_pos(self):
        return int(self.x), int(self.y)

    def set_color(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def get_moved_pos(self, direction):
        x, y = self.get_pos()

        if direction == MoveCmd.LEFT:
            return x-1, y
        elif direction == MoveCmd.RIGHT:
            return x+1, y
        elif direction == MoveCmd.DOWN:
            return x, y+1
        else:
            return x, y


class TetrisBlock():
    def __init__(self):
        self.squares = []

        block_type = random.choice(list(BlockType))

        if block_type == BlockType.I:
            color = "cyan"
            poss = [
                [FIELD_WIDTH / 2, 0],
                [FIELD_WIDTH / 2, 1],
                [FIELD_WIDTH / 2, 2],
                [FIELD_WIDTH / 2, 3],
            ]
        elif block_type == BlockType.J:
            color = "blue"
            poss = [
                [FIELD_WIDTH / 2, 0],
                [FIELD_WIDTH / 2, 1],
                [FIELD_WIDTH / 2, 2],
                [FIELD_WIDTH / 2 - 1, 2],
            ]
        elif block_type == BlockType.L:
            color = "orange"
            poss = [
                [FIELD_WIDTH / 2 - 1, 0],
                [FIELD_WIDTH / 2 - 1, 1],
                [FIELD_WIDTH / 2 - 1, 2],
                [FIELD_WIDTH / 2, 2],
            ]
        elif block_type == BlockType.O:
            color = "yellow"
            poss = [
                [FIELD_WIDTH / 2, 0],
                [FIELD_WIDTH / 2, 1],
                [FIELD_WIDTH / 2 - 1, 0],
                [FIELD_WIDTH / 2 - 1, 1],
            ]
        elif block_type == BlockType.S:
            color = "green"
            poss = [
                [FIELD_WIDTH / 2 + 1, 0],
                [FIELD_WIDTH / 2, 0],
                [FIELD_WIDTH / 2, 1],
                [FIELD_WIDTH / 2 - 1, 1],
            ]
        elif block_type == BlockType.T:
            color = "purple"
            poss = [
                [FIELD_WIDTH / 2, 0],
                [FIELD_WIDTH / 2 - 1, 1],
                [FIELD_WIDTH / 2, 1],
                [FIELD_WIDTH / 2 + 1, 1],
            ]
        elif block_type == BlockType.Z:
            color = "red"
            poss = [
                [FIELD_WIDTH / 2 - 1, 0],
                [FIELD_WIDTH / 2, 0],
                [FIELD_WIDTH / 2, 1],
                [FIELD_WIDTH / 2 + 1, 1],
            ]

        for pos in poss:
            self.squares.append(TetrisSquare(pos[0], pos[1], color))

    def get_squares(self):
        return self.squares

    def move(self, direction):
        for square in self.squares:
            x, y = square.get_moved_pos(direction)
            square.set_pos(x, y)


class TetrisField():
    def __init__(self):
        self.width = FIELD_WIDTH
        self.height = FIELD_HEIGHT

        self.squares = []
        for y in range(self.height):
            for x in range(self.width):
                self.squares.append(TetrisSquare(x, y, "gray"))

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_squares(self):
        return self.squares

    def get_square(self, x, y):
        return self.squares[y * self.width + x]

    def is_game_over(self, block):
        not_empty_pos = set(square.get_pos() for square in self.get_squares() if square.get_color() != "gray")
        block_pos = set(square.get_pos() for square in block.get_squares())

        collision_set = not_empty_pos & block_pos
        if  len(collision_set) == 0:
            ret = False
        else:
            ret = True
        
        return ret
    
    def can_move(self, block, direction):
        not_empty_pos = set(square.get_pos() for square in self.get_squares() if square.get_color() != "gray")
        move_block_pos = set(square.get_moved_pos(direction) for square in block.get_squares())

        for x, y in move_block_pos:
            if x < 0 or x >= self.width or y < 0 or y >= self.height:
                return False

        collision_set = not_empty_pos & move_block_pos

        if len(collision_set) == 0:
            ret = True
        else:
            ret = False

        return ret

    def fix_block(self, block):
        for square in block.get_squares():
            x, y = square.get_pos()
            color = square.get_color()

            field_square = self.get_square(x, y)
            field_square.set_color(color)

    def delete_line(self):
        for y in range(self.height):
            for x in range(self.width):
                square = self.get_square(x, y)
                if square.get_color() == "gray":
                    break
            else:
                for down_y in range(y, 0, -1):
                    for x in range(self.width):
                        src_square = self.get_square(x, down_y - 1)
                        dst_square = self.get_square(x, down_y)
                        dst_square.set_color(src_square.get_color())
                for x in range(self.width):
                    square = self.get_square(x, 0)
                    square.set_color("gray")


class TetrisCanvas(tk.Canvas):
    def __init__(self, master, field):
        canvas_width = field.get_width() * SQUARE_SIZE
        canvas_height = field.get_height() * SQUARE_SIZE

        super().__init__(master, width=canvas_width, height=canvas_height, bg="white")

        self.place(x=25, y=25)

        for y in range(field.get_height()):
            for x in range(field.get_width()):
                square = field.get_square(x, y)
                x1 = x * SQUARE_SIZE
                x2 = (x + 1) * SQUARE_SIZE
                y1 = y * SQUARE_SIZE
                y2 = (y + 1) * SQUARE_SIZE
                self.create_rectangle(
                    x1, y1, x2, y2,
                    outline="white",
                    width=1,
                    fill="gray"
                )

        self.before_field = field

    def update(self, field, block):
        new_field = TetrisField()
 
        for y in range(field.get_height()):
            for x in range(field.get_width()):
                color = field.get_square(x, y).get_color()
                new_field.get_square(x, y).set_color(color)

        if block is not None:
            block_squares = block.get_squares()
            for block_square in block_squares:
                x, y = block_square.get_pos()
                color = block_square.get_color()
                new_field.get_square(x, y).set_color(color)

        for y in range(field.get_height()):
            for x in range(field.get_width()):
                new_color = new_field.get_square(x, y).get_color()
                before_color = self.before_field.get_square(x, y).get_color()
                if(new_color == before_color):
                    continue

                x1 = x * SQUARE_SIZE
                x2 = (x + 1) * SQUARE_SIZE
                y1 = y * SQUARE_SIZE
                y2 = (y + 1) * SQUARE_SIZE
                self.create_rectangle(
                    x1, y1, x2, y2,
                    outline="white", width=1, fill=new_color
                )

        self.before_field = new_field


class TetrisGame():
    def __init__(self, master):
        self.field = TetrisField()
        self.block = None
        
        self.canvas = TetrisCanvas(master, self.field)
        self.canvas.update(self.field, self.block)

    def start(self, func):
        self.end_func = func

        self.field = TetrisField()
        self.new_block()

    def new_block(self):
        self.block = TetrisBlock()

        if self.field.is_game_over(self.block):
            self.end_func()
            print("GAMEOVER")

        self.canvas.update(self.field, self.block)

    def move_block(self, direction):
        if self.field.can_move(self.block, direction):
            self.block.move(direction)
            self.canvas.update(self.field, self.block)
        else:
            if direction == MoveCmd.DOWN:
                self.field.fix_block(self.block)
                self.field.delete_line()
                self.new_block()


class EventHandller():
    def __init__(self, master, game):
        self.master = master
        self.game = game

        self.running = False
        self.timer = None

        # start button
        button = tk.Button(master, text='START', command=self.start_event)
        button.place(x=25 + SQUARE_SIZE * FIELD_WIDTH + 25, y=30)

    def start_event(self):
        self.master.bind("<Left>", self.left_key_event)
        self.master.bind("<Right>", self.right_key_event)
        self.master.bind("<Down>", self.down_key_event)

        self.running = True
        self.timer_start()

        self.game.start(self.end_event)

    def end_event(self):
        self.master.unbind("<Left>")
        self.master.unbind("<Right>")
        self.master.unbind("<Down>")

        self.running = False
        self.timer_end()

    def left_key_event(self, event):
        self.game.move_block(MoveCmd.LEFT)

    def right_key_event(self, event):
        self.game.move_block(MoveCmd.RIGHT)

    def down_key_event(self, event):
        self.game.move_block(MoveCmd.DOWN)
        self.timer_start()

    def timer_start(self):
        if self.timer is not None:
            self.master.after_cancel(self.timer)

        if self.running:
            self.timer = self.master.after(1000, self.timer_event)

    def timer_end(self):
        if self.timer is not None:
            self.master.after_cancel(self.timer)
            self.timer = None

    def timer_event(self):
        self.down_key_event(None)


class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry("400x600")
        self.title("Tetris")

        game = TetrisGame(self)

        EventHandller(self, game)


def main():
    app = Application()
    app.mainloop()


if __name__ == '__main__':
    main()
