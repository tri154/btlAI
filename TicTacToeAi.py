import heapq
import time
global max_depth, hashT, HEURISTIC_SOCRES, R, Q, R5, R6, A, B, cacheT, count, count_leaf, count_id, delay_time, total
total = 0
delay_time = 0
count_id = 0
cacheT = dict()
A = 3
B = 5
count = 0
count_leaf = 0

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
    for i in range(len(s)):
        count += 1
        c = s[i]
        if count < 5:
            h = (h * R + ord(c)) % Q
        if count == 5:
            h = (h * R + ord(c)) % Q
            value = hashT.get(h)
            if value != None:
                res += value
        if count == 6:
            h = (h * R + ord(c)) % Q
            value = hashT.get(h)
            if value != None:
                res += value
            if i == len(s) - 1:
                h = (h + Q - R6 * ord(s[i - 5]) % Q) % Q
                value = hashT.get(h)
                if value != None:
                    res += value
        if count > 6:
            h = (h + Q - R6 * ord(s[i - 6]) % Q) % Q
            value = hashT.get(h)
            if value != None:
                res += value
            h = (h * R + ord(c)) % Q
            value = hashT.get(h)
            if value != None:
                res += value
            if i == len(s) - 1:
                h = (h + Q - R6 * ord(s[i - 5]) % Q) % Q
                value = hashT.get(h)
                if value != None:
                    res += value
    return res

def compute(b):
    lines = get_all_lines(b)
    res = 0
    for i in lines:
        res += rk(i)
    return res
def brute_force(s):
    res = 0
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
    return res
HEURISTIC_SCORES = {
        "ooooo": -1000000000000,
        "xxxxx": 1000000000000,
        " oooo ": -50000000000,
        " xxxx ": 10000000000,


        "oxxxx ": 100000000,
        " xxxxo": 100000000,
        " xxx ": 1000,

        " oooox": -500000000,
        "xoooo ": -500000000,
        " ooo ": -5000,


        " xxxo": 150,
        "oxxx ": 150,
        " ooox": -50,
        "xooo ": -50,
        # " xx  ": 10,
        # "  xx ": 10,
        # " oo ": -50
    }
# hashT = {
#     6628 : float("-inf"),
#     22020 : float("inf"),
#     19967 : float("-inf"),
#     7869 : float("inf"),
#     8361 : 100000000,
#     7948 : 100000000,
#     20055 : -100000000,
#     15645 : -100000000,
#     2841 : 1000,
#     2920 : 150,
#     8425 : 150,
#     1053 : -150,
#     20056 : -150,
#     965 : -1000,
# }
hashT = {
    6628 : float("-inf"),
    22020 : float("inf"),
    19967 : float("-inf"),
    7869 : float("inf"),
    8361 : 100000000.1,
    7948 : 100000000.1,
    20055 : -100000001,
    15645 : -100000001,
    2841 : 1000.1,
    2920 : 150,
    8425 : 150,
    1053 : -150,
    20056 : -150,
    965 : -1001,
}
R = 256
R5 = 16768
R6 = 5572

Q = 27481
# def toHash(str):
#     t  = 0
#     for c in str:
#         t = (R * t + ord(c)) % Q
#     return t


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

# print(pow(R, 4) % Q)
# print(pow(R, 5) % Q)
def init_node(board):
    init = node()
    init.id = get_id(board)
    init.children = get_children(board)
    init.cache = compute(board)
    init.board = board
    init.depth = 0
    return init

def move_as_o(board):
    size = len(board)
    init = init_node(board)
    next_action = None
    value = float("inf")
    alpha = float("-inf")
    beta = float("inf")
    lres = list()
    cres = list()

    # l = list(init.children)
    # for c in l:
    #     cur = node('o', c, init.cache, init.id, init) # role o as min value
    #     cres.append((cur.move, cur.cache))
    #     t = cur.max_value(alpha, beta)
    #     lres.append((c, t))
    #     if t < value:
    #         value = t
    #         next_action = c
    #     beta = min(beta, t)
    #     if value == float("-inf"): break

    l = list()
    for c in init.children:
        cur = node('o', c, init.cache, init.id, init)
        l.append(cur)
    heapq.heapify(l)
    while len(l) != 0:
        cur = heapq.heappop(l)
        cres.append((cur.move, cur.cache))
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
    print("cache hit: " + str(count_leaf - count_id))
    return next_action

def move_as_x(board):
    size = len(board)
    init = init_node(board)
    next_action = None
    value = float("-inf")
    alpha = float("-inf")
    beta = float("inf")
    lres = list()
    cres = list()

    # l = list(init.children)
    # for c in l:
    #     cur = node('x', c, init.cache, init.id, init)
    #     cres.append((cur.move, cur.cache))
    #     t = cur.min_value(alpha, beta)
    #     lres.append((c, t))
    #     if t > value:
    #         value = t
    #         next_action = c
    #     alpha = max(alpha, t)
    #     if value == float("inf"): break

    l = list()
    for c in init.children:
        cur = node('x', c, init.cache, init.id, init, True)
        l.append(cur)
    heapq.heapify(l)
    while len(l) != 0:
        cur = heapq.heappop(l)
        cres.append((cur.move, -cur.cache))
        t = cur.min_value(alpha, beta)
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
    print("cache hit: " + str(count_leaf - count_id))
    return next_action

def get_move(board, size):
    return move_as_o(board)

    # move_as_o
    # move_as_x



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
    for i in range(size):
        for j in range(size):
            char = board[i][j]
            res += ord(char) * pow(A, i) * pow(B, j)
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
        self.id = lastID - ord(' ')*pow(A, x)*pow(B, y) + ord(self.role)*pow(A, x)*pow(B, y)

        # if self.depth == max_depth:
        #     self.cache = cacheT.get(self.id)
        #     if self.cache is None:
        #         count_id += 1
        #         self.cache = self.computeCache(lastCache)
        #         cacheT[self.id] = self.cache
        #     else:
        #         self.board[x][y] = self.role
        #         testValue = compute(self.board)
        #         if testValue != self.cache:
        #             print_caro_table(self.board)
        #             print(testValue)
        #             print(self.cache)
        #             print(self.id)
        #             input()
        #         self.board[x][y] = ' '


        # else:
        self.cache = self.computeCache(lastCache)
            # self.cache = self.computeCache(lastCache)
        self.reverse = reverse
        if reverse:
            self.cache = -self.cache

    def __lt__(self, other):
        return self.cache < other.cache
    def restore(self):
        self.board[self.move[0]][self.move[1]] = ' '
        for i in self.to_remove:
            self.children.remove(i)
        self.children.add(self.move)

    def min_value(self, alpha, beta):
        if self.reverse: self.cache = -self.cache
        if self.depth == max_depth:
            global count_leaf
            count_leaf += 1
            return self.cache
        if self.cache == float("inf"):
            return self.cache

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
                li.append(node('o', c, self.cache, self.id, self))
            heapq.heapify(li)
            while len(li) != 0:
                cur = heapq.heappop(li)
                t = cur.max_value(alpha, beta)
                value = min(value, t)
                beta = min(beta, t)
                if alpha >= beta:
                    break
        else:
            li = list(self.children)
            for c in li:
                cur = node('o', c, self.cache, self.id, self)
                # cur = node('o', c, self.board, self.children, self.depth + 1, len(self.board), self.cache, self.id)
                t = cur.max_value(alpha, beta)
                value = min(value, t)
                beta = min(beta, t)
                if alpha >= beta:
                    break

        self.restore()
        return value

    def max_value(self, alpha, beta):
        if self.reverse: self.cache = -self.cache
        if self.depth == max_depth:
            global count_leaf
            count_leaf += 1
            return self.cache
        if self.cache == float("-inf"):
            return self.cache

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
                li.append(node('x', c, self.cache, self.id, self, True))
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
                # cur = node('x', c, self.board, self.children, self.depth + 1, len(self.board), self.cache, self.id)
                cur = node('x', c, self.cache, self.id, self)
                t = cur.min_value(alpha, beta)
                value = max(value, t)
                alpha = max(alpha, t)
                if alpha >= beta:
                    break
        self.restore()
        return value
    def computeCache(self, lastCache):
        start = time.time()
        x = self.move[0]
        y = self.move[1]

        before = self.computeBoardRabinKarp()

        self.board[x][y] = self.role

        after = self.computeBoardRabinKarp()

        # test_value = compute(self.board)
        self.board[x][y] = ' '
        # if test_value != lastCache + after - before:
        #     print(lastCache)
        #     print(after)
        #     print(before)
        #     print_caro_table(self.board)
        #     self.board[x][y] = self.role
        #     print()
        #     print_caro_table(self.board)
        #     self.board[x][y] = ' '
        #     print(test_value)
        #     print("error")
        #     input()
        diff = time.time() - start
        print("{:.10f}".format(diff))
        global delay_time
        delay_time += diff

        return lastCache + after - before

    def computeBoardRabinKarp(self):
        h = self.horizontal()
        v = self.vertical()
        rd = self.right_diagonal()
        ld = self.left_diagonal()
        return h + v + rd + ld

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
        value = rk(st)
        # if value != brute_force(st):
        #     print("error")
        return rk(st)

        # for i in range(y - 5, y + 6):
        #     if i < 0: continue
        #     if i >= s:
        #         if count >= 6:
        #             h = (h + Q - R6 * ord(b[x][i - 6]) % Q) % Q
        #             value = hashT.get(h)
        #             if value != None:
        #                 res += value
        #     count += 1
        #     c = b[x][i]
        #     if count < 5:
        #         h = (h * R + ord(c)) % Q
        #     if count == 5:
        #         h = (h * R + ord(c)) % Q
        #         value = hashT.get(h)
        #         if value != None:
        #             res += value
        #     if count == 6:
        #         h = (h * R + ord(c)) % Q
        #         value = hashT.get(h)
        #         if value != None:
        #             res += value
        #         if i == y + 5:
        #             h = (h + Q - R6 * ord(b[x][i - 5]) % Q) % Q
        #             value = hashT.get(h)
        #             if value != None:
        #                 res += value
        #     if count > 6:
        #         h = (h + Q - R6 * ord(b[x][i - 6]) % Q) % Q
        #         value = hashT.get(h)
        #         if value != None:
        #             res += value
        #         h = (h * R + ord(c)) % Q
        #         value = hashT.get(h)
        #         if value != None:
        #             res += value
        #         if i == y + 5:
        #             h = (h + Q - R6 * ord(b[x][i - 5]) % Q) % Q
        #             value = hashT.get(h)
        #             if value != None:
        #                 res += value

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

# test
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
tb = [
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', 'o', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', 'o', 'x', 'x', 'x', 'x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', 'o', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', 'o', ' ', 'o', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']

]
# max_depth = 5
# start = time.time()
# move = get_move(tb, 20)
# print(move)
# print(time.time() - start)
# print(count)
# print(count_leaf)
# tb[move[0]][move[1]] = 'o'
# print_caro_table(tb)
# print(delay_time)
# print(count_id)

# # print(compute(tb))
#
# chars = ['x', 'o', ' ']
# def generate_random_pat(size):
#     row = [random.choice(chars) for _ in range(size)]
#     return ''.join(row)
#
# print(compute(tb))
# get_all_lines(tb)
# print(generate_random_pat(20))
# count = 0
# for i in range(100000):
#     s = generate_random_pat(7)
#     if (rk(s) != brute_force(s)):
#         print("error: " + s)
#         count+=1
#
# print(count)
#
# s = "xooxoooooo   o  xxxo"
# print(rk(s))
# print(brute_force(s))

# [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
# [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
# [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
# [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
# [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
# [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
# [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'o', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
# [' ', ' ', ' ', ' ', ' ', 'x', 'o', 'o', 'o', 'o', 'x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
# [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'o', 'x', 'x', 'x', 'x', 'o', ' ', ' ', ' ', ' ', ' ', ' '],
# [' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x', ' ', 'o', 'x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
# [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
# [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'o', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
# [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
# [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
# [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
# [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
# [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
# [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
# [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
# [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']