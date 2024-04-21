import unittest

from engine import *


# noinspection PyShadowingNames,PyMethodMayBeStatic


class BoardTests(unittest.TestCase):
    def test_square_out_of_bounds_lower(self):
        board = Board()
        shape = [[1, 1, 0, 0]] * 2
        board.check_piece_position(0, BOARD_HEIGHT - 1, shape)


if __name__ == '__main__':
    unittest.main()
