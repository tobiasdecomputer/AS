import csv
import numpy as np

class Board:
    def __init__(self, filename):
        self.board_original = self.load_board(filename)
        self.board_player = np.zeros((8, 8), dtype=str)

    def load_board(self, filename):
        with open(filename, "r") as file:
            reader = csv.reader(file, delimiter=",")
            x = list(reader)
        return np.array(x, dtype=str)

    def click_tile(self, row, col):
        self.board_player[row, col] = self.board_original[row, col]

    def available_moves(self):
        return np.transpose(np.where(self.board_player == ''))


class Game:
    def __init__(self, board):
        self.board = board
        self.iteration_count = 0
        self.max_iterations = 51
        self.rng = np.random.default_rng()

    def play(self):
        game_over = False
        while not game_over:
            moves = self.board.available_moves()
            if moves.size == 0:
                break
            row, col = self.rng.choice(moves, axis=0)
            self.board.click_tile(row, col)
            self.iteration_count += 1
            game_over = self.evaluate(row, col)
        return self.iteration_count

    def evaluate(self, row, col):
        if self.board.board_original[row, col] == "x":
            return True
        elif self.iteration_count >= self.max_iterations:
            return True
        else:
            return False


class Simulator:
    def __init__(self, filename, nr_runs):
        self.filename = filename
        self.nr_runs = nr_runs
        self.sim_results = np.zeros(nr_runs)

    def run(self):
        for i in range(self.nr_runs):
            board = Board(self.filename)
            game = Game(board)
            self.sim_results[i] = game.play()
            if i % 1000 == 0:  # Print progress every 1000 runs
                print(f"Running simulation {i}")
        return np.mean(self.sim_results)


# Example usage:
filename = 'board.csv'
nr_runs = 1

simulator = Simulator(filename, nr_runs)
average_iterations = simulator.run()
print(f"Average number of iterations: {average_iterations}")
