import engine


def choose_move(board_state, current_piece, next_piece):

    # Your logic goes here

    return 0, 0


if __name__ == "main":
    game = engine.Game()
    while game.can_continue():
        left_index, clockwise_rotations = choose_move(game.board.tiles, game.current_piece, game.next_piece)
        game.make_move(left_index, clockwise_rotations)

    print("Score: " + game.get_score())
