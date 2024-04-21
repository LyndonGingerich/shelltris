import random

# Game board dimensions
BOARD_WIDTH = 10
BOARD_HEIGHT = 20

# Tetris pieces
PIECES = (
    ((1, 1, 1, 1),
     (0, 0, 0, 0)),

    ((1, 0, 0, 0),
     (1, 1, 1, 0)),

    ((1, 1, 1, 0),
     (1, 0, 0, 0)),

    ((1, 1, 0, 0),
     (1, 1, 0, 0)),

    ((0, 1, 1, 0),
     (1, 1, 0, 0)),

    ((1, 1, 1, 0),
     (0, 1, 0, 0)),

    ((1, 1, 0, 0),
     (0, 1, 1, 0))
)


# General helpers

def first(items, f=None):
    for item in items:
        if f is None:
            if item:
                return item
        else:
            if f(item):
                return item
    return None


def allf(items, f):
    return all(map(f, items))


def alli(items, f):
    return allf(f, enumerate(items))


def transpose(items):
    return list(map(lambda collection: list(collection), zip(*items)))


# Program-specific helpers

def rotate(piece, times):
    if times <= 0:
        return piece
    return rotate(piece, times - 1)


class Bag:
    def __init__(self):
        self.contents = []

    def next(self):
        if not self.contents:
            new_contents = list(PIECES)
            random.shuffle(new_contents)
            self.contents = new_contents

        return self.contents.pop()


class Board:
    def __init__(self):
        self.tiles = [[0] * BOARD_WIDTH] * BOARD_HEIGHT
        self.last_cleared_rows = 0
        self.last_was_valid = True

    def check_piece_position(self, offset_x, offset_y, piece):
        for y, row in enumerate(piece):
            for x, value in enumerate(row):
                index_y = offset_y + y
                if value and (index_y > BOARD_HEIGHT - 1 or self.tiles[index_y][offset_x + x]):
                    return False

        return True

    def find_piece_row(self, offset: int, piece: list[list[int]]):
        for self_row_index, _ in enumerate(self.tiles):
            if not self.check_piece_position(offset, self_row_index, piece):
                return self_row_index - 1

    def place_tiles(self, offset, piece):
        row = self.find_piece_row(offset, piece)

        if row < 0:
            self.last_was_valid = False
            return

        for y, piece_row in enumerate(piece):
            for x, value in enumerate(piece_row):
                if value:
                    self.tiles[y + row][x + offset] = 1

        self.tiles = [x for x in self.tiles if not all(x)]
        self.last_cleared_rows = BOARD_HEIGHT - len(self.tiles)
        self.tiles = [0] * BOARD_WIDTH + self.tiles


class Score:
    def __init__(self):
        self.points = 0
        self.previous_was_tetris = False

    def enter_move_score(self, rows_cleared):
        is_tetris = rows_cleared >= 4

        if is_tetris:  # Tetris
            if self.previous_was_tetris:
                self.points += 1200
            else:
                self.points += 800
            rows_cleared -= 4

        self.points += rows_cleared * 100

        self.previous_was_tetris = is_tetris


class Game:
    def __init__(self):
        self.bag = Bag()
        self.current_piece = self.bag.next()
        self.next_piece = self.bag.next()
        self.board = Board()
        self.score = Score()

    def advance_pieces(self):
        self.current_piece = self.next_piece
        self.next_piece = self.bag.next()

    def can_continue(self):
        return self.board.last_was_valid

    def make_move(self, offset, rotations):
        if not self.can_continue():
            return
        self.board.place_tiles(offset, rotate(self.current_piece, rotations))
        self.advance_pieces()
        self.score.enter_move_score(self.board.last_cleared_rows)

    def get_score(self):
        return self.score.points
