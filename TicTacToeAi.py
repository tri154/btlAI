import copy
import random
import time
global max_depth, hashT, HEURISTIC_SOCRES, R, Q, R4, R5, R6, count, count_leaf, delay_time
max_depth = 6
delay_time = 0

HEURISTIC_SCORES = {
'ooooox' : -1000000000001,
'ooooo ' : -1000000000001,
'xooooo' : -1000000000001,
' ooooo' : -1000000000001,
'xxxxxo' : 1000000000001,
'xxxxx ' : 1000000000001,
'oxxxxx' : 1000000000001,
' xxxxx' : 1000000000001,
' oooo ' : -10000000002,
' xxxx ' : 10000000002,
'oxxxx ' : 100000000,
' xxxxo' : 100000000,
' oooox' : -100000000,
'xoooo ' : -100000000,
' xxx x' : 1000,
' xxx o' : 1000,
' xxx  ' : 1000,
'x xxx ' : 1000,
'o xxx ' : 1000,
'  xxx ' : 1000,
' ooo x' : -1000,
' ooo o' : -1000,
' ooo  ' : -1000,
'x ooo ' : -1000,
'o ooo ' : -1000,
'  ooo ' : -1000,
' xxxox' : 150,
' xxxoo' : 150,
' xxxo ' : 150,
'x xxxo' : 150,
'  xxxo' : 150,
' oooxx' : -150,
' oooxo' : -150,
' ooox ' : -150,
'o ooox' : -150,
'  ooox' : -150,
'oxxx x' : 150,
'oxxx  ' : 150,
'xoxxx ' : 150,
'ooxxx ' : 150,
' oxxx ' : 150,
'oxxx ' : 150,
'xooo o' : -150,
'xooo  ' : -150,
'xxooo ' : -150,
'oxooo ' : -150,
' xooo ' : -150,
'xooo ' : -150,
' xx  x' : 10,
' xx  o' : 10,
' xx   ' : 10,
'x xx  ' : 10,
'o xx  ' : 10,
' xx  ' : 10,
'  xx x' : 10,
'  xx o' : 10,
'  xx  ' : 10,
'x  xx ' : 10,
'o  xx ' : 10,
'   xx ' : 10,
'  xx ' : 10,
' oo  x' : -10,
' oo  o' : -10,
' oo   ' : -10,
'x oo  ' : -10,
'o oo  ' : -10,
' oo  ' : -10,
'  oo x' : -10,
'  oo o' : -10,
'  oo  ' : -10,
'x  oo ' : -10,
'o  oo ' : -10,
'   oo ' : -10,
'  oo ' : -10,
}
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
# hashT = {
# #     6628 : -1000000000001,
# # 22020 : 1000000000001,
#     6628 : float("-inf"),
#     22020 : float("inf"),
#     19967 : -10000000002,
#     7869 : 10000000002,
#     8361 : 100000000,
#     7948 : 100000000,
#     20055 : -100000000,
#     15645 : -100000000,
#     2841 : 1000,
#     965 : -1000,
#     2920 : 150,
#     1053 : -150,
#     8425 : 150,
#     20056 : -150,
#     7794 : 10,
#     24558 : 10,
#     8222 : -10,
#     9531 : -10,
# }
hashT = {
    20547 : float("-inf"),
    20459 : float("-inf"),
    15724 : float("-inf"),
    20046 : float("-inf"),
    3626 : float("inf"),
    3547 : float("inf"),
    8449 : float("inf"),
    7957 : float("inf"),
    19967 : -10000000002,
    7869 : 10000000002,
    8361 : 100000000,
    7948 : 100000000,
    20055 : -100000000,
    15645 : -100000000,
    12910 : 1000,
    12901 : 1000,
    12822 : 1000,
    11937 : 1000,
    16751 : 1000,
    16259 : 1000,
    27312 : -1000,
    27303 : -1000,
    27224 : -1000,
    10061 : -1000,
    14875 : -1000,
    14383 : -1000,
    5653 : 150,
    5644 : 150,
    5565 : 150,
    12016 : 150,
    16338 : 150,
    22359 : -150,
    22350 : -150,
    22271 : -150,
    14963 : -150,
    14471 : -150,
    13402 : 150,
    13314 : 150,
    17521 : 150,
    22335 : 150,
    21843 : 150,
    8425 : 150,
    22981 : -150,
    22902 : -150,
    1671 : -150,
    6485 : -150,
    5993 : -150,
    20056 : -150,
    16752 : 10,
    16743 : 10,
    16664 : 10,
    16890 : 10,
    21704 : 10,
    7794 : 10,
    21300 : 10,
    21291 : 10,
    21212 : 10,
    6173 : 10,
    10987 : 10,
    10495 : 10,
    24558 : 10,
    16396 : -10,
    16387 : -10,
    16308 : -10,
    17318 : -10,
    22132 : -10,
    8222 : -10,
    21728 : -10,
    21719 : -10,
    21640 : -10,
    18627 : -10,
    23441 : -10,
    22949 : -10,
    9531 : -10,
}
R = 256
# R6 = 205707292
# R5 = 102220456
# R4 = 128109484
R6 = 5572
# R5 = 16768

# R4 = 16777216
Q = 27481

# def toHash(str):
#     t  = 0
#     for c in str:
#         t = (R * t + ord(c)) % Q
#     return t
#

# for key in HEURISTIC_SCORES:
#     t = toHash(key)
#     # if len(key) == 5:
#     #     print("\'" + key + "x" + "\'" + " : " + str(HEURISTIC_SCORES[key]) + ", ")
#     #     print("\'" + key + "o" + "\'" + " : " + str(HEURISTIC_SCORES[key]) + ", ")
#     #     print("\'" + key + " " + "\'" + " : " + str(HEURISTIC_SCORES[key]) + ", ")
#     #     print("\'" + "x" + key + "\'" + " : " + str(HEURISTIC_SCORES[key]) + ", ")
#     #     print("\'" + "o" + key + "\'" + " : " + str(HEURISTIC_SCORES[key]) + ", ")
#     #     print("\'" + " " + key + "\'" + " : " + str(HEURISTIC_SCORES[key]) + ", ")
#     # print("\'" + key + "\'" + " : " + str(HEURISTIC_SCORES[key]) + ", ")
#     print(str(t) + " : " + str(HEURISTIC_SCORES[key]) + ",")


# print(pow(R, 5) % Q)
# print(pow(R, 4) % Q)


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
    testList = list(children)
    # testList.remove((6, 9))
    # testList.insert(0, (6, 9))
    for c in testList:
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
        # start = time.time()
        global count
        count += 1
        # print(str(count) + " depth: " + str(depth))
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
        # diff = time.time() - start
        # print("init = " + '{0:.30f}'.format(diff))
        # global delay_time
        # delay_time += diff

    def restore(self):
        # start = time.time()
        self.board[self.move[0]][self.move[1]] = ' '
        for i in self.to_remove:
            self.children.remove(i)
        self.children.add(self.move)
        # diff = time.time() - start
        # print("restore = " + '{0:.30f}'.format(diff))
        # global delay_time
        # delay_time += diff
    def min_value(self, alpha, beta):
        if self.depth == max_depth:
            global count_leaf
            count_leaf += 1
            return self.cache
            # t = self.compute()
            # self.restore()
            # return t
        if self.cache == float("-inf"):
            self.restore()
            return self.cache
        value = float("inf")
        l = list(self.children)
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
            global count_leaf
            count_leaf += 1
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
        # start = time.time()
        x = self.move[0]
        y = self.move[1]

        before = self.computeBoardRabinKarp()
        # before = self.computeBoardSubString()

        self.board[x][y] = self.role

        after = self.computeBoardRabinKarp()
        # after = self.computeBoardSubString()

        self.board[x][y] = ' '
        # diff = time.time() - start
        # print("restore = " + '{0:.30f}'.format(diff))
        # global delay_time
        # delay_time += diff
        return lastCache + after - before
    # def computeBoardSubString(self):
    #     x = self.move[0]
    #     y = self.move[1]
    #     b = self.board
    #     s = len(b)
    #


    def computeBoardRabinKarp(self):
        h = self.horizontal()
        v = self.vertical()
        # start = time.time()
        rd = self.right_diagonal()
        ld = self.left_diagonal()
        # diff = time.time() - start
        # print("restore = " + '{0:.30f}'.format(diff))
        # global delay_time
        # delay_time += diff
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
            # if count < 5: t5 = (R * t5 + ord(char)) % Q
            # if count >= 5:
            #     if count == 5:
            #         t5 = (R * t5 + ord(char)) % Q
            #     else:
            #         t5 = (t5 + Q - R5 * ord(b[x][j - 5]) % Q) % Q
            #         t5 = (t5 * R + ord(char)) % Q
            #     if (t5 in hashT): res += hashT[t5]
            #
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

            # if count < 5: t5 = (R * t5 + ord(char)) % Q
            # if count >= 5:
            #     if count == 5:
            #         t5 = (R * t5 + ord(char)) % Q
            #     else:
            #         t5 = (t5 + Q - R5 * ord(b[i - 5][y]) % Q) % Q
            #         t5 = (t5 * R + ord(char)) % Q
            #     if (t5 in hashT): res += hashT[t5]

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

            # if count < 5: t5 = (R * t5 + ord(char)) % Q
            # if count >= 5:
            #     if count == 5:
            #         t5 = (R * t5 + ord(char)) % Q
            #     else:
            #         t5 = (t5 + Q - R5 * ord(b[i - 5][j - 5]) % Q) % Q
            #         t5 = (t5 * R + ord(char)) % Q
            #     if (t5 in hashT): res += hashT[t5]

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

            # if count < 5: t5 = (R * t5 + ord(char)) % Q
            # if count >= 5:
            #     if count == 5:
            #         t5 = (R * t5 + ord(char)) % Q
            #     else:
            #         t5 = (t5 + Q - R5 * ord(b[i + 5][j + 5]) % Q) % Q
            #         t5 = (t5 * R + ord(char)) % Q
            #     if (t5 in hashT): res += hashT[t5]

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
start = time.time()
move = get_move(tb, 20)
print(move)
print(time.time() - start)
print(count)
print(count_leaf)
tb[move[0]][move[1]] = 'o'
print_caro_table(tb)
print(delay_time)


# t = 10000000000000000
# print(type(t))
# c = 's'
# while True:
#     start = time.time()
#     t *= 100
#     diff = time.time() - start
#     # print(str(t) + " = " + '{0:.30f}'.format(diff))
#     if diff > 0.0000008:
#         print(str(t) + " = " + '{0:.30f}'.format(diff))
#         input()