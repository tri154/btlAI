import heapq
import time
import copy
import random
global max_depth, hashT, HEURISTIC_SCORE, R, Q, R5, R6, A, B, cacheT, count, count_leaf, count_id, delay_time, countX, countO, ZobristTable
max_depth = 6
delay_time = 0
count_id = 0
cacheT = dict()
count = 0
count_leaf = 0
ZobristTable = None

def indexOf(c):
    if c == 'x': return 0
    if c == 'o': return 1

global minV, maxV
minV = 0
maxV = pow(2, 64)
def randomInt():
    return random.randint(minV, maxV)
def init_Zobrist_table(size):
    global ZobristTable
    ZobristTable = [[[randomInt() for k in range(2)] for j in range(size)] for i in range(size)]

def get_all_lines(board):
    size = len(board)
    lines = []

    # Lấy tất cả các đường ngang
    for row in board:
        if len(row) >= 5:
            lines.append(row)

    # Lấy tất cả các đường dọc
    for col in range(size):
        column = [board[row][col] for row in range(size)]
        if len(column) >= 5:
            lines.append(column)

    # Lấy các đường chéo chính và chéo phụ
    # Các đường chéo chính
    for start in range(size - 4):
        # Chéo chính từ trên trái xuống dưới phải
        main_diagonal1 = [board[i][i + start] for i in range(size - start)]
        if len(main_diagonal1) >= 5:
            lines.append(main_diagonal1)
        if start != 0 :
            main_diagonal2 = [board[i + start][i] for i in range(size - start)]
            if len(main_diagonal2) >= 5:
                lines.append(main_diagonal2)

        # Chéo phụ từ trên phải xuống dưới trái
        anti_diagonal1 = [board[i][size - 1 - i - start] for i in range(size - start)]
        if len(anti_diagonal1) >= 5:
            lines.append(anti_diagonal1)
        if start != 0:
            anti_diagonal2 = [board[i + start][size - 1 - i] for i in range(size - start)]
            if len(anti_diagonal2) >= 5:
                lines.append(anti_diagonal2)

    return lines

def rk(s):
    h = 0
    res = 0
    count = 0
    cX2 = 0
    cO2 = 0

    cX3 = 0
    cO3 = 0

    for i in range(len(s)):
        count += 1
        c = s[i]
        if count < 5:
            h = (h * R + ord(c)) % Q
        if count == 5:
            h = (h * R + ord(c)) % Q
            value = hashT.get(h)
            if value != None:
                if h in countX2: cX2 += 1
                if h in countO2: cO2 += 1
                if h in countX3: cX3 += 1
                if h in countO3: cO3 += 1
                res += value
        if count == 6:
            h = (h * R + ord(c)) % Q
            value = hashT.get(h)
            if value != None:
                if h in countX2: cX2 += 1
                if h in countO2: cO2 += 1
                if h in countX3: cX3 += 1
                if h in countO3: cO3 += 1
                res += value
            if i == len(s) - 1:
                h = (h + Q - R6 * ord(s[i - 5]) % Q) % Q
                value = hashT.get(h)
                if value != None:
                    if h in countX2: cX2 += 1
                    if h in countO2: cO2 += 1
                    if h in countX3: cX3 += 1
                    if h in countO3: cO3 += 1
                    res += value
        if count > 6:
            h = (h + Q - R6 * ord(s[i - 6]) % Q) % Q
            value = hashT.get(h)
            if value != None:
                if h in countX2: cX2 += 1
                if h in countO2: cO2 += 1
                if h in countX3: cX3 += 1
                if h in countO3: cO3 += 1
                res += value
            h = (h * R + ord(c)) % Q
            value = hashT.get(h)
            if value != None:
                if h in countX2: cX2 += 1
                if h in countO2: cO2 += 1
                if h in countX3: cX3 += 1
                if h in countO3: cO3 += 1
                res += value
            if i == len(s) - 1:
                h = (h + Q - R6 * ord(s[i - 5]) % Q) % Q
                value = hashT.get(h)
                if value != None:
                    if h in countX2: cX2 += 1
                    if h in countO2: cO2 += 1
                    if h in countX3: cX3 += 1
                    if h in countO3: cO3 += 1

    return [res, cX2, cO2, cX3, cO3]

def compute(b):
    lines = get_all_lines(b)
    res = [0, 0, 0, 0, 0]
    for i in lines:
        lv = rk(i)
        for i in range(len(res)):
            res[i] += lv[i]
    if res[1] >= 2: res[0] += 500000
    if res[2] >= 2: res[0] += -500000
    if res[3] >= 3: res[0] += (res[3] // 3) * 500
    if res[4] >= 3: res[0] += (res[4] // 3) * -500
    return res




# def brute_force(s):
#     res = 0
#     for i in range(len(s)):
#         t = ""
 #         for j in range(i, i + 5):
#             if j >= len(s):
#                 t = None
#                 break
#             t += s[j]
#         if t != None:
#             value = HEURISTIC_SCORES.get(t)
#             if value != None:
#                 res += value
#
#     for i in range(len(s)):
#         t = ""
#         for j in range(i, i + 6):
#             if j >= len(s):
#                 t = None
#                 break
#             t += s[j]
#         if t != None:
#             value = HEURISTIC_SCORES.get(t)
#             if value != None:
#                 res += value
#     return res
HEURISTIC_SCORES = {
        "ooooo": float("-inf"),
        "xxxxx": float("inf"),
        " oooo ": -1000000,
        " xxxx ":  1000000,

        "oxxxx ": 100000,
        " xxxxo": 100000,

        " xxx ": 1000,
        " x xx ": 1000,
        " xx x ": 1000,

        "x xxx": 50000,
        "xx xx": 50000,
        "xxx x": 50000,

        " oooox": -100000,
        "xoooo ": -100000,

        " ooo ": -1000,
        " oo o ": -1000,
        " o oo ": -1000,

        "o ooo": -50000,
        "oo oo": -50000,
        "ooo o": -50000,


        "  xxxo": 100,
        "oxxx  ": 100,

        "  xx  ": 50,
        " x x ": 50,

        "oxx   ": 10,
        "ox x  ": 10,
        "   xxo": 10,
        "  x xo": 10,

        "  ooox": -100,
        "xooo  ": -100,

        "  oo  ": -50,
        " o o ": -50,

        "xoo   ": -10,
        "xo o  ": -10,
        "   oox": -10,
        "  o ox": -10,
}

hashT = {
    6628 : float("-inf"),
    22020 : float("inf"),

    19967 : -1000000,
    7869 : 1000000,

    8361 : 100000,
    7948 : 100000,

    2841 : 1000,
    2105 : 1000,
    11711 : 1000,

    16256 : 50000,
    25862 : 50000,
    26973 : 50000,

    20055 : -100000,
    15645 : -100000,

    965 : -1000,
    9051 : -1000,
    1052 : -1000,

    15194 : -50000,
    23193 : -50000,
    13885 : -50000,

    16338 : 100,
    13314 : 100,

    21212 : 50,
    6683 : 50,

    17156 : 10,
    7550 : 10,
    10574 : 10,
    20180 : 10,

    14471 : -100,
    22902 : -100,

    21640 : -50,
    17530 : -50,

    11986 : -10,
    3987 : -10,
    23037 : -10,
    3555 : -10,

}
countX2 = {
    8361,
    7948,
    2841,
    2105,
    11711,
    16256,
    25862,
    26973,

}
countX3 = {
    21212,
    6683,
    17156,
    7550,
    10574,
    20180,
}
countO2 = {
    20055,
    15645,
    965,
    9051,
    1052,
    15194,
    23193,
    13885,
}
countO3 = {
    21640,
    17530,
    11986,
    3987,
    23037,
    3555
}


R = 256
R5 = 16768
R6 = 5572

Q = 27481


def compute_brute_force(b):
    d = dict()
    lines = get_all_lines(b)
    res = 0
    for s in lines:
        for i in range(len(s)):
            t = ""
            for j in range(i, i + 5):
                if j >= len(s):
                    t = None
                    break
                t += s[j]
            if t != None:
                value = HEURISTIC_SCORES.get(t)
                if value != None:
                    res += value
                    if t in d:
                        d[t] += 1
                    else:
                        d[t] = 1

        for i in range(len(s)):
            t = ""
            for j in range(i, i + 6):
                if j >= len(s):
                    t = None
                    break
                t += s[j]
            if t != None:
                value = HEURISTIC_SCORES.get(t)
                if value != None:
                    res += value
                    if t in d:
                        d[t] += 1
                    else:
                        d[t] = 1
    countX = 0
    countO = 0
    for k, v in d.items():
        print(str(k) + " " + str(v))
    for key in d:
        if key == "oxxxx " or key == " xxxxo" or key == " xxx ": countX += d[key]
        if key == " oooox" or key == "xoooo " or key == " ooo ": countO += d[key]
    print(res)
    if countX >= 2: return float("inf")
    if countO >= 2: return float("-inf")
    return res

def toHash(str):
    t  = 0
    for c in str:
        t = (R * t + ord(c)) % Q
    return t


# for key in HEURISTIC_SCORES:
#     t = toHash(key)
#     # if len(key) == 5:
#     #     print("\'" + key + "x" + "\'" + " : " + str(HEURISTIC_SCORES[key]) + ", ")
#     #     print("\'" + key + "o" + "\'" + " : " + str(HEURISTIC_SCORES[key]) + ", ")
#     #     print("\'" + key + " " + "\'" + " : " + str(HEURISTIC_SCORES[key]) + ", ")
#     #     print("\'" + "x" + key + "\'" + " : " + str(HEURISTIC_SCORES[key]) + ", ")
#     #     print("\'" + "o" + key + "\'" + " : " + str(HEURISTIC_SCORES[key]) + ", ")
#     #     print("\'" + " " + key + "\'" + " : " + str(HEURISTIC_SCORES[key]) + ", ")
    # print("\'" + key + "\'" + " : " + str(HEURISTIC_SCORES[key]) + ", ")
    # print(str(t) + " : " + str(HEURISTIC_SCORES[key]) + ",")
#


def init_node(board):
    init = node()
    init.id = get_id(board)
    init.children = get_children(board)
    init.cache = compute(board)
    init.board = board
    init.depth = 0
    return init

def move_as_o(board):
    global cacheT, ZobristTable
    print(len(cacheT))
    if len(cacheT) > 3000000:
        cacheT = dict()
    print(count_id)
    # input("size bang **: ")
    if ZobristTable == None:
        init_Zobrist_table(len(board))

    size = len(board)
    init = init_node(board)
    if len(init.children) == 0: return ((size / 2, size / 2))
    next_action = None
    value = float("inf")
    alpha = float("-inf")
    beta = float("inf")
    lres = list()
    cres = list()

    l = list()
    for c in init.children:
        cur = node('o', c, init.cache, init.id, init)
        l.append(cur)
    heapq.heapify(l)
    next_action = l[0].move
    while len(l) != 0:
        cur = heapq.heappop(l)
        cres.append((cur.move, cur.cache[0]))
        t = cur.max_value(alpha, beta)
        lres.append((cur.move, t))
        if t < value:
            value = t
            next_action = cur.move
        beta = min(beta, t)
        if value == float("-inf"): break


    print(value)
    print(lres)
    print(cres)
    print("total node: " +  str(count))
    print("total leaf: " + str(count_leaf))
    print("delay time: " + str(delay_time))
    print("cache hit: " + str(count_id))
    return next_action

def move_as_x(board):

    global cacheT, ZobristTable
    print(len(cacheT))
    if len(cacheT) > 300000:
        cacheT = dict()
    print(count_id)
    # input("size bang **: ")
    if ZobristTable == None:
        init_Zobrist_table(len(board))

    size = len(board)
    init = init_node(board)
    if len(init.children) == 0: return ((size / 2, size / 2))
    next_action = None
    value = float("-inf")
    alpha = float("-inf")
    beta = float("inf")
    lres = list()
    cres = list()

    l = list()
    for c in init.children:
        cur = node('x', c, init.cache, init.id, init, True)
        l.append(cur)
    heapq.heapify(l)
    next_action = l[0].move
    while len(l) != 0:
        cur = heapq.heappop(l)
        cres.append((cur.move, -cur.cache[0]))
        t = cur.min_value(alpha, beta)

        # if cur.role == 'x' and cur.move == (7, 10) and cur.depth == 1:
        #     print(t)
        #     input()


        lres.append((cur.move, t))
        if t > value:
            value = t
            next_action = cur.move
        alpha = max(alpha, t)
        if value == float("inf"): break
    print(value)
    print(lres)
    print(cres)
    print("total node: " +  str(count))
    print("total leaf: " + str(count_leaf))
    print("delay time: " + str(delay_time))
    print("cache hit: " + str(count_id))
    return next_action

def get_move(board, size):

    return move_as_o(board)

#x max, o min
def check_neighbor_blank(x, y, board, size):
    for i in range(x - 1, x + 2):
        for j in range(y - 1, y + 2):
            if i == x and j == y:
                continue
            if i < 0 or i >= size:
                continue
            if j < 0 or j >= size:
                continue
            if board[i][j] == ' ':
                return True
    return False
def get_children(board):
    size = len(board)
    bound = set()
    res = set()
    for i in range(size):
        for j in range(size):
            if board[i][j] == ' ': continue
            if check_neighbor_blank(i, j, board, size):
                bound.add((i, j))
    for t in bound:
        x = t[0]
        y = t[1]
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if i < 0 or i >= size: continue
                if j < 0 or j >= size: continue
                if board[i][j] == ' ':
                    res.add((i, j))
    return res

def get_id(board):
    size = len(board)
    res = 0
    global ZobristTable
    for i in range(size):
        for j in range(size):
            char = board[i][j]
            if char == ' ': continue
            piece = indexOf(char)
            res ^= ZobristTable[i][j][piece]
    return res;

class node:
    def __init__(self, role=None, move=None, lastCache=None, lastID=None, parent=None, reverse=False):
        if parent is None:
            return
        global count_id
        global count
        count += 1
        self.role = role
        self.move = move
        self.board = parent.board
        self.depth = parent.depth + 1
        self.children = parent.children
        self.to_remove = list()
        print(str(count) + " depth: " + str(self.depth))
        x = move[0]
        y = move[1]
        piece = indexOf(self.role)
        self.id = lastID ^ ZobristTable[x][y][piece]
        # if self.depth == max_depth:
        self.cache = copy.deepcopy(cacheT.get(self.id))
        if self.cache is None:
            self.cache = self.computeCache(lastCache)
            cacheT[self.id] = copy.deepcopy(self.cache)
        else:
            count_id += 1
            # self.board[x][y] = self.role
            # test_value = compute(self.board)
            # self.board[x][y] = ' '
            # if test_value[0] != self.cache[0]:
            #     print_caro_table(self.board)
            #     print(test_value)
            #     print(self.cache)
            #     input()

        # self.cache = self.computeCache(lastCache)
        # self.board[x][y] = self.role
        # test_value = compute(self.board)
        # self.board[x][y] = ' '
        # if test_value[0] != self.cache[0]:
        #     print_caro_table(self.board)
        #     print(test_value)
        #     print(self.cache)
        #     input()
        self.reverse = reverse
        if reverse:
            self.cache[0] = -self.cache[0]

    def __lt__(self, other):
        return self.cache[0] < other.cache[0]
    def restore(self):
        self.board[self.move[0]][self.move[1]] = ' '
        for i in self.to_remove:
            self.children.remove(i)
        self.children.add(self.move)

    def min_value(self, alpha, beta):
        if self.reverse: self.cache[0] = -self.cache[0]
        if self.depth == max_depth:
            global count_leaf
            count_leaf += 1
            return self.cache[0]
        if self.cache[0] == float("inf"):
            return self.cache[0]

        x = self.move[0]
        y = self.move[1]
        self.board[x][y] = self.role
        self.children.remove((x, y))
        size = len(self.board)
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if i < 0 or i >= size: continue
                if j < 0 or j >= size: continue
                if self.board[i][j] == ' ':
                    if not ((i, j) in self.children):
                        self.children.add((i, j))
                        self.to_remove.append((i, j))

        value = float("inf")
        if self.depth < max_depth - 1:
            li = list()
            for c in self.children:
                nd = node('o', c, self.cache, self.id, self)
                li.append(nd)
                if nd.cache == float("-inf"): break
            heapq.heapify(li)
            while len(li) != 0:
                cur = heapq.heappop(li)
                t = cur.max_value(alpha, beta)

                # if self.role == 'x' and self.move == (7, 10) and self.depth == 1:
                #     print_caro_table(cur.board)
                #     print(cur.cache)
                #     print(cur.move)
                #     print(t)
                #     input()

                value = min(value, t)
                beta = min(beta, t)
                if alpha >= beta:
                    break
        else:
            li = list(self.children)
            for c in li:
                cur = node('o', c, self.cache, self.id, self)
                t = cur.max_value(alpha, beta)
                value = min(value, t)
                beta = min(beta, t)
                if alpha >= beta:
                    break

        self.restore()
        return value

    def max_value(self, alpha, beta):
        if self.reverse: self.cache[0] = -self.cache[0]
        if self.depth == max_depth:
            global count_leaf
            count_leaf += 1
            return self.cache[0]
        if self.cache[0] == float("-inf"):
            return self.cache[0]

        x = self.move[0]
        y = self.move[1]
        self.board[x][y] = self.role
        self.children.remove((x, y))
        size = len(self.board)
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if i < 0 or i >= size: continue
                if j < 0 or j >= size: continue
                if self.board[i][j] == ' ':
                    if not ((i, j) in self.children):
                        self.children.add((i, j))
                        self.to_remove.append((i, j))

        value = float("-inf")
        if self.depth < max_depth - 1:
            li = list()
            for c in self.children:
                nd = node('x', c, self.cache, self.id, self, True)
                li.append(nd)
                if nd.cache == float("-inf"): break
            heapq.heapify(li)
            while len(li) != 0:
                cur = heapq.heappop(li)
                t = cur.min_value(alpha, beta)
                value = max(value, t)
                alpha = max(alpha, t)
                if alpha >= beta:
                    break
        else:
            li = list(self.children)
            for c in li:
                cur = node('x', c, self.cache, self.id, self)
                t = cur.min_value(alpha, beta)
                value = max(value, t)
                alpha = max(alpha, t)
                if alpha >= beta:
                    break
        self.restore()
        return value
    def computeCache(self, lastCache):
        x = self.move[0]
        y = self.move[1]
        res = [0, 0, 0, 0, 0]

        before = self.computeBoardRabinKarp()

        self.board[x][y] = self.role

        after = self.computeBoardRabinKarp()
        self.board[x][y] = ' '


        res[0] = lastCache[0] + after[0] - before[0]
        res[1] = lastCache[1] + after[1] - before[1]
        res[2] = lastCache[2] + after[2] - before[2]
        res[3] = lastCache[3] + after[3] - before[3]
        res[4] = lastCache[4] + after[4] - before[4]

        if lastCache[1] >= 2 and res[1] < 2: res[0] -= 500000
        if lastCache[2] >= 2 and res[2] < 2: res[0] += 500000

        if lastCache[1] < 2 and res[1] >= 2: res[0] += 500000
        if lastCache[2] < 2 and res[2] >= 2: res[0] -= 500000

        if lastCache[3] != res[3]: res[0] = res[0] - (lastCache[3] // 3) * 500 + (res[3] // 3) * 500
        if lastCache[4] != res[4]: res[0] = res[0] + (lastCache[4] // 3) * 500 - (res[4] // 3) * 500

        return res

    def computeBoardRabinKarp(self):
        h = self.horizontal()
        v = self.vertical()
        rd = self.right_diagonal()
        ld = self.left_diagonal()
        res = h[0] + v[0] + rd[0] + ld[0]
        cX2 = h[1] + v[1] + rd[1] + ld[1]
        cO2 = h[2] + v[2] + rd[2] + ld[2]
        cX3 = h[3] + v[3] + rd[3] + ld[3]
        cO3 = h[4] + v[4] + rd[4] + ld[4]

        return [res, cX2, cO2, cX3, cO3]

    def horizontal(self):
        x = self.move[0]
        y = self.move[1]
        b = self.board
        s = len(b)
        st = ""
        for i in range(y - 5, y + 6):
            if i < 0: continue
            if i >= s: break
            st += b[x][i]
        return rk(st)

    def vertical(self):
        x = self.move[0]
        y = self.move[1]
        b = self.board
        s = len(b)
        st = ""
        for i in range(x - 5, x + 6):
            if i < 0: continue
            if i >= s: break
            st += b[i][y]
        return rk(st)

    def left_diagonal(self):
        x = self.move[0] - 5
        y = self.move[1] - 5
        b = self.board
        s = len(b)
        st = ""
        for i in range(11):
            if x < 0 or y < 0:
                x += 1
                y += 1
                continue
            if x >= s or y >= s: break
            st += b[x][y]
            x += 1
            y += 1
        return rk(st)

    def right_diagonal(self):
        x = self.move[0] - 5
        y = self.move[1] + 5
        b = self.board
        s = len(b)
        st = ""
        for i in range(11):
            if x < 0 or y >= s:
                x += 1
                y -= 1
                continue
            if x >= s or y < 0:
                break
            st += b[x][y]
            x += 1
            y -= 1
        return rk(st)

def print_caro_table(board):
    size = len(board)
    for row in range(size):
        line = ""
        for col in range(size):
            if board[row][col] == ' ':
                line += "   "  # Use spaces for empty cells
            else:
                line += f" {board[row][col]} "  # Use the value from the board
            if col < size - 1:
                line += "|"  # Add vertical separator
        print(line)
        if row < size - 1:
            print("---" * size)  # Add horizontal separator