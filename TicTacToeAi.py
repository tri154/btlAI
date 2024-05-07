global role, n, max_depth, board
role = "x"


def get_move(board, size):
    # Find all available positions on the board
    global n
    n = int(size)
    board = board
    return alpha_beta_minimax()
def alpha_beta_minimax():
    alpha = float('-inf')
    beta = float('inf')
    act = None
    value = float('-inf')
    init_node = get_node_from_board(board)
    for move in init_node.children:
        node = Node(move, 0, init_node)
        t = node.min_value(alpha, beta)
        if (value <= t):
            value = t
            act = t.action
    return act
def get_first_children():
    bound = set()
    res = set()
    for i in range(n):
        for j in range(n):
            if board[i][j] == '': continue
            if check_neighbor_blank(i, j, board):
                bound.add((i, j))
    for t in bound:
        t = tuple(t)
        x = t[0]
        y = t[1]
        for i in range(x - 2, x + 3):
            for j in range(y - 2, y + 3):
                if i < 0 or i >= n: continue
                if j < 0 or j >= n: continue
                if board[i][j] == ' ':
                    res.add((i, j))
    return res
def check_neighbor_blank(x, y):
    for i in range(x - 1, x + 2):
        for j in range(y - 1, y + 2):
            if i == x and j == y:
                continue
            if i < 0 or i >= n:
                continue
            if j < 0 or j >= n:
                continue
            if board[i][j] == ' ':
                return True
    return False
def get_node_from_board():
    node = Node(None, 0, None)
    node.children = get_first_children(board)
    return node

class Node:
    def __intit__(self, move, depth, parent):
        self.move = move
        self.depth = 1
        if parent == None: return
        self.previous_moves = parent.previous_move
        self.previous_moves.add(move)
        self.children = parent.children.copy()
        self.children.remove(move)
        for i in range(move[0] - 2, move[0] + 3):
            for j in range(move[1] - 2, move[1] + 3):
                if i < 0 or i >= n: continue
                if j < 0 or j >= n: continue
                if (i, j) in self.previous_moves: continue
                if board[i][j] != ' ': continue
                self.children.add((i, j))

    def min_value(self, alpha, beta):
        if self.depth == max_depth:
            return self.heuristic()
        value = float('inf')
        for t in self.children:
            node = Node(t, self.depth + 1, self)
            t = node.max_value(alpha, beta)
            value = min(value, t)
            beta = min(beta, t)
            if (alpha >= beta): return value
        return value
    def max_value(self, alpha, beta):
        if self.depth == max_depth:
            return self.heuristic()
        value = float('-inf')
        for t in self.children:
            node = Node(t, self.depth + 1, self)
            t = node.min_value(alpha, beta)
            value = max(value, t)
            alpha = max(alpha, t)
            if (alpha >= beta): return value
        return value
    def heuristic(self):
        pass

        # HEURISTIC_SCORES = {
        #     "-----": -1000000000000,
        #     "+++++": 1000000000000,
        #     " ---- ": -50000000000,
        #     " ++++ ":  10000000000,
        #     "-++++ ": 100000000,
        #     " ++++-": 100000000,
        #     " ----+": -500000000,
        #     "+---- ": -500000000,
        #     " +++ ": 1000,
        #     " +++-": 150,
        #     " ---+": -50,
        #     " --- ": -5000,
        #     " ++ ": 10,
        #     " -- ": -50
        # }

