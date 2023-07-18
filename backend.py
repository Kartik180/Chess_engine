from flask import Flask, request
import chess
import math
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


class ChessEvaluator:
    def __init__(self):
        self.piece_values = {
            chess.PAWN: 100,
            chess.BISHOP: 350,
            chess.KNIGHT: 350,
            chess.ROOK: 525,
            chess.QUEEN: 1000,
            chess.KING: 20000
        }

        self.square_tables = {
            chess.PAWN: [
                100, 100, 100, 100, 105, 100, 100, 100,
                78, 83, 86, 73, 102, 82, 85, 90,
                7, 29, 21, 44, 40, 31, 44, 7,
                -17, 16, -2, 15, 14, 0, 15, -13,
                -26, 3, 10, 9, 6, 1, 0, -23,
                -22, 9, 5, -11, -10, -2, 3, -19,
                -31, 8, -7, -37, -36, -14, 3, -31,
                0, 0, 0, 0, 0, 0, 0, 0
            ],
            chess.BISHOP: [
                -14, -10, -11, -6, -6, -11, -10, -14,
                -10, 1, 2, 3, 3, 2, 1, -10,
                -10, 2, 8, 9, 9, 8, 2, -10,
                -10, 3, 9, 12, 12, 9, 3, -10,
                -10, 2, 9, 12, 12, 9, 2, -10,
                -10, 1, 2, 3, 3, 2, 1, -10,
                -14, -10, -11, -6, -6, -11, -10, -14
            ],
            chess.KNIGHT: [
                -35, -25, -20, -20, -20, -20, -25, -35,
                -25, -15, 10, 5, 5, 10, -15, -25,
                -20, 5, 20, 15, 15, 20, 5, -20,
                -20, 0, 15, 20, 20, 15, 0, -20,
                -20, 5, 15, 20, 20, 15, 5, -20,
                -20, 0, 10, 15, 15, 10, 0, -20,
                -25, -15, 5, 0, 0, 5, -15, -25,
                -35, -25, -20, -20, -20, -20, -25, -35
            ],
            chess.ROOK: [
                5, 5, 5, 5, 5, 5, 5, 5,
                10, 10, 10, 10, 10, 10, 10, 10,
                -5, 0, 0, 0, 0, 0, 0, -5,
                -5, 0, 0, 0, 0, 0, 0, -5,
                -5, 0, 0, 0, 0, 0, 0, -5,
                -5, 0, 0, 0, 0, 0, 0, -5,
                -5, 0, 0, 0, 0, 0, 0, -5,
                0, 0, 0, 5, 5, 0, 0, 0
            ],
            chess.QUEEN: [
                -20, -10, -10, -5, -5, -10, -10, -20,
                -10, 0, 5, 0, 0, 0, 0, -10,
                -10, 5, 5, 5, 5, 5, 0, -10,
                0, 0, 5, 5, 5, 5, 0, -5,
                -5, 0, 5, 5, 5, 5, 0, -5,
                -10, 0, 5, 5, 5, 5, 0, -10,
                -10, 0, 0, 0, 0, 0, 0, -10,
                -20, -10, -10, -5, -5, -10, -10, -20
            ],
            chess.KING: [
                -30, -40, -40, -50, -50, -40, -40, -30,
                -30, -40, -40, -50, -50, -40, -40, -30,
                -30, -40, -40, -50, -50, -40, -40, -30,
                -30, -40, -40, -50, -50, -40, -40, -30,
                -20, -30, -30, -40, -40, -30, -30, -20,
                -10, -20, -20, -20, -20, -20, -20, -10,
                20, 20, 0, 0, 0, 0, 20, 20,
                20, 30, 10, 0, 0, 10, 30, 20
            ]
        }

    def calculate_piece_value(self, piece):
        return self.piece_values.get(piece.piece_type, 0)

    def calculate_square_score(self, piece, square):
        square_scores = self.square_tables[piece.piece_type]
        if piece.color == chess.BLACK:
            square_scores = square_scores[::-1]  # Reverse the table for black pieces

        if 0 <= square < len(square_scores):
            return square_scores[square]
        else:
            return 0

    def evaluate_position(self, board):
        white_material = 0
        black_material = 0
        white_square_score = 0
        black_square_score = 0

        for square in chess.SQUARES:
            piece = board.piece_at(square)

            if piece is not None:
                piece_value = self.calculate_piece_value(piece)
                square_score = self.calculate_square_score(piece, square)

                if piece.color == chess.WHITE:
                    white_material += piece_value
                    white_square_score += square_score
                else:
                    black_material += piece_value
                    black_square_score += square_score

        total_score = (white_material - black_material) + (white_square_score - black_square_score)
        return total_score

    def minimax(self, board, depth, alpha, beta, maximizing_player):
        if depth == 0 or board.is_game_over():
            return self.evaluate_position(board)

        if maximizing_player:
            max_eval = -math.inf
            moves = list(board.legal_moves)
            best_moves = sorted(moves, key=lambda move: self.evaluate_move(board, move), reverse=True)[:3]
            for move in best_moves:
                board.push(move)
                eval = self.minimax(board, depth - 1, alpha, beta, False)
                board.pop()
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if alpha >= beta and maximizing_player:
                    break
            return max_eval
        else:
            min_eval = math.inf
            moves = list(board.legal_moves)
            best_moves = sorted(moves, key=lambda move: self.evaluate_move(board, move))[:3]
            for move in best_moves:
                board.push(move)
                eval = self.minimax(board, depth - 1, alpha, beta, True)
                board.pop()
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if alpha >= beta:
                    break
            return min_eval

    def evaluate_move(self, board, move):
        board.push(move)
        score = self.evaluate_position(board)
        board.pop()
        return score

    def get_best_move(self, board, depth):
        best_score = -math.inf
        best_move = None
        for move in board.legal_moves:
            board.push(move)
            score = self.minimax(board, depth - 1, -math.inf, math.inf, False)
            board.pop()
            if score > best_score:
                best_score = score
                best_move = move
        return best_move
chess_evaluator = ChessEvaluator()


@app.route('/best-move', methods=['POST'])
def get_best_move_endpoint():
    fen = request.json.get('fen')
    depth = 9

    board = chess.Board(fen)
    best_move = chess_evaluator.get_best_move(board, depth)

    board.push(best_move)

    return {'fen': board.fen()}


if __name__ == '__main__':
    app.run()
