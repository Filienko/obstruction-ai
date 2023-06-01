import numpy as np
from Solver import Node, mm


class Board:
    game_map: dict[Node, tuple] = None
    exp: int = 0
    depth_limit: int = 0
    iteration: int = 0

    def __init__(self, arguments: str):
        tokens = arguments[2].split("*")
        self.size = (int(tokens[0]), int(tokens[1]))

        # Declare the 2D Array with buffer zone
        self.search_method = arguments[1]
        self.history = []
        self.ai_player = int(arguments[0])
        self.current_state = Node(np.full(((self.size[1] + 2), (self.size[0] + 2)), 'p'), (0, 0), self.ai_player - 1, self.ai_player == 1)
        self.current_state.state[1:-1, 1:-1] = ' '

    # Sets initial and final state of a board to determine the moves
    def initialize_game(self):
        # Add data about evaluation function new found node heuristic
        f = open("ReadMe.txt", "a")
        f.write("\n--------------")
        f.write("\nNEW GAME")
        f.write(f"\nEvaluation function: number of occupied spots in a child node's 2d state")
        f.write(f"\nAI plays as {'Min, X' if self.ai_player == 2 else 'Max, O'}")
        f.write(f"\nSize: {self.size}")
        f.close()

        # Default non-human player
        if self.ai_player == 1:
            # Our AI new turn
            ai_move: Node = self.analyze_game()
            print(f"AI move:{ai_move.move[1]}/{ai_move.move[0]}")
            self.current_state = ai_move
            # Display recent updated state currently
            self.current_state.display()

        self.next_turn()

    def end_game(self, winner: str):
        print(f" Thank you for the game! \n {winner} won!")
        f = open("ReadMe.txt", "a")
        f.write("\nEND OF GAME\n")
        f.close()
        exit()

    # Sets initial and final state of a board to determine the moves
    def analyze_game(self):
        if self.search_method == "MM":
            return self.mm_output(False)
        elif self.search_method == "AB":
            return self.mm_output(True)

    # Makes an AI/player turn with given coordinates
    def next_turn(self):
        # The player's turn
        player_move = input("Your turn, enter the coordinates in the format row/column").split("/")
        # Prevent attempting to input illegal argument from outside of the appropriate limit numbers
        if len(player_move) != 2:
            print("Not a valid move. Attempt again")
            self.next_turn()

        if not player_move[0].isdigit() or not player_move[1].isdigit():
            print("Not a valid move. Attempt again")
            self.next_turn()

        if int(player_move[0]) > self.size[0] or int(player_move[1]) > self.size[1]:
            print("Not a valid move. Attempt again")
            self.next_turn()

        # Returns 0 for a non valid move, prevent one from accessing potentially inappropriate coordinates
        valid_move = self.current_state.update_board((int(player_move[1]), int(player_move[0])), 'O' if self.ai_player == 2 else 'X')

        # Prevent player from placing the player's mark in the inappropriate spot
        if valid_move == 0:
            print("Not a valid move. Attempt again")
            self.next_turn()
        print(f"Your move:{player_move[0]}/{player_move[1]}")
        self.current_state.display()

        # Provided a correct move is given, then possibility of ending the interaction would be properly considered
        if self.current_state.is_terminal_state():
            self.end_game("Human")

        # Our AI new turn
        ai_move: Node = self.analyze_game()
        print(f"AI move:{ai_move.move[1]}/{ai_move.move[0]}")
        self.current_state = ai_move

        # Display updated state currently
        self.current_state.display()

        # Provided a correct move is given, then possibility of ending the interaction would be properly considered
        if self.current_state.is_terminal_state():
            self.end_game("AI")

        self.next_turn()

    # Function to display the required data about the game
    def write_file_output(self, exp: int, search_method: str):
        f = open("ReadMe.txt", "a")
        f.write("\n--------------")
        f.write(f"\nSearch Method: {search_method}")
        # Count new current number of children nodes expanded at given depth
        f.write(f"\nExpanded now: {exp}, Total Expanded: {self.exp} \nDepth: {self.iteration}")
        f.write("\n--------------")
        f.close()

    def mm_output(self, ab_enabled: bool):
        state, exp = mm(self, ab_enabled)
        # If it is first, updated, or terminal move, produce the text output print values

        # Count number of moves
        self.iteration += 1

        self.exp += exp
        if self.iteration == 2 or self.iteration == 4:
            self.write_file_output(exp, 'Minimax with Alpha-Beta pruning enabled' if ab_enabled else 'Minimax')

        return state

    def __repr__(self) -> str:
        return f"{type(self).__name__}(size={self.size}, search method={self.search_method})\n"

