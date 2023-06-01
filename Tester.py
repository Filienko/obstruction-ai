from Board import Board
import sys

# IMPORTANT: I have done 8 by 8 with minimal possible depth growth value to allow the model to run on the older laptop


# Initiated the main python solving test program
if __name__ == '__main__':
    # Proceed to input all of the lines listed among the inputted file as separate lines
    board = Board(sys.argv[1:])
    board.initialize_game()
