from copy import deepcopy
import pygame

RED = (255, 0, 0)
WHITE = (255, 255, 255)


# position = it's a board object. This is the current board configuration. Given the current board configuration
# the minimax should provide the optimal board configuration (best board configuration) as we play.

# depth = how far we are extending the minimax tree. Everytime we evaluate the algorithm,
# we will decrease the depth by 1. Remember: we only evaluate a position when we reach the end of the tree (root node).

# max_player = boolean value (True/False) that tells us if we are maximizing or minimizing the reward.
# If max_player is TRUE, we tend to maximize our rewards.

# game = this is the game object from main.py. It is used to draw and update the board as we play.

def minimax(position, depth, max_player, game):
    # if we are in the root node (depth == 0) and the game hasn't finished yet (position.winner() != None)
    # we return the current board position and the evaluation of that position.
    if depth == 0 or position.winner() != None:
        return position.evaluate(), position

    if max_player:
        # initialize the max evaluation at -inf. This is needed when we compare with next evaluations.
        maxEval = float('-inf')
        # best_move will store the best move we could make. It is initialized as None
        best_move = None
        # the function get_all_moves will provide all possible moves of a given player (WHITE, in this case)
        # from its current position. The third argument ("game") is used so that we can draw and update the board game.
        for move in get_all_moves(position, WHITE, game):
            # This is a recursive call
            # Remember: we only evaluate a position using the minimax algorithm when we reach the
            # end of the tree (root node).
            # Note: minimax returns the best reward (maxEval in this case, the maximum) +
            # the best move that led to that reward.
            # In this way, the [0] below means that we only pick the first output (maxEval).
            evaluation = minimax(move, depth - 1, False, game)[0]
            maxEval = max(maxEval, evaluation)
            # If the maximum reward we found is equal to the current reward,
            # this means that the best move is the current move.
            # In this way, we can keep track of the best moves the AI agent can make during the game.
            if maxEval == evaluation:
                best_move = move
        return maxEval, best_move
    else:

        # INSERT CODE HERE #

        minEval = float('inf')

        best_move = None

        for move in get_all_moves(position, WHITE, game):
            evaluation = minimax(move, depth - 1, True, game)[0]
            minEval = min(minEval, evaluation)
            if minEval == evaluation:
                best_move = move

        return minEval, best_move


def simulate_move(piece, move, board, game, skip):
    board.move(piece, move[0], move[1])
    if skip:
        board.remove(skip)

    return board


def get_all_moves(board, color, game):
    moves = []

    for piece in board.get_all_pieces(color):
        valid_moves = board.get_valid_moves(piece)
        for move, skip in valid_moves.items():
            draw_moves(game, board, piece)
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            new_board = simulate_move(temp_piece, move, temp_board, game, skip)
            moves.append(new_board)

    return moves


def draw_moves(game, board, piece):
    valid_moves = board.get_valid_moves(piece)
    board.draw(game.win)
    pygame.draw.circle(game.win, (0, 255, 0), (piece.x, piece.y), 50, 5)
    game.draw_valid_moves(valid_moves.keys())
    pygame.display.update()
    # pygame.time.delay(100)
