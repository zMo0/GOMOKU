"""Gomoku starter code
You should complete every incomplete function,
and add more functions and variables as needed.
Note that incomplete functions have 'pass' as the first statement:
pass is a Python keyword; it is a statement that does nothing.
This is a placeholder that you should remove once you modify the function.
Author(s): Michael Guerzhoy with tests contributed by Siavash Kazemian.  Last modified: Oct. 26, 2020
"""
import copy

def is_empty(board):
    for i in range (0, len(board)):
        for a in range (0, len(board[0])):
            if board[i][a] != ' ':
                return False
    
    return True
    
    
def is_bounded(board, y_end, x_end, length, d_y, d_x):
    if d_y == 0:
        if x_end+1 >= len(board[0]) or x_end - length < 0 :
            if (x_end+1 >= len(board[0]) and board[y_end][x_end - length] == ' ') or (x_end - length < 0 and board[y_end][x_end+1] == ' '):
                return "SEMIOPEN"
            else: 
                return "CLOSED"

        elif board[y_end][x_end + 1] == ' ' and board[y_end][x_end-length] == ' ':
            return "OPEN"

        elif board[y_end][x_end + 1] == ' ' or board[y_end][x_end-length] == ' ':
            return "SEMIOPEN"

        else:
            return "CLOSED"

    elif d_x == 0:
        if y_end + 1 >= len(board) or y_end - length < 0:
            if (y_end + 1 >= len(board) and board[y_end - length][x_end] == ' ') or (y_end - length < 0 and board[y_end + 1][x_end] == ' '):
                return "SEMIOPEN"
            
            else: 
                return "CLOSED"
            
        elif board[y_end - length][x_end] == ' ' and board[y_end + 1][x_end] == ' ' :
            return "OPEN"

        elif board[y_end - length][x_end] == ' ' or board[y_end + 1][x_end] == ' ' :
            return "SEMIOPEN"
        
        else:
            return "CLOSED"
    
    elif d_x == -1 :
        if x_end - 1 < 0 or y_end + 1 == len(board):
            if (y_end - length > -1 and x_end + length < len(board[0])):
                if board[y_end - length][x_end + length] == ' ':
                    return "SEMIOPEN"
                else: return "CLOSED"
            else:
                return "CLOSED"
        
        elif x_end + length >= len(board[0]) or y_end - length < 0 :
            if y_end + 1 < len(board) and x_end - 1 > -1:
                if board[y_end + 1][x_end - 1] == ' ':
                    return "SEMIOPEN"
                else: 
                    return "CLOSED"
            else: return "CLOSED"

        elif board[y_end - length][x_end + length] == ' ' and board[y_end + 1][x_end - 1] == ' ':
            return "OPEN"
        
        elif board[y_end - length][x_end + length] == ' ' or board[y_end + 1][x_end - 1] == ' ':
            return "SEMIOPEN"
        
        else: 
            return "CLOSED"
    
    else:
        if x_end + 1 == len(board) or y_end + 1 == len(board) :
            if x_end-length >= 0 and y_end - length >= 0 :
                if board[y_end-length][x_end-length] == ' ':
                    return "SEMIOPEN"
                else:
                    return "CLOSED"
            else: 
                return "CLOSED"

        elif x_end - length <= -1 or y_end - length <= -1:
            if x_end + 1 <= len(board[0]) and y_end + 1 <= len(board):
                if board[y_end+1][x_end + 1] == ' ':
                    return "SEMIOPEN"
                else:
                    return "CLOSED"
            else: 
                return "CLOSED"
        
        elif board[y_end + 1][x_end + 1] == ' ' and board[y_end-length][x_end - length] == ' ':
            return "OPEN"
        
        elif board[y_end + 1][x_end + 1] == ' ' or board[y_end-length][x_end - length] == ' ':
            return "SEMIOPEN"
        
        else:
            return "CLOSED"


    
def detect_row(board, col, y_start, x_start, length, d_y, d_x):
    Open= Semi = count = 0
    for a in range (0,len(board)):
        if (y_start + d_y * a > -1 and y_start + d_y * a< len(board)) and (x_start + d_x * a > -1 and x_start + d_x * a < len(board)):
            if board[y_start + d_y * a][x_start + d_x * a] == col:
                count += 1
            else:
                count = 0
            num1 = y_start + d_y * (a+1)
            num2 = x_start + d_x * (a+1)
            out_of_range = num1< 0 or num2 < 0 or num1 >= len(board) or num2>= len(board[0])
            if count ==  length and (not out_of_range):
                if board[num1][num2] != col: 
                    if is_bounded(board, y_start + d_y * a, x_start + d_x * a, length, d_y, d_x) == 'OPEN':
                        Open += 1
                    elif is_bounded(board, y_start + d_y * a, x_start + d_x * a, length, d_y, d_x) == 'SEMIOPEN':
                        Semi += 1
                    count = 0
            elif count ==  length and out_of_range:
                if is_bounded(board, y_start + d_y * a, x_start + d_x * a, length, d_y, d_x) == 'SEMIOPEN':
                    Semi += 1
                count = 0
        else:
            break
    return Open, Semi
    
def detect_rows(board, col, length):
    open_seq_count = 0
    semi_open_seq_count = 0

    for y in range (0, len(board)):
        open_seq_count += detect_row(board, col, y, 0, length, 0, 1)[0]
        semi_open_seq_count += detect_row(board, col, y, 0, length, 0, 1)[1]

        open_seq_count += detect_row(board, col, y, 0, length, 1, 1)[0]
        semi_open_seq_count += detect_row(board, col, y, 0, length, 1, 1)[1]

    for x in range (0, len(board[0])):
        open_seq_count += detect_row(board, col, 0, x, length, 1, 0)[0]
        semi_open_seq_count += detect_row(board, col, 0, x, length, 1, 0)[1]

        open_seq_count += detect_row(board, col, 0, x, length, 1, -1)[0]
        semi_open_seq_count += detect_row(board, col, 0, x, length, 1, -1)[1]

    for y in range (1, len(board)):
        open_seq_count += detect_row(board, col, y, len(board[0]) - 1, length, 1, -1)[0] 
        semi_open_seq_count += detect_row(board, col, y, len(board[0]) - 1 , length, 1, -1)[1]
    
    for x in range (1, len(board[0])):
        open_seq_count += detect_row(board, col, 0, x, length, 1, 1)[0] 
        semi_open_seq_count += detect_row(board, col, 0, x, length, 1, 1)[1]

    return open_seq_count, semi_open_seq_count
    
def search_max(board):
    max_score = None
    move_x = None
    move_y = None
    board_replica = []
    for i in range (0, len(board)):
        for a in range(0, len(board[0])):
            board_replica = copy.deepcopy(board)
            if board[i][a] == " ":
                board_replica[i][a] = 'b'
                if max_score == None or score(board_replica) > max_score:
                    move_y = i
                    move_x = a
                    max_score = score(board_replica)     

    return move_y, move_x
    
def score(board):
    MAX_SCORE = 100000
    
    open_b = {}
    semi_open_b = {}
    open_w = {}
    semi_open_w = {}
    
    for i in range(2, 6):
        open_b[i], semi_open_b[i] = detect_rows(board, "b", i)
        open_w[i], semi_open_w[i] = detect_rows(board, "w", i)
        
    
    if open_b[5] >= 1 or semi_open_b[5] >= 1:
        return MAX_SCORE
    
    elif open_w[5] >= 1 or semi_open_w[5] >= 1:
        return -MAX_SCORE
        
    return (-10000 * (open_w[4] + semi_open_w[4])+ 
            500  * open_b[4]                     + 
            50   * semi_open_b[4]                + 
            -100  * open_w[3]                    + 
            -30   * semi_open_w[3]               + 
            50   * open_b[3]                     + 
            10   * semi_open_b[3]                +  
            open_b[2] + semi_open_b[2] - open_w[2] - semi_open_w[2])

    
def is_win(board):
    if detect_rows(board, 'w', 5) != (0,0) or closed_five_row(board,'w'):
        return "White won"
    if detect_rows(board, 'b', 5) != (0,0) or closed_five_row(board,'b'):
        return 'Black won'

    else:
        for i in range (0, len(board)):
            for a in range (0, len(board[0])):
                if board[i][a] == ' ':
                    return "Continue playing"
        
        return "Draw"

def closed_five_row(board, col):
    for y in range (0, len(board)):
        if detect_row_5close(board, col, y, 0, 5, 0, 1) or\
        detect_row_5close(board, col, y, 0, 5, 1, 1):
            return True

    for x in range (0, len(board[0])):
        if detect_row_5close(board, col, 0, x, 5, 1, 0)or\
        detect_row_5close(board, col, 0, x, 5, 1, -1):
            return True

    for y in range (1, len(board)):
        if detect_row_5close(board, col, y, len(board[0]) - 1, 5, 1, -1):
            return True
    
    for x in range (1, len(board[0])):
        if detect_row_5close(board, col, 0, x, 5, 1, 1):
            return True
            
def detect_row_5close(board, col, y_start, x_start, length, d_y, d_x):
    count = 0
    for a in range (0,len(board)):
        if (y_start + d_y * a > -1 and y_start + d_y * a< len(board)) and (x_start + d_x * a > -1 and x_start + d_x * a < len(board)):
            if board[y_start + d_y * a][x_start + d_x * a] == col:
                count += 1
            else:
                count = 0
            num1 = y_start + d_y * (a+1)
            num2 = x_start + d_x * (a+1)
            out_of_range = num1< 0 or num2 < 0 or num1 >= len(board) or num2>= len(board[0])
            if count ==  length and (not out_of_range):
                if board[num1][num2] != col: 
                    if is_bounded(board, y_start + d_y * a, x_start + d_x * a, length, d_y, d_x) == 'CLOSED':
                        return True
            elif count ==  length and out_of_range:
                if is_bounded(board, y_start + d_y * a, x_start + d_x * a, length, d_y, d_x) == 'CLOSED':
                    return True
        else:
            break
    return False

def print_board(board):
    
    s = "*"
    for i in range(len(board[0])-1):
        s += str(i%10) + "|"
    s += str((len(board[0])-1)%10)
    s += "*\n"
    
    for i in range(len(board)):
        s += str(i%10)
        for j in range(len(board[0])-1):
            s += str(board[i][j]) + "|"
        s += str(board[i][len(board[0])-1]) 
    
        s += "*\n"
    s += (len(board[0])*2 + 1)*"*"
    
    print(s)
    

def make_empty_board(sz):
    board = []
    for i in range(sz):
        board.append([" "]*sz)
    return board
                

def analysis(board):
    for c, full_name in [["b", "Black"], ["w", "White"]]:
        print("%s stones" % (full_name))
        for i in range(2, 6):
            open, semi_open = detect_rows(board, c, i);
            print("Open rows of length %d: %d" % (i, open))
            print("Semi-open rows of length %d: %d" % (i, semi_open))
    
def play_gomoku(board_size):
    board = make_empty_board(board_size)
    board_height = len(board)
    board_width = len(board[0])
    
    while True:
        print_board(board)
        if is_empty(board):
            move_y = board_height // 2
            move_x = board_width // 2
        else:
            move_y, move_x = search_max(board)
            
        print("Computer move: (%d, %d)" % (move_y, move_x))
        board[move_y][move_x] = "b"
        print_board(board)
        analysis(board)
        
        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res
            
        
        print("Your move:")
        move_y = int(input("y coord: "))
        move_x = int(input("x coord: "))
        board[move_y][move_x] = "w"
        print_board(board)
        analysis(board)
        
        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res
        
            
            
def put_seq_on_board(board, y, x, d_y, d_x, length, col):
    for i in range(length):
        board[y][x] = col        
        y += d_y
        x += d_x


def test_is_empty():
    board  = make_empty_board(8)
    if is_empty(board):
        print("TEST CASE for is_empty PASSED")
    else:
        print("TEST CASE for is_empty FAILED")

def test_is_bounded():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    
    y_end = 3
    x_end = 5

    if is_bounded(board, y_end, x_end, length, d_y, d_x) == 'OPEN':
        print("TEST CASE for is_bounded PASSED")
    else:
        print("TEST CASE for is_bounded FAILED")


def test_detect_row():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_row_5close(board, "w", 0,x,length,d_y,d_x) == (1,0):
        print("TEST CASE for detect_row PASSED")
    else:
        print("TEST CASE for detect_row FAILED")

def test_detect_rows():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_rows(board, col,length) == (1,0):
        print("TEST CASE for detect_rows PASSED")
    else:
        print("TEST CASE for detect_rows FAILED")

def test_search_max():
    board = make_empty_board(8)
    x = 5; y = 0; d_x = 0; d_y = 1; length = 4; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    x = 6; y = 0; d_x = 0; d_y = 1; length = 4; col = 'b'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    print_board(board)
    if search_max(board) == (4,6):
        print("TEST CASE for search_max PASSED")
    else:
        print("TEST CASE for search_max FAILED")

def easy_testset_for_main_functions():
    test_is_empty()
    test_is_bounded()
    test_detect_row()
    test_detect_rows()
    test_search_max()

def some_tests():
    board = make_empty_board(8)

    # board[0][5] = "w"
    # board[0][6] = "b"
    # y = 5; x = 2; d_x = 0; d_y = 1; length = 3
    # put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    # print_board(board)
    # analysis(board)
    #
    # # Expected output:
    # #       *0|1|2|3|4|5|6|7*
    # #       0 | | | | |w|b| *
    # #       1 | | | | | | | *
    # #       2 | | | | | | | *
    # #       3 | | | | | | | *
    # #       4 | | | | | | | *
    # #       5 | |w| | | | | *
    # #       6 | |w| | | | | *
    # #       7 | |w| | | | | *
    # #       *****************
    # #       Black stones:
    # #       Open rows of length 2: 0
    # #       Semi-open rows of length 2: 0
    # #       Open rows of length 3: 0
    # #       Semi-open rows of length 3: 0
    # #       Open rows of length 4: 0
    # #       Semi-open rows of length 4: 0
    # #       Open rows of length 5: 0
    # #       Semi-open rows of length 5: 0
    # #       White stones:
    # #       Open rows of length 2: 0
    # #       Semi-open rows of length 2: 0
    # #       Open rows of length 3: 0
    # #       Semi-open rows of length 3: 1
    # #       Open rows of length 4: 0
    # #       Semi-open rows of length 4: 0
    # #       Open rows of length 5: 0
    # #       Semi-open rows of length 5: 0
    #
    # y = 3; x = 5; d_x = -1; d_y = 1; length = 2
    #
    # put_seq_on_board(board, y, x, d_y, d_x, length, "b")
    # print_board(board)
    # analysis(board)
    #
    # # Expected output:
    # #        *0|1|2|3|4|5|6|7*
    # #        0 | | | | |w|b| *
    # #        1 | | | | | | | *
    # #        2 | | | | | | | *
    # #        3 | | | | |b| | *
    # #        4 | | | |b| | | *
    # #        5 | |w| | | | | *
    # #        6 | |w| | | | | *
    # #        7 | |w| | | | | *
    # #        *****************
    # #
    # #         Black stones:
    # #         Open rows of length 2: 1
    # #         Semi-open rows of length 2: 0
    # #         Open rows of length 3: 0
    # #         Semi-open rows of length 3: 0
    # #         Open rows of length 4: 0
    # #         Semi-open rows of length 4: 0
    # #         Open rows of length 5: 0
    # #         Semi-open rows of length 5: 0
    # #         White stones:
    # #         Open rows of length 2: 0
    # #         Semi-open rows of length 2: 0
    # #         Open rows of length 3: 0
    # #         Semi-open rows of length 3: 1
    # #         Open rows of length 4: 0
    # #         Semi-open rows of length 4: 0
    # #         Open rows of length 5: 0
    # #         Semi-open rows of length 5: 0
    # #
    #
    # y = 5; x = 3; d_x = -1; d_y = 1; length = 1
    # put_seq_on_board(board, y, x, d_y, d_x, length, "b");
    # print_board(board);
    # analysis(board);
    #
    # #        Expected output:
    # #           *0|1|2|3|4|5|6|7*
    # #           0 | | | | |w|b| *
    # #           1 | | | | | | | *
    # #           2 | | | | | | | *
    # #           3 | | | | |b| | *
    # #           4 | | | |b| | | *
    # #           5 | |w|b| | | | *
    # #           6 | |w| | | | | *
    # #           7 | |w| | | | | *
    # #           *****************
    # #
    # #
    # #        Black stones:
    # #        Open rows of length 2: 0
    # #        Semi-open rows of length 2: 0
    # #        Open rows of length 3: 0
    # #        Semi-open rows of length 3: 1
    # #        Open rows of length 4: 0
    # #        Semi-open rows of length 4: 0
    # #        Open rows of length 5: 0
    # #        Semi-open rows of length 5: 0
    # #        White stones:
    # #        Open rows of length 2: 0
    # #        Semi-open rows of length 2: 0
    # #        Open rows of length 3: 0
    # #        Semi-open rows of length 3: 1
    # #        Open rows of length 4: 0
    # #        Semi-open rows of length 4: 0
    # #        Open rows of length 5: 0
    # #        Semi-open rows of length 5: 0
    #
    # board[3][3]=board[4][4]=board[5][5]=board[6][6]=board[2][2]='w'
    # board[1][1]=board[7][7]='b'
    # print_board(board);
    # analysis(board);
    # print(is_win(board))

    board = make_empty_board(15)
    for i in range (6,11):
        board[9][i] = 'w'
    
    board = [[' ', ' ', 'w', ' ', ' ', 'b', ' ', 'b'], [' ', ' ', 'w', ' ', 'b', 'b', 'w', 'w'], [' ', 'b', 'w', ' ', 'b', 'b', 'b', 'b'], ['w', ' ', 'w', 'b', ' ', ' ', 'w', ' '], ['w', ' ', 'b', ' ', ' ', ' ', ' ', 'w'], ['w', 'b', 'b', ' ', ' ', ' ', 'b', 'w'], ['w', 'w', 'w', 'w', 'w', 'w', 'w', 'w'], ['b', ' ', 'w', ' ', ' ', ' ', 'b', 'b']]
    analysis(board);
    print(is_win(board))
    print_board(board)





            
if __name__ == '__main__':
    #print(play_gomoku(15))
    some_tests()
