import numpy as np

# LIMIT for DFS, as a result of a local machine time limitation and space size
# allowed that, so that it does not run excessive amount of time if no solution can be found by DPS
# Added that set of numbers due to the available time/hardware set
# constraints, implemented that to produce output faster.

# Increase the step for a much better total AI count performance
# STEP FOR THE 8*8 MM/AB PRUNING EXP COUNT
# STEP = 3
STEP = 4
# TODO: If you have a stronger local computer, uncomment this:
# STEP = 6


# Node class, containing the 2d array of a current state of an environment of a current puzzle
def find_utility(position) -> int:
    position_evals = position.state.shape
    # 1 / 1, 1 / 6, 6 / 1, 6 / 6
    evals = 0
    # SIMPLE COUNT CALCULATED SET OPTION
    # Not using the non-usable surrounding padded spots,
    for ix in range(position_evals[1]):
        for iy in range(position_evals[0]):
            if position.state[iy, ix] == 'p':
                continue
            if position.state[iy, ix] == '/' or position.state[iy, ix] == 'O' or position.state[iy, ix] == 'X':
                evals += 1

    # Return a max number of available squares, assuming more squares are available for a future move, the better
    # return sum(sum(position_evals))
    return evals


class Node:
    def __init__(self, state: np.ndarray, move: tuple, depth: int, is_max: bool):
        self.move = move
        self.state = state
        self.depth = depth
        self.is_max = is_max

    def __repr__(self) -> str:
        return_string = "\n"
        for row in self.state:
            return_string = return_string + str(row) + "\n"
        return return_string

    def __eq__(self, other):
        if not isinstance(other, Node):
            # don't attempt to compare against unrelated types
            return NotImplemented
        """Overrides the default implementation"""
        return (self.state == other.state).all()

    def __key(self):
        return (self.move, str(self.state))

    def __hash__(self):
        return hash(self.__key())

    def display(self):
        print('   ', end='')
        for i in range(1, self.state.shape[0] - 1):
            print(' ' + str(i) + '  ', end='')
        print()
        print('  ', end='')
        for i in range(1, self.state.shape[0] - 1):
            print('----', end='')
        print()

        for i in range(1, self.state.shape[1] - 1):
            print(str(i) + ' |', end='')
            for j in range(1, self.state.shape[0] - 1):
                print(' ' + self.state[j, i] + ' |', end='')
            print()
            print('  ', end='')
            for j in range(1, self.state.shape[0] - 1):
                print('----', end='')
            print()

    def is_terminal_state(self):
        if find_utility(self) == (self.state.shape[0] - 2) * (self.state.shape[1] - 2):
            return True
        return False

    def update_board(self, new_move: tuple, mark):
        self.move = new_move

        x_count: int = len(np.asarray(np.where(self.state == 'X')).T)
        y_count: int = len(np.asarray(np.where(self.state == 'O')).T)
        if x_count < y_count:
            mark = 'X'
        else:
            mark = 'O'

        if self.state[new_move] == 'p' or self.state[new_move] == 'O' or self.state[new_move] == 'X' \
                or self.state[new_move] == '/':
            # Interrupting the move if the new move was placed in non valid spot for the total puzzle array
            return 0

        moving_directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1)]

        for direction in moving_directions:
            # Moving in all 9 directions surrounding the given piece of spot
            new_y, new_x = new_move[0] + direction[0], new_move[1] + direction[1]
            # Prevent the padding from being listed in list
            if self.state[new_y, new_x] != 'p':
                self.state[new_y, new_x] = '/'

        self.state[new_move[0], new_move[1]] = mark

        return 1


def mm(board, ab_enabled: bool):
    # If call occurs, another human move happened, adjust to a new potential puzzle state=
    exp = 0

    # First iteration, no game map provided
    if board.game_map is None or board.current_state not in board.game_map.keys():
        # For AB, the only condition a child evaluation is if it is a terminal node, count
        board.depth_limit = board.depth_limit + STEP
        value, board.game_map, exp, depth = minimax(board.current_state, float("-inf"), float("inf"),
                                                True, board, ab_enabled=ab_enabled, curr_depth=0)

    target_move: list[tuple] = board.game_map.get(board.current_state)
    board.current_state = target_move[0][0]

    # Return the first child, which is the best possible child node
    return board.current_state, exp


def minimax(node: Node, alpha: float, beta: float, maximizing_player: bool, board,
            ab_enabled: bool = False, curr_depth: int = 0):
    exp: int = 0
    value: float = 0
    curr_depth = node.depth

    # For the terminal states or the last node at current IDS level iteration in, return inf, 0 terminal count value
    if node.is_terminal_state():
        if maximizing_player:
            return float("-inf"), {}, exp, node.depth
        return float("inf"), {}, exp, node.depth

    if curr_depth >= board.depth_limit:
        return find_utility(node), {}, exp, curr_depth-1

    legal_moves: list[tuple] = np.asarray(np.where(node.state == ' ')).T
    my_subtree: dict[Node, list] = {node: []}
    curr_children: list[tuple] = []
    all_subtrees_below_that_depth: dict[Node, list] = {}
    # Iterate over the nodes, initially prefer one appearing better by default, modify then by updating the children
    # weights

    for move in legal_moves:

        if maximizing_player:
            child_node = Node(np.copy(node.state), (move[0], move[1]), node.depth + 1, False)
            child_node.update_board((move[0], move[1]), 'X')
            value: float = float('-inf')

            child_value, child_subtree, curr_exp, curr_depth = minimax(child_node, alpha, beta, False, board,
                                                                       ab_enabled=ab_enabled, curr_depth=node.depth)
            curr_children.append((child_node, child_value))
            all_subtrees_below_that_depth = {**all_subtrees_below_that_depth, **child_subtree}
            exp += curr_exp + 1

            if child_value > value:
                value = child_value

            if ab_enabled:
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
        # Minimizing node counts node children
        else:
            child_node = Node(np.copy(node.state), (move[0], move[1]), node.depth + 1, True)
            child_node.update_board((move[0], move[1]), 'O')
            value: float = float('inf')

            child_value, child_subtree, curr_exp, curr_depth = minimax(child_node, alpha, beta, True, board,
                                                                       ab_enabled=ab_enabled, curr_depth=curr_depth)
            curr_children.append((child_node, child_value))
            all_subtrees_below_that_depth = {**all_subtrees_below_that_depth, **child_subtree}
            exp += curr_exp + 1

            if child_value < value:
                value = child_value

            if ab_enabled:
                beta = min(beta, value)
                if alpha >= beta:
                    break

    if maximizing_player:
        curr_children.sort(key=lambda n: -n[1])
    else:
        curr_children.sort(key=lambda n: n[1])

    # Return the sorted list of possible child nodes I can currently achieve here
    my_subtree[node] = curr_children
    my_subtree = {**my_subtree, **all_subtrees_below_that_depth}

    return value, my_subtree, exp, node.depth

