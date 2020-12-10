# -*- coding:utf-8 -*-
import tkinter as tk
import random

BLOCK_SIZE = 25
FIELD_WIDTH = 10
FIELD_HEIGHT = 20

MOVE_LEFT = 0
MOVE_RIGHT = 1
MOVE_DOWN = 2


class TetrisSquare():
    def __init__(self, x=0, y=0, color="gray"):
        self.x = x
        self.y = y
        self.color = color

    def set_cord(self, x, y):
        self.x = x
        self.y = y

    def get_cord(self):
        return int(self.x), int(self.y)

    def set_color(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def get_moved_cord(self, direction):
        x, y = self.get_cord()

        if direction == MOVE_LEFT:
            return x-1, y
        elif direction == MOVE_RIGHT:
            return x+1, y
        elif direction == MOVE_DOWN:
            return x, y+1
        else:
            return x, y


class TetrisCanvas(tk.Canvas):
    def __init__(self, master, field):
        canvas_width = field.get_width() * BLOCK_SIZE
        canvas_height = field.get_height() * BLOCK_SIZE

        super().__init__(master, width=canvas_width, height=canvas_height, bg="white")

        self.place(x=25, y=25)

        for y in range(field.get_height()):
            for x in range(field.get_width()):
                square = field.get_square(x, y)
                x1 = x * BLOCK_SIZE
                x2 = (x + 1) * BLOCK_SIZE
                y1 = y * BLOCK_SIZE
                y2 = (y + 1) * BLOCK_SIZE
                self.create_rectangle(
                    x1, y1, x2, y2,
                    outline="white",
                    width=1,
                    fill=square.get_color()
                )

        self.before_field = field

    def update(self, field, block):
        'テトリス画面をアップデート'

        # 描画用のフィールド（フィールド＋ブロック）を作成
        new_field = TetrisField()
        for y in range(field.get_height()):
            for x in range(field.get_width()):
                square = field.get_square(x, y)
                color = square.get_color()

                new_square = new_field.get_square(x, y)
                new_square.set_color(color)

        # フィールドにブロックの正方形情報を合成
        if block is not None:
            block_squares = block.get_squares()
            for block_square in block_squares:
                # ブロックの正方形の座標と色を取得
                x, y = block_square.get_cord()
                color = block_square.get_color()

                # 取得した座標のフィールド上の正方形の色を更新
                new_field_square = new_field.get_square(x, y)
                new_field_square.set_color(color)

        # 描画用のフィールドを用いてキャンバスに描画
        for y in range(field.get_height()):
            for x in range(field.get_width()):

                # (x,y)座標のフィールドの色を取得
                new_square = new_field.get_square(x, y)
                new_color = new_square.get_color()

                # (x,y)座標が前回描画時から変化ない場合は描画しない
                before_square = self.before_field.get_square(x, y)
                before_color = before_square.get_color()
                if(new_color == before_color):
                    continue

                x1 = x * BLOCK_SIZE
                x2 = (x + 1) * BLOCK_SIZE
                y1 = y * BLOCK_SIZE
                y2 = (y + 1) * BLOCK_SIZE
                # フィールドの各位置の色で長方形描画
                self.create_rectangle(
                    x1, y1, x2, y2,
                    outline="white", width=1, fill=new_color
                )

        # 前回描画したフィールドの情報を更新
        self.before_field = new_field

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

    def judge_game_over(self, block):
        no_empty_cord = set(square.get_cord() for square in self.get_squares() 
                            if square.get_color() != "gray")

        block_cord = set(square.get_cord() for square in block.get_squares())

        collision_set = no_empty_cord & block_cord
        if  len(collision_set) == 0:
            ret = False
        else:
            ret = True
        
        return ret
    
    def judge_can_move(self, block, direction):
        no_empty_cord = set(square.get_cord() for square in self.get_squares() if square.get_color() != "gray")

        move_block_cord = set(square.get_moved_cord(direction) for square in block.get_squares())

        for x, y in move_block_cord:
            if x < 0 or x >= self.width or y < 0 or y >= self.height:
                return False

        collision_set = no_empty_cord & move_block_cord

        if len(collision_set) == 0:
            ret = True
        else:
            ret = False

        return ret

    def fix_block(self, block):
        'ブロックを固定してフィールドに追加'

        for square in block.get_squares():
            # ブロックに含まれる正方形の座標と色を取得
            x, y = square.get_cord()
            color = square.get_color()

            # その座標と色をフィールドに反映
            field_square = self.get_square(x, y)
            field_square.set_color(color)
    def delete_line(self):
        '行の削除を行う'

        # 全行に対して削除可能かどうかを調べていく
        for y in range(self.height):
            for x in range(self.width):
                # 行内に１つでも空があると消せない
                square = self.get_square(x, y)
                if(square.get_color() == "gray"):
                    # 次の行へ
                    break
            else:
                # break されなかった場合はその行は空きがない
                # この行を削除し、この行の上側にある行を１行下に移動
                for down_y in range(y, 0, -1):
                    for x in range(self.width):
                        src_square = self.get_square(x, down_y - 1)
                        dst_square = self.get_square(x, down_y)
                        dst_square.set_color(src_square.get_color())
                # 一番上の行は必ず全て空きになる
                for x in range(self.width):
                    square = self.get_square(x, 0)
                    square.set_color("gray")

class TetrisBlock():
    def __init__(self):
        'テトリスのブロックを作成'

        # ブロックを構成する正方形のリスト
        self.squares = []

        # ブロックの形をランダムに決定
        block_type = random.randint(1, 4)

        # ブロックの形に応じて４つの正方形の座標と色を決定
        if block_type == 1:
            color = "red"
            cords = [
                [FIELD_WIDTH / 2, 0],
                [FIELD_WIDTH / 2, 1],
                [FIELD_WIDTH / 2, 2],
                [FIELD_WIDTH / 2, 3],
            ]
        elif block_type == 2:
            color = "blue"
            cords = [
                [FIELD_WIDTH / 2, 0],
                [FIELD_WIDTH / 2, 1],
                [FIELD_WIDTH / 2 - 1, 0],
                [FIELD_WIDTH / 2 - 1, 1],
            ]
        elif block_type == 3:
            color = "green"
            cords = [
                [FIELD_WIDTH / 2 - 1, 0],
                [FIELD_WIDTH / 2, 0],
                [FIELD_WIDTH / 2, 1],
                [FIELD_WIDTH / 2, 2],
            ]
        elif block_type == 4:
            color = "orange"
            cords = [
                [FIELD_WIDTH / 2, 0],
                [FIELD_WIDTH / 2 - 1, 0],
                [FIELD_WIDTH / 2 - 1, 1],
                [FIELD_WIDTH / 2 - 1, 2],
            ]

        # 決定した色と座標の正方形を作成してリストに追加
        for cord in cords:
            self.squares.append(TetrisSquare(cord[0], cord[1], color))

    def get_squares(self):
        'ブロックを構成する正方形を取得'

        # return [square for square in self.squares]
        return self.squares

    def move(self, direction):
        'ブロックを移動'

        # ブロックを構成する正方形を移動
        for square in self.squares:
            x, y = square.get_moved_cord(direction)
            square.set_cord(x, y)


class TetrisGame():
    def __init__(self, master):
        """
        Create tetris game
        """
        self.field = TetrisField()
        self.block = None

        
        self.canvas = TetrisCanvas(master, self.field)

        # テトリス画面アップデート
        self.canvas.update(self.field, self.block)

    def start(self, func):
        'テトリスを開始'

        # 終了時に呼び出す関数をセット
        self.end_func = func

        # ブロック管理リストを初期化
        self.field = TetrisField()

        # 落下ブロックを新規追加
        self.new_block()

    def new_block(self):
        'ブロックを新規追加'

        # 落下中のブロックインスタンスを作成
        self.block = TetrisBlock()

        if self.field.judge_game_over(self.block):
            self.end_func()
            print("GAMEOVER")

        # テトリス画面をアップデート
        self.canvas.update(self.field, self.block)

    def move_block(self, direction):
        'ブロックを移動'

        # 移動できる場合だけ移動する
        if self.field.judge_can_move(self.block, direction):

            # ブロックを移動
            self.block.move(direction)

            # 画面をアップデート
            self.canvas.update(self.field, self.block)

        else:
            # ブロックが下方向に移動できなかった場合
            if direction == MOVE_DOWN:
                # ブロックを固定する
                self.field.fix_block(self.block)
                self.field.delete_line()
                self.new_block()

# イベントを受け付けてそのイベントに応じてテトリスを制御するクラス
class EventHandller():
    def __init__(self, master, game):
        self.master = master

        # 制御するゲーム
        self.game = game

        # イベントを定期的に発行するタイマー
        self.timer = None

        # ゲームスタートボタンを設置
        button = tk.Button(master, text='START', command=self.start_event)
        button.place(x=25 + BLOCK_SIZE * FIELD_WIDTH + 25, y=30)

    def start_event(self):
        'ゲームスタートボタンを押された時の処理'

        # テトリス開始
        self.game.start(self.end_event)
        self.running = True

        # タイマーセット
        self.timer_start()

        # キー操作入力受付開始
        self.master.bind("<Left>", self.left_key_event)
        self.master.bind("<Right>", self.right_key_event)
        self.master.bind("<Down>", self.down_key_event)

    def end_event(self):
        'ゲーム終了時の処理'
        self.running = False

        # イベント受付を停止
        self.timer_end()
        self.master.unbind("<Left>")
        self.master.unbind("<Right>")
        self.master.unbind("<Down>")

    def timer_end(self):
        'タイマーを終了'

        if self.timer is not None:
            self.master.after_cancel(self.timer)
            self.timer = None

    def timer_start(self):
        'タイマーを開始'

        if self.timer is not None:
            # タイマーを一旦キャンセル
            self.master.after_cancel(self.timer)

        # テトリス実行中の場合のみタイマー開始
        if self.running:
            # タイマーを開始
            self.timer = self.master.after(1000, self.timer_event)

    def left_key_event(self, event):
        '左キー入力受付時の処理'

        # ブロックを左に動かす
        self.game.move_block(MOVE_LEFT)

    def right_key_event(self, event):
        '右キー入力受付時の処理'

        # ブロックを右に動かす
        self.game.move_block(MOVE_RIGHT)

    def down_key_event(self, event):
        '下キー入力受付時の処理'

        # ブロックを下に動かす
        self.game.move_block(MOVE_DOWN)

        # 落下タイマーを再スタート
        self.timer_start()

    def timer_event(self):
        'タイマー満期になった時の処理'

        # 下キー入力受付時と同じ処理を実行
        self.down_key_event(None)
    



class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        # App setting
        self.geometry("400x600")
        self.title("Tetris")

        game = TetrisGame(self)

        # イベントハンドラー生成
        EventHandller(self, game)



def main():
    app = Application()
    app.mainloop()


if __name__ == '__main__':
    main()
