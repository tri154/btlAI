import copy
import random
import time
global max_depth, hashT, HEURISTIC_SOCRES, R, Q, R4, R5, R6, count, count_leaf
max_depth = 6

# HEURISTIC_SCORES = {
#         "ooooo": -1000000000001,
#         "xxxxx": 1000000000001,
#         " oooo ": -10000000002,
#         " xxxx ": 10000000002,
#         "oxxxx ": 100000000,
#         " xxxxo": 100000000,
#         " oooox": -100000000,
#         "xoooo ": -100000000,
#         " xxx ": 1000,
#         " ooo ": -1000,
#         " xxxo": 150,
#         " ooox": -150,
#         "oxxx ": 150,
#         "xooo ": -150,
#         " xx  ": 10,
#         "  xx ": 10,
#         " oo  ": -10,
#         "  oo ": -10,
# }
count = 0
count_leaf = 0
hashT = {
    # 63350523 : -1000000000001,
    # 85812864 : 1000000000001,
    63350523 : float("-inf"),
    85812864 : float("inf"),
    129129796 : -10000000002,
    151592128 : 10000000002,
    213820052 : 100000000,
    151592207 : 100000000,
    129129884 : -100000000,
    149759252 : -100000000,
    30641524 : 1000,
    199581976 : -1000,
    30641603 : 150,
    199582064 : -150,
    214937516 : 150,
    254753228 : -150,
    30618996 : 10,
    156884136 : 10,
    199561752 : -10,
    156292008 : -10,
}
R = 256
# R6 = 205707292
# R5 = 102220456
# R4 = 128109484
R6 = 102220456
R5 = 128109484
# R4 = 16777216
Q = 320527524
# for key in HEURISTIC_SCORES:
#     t  = 0
#     for c in key:
#         t = (R * t + ord(c)) % Q
#     print(str(t) + " : " + str(HEURISTIC_SCORES[key]) + ",")

# print(pow(R, 5) % Q)
# print(pow(R, 4) % Q)
# print(pow(R, 3) % Q)


def get_move(board, size):
    # Find all available positions on the board
    size = int(size)
    children = get_children(board, size)
    next_action = None
    value = float("inf") # role o as min value
    # value = float("-inf") # role x as max value
    alpha = float("-inf")
    beta = float("inf")
    lres = list()
    for c in list(children):
        cur = node('o', c, board, children, 1, size, 0) # role o as min value
        t = cur.max_value(alpha, beta)
        lres.append((c, t))
        if (t < value):
            value = t
            next_action = c
        beta = min(beta, t)
        if value == float("-inf"): break

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
class node:
    def __init__(self, role, move, board, children, depth, size, lastCache):
        start = time.time()
        global count
        count += 1
        print(str(count) + " depth: " + str(depth))
        self.role = role
        self.move = move
        x = move[0]
        y = move[1]
        self.board = board
        self.depth = depth
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
        diff =time.time() - start
        print("init = " + '{0:.30f}'.format(diff))
        if diff > 0.001:
            print_caro_table(self.board)
            input()
    def restore(self):
        self.board[self.move[0]][self.move[1]] = ' '
        for i in self.to_remove:
            self.children.remove(i)
        self.children.add(self.move)
    def min_value(self, alpha, beta):
        if self.depth == max_depth:
            return self.cache
            # t = self.compute()
            # self.restore()
            # return t
        if self.cache == float("-inf"):
            self.restore()
            return self.cache
        value = float("inf")
        # start = time.time()
        l = list(self.children)
        # print("copy list = " + '{0:.30f}'.format(time.time() - start))
        for c in l:
            cur = node('o', c, self.board, self.children, self.depth + 1, len(self.board), self.cache)
            t = cur.max_value(alpha, beta)
            value = min(value, t)
            beta = min(beta, t)
            if (alpha >= beta):
                break
        self.restore()
        return value

    def max_value(self, alpha, beta):
        if self.depth == max_depth:
            return self.cache
            # t = self.compute()
            # # self.restore()
            # return t
        if self.cache == float("inf"):
            self.restore()
            return self.cache

        value = float("-inf")
        # start = time.time()
        l = list(self.children)
        # print("copy list = " + '{0:.30f}'.format(time.time() - start))
        for c in l:
            cur = node('x', c, self.board, self.children, self.depth + 1, len(self.board), self.cache)
            t = cur.min_value(alpha, beta)
            value = max(value, t)
            alpha = max(alpha, t)
            if (alpha >= beta):
                break
        self.restore()
        # if value == float("inf"):
        #     print_caro_table(self.board)
        #     input()
        return value
    def computeCache(self, lastCache):
        x = self.move[0]
        y = self.move[1]

        before = self.computeBoard()

        self.board[x][y] = self.role

        after = self.computeBoard()

        self.board[x][y] = ' '

        return lastCache + after - before
    def computeBoard(self):
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
        res = 0
        count = 0
        t5 = 0
        t6 = 0
        for j in range(y - 5, y + 6):
            if j < 0: continue
            if j >= s: return res
            char = b[x][j]
            count+=1

            if count < 5: t5 = (R * t5 + ord(char)) % Q
            if count >= 5:
                if count == 5:
                    t5 = (R * t5 + ord(char)) % Q
                else:
                    t5 = (t5 + Q - R5 * ord(b[x][j - 5]) % Q) % Q
                    t5 = (t5 * R + ord(char)) % Q
                if (t5 in hashT): res += hashT[t5]

            if count < 6: t6 = (R * t6 + ord(char)) % Q
            if count >= 6:
                if count == 6:
                    t6 = (R * t6 + ord(char)) % Q
                else:
                    t6 = (t6 + Q - R6 * ord(b[x][j - 6]) % Q) % Q
                    t6 = (t6 * R + ord(char)) % Q
                if (t6 in hashT): res += hashT[t6]
        return res

    def vertical(self):
        x = self.move[0]
        y = self.move[1]
        b = self.board
        s = len(b)
        res = 0
        count = 0
        t5 = 0
        t6 = 0
        for i in range(x - 5, x + 6):
            if i < 0: continue
            if i >= s: return res
            char = b[i][y]
            count += 1

            if count < 5: t5 = (R * t5 + ord(char)) % Q
            if count >= 5:
                if count == 5:
                    t5 = (R * t5 + ord(char)) % Q
                else:
                    t5 = (t5 + Q - R5 * ord(b[i - 5][y]) % Q) % Q
                    t5 = (t5 * R + ord(char)) % Q
                if (t5 in hashT): res += hashT[t5]

            if count < 6: t6 = (R * t6 + ord(char)) % Q
            if count >= 6:
                if count == 6:
                    t6 = (R * t6 + ord(char)) % Q
                else:
                    t6 = (t6 + Q - R6 * ord(b[i - 6][y]) % Q) % Q
                    t6 = (t6 * R + ord(char)) % Q
                if (t6 in hashT): res += hashT[t6]
        return res

    def left_diagonal(self):
        x = self.move[0] - 5
        y = self.move[1] - 5
        b = self.board
        s = len(b)
        res = 0
        t5 = 0
        t6 = 0
        for count in range(1, 12):
            i = x + count
            j = y + count
            if i < 0 or j < 0: continue
            if i >= s or j >= s: return res
            char = b[i][j]

            if count < 5: t5 = (R * t5 + ord(char)) % Q
            if count >= 5:
                if count == 5:
                    t5 = (R * t5 + ord(char)) % Q
                else:
                    t5 = (t5 + Q - R5 * ord(b[i - 5][j - 5]) % Q) % Q
                    t5 = (t5 * R + ord(char)) % Q
                if (t5 in hashT): res += hashT[t5]

            if count < 6: t6 = (R * t6 + ord(char)) % Q
            if count >= 6:
                if count == 6:
                    t6 = (R * t6 + ord(char)) % Q
                else:
                    t6 = (t6 + Q - R6 * ord(b[i - 6][j - 6]) % Q) % Q
                    t6 = (t6 * R + ord(char)) % Q
                if (t6 in hashT): res += hashT[t6]
        return res


    def right_diagonal(self):
        x = self.move[0] + 5
        y = self.move[1] + 5
        b = self.board
        s = len(b)
        res = 0
        t5 = 0
        t6 = 0
        for count in range(1, 12):
            i = x - count
            j = y - count
            if i < 0 or j < 0: continue
            if i >= s or j >= s: return res
            char = b[i][j]

            if count < 5: t5 = (R * t5 + ord(char)) % Q
            if count >= 5:
                if count == 5:
                    t5 = (R * t5 + ord(char)) % Q
                else:
                    t5 = (t5 + Q - R5 * ord(b[i + 5][j + 5]) % Q) % Q
                    t5 = (t5 * R + ord(char)) % Q
                if (t5 in hashT): res += hashT[t5]

            if count < 6: t6 = (R * t6 + ord(char)) % Q
            if count >= 6:
                if count == 6:
                    t6 = (R * t6 + ord(char)) % Q
                else:
                    t6 = (t6 + Q - R6 * ord(b[i + 6][j + 6]) % Q) % Q
                    t6 = (t6 * R + ord(char)) % Q
                if (t6 in hashT): res += hashT[t6]
        return res
    # def compute(self):
    #     global count_leaf
    #     count_leaf += 1
    #     self.board[self.move[0]][self.move[1]] = self.role
    #     start = time.time()
    #     b = self.board
    #     s = len(b)
    #     v = self.vertical_compute(b, s)
    #
    #     h = self.horizontal_compute(b, s)
    #
    #     rd = self.right_diagonal_compute(b, s)
    #
    #     ld = self.left_diagonal_compute(b, s)
    #     print("compute = " + '{0:.30f}'.format(time.time() - start))
    #     # print("compute = " + str(time.monotonic() - start) )
    #     self.board[self.move[0]][self.move[1]] = ' '
    #     return v + h + rd + ld

    # def left_diagonal_compute(self, b, s):
    #     j = 4
    #     i = s - 1
    #     ld = 0
    #     while j < s:
    #         t4 = t5 = t6 = 0
    #         for c in range(j + 1):
    #             char = b[i - c][j - c]
    #
    #             if c < 3: t4 = (R * t4 + ord(char)) % Q
    #             if c >= 3:
    #                 if c == 3:
    #                     t4 = (R * t4 + ord(char)) % Q
    #                 else:
    #                     t4 = (t4 + Q - R4 * ord(b[i - c + 4][j - c + 4]) % Q) % Q
    #                     t4 = (t4 * R + ord(char)) % Q
    #                 if t4 in hashT: ld += hashT[t4]
    #
    #             if c < 4: t5 = (R * t5 + ord(char)) % Q
    #             if c >= 4:
    #                 if c == 4:
    #                     t5 = (R * t5 + ord(char)) % Q
    #                 else:
    #                     t5 = (t5 + Q - R5 * ord(b[i - c + 5][j - c + 5]) % Q) % Q
    #                     t5 = (t5 * R + ord(char)) % Q
    #                 if (t5 in hashT): ld += hashT[t5]
    #
    #             if c < 5: t6 = (R * t6 + ord(char)) % Q
    #             if c >= 5:
    #                 if c == 5:
    #                     t6 = (R * t6 + ord(char)) % Q
    #                 else:
    #                     t6 = (t6 + Q - R6 * ord(b[i - c + 6][j - c + 6]) % Q) % Q
    #                     t6 = (t6 * R + ord(char)) % Q
    #                 if (t6 in hashT): ld += hashT[t6]
    #         j += 1
    #     j -= 1
    #     i -= 1
    #     while i > 3:
    #         t4 = t5 = t6 =0
    #         for c in range(i + 1):
    #             char = b[i - c][j - c]
    #
    #             if c < 3: t4 = (R * t4 + ord(char)) % Q
    #             if c >= 3:
    #                 if c == 3:
    #                     t4 = (R * t4 + ord(char)) % Q
    #                 else:
    #                     t4 = (t4 + Q - R4 * ord(b[i - c + 4][j - c + 4]) % Q) % Q
    #                     t4 = (t4 * R + ord(char)) % Q
    #                 if (t4 in hashT): ld += hashT[t4]
    #
    #             if c < 4: t5 = (R * t5 + ord(char)) % Q
    #             if c >= 4:
    #                 if c == 4:
    #                     t5 = (R * t5 + ord(char)) % Q
    #                 else:
    #                     t5 = (t5 + Q - R5 * ord(b[i - c + 5][j - c + 5]) % Q) % Q
    #                     t5 = (t5 * R + ord(char)) % Q
    #                 if (t5 in hashT): ld += hashT[t5]
    #
    #             if c < 5: t6 = (R * t6 + ord(char)) % Q
    #             if c >= 5:
    #                 if c == 5:
    #                     t6 = (R * t6 + ord(char)) % Q
    #                 else:
    #                     t6 = (t6 + Q - R6 * ord(b[i - c + 6][j - c + 6]) % Q) % Q
    #                     t6 = (t6 * R + ord(char)) % Q
    #                 if (t6 in hashT): ld += hashT[t6]
    #         i -= 1
    #     return ld
    #
    # def right_diagonal_compute(self, b, s):
    #     i = 0
    #     j = 4
    #     rd = 0
    #     while j < s:
    #         t4 = t5 = t6 = 0
    #         for c in range(j + 1):
    #             char = b[i + c][j - c]
    #
    #             if c < 3: t4 = (R * t4 + ord(char)) % Q
    #             if c >= 3:
    #                 if c == 3:
    #                     t4 = (R * t4 + ord(char)) % Q
    #                 else:
    #                     t4 = (t4 + Q - R4 * ord(b[i + c - 4][j - c + 4]) % Q) % Q
    #                     t4 = (t4 * R + ord(char)) % Q
    #                 if (t4 in hashT): rd += hashT[t4]
    #
    #             if c < 4: t5 = (R * t5 + ord(char)) % Q
    #             if c >= 4:
    #                 if c == 4:
    #                     t5 = (R * t5 + ord(char)) % Q
    #                 else:
    #                     t5 = (t5 + Q - R5 * ord(b[i + c - 5][j - c + 5]) % Q) % Q
    #                     t5 = (t5 * R + ord(char)) % Q
    #                 if (t5 in hashT): rd += hashT[t5]
    #
    #             if c < 5: t6 = (R * t6 + ord(char)) % Q
    #             if c >= 5:
    #                 if c == 5:
    #                     t6 = (R * t6 + ord(char)) % Q
    #                 else:
    #                     t6 = (t6 + Q - R6 * ord(b[i + c - 6][j - c + 6]) % Q) % Q
    #                     t6 = (t6 * R + ord(char)) % Q
    #                 if (t6 in hashT): rd += hashT[t6]
    #         j += 1
    #     j -= 1
    #     while i < s - 4:
    #         t4 = t5 = t6 = 0
    #         for c in range(s - i):
    #             char = b[i + c][j - c]
    #
    #             if c < 3: t4 = (R * t4 + ord(char)) % Q
    #             if c >= 3:
    #                 if c == 3:
    #                     t4 = (R * t4 + ord(char)) % Q
    #                 else:
    #                     t4 = (t4 + Q - R4 * ord(b[i + c - 4][j - c + 4]) % Q) % Q
    #                     t4 = (t4 * R + ord(char)) % Q
    #                 if (t4 in hashT): rd += hashT[t4]
    #
    #             if c < 4: t5 = (R * t5 + ord(char)) % Q
    #             if c >= 4:
    #                 if c == 4:
    #                     t5 = (R * t5 + ord(char)) % Q
    #                 else:
    #                     t5 = (t5 + Q - R5 * ord(b[i + c - 5][j - c + 5]) % Q) % Q
    #                     t5 = (t5 * R + ord(char)) % Q
    #                 if (t5 in hashT): rd += hashT[t5]
    #
    #             if c < 5: t6 = (R * t6 + ord(char)) % Q
    #             if c >= 5:
    #                 if c == 5:
    #                     t6 = (R * t6 + ord(char)) % Q
    #                 else:
    #                     t6 = (t6 + Q - R6 * ord(b[i + c - 6][j - c + 6]) % Q) % Q
    #                     t6 = (t6 * R + ord(char)) % Q
    #                 if (t6 in hashT): rd += hashT[t6]
    #         i += 1
    #     return rd
    #
    # def vertical_compute(self, b, s):
    #     h = 0
    #     for i in range(s):
    #         t4 = t5 = t6 = 0
    #         for j in range(s):
    #             c = b[j][i]
    #             if j < 3: t4 = (R * t4 + ord(c)) % Q
    #             if j >= 3:
    #                 if j == 3:
    #                     t4 = (R * t4 + ord(c)) % Q
    #                 else:
    #                     t4 = (t4 + Q - R4 * ord(b[j - 4][i]) % Q) % Q
    #                     t4 = (t4 * R + ord(c)) % Q
    #                 if (t4 in hashT): h += hashT[t4]
    #
    #             if j < 4: t5 = (R * t5 + ord(c)) % Q
    #             if j >= 4:
    #                 if j == 4:
    #                     t5 = (R * t5 + ord(c)) % Q
    #                 else:
    #                     t5 = (t5 + Q - R5 * ord(b[j - 5][i]) % Q) % Q
    #                     t5 = (t5 * R + ord(c)) % Q
    #                 if (t5 in hashT): h += hashT[t5]
    #
    #             if j < 5: t6 = (R * t6 + ord(c)) % Q
    #             if j >= 5:
    #                 if j == 5:
    #                     t6 = (R * t6 + ord(c)) % Q
    #                 else:
    #                     t6 = (t6 + Q - R6 * ord(b[j - 6][i]) % Q) % Q
    #                     t6 = (t6 * R + ord(c)) % Q
    #                 if (t6 in hashT): h += hashT[t6]
    #     return h
    #
    # def horizontal_compute(self, b, s):
    #     v = 0
    #     for i in range(s):
    #         t4 = t5 = t6 = 0
    #         for j in range(s):
    #             c = b[i][j]
    #             if j < 3: t4 = (R * t4 + ord(c)) % Q
    #             if j >= 3:
    #                 if j == 3:
    #                     t4 = (R * t4 + ord(c)) % Q
    #                 else:
    #                     t4 = (t4 + Q - R4 * ord(b[i][j - 4]) % Q) % Q
    #                     t4 = (t4 * R + ord(c)) % Q
    #                 if (t4 in hashT): v += hashT[t4]
    #
    #             if j < 4: t5 = (R * t5 + ord(c)) % Q
    #             if j >= 4:
    #                 if j == 4:
    #                     t5 = (R * t5 + ord(c)) % Q
    #                 else:
    #                     t5 = (t5 + Q - R5 * ord(b[i][j - 5]) % Q) % Q
    #                     t5 = (t5 * R + ord(c)) % Q
    #                 if (t5 in hashT): v += hashT[t5]
    #
    #             if j < 5: t6 = (R * t6 + ord(c)) % Q
    #             if j >= 5:
    #                 if j == 5:
    #                     t6 = (R * t6 + ord(c)) % Q
    #                 else:
    #                     t6 = (t6 + Q - R6 * ord(b[i][j - 6]) % Q) % Q
    #                     t6 = (t6 * R + ord(c)) % Q
    #                 if (t6 in hashT): v += hashT[t6]
    #     return v
    #
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
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'o', 'o', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'o', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'o', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
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
# start = time.time()
# move = get_move(tb, 20)
# print(move)
# print(time.time() - start)
# print(count)
# print(count_leaf)
# tb[move[0]][move[1]] = 'o'


# print_caro_table(tb)
t = 10000000
c = 's'
while True:
    start = time.time()
    c *= 10
    diff = time.time() - start
    print("init = " + '{0:.30f}'.format(diff))
    if diff > 0.001:
        input()
