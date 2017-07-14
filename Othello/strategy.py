import strategy4_2018aganotra.Othello_Core as othello_core
import random
import pickle
from multiprocessing import Value, Process


class Strategy(othello_core.OthelloCore):
    SQUARE_WEIGHTS = [
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 120, -20, 20, 5, 5, 20, -20, 120, 0,
        0, -20, -40, -5, -5, -5, -5, -40, -20, 0,
        0, 20, -5, 15, 3, 3, 15, -5, 20, 0,
        0, 5, -5, 3, 3, 3, 3, -5, 5, 0,
        0, 5, -5, 3, 3, 3, 3, -5, 5, 0,
        0, 20, -5, 15, 3, 3, 15, -5, 20, 0,
        0, -20, -40, -5, -5, -5, -5, -40, -20, 0,
        0, 120, -20, 20, 5, 5, 20, -20, 120, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    minimaxD = dict()

    def is_valid(self, move):
        if move >= 0 and move <= 100:
            return True
        else:
            return False

    def opponent(self, player):
        if player is othello_core.BLACK:
            return othello_core.WHITE
        else:
            return othello_core.BLACK

    def find_bracket(self, square, player, board, direction):
        index = square + direction
        if board[index] == player or board[index] == othello_core.OUTER:
            return None
        opponent = self.opponent(player)
        while board[index] == opponent:
            index += direction
            if index >= len(board):
                return None
        if board[index] in (othello_core.OUTER, othello_core.EMPTY):
            return None
        else:
            return index
            # iterates through the fuction by going in the direction given

    def is_legal(self, move, player, board):
        # if self.is_valid(move) and board[move] == ".":
        #    for i in othello_core.DIRECTIONS:
        #        if self.find_bracket(move, player, board, i) != None:
        #            return True
        # return False
        function = lambda direction: self.find_bracket(move, player, board, direction)
        return board[move] == othello_core.EMPTY and any(map(function, othello_core.DIRECTIONS))
        # any(map(blah) checks thorugh all directions to see which moves are legal
        # map goes through directions and runs the fuction
        # lambda function goes through the current direction and sees if the bracket will return something

    def make_move(self, move, player, board):
        board[move] = player
        for direction in othello_core.DIRECTIONS:
            self.make_flips(move, player, board, direction)
        return board

        # Function updates board by first changing the move spot and making flips in all directions

    def make_flips(self, move, player, board, direction):
        bracket = self.find_bracket(move, player, board, direction)
        if not bracket:
            return
        square = move + direction
        while square != bracket:
            board[square] = player
            square += direction
            # first finds bracked
            # then makes flips if the bracket is not None

    def legal_moves(self, player, board):
        # moves = []
        # for i in self.squares():
        #    if self.is_legal(i, player, board):
        #        moves.append(i)
        # return moves
        # Bottom code is just a fancier way
        return [moves for moves in self.squares() if self.is_legal(moves, player, board)]
        # brackets put all legal moves into a list

    def any_legal_move(self, player, board):
        return any(self.is_legal(sq, player, board) for sq in self.squares())
        # Goes through al squares and returns any legal moves

    def next_player(self, board, prev_player):
        opp = self.opponent(prev_player)
        if self.any_legal_move(opp, board):
            return opp
        elif self.any_legal_move(prev_player, board):
            return prev_player
        return None

    def score(self, player, board):
        total = 0
        for i in range(11, 90):
            if board[i] == othello_core.BLACK:
                total += self.SQUARE_WEIGHTS[i]
            elif board[i] == othello_core.WHITE:
                total -= self.SQUARE_WEIGHTS[i]
        return total
        # returns score with weights

    def terminal_score(self, player, board):
        cooler, weirdo = 0, 0
        opp = self.opponent(player)
        for cool in self.squares():
            piece = board[cool]
            if piece == player:
                cooler += 1
            elif piece == opp:
                weirdo += 1
        return cooler - weirdo
        # returns score to see who won

    def rand(self, board, player):
        list = self.legal_moves(player, board)
        x = list[random.randrange(0, len(list))]
        self.find_bracket(63, player, board, othello_core.DOWN)
        return x
        # returns random move

    def min_dfs(self, board, player, max_d, current_d, alpha, beta):
        v = 10000
        move = -1
        moves = self.legal_moves(player, board)
        random.shuffle(moves)
        for m in moves:
            cool = board.copy()
            temp = self.make_move(m, player, cool)
            movesForMe = self.any_legal_move(player, board)
            movesforOpp = self.any_legal_move(self.opponent(player), board)
            gameOver = movesForMe is False and movesforOpp is False
            if gameOver:
                result = self.terminal_score(player, board)
                if result < 0:  # LOSE
                    return 10000, m
                if result > 0:  # WIN
                    return -10000, m
                else:  # TIE
                    return 0, m
            if movesforOpp is False:
                result = self.score(player, board) + 10
                return result, m

            if current_d >= max_d:
                return self.score(player, board), m

            new_value = self.max_dfs(temp, self.next_player(board, player), max_d, current_d + 1, alpha, beta)[0]
            if new_value < v:
                v = new_value
                move = m
            if v <= alpha:
                return v, move
            beta = min(beta, v)
        return v, move

    def max_dfs(self, board, player, max_d, current_d, alpha, beta):
        v = -10000
        move = -1
        moves = self.legal_moves(player, board)
        random.shuffle(moves)
        for m in moves:
            cool = board.copy()
            temp = self.make_move(m, player, cool)
            movesForMe = self.any_legal_move(player, board)
            movesforOpp = self.any_legal_move(self.opponent(player), board)

            if movesForMe is False and movesforOpp is False:
                result = self.terminal_score(player, board)
                if result < 0:  # LOSE
                    return -10000, m
                if result > 0:  # WIN
                    return 10000, m
                else:  # TIE
                    return 0, m
            if current_d >= max_d:
                return self.score(player, board), m
            new_value = self.min_dfs(temp, self.next_player(board, player), max_d, current_d + 1, alpha, beta)[0]
            if new_value >= 1:
                return new_value, m
            if new_value > v:
                v = new_value
                move = m
            if v >= beta:
                return v, move
            alpha = max(alpha, v)
        return v, move

    def best_strategy(self, board, player, best_move, still_running):
        """
        :param board: a length 100 list representing the board state
        :param player: WHITE or BLACK
        :param best_move: shared multiptocessing.Value containing an int of
                the current best move
        :param still_running: shared multiprocessing.Value containing an int
                that is 0 iff the parent process intends to kill this process
        :return: best move as an int in [11,88] or possibly 0 for 'unknown'
        """
        depth = 2
        boardString = "".join(board)
        # if (boardString, player) in self.miniMaxD:
        #    best_move.value = self.minimaxD[(board, player)]


        while still_running.value > 0:
            best_move.value = self.minimax(board, player, depth)
            depth += 1
        # self.minimaxD[(boardString, player)] = best_move.value

        return best_move.value

    def saveFile(self):
        file = open('filename.pickle', 'wb')
        pickle.dump(self.minimaxD, file)
        file.close()

    def minimax(self, board, player, max_depth):
        """ Takes a current board and player and max_depth and returns a best move
        This is the top level mini-max function. Note depth is ignored. W
        always search to the end of the game."""
        if player == othello_core.BLACK: move = self.max_dfs(board, player, max_depth, 0, -1000000, 100000)[1]
        if player == othello_core.WHITE: move = self.min_dfs(board, player, max_depth, 0, -1000000, 100000)[1]
        return move
