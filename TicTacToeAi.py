import copy
import random
import time
global max_depth, hashT, HEURISTIC_SOCRES, R, Q, R4, R5, R6, A, B, cacheT, count, count_leaf, count_id, delay_time
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
        " oooox": -500000000,
        "xoooo ": -500000000,
        " xxx ": 1000,
        " xxxo": 150,
        " ooox": -50,
        " ooo ": -5000,
        # " xx  ": 10,
        # "  xx ": 10,
        # " oo ": -50
    }
hashT = {
6628 : -1000000000000,
22020 : 1000000000000,
19967 : -50000000000,
7869 : 10000000000,
8361 : 100000000,
7948 : 100000000,
20055 : -500000000,
15645 : -500000000,
2841 : 1000,
2920 : 150,
1053 : -50,
965 : -5000,
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


def get_move(board, size):
    # Find all available positions on the board
    size = int(size)
    children = get_children(board, size)
    id = get_id(board, size)
    next_action = None
    value = float("inf") # role o as min value
    # value = float("-inf") # role x as max value
    alpha = float("-inf")
    beta = float("inf")
    lres = list()
    testList = list(children)
    lastCache = compute(board)
    for c in testList:
        cur = node('o', c, board, children, 1, size, lastCache, id) # role o as min value
        t = cur.max_value(alpha, beta)
        lres.append((c, t))
        if t < value:
            value = t
            next_action = c
        beta = min(beta, t)
        # if value == float("-inf"): break

        # cur = node('x', c, board, children, 1, size) # role x as max value
        # t = cur.min_value(alpha, beta)
        # if (t > value):
        #     value = t
        #     next_action = c
        # alpha = max(alpha, t)
        # if value == float("inf"): break
    print(value)
    print(lres)
    return next_action


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
def get_children(board, size):
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

def get_id(board, size):
    res = 0
    for i in range(size):
        for j in range(size):
            char = board[i][j]
            res += ord(char) * pow(A, i) * pow(B, j)
    return res;

class node:
    def __init__(self, role, move, board, children, depth, size, lastCache, lastID):
        global count_id
        global count
        count += 1
        print(str(count) + " depth: " + str(depth))
        self.role = role
        self.move = move
        x = move[0]
        y = move[1]
        self.board = board
        self.depth = depth
        self.id = lastID - ord(' ')*pow(A, x)*pow(B, y) + ord(self.role)*pow(A, x)*pow(B, y)
        if depth == max_depth:
            self.cache = cacheT.get(self.id)
            if (self.cache == None):
                count_id += 1
                self.cache = self.computeCache(lastCache)
                cacheT[self.id] = self.cache
        else:
        # self.cache = self.computeCache(lastCache)
            self.cache = self.computeCache(lastCache)
        if depth == max_depth: return
        board[x][y] = role
        self.children = children
        self.children.remove((x, y))
        self.to_remove = list()
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if i < 0 or i >= size: continue
                if j < 0 or j >= size: continue
                if board[i][j] == ' ':
                    if not((i, j) in self.children):
                        self.children.add((i, j))
                        self.to_remove.append((i, j))

    def restore(self):
        self.board[self.move[0]][self.move[1]] = ' '
        for i in self.to_remove:
            self.children.remove(i)
        self.children.add(self.move)

    def min_value(self, alpha, beta):
        if self.depth == max_depth:
            global count_leaf
            count_leaf += 1
            return self.cache
        if self.cache == float("-inf"):
            self.restore()
            return self.cache
        value = float("inf")
        l = list(self.children)
        for c in l:
            cur = node('o', c, self.board, self.children, self.depth + 1, len(self.board), self.cache, self.id)
            t = cur.max_value(alpha, beta)
            value = min(value, t)
            beta = min(beta, t)
            if alpha >= beta:
                break

        self.restore()
        return value

    def max_value(self, alpha, beta):
        if self.depth == max_depth:
            global count_leaf
            count_leaf += 1
            return self.cache
        if self.cache == float("inf"):
            self.restore()
            return self.cache

        value = float("-inf")
        l = list(self.children)
        for c in l:
            cur = node('x', c, self.board, self.children, self.depth + 1, len(self.board), self.cache, self.id)
            t = cur.min_value(alpha, beta)
            value = max(value, t)
            alpha = max(alpha, t)
            if (alpha >= beta):
                break
        self.restore()
        return value
    def computeCache(self, lastCache):
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
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'o', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', 'o', ' ', 'x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'o', 'x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', 'o', 'x', 'x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
]
max_depth = 6
start = time.time()
move = get_move(tb, 20)
print(move)
print(time.time() - start)
print(count)
print(count_leaf)
tb[move[0]][move[1]] = 'o'
print_caro_table(tb)
print(delay_time)
print(count_id)

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



# Ví dụ sử dụng
# board = [
#     [1, 2, 3, 4, 5, 6, 7],
#     [8, 9, 10, 11, 12, 13, 14],
#     [15, 16, 17, 18, 19, 20, 21],
#     [22, 23, 24, 25, 26, 27, 28],
#     [29, 30, 31, 32, 33, 34, 35],
#     [36, 37, 38, 39, 40, 41, 42],
#     [43, 44, 45, 46, 47, 48, 49]
# ]
# #
# all_lines = get_all_lines(tb)
# for line in all_lines:
#     print(line)
