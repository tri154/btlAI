import copy

WIN_SCORE = 100000000

transposition_table = {}

def generate_moves(board):
    move_list = []

    board_size = len(board)

    # Look for cells that has at least one stone in an adjacent cell.
    for i in range(board_size):
        for j in range(board_size):

            if board[i][j] != " ":
                continue

            if i != " ":
                if j != " ":
                    if board[i - 1][j - 1] != " " or board[i][j - 1] != " ":
                        move = [i, j]
                        move_list.append(move)
                        continue

                if j < board_size - 1:
                    if board[i - 1][j + 1] != " " or board[i][j + 1] != " ":
                        move = [i, j]
                        move_list.append(move)
                        continue

                if board[i - 1][j] != " ":
                    move = [i, j]
                    move_list.append(move)
                    continue

            if i < board_size - 1:
                if j != " ":
                    if board[i + 1][j - 1] != " " or board[i][j - 1] != " ":
                        move = [i, j]
                        move_list.append(move)
                        continue

                if j < board_size - 1:
                    if board[i + 1][j + 1] != " " or board[i][j + 1] != " ":
                        move = [i, j]
                        move_list.append(move)
                        continue

                if board[i + 1][j] != " ":
                    move = [i, j]
                    move_list.append(move)
                    continue

    return move_list


def get_consecutive_set_score(count, blocks, current_turn):
    win_guarantee = 1000000
    if blocks == 2 and count < 5:
        return 0

    if count == 5:
        return WIN_SCORE
    elif count == 4:
        if current_turn:
            return win_guarantee
        else:
            if blocks == 0:
                return win_guarantee / 4
            else:
                return 200
    elif count == 3:
        if blocks == 0:
            if current_turn:
                return 50000
            else:
                return 200
        else:
            if current_turn:
                return 10
            else:
                return 5
    elif count == 2:
        if blocks == 0:
            if current_turn:
                return 7
            else:
                return 5
        else:
            return 3
    elif count == 1:
        return 1

    return WIN_SCORE * 2

def evaluate_directions(board_matrix, i, j, is_bot, bots_turn, eval):
    if board_matrix[i][j] == ('o' if is_bot else 'x'):
        eval[0] += 1
    elif board_matrix[i][j] == ' ':
        if eval[0] > 0:
            eval[2] += get_consecutive_set_score(eval[0], eval[1], True if (is_bot == bots_turn) else False)
            eval[0] = 0
        eval[1] = 1
    else:
        if eval[0] > 0:
            eval[2] += get_consecutive_set_score(eval[0], eval[1], True if (is_bot == bots_turn) else False)
            eval[0] = 0
        eval[1] = 2



def evaluate_directions_after_one_pass(eval, is_bot, players_turn):
    if eval[0] > 0:
        eval[2] += get_consecutive_set_score(eval[0], eval[1], True if (is_bot == players_turn) else False)
    eval[0] = 0
    eval[1] = 2

def evaluate_horizontal(board_matrix, for_black, players_turn):
    evaluations = [0, 2, 0]

    for i in range(len(board_matrix)):
        for j in range(len(board_matrix[0])):
            evaluate_directions(board_matrix, i, j, for_black, players_turn, evaluations)
        evaluate_directions_after_one_pass(evaluations, for_black, players_turn)

    return evaluations[2]

def evaluate_vertical(board_matrix, for_black, players_turn):
    evaluations = [0, 2, 0]

    for j in range(len(board_matrix[0])):
        for i in range(len(board_matrix)):
            evaluate_directions(board_matrix, i, j, for_black, players_turn, evaluations)
        evaluate_directions_after_one_pass(evaluations, for_black, players_turn)

    return evaluations[2]

def evaluate_diagonal(board_matrix, for_black, players_turn):
    evaluations = [0, 2, 0]

    for k in range(2 * (len(board_matrix) - 1) + 1):
        i_start = max(0, k - len(board_matrix) + 1)
        i_end = min(len(board_matrix) - 1, k)
        for i in range(i_start, i_end + 1):
            evaluate_directions(board_matrix, i, k - i, for_black, players_turn, evaluations)
        evaluate_directions_after_one_pass(evaluations, for_black, players_turn)

    for k in range(1 - len(board_matrix), len(board_matrix)):
        i_start = max(0, k)
        i_end = min(len(board_matrix) + k - 1, len(board_matrix) - 1)
        for i in range(i_start, i_end + 1):
            evaluate_directions(board_matrix, i, i - k, for_black, players_turn, evaluations)
        evaluate_directions_after_one_pass(evaluations, for_black, players_turn)

    return evaluations[2]

def search_winning_move(board):
    all_possible_moves = generate_moves(board)
    winning_move = [None, None, None]

    for move in all_possible_moves:
        dummy_board = copy.deepcopy(board)
        add_stone_no_gui(dummy_board, move[0], move[1], False)

        if get_score(dummy_board, False, False) >= WIN_SCORE:
            winning_move[1] = move[0]
            winning_move[2] = move[1]
            return winning_move

    return None

def search_losing_move(board):
    all_possible_moves = generate_moves(board)
    losing_move = [None, None, None]

    for move in all_possible_moves:
        dummy_board = copy.deepcopy(board)
        add_stone_no_gui(dummy_board, move[0], move[1], True)

        if get_score(dummy_board, True, True) >= 50000:
            losing_move[1] = move[0]
            losing_move[2] = move[1]
            return losing_move

    return None

def evaluate_board_for_white(board, blacks_turn):
    black_score = get_score(board, True, blacks_turn)
    white_score = get_score(board, False, blacks_turn)

    if black_score == 0:
        black_score = 1.0

    return white_score / black_score

def get_score(board_matrix, for_black, blacks_turn):
    return (evaluate_horizontal(board_matrix, for_black, blacks_turn) +
            evaluate_vertical(board_matrix, for_black, blacks_turn) +
            evaluate_diagonal(board_matrix, for_black, blacks_turn))

def calculate_next_move(board, depth):
    move = [0, 0]

    best_move = search_winning_move(board)
    cps_move = search_losing_move(board)

    if best_move is not None:
        move[0] = best_move[1]
        move[1] = best_move[2]
    else:
        if cps_move is not None:
            move[0] = cps_move[1]
            move[1] = cps_move[2]
            return move
        else:
            best_move = minimax_search_ab(depth, copy.deepcopy(board), True, -1.0, WIN_SCORE)
            if best_move[1] is None:
                move = None
            else:
                move[0] = best_move[1]
                move[1] = best_move[2]

    return move

def minimax_search_ab(depth, dummy_board, max, alpha, beta):
    # board_tuple = tuple(map(tuple, dummy_board))
    # if board_tuple in transposition_table:
    #     return transposition_table[board_tuple]

    if depth == 0:
        score = evaluate_board_for_white(dummy_board, not max)
        # transposition_table[board_tuple] = [score, None, None]
        return [evaluate_board_for_white(dummy_board, not max), None, None]

    all_possible_moves = generate_moves(dummy_board)

    if len(all_possible_moves) == 0:
        score = evaluate_board_for_white(dummy_board, not max)
        # transposition_table[board_tuple] = [score, None, None]
        return [evaluate_board_for_white(dummy_board, not max), None, None]

    best_move = [None, None, None]

    if max:
        best_move[0] = -1.0
        for move in all_possible_moves:
            add_stone_no_gui(dummy_board, move[0], move[1], False)
            temp_move = minimax_search_ab(depth - 1, dummy_board, False, alpha, beta)
            remove_stone_no_gui(dummy_board, move[0], move[1])

            if temp_move[0] > alpha:
                alpha = temp_move[0]

            if temp_move[0] >= beta:
                # transposition_table[board_tuple] = temp_move
                return temp_move

            if temp_move[0] > best_move[0]:
                best_move = temp_move
                best_move[1] = move[0]
                best_move[2] = move[1]
                print(best_move)
    else:
        best_move[0] = 100000000.0
        best_move[1] = all_possible_moves[0][0]
        best_move[2] = all_possible_moves[0][1]

        for move in all_possible_moves:
            add_stone_no_gui(dummy_board, move[0], move[1], True)
            temp_move = minimax_search_ab(depth - 1, dummy_board, True, alpha, beta)
            remove_stone_no_gui(dummy_board, move[0], move[1])

            if temp_move[0] < beta:
                beta = temp_move[0]

            if temp_move[0] <= alpha:
                # transposition_table[board_tuple] = temp_move
                return temp_move

            if temp_move[0] < best_move[0]:
                best_move = temp_move
                best_move[1] = move[0]
                best_move[2] = move[1]
                print(best_move)

    # transposition_table[board_tuple] = best_move
    return best_move

def add_stone_no_gui(board, x, y, is_black):
    board[x][y] = 'o' if is_black else 'x'

def remove_stone_no_gui(board, x, y):
    board[x][y] = ' '

# def print_caro_table(board):
#     size = len(board)

#     # Print column headers
#     print("   " + " ".join([f"{i:2}" for i in range(size)]))

#     # Print each row with row headers
#     for i in range(size):
#         row = board[i]
#         print(f"{i:2} " + " ".join(row))



# tb = [
#     [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
#     [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
#     [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
#     [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
#     [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
#     [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
#     [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
#     [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
#     [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
#     [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x', ' ', ' ', ' ', ' ', ' ', ' '],
#     [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
#     [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
#     [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
#     [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'o', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
#     [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
#     [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
#     [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
#     [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
#     [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
# ]

# move = calculate_next_move(tb, 4)
# tb[int(move[0])][int(move[1])] = 'o'
# print(move)
# print_caro_table(tb)
# print(len(tb))