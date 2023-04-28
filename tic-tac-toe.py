from math import inf as infinity
import time
from os import system
import platform
from random import choice

"""
Build an AI algorithm for the famous tic-tac-toe game
"""

board = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
] # define the board
HUMAN = -1 # define human
COMP = +1 # define computer


def Evaluate(state):
    """
    Obtain the result by evaluating the given state
    Return +1 if computer wins, -1 if human wins, 0 if draw
    :param state: the state of the current board
    """
    if Wins(state, COMP):
        score = +1
    elif Wins(state, HUMAN):
        score = -1
    else:  
        score = 0
    return score


def Wins(state, player):
    """
    Judge if the given player wins by testing the given state
    8 states are considered to be winning:
    1. Three rows [X X X] or [O O O]
    2. Three columns [X X X] or [O O O]
    3. Two diagonals [X X X] or [O O O]
    :param state: the state of the current board
    :param player: the player, human or computer
    :return: true if the player wins, false or not
    """
    win_state = [
        [state[0][0], state[0][1], state[0][2]], # row 1
        [state[1][0], state[1][1], state[1][2]], # row 2
        [state[2][0], state[2][1], state[2][2]], # row 3
        [state[0][0], state[1][0], state[2][0]], # column 1
        [state[0][1], state[1][1], state[2][1]], # column 2
        [state[0][2], state[1][2], state[2][2]], # column 3
        [state[0][0], state[1][1], state[2][2]], # diagonal 1
        [state[2][0], state[1][1], state[0][2]], # diagonal 2
    ]
    if [player, player, player] in win_state:
        return True
    else:
        return False


def Gameover(state):
    """
    Judge if the human or the computer wins
    :param state: the state of the current board
    :return: true if human or the computer wins
    """
    return Wins(state, HUMAN) or Wins(state, COMP)


def Empty_cells(state):
    """
    Judge if the cell is empty and will be added to the empty list if it is
    :param state: the state of the current board
    :return: the list of the empty cell
    """
    cells = []
    for x, row in enumerate(state): # return the element along with its index
        for y, cell in enumerate(row): # return the element along with its index
            if cell == 0:
                cells.append([x, y])
    return cells


def Valid_move(x, y):
    """
    Judge whether the move is valid
    :param x: the x coordinate of the board
    :param y: the y coordinate of the board
    :return: true if the move is valid, false if not
    """
    if [x, y] in Empty_cells(board):
        return True
    else:
        return False


def Set_move(x, y, player):
    """
    Set the move on board if the coordinates are valid
    :param x: the x coordinate of the board
    :param y: the y coordinate of the board
    :param player: the player of the game, human or computer
    :return: true and set the current player
    """
    if Valid_move(x, y):
        board[x][y] = player
        return True
    else:
        return False


def minimax(state, depth, player):
    """
    AI algorithm for the computer to make the best move
    :param state: current state of the board
    :param depth: node index in the tree (0 <= depth <= 9),
    but never 9 in this case (see AI_turn() function)
    :param player: an human or a computer
    :return: a list with [the best row, best col, best score]
    """
    if player == COMP:
        best = [-1, -1, -infinity]
    else:
        best = [-1, -1, +infinity]

    if depth == 0 or Gameover(state):
        score = Evaluate(state)
        return [-1, -1, score]

    for cell in Empty_cells(state):
        x, y = cell[0], cell[1]
        state[x][y] = player
        score = minimax(state, depth - 1, -player)
        state[x][y] = 0
        score[0], score[1] = x, y

        if player == COMP:
            if score[2] > best[2]:
                best = score  # max value
        else:
            if score[2] < best[2]:
                best = score  # min value

    return best



def clean():
    """
    clear the console
    """
    os_name = platform.system().lower()
    if 'windows' in os_name:
        system('cls')
    else:
        system('clear')


def Render(state, computer_choice, human_choice):
    """
    Print the board on console
    """
    chars = {
        -1: human_choice,
        +1: computer_choice,
        0: ' '
    }
    str_line = '---------------'

    print('\n' + str_line)
    for row in state:
        for cell in row:
            symbol = chars[cell]
            print(f'| {symbol} |', end='')
        print('\n' + str_line)



def AI_turn(computer_choice, human_choice):
    """
    It calls the minimax function if the depth < 9,
    else it choices a random coordinate.
    :param computer_choice: computer's choice X or O
    :param human_choice: human's choice X or O
    :return:
    """
    depth = len(Empty_cells(board))
    if depth == 0 or Gameover(board):
        return
    clean()
    print(f'Computer turn [{computer_choice}]')
    Render(board, computer_choice, human_choice)

    if depth == 9:
        x = choice([0, 1, 2])
        y = choice([0, 1, 2])
    else:
        move = minimax(board, depth, COMP)
        x, y = move[0], move[1]

    Set_move(x, y, COMP)
    time.sleep(1)
    pass


def Human_turn(computer_choice, human_choice):
    """
    The Human plays choosing a valid move.
    :param c_choice: computer's choice X or O
    :param h_choice: human's choice X or O
    :return:
    """
    depth = len(Empty_cells(board))
    if depth == 0 or Gameover(board):
        return

    # Dictionary of valid moves
    move = -1
    moves = {
        1: [0, 0], 2: [0, 1], 3: [0, 2],
        4: [1, 0], 5: [1, 1], 6: [1, 2],
        7: [2, 0], 8: [2, 1], 9: [2, 2],
    }

    clean()
    print(f'Human turn [{human_choice}]')
    Render(board, computer_choice, human_choice)
    while move < 1 or move > 9:
        try:
            move = int(input('Use numpad (1..9): '))
            coord = moves[move]
            can_move = Set_move(coord[0], coord[1], HUMAN)

            if not can_move:
                print('Bad move')
                move = -1
        except (EOFError, KeyboardInterrupt):
            print('Bye')
            exit()
        except (KeyError, ValueError):
            print('Bad choice')
    pass


def main():
    clean()
    human_choice = ''  # X or O
    computer_choice = ''  # X or O
    first = ''  # if human is the first

    # human chooses X or O to play
    while human_choice != 'O' and human_choice != 'X':
        try:
            print('')
            human_choice = input('Choose X or O\nChosen: ').upper()
        except (EOFError, KeyboardInterrupt):
            print('Bye')
            exit()
        except (KeyError, ValueError):
            print('Bad choice')
    
    # Setting computer's choice
    if human_choice == 'X':
        computer_choice = 'O'
    else:
        computer_choice = 'X'
    
    # Human may starts first
    clean()
    while first != 'Y' and first != 'N':
        try:
            first = input('First to start?[y/n]: ').upper()
        except (EOFError, KeyboardInterrupt):
            print('Bye')
            exit()
        except (KeyError, ValueError):
            print('Bad choice')
    
    # main loop of the game
    while len(Empty_cells(board)) > 0 and not Gameover(board):
        if first == 'N':
            AI_turn(computer_choice, human_choice)
            first = ''
        Human_turn(computer_choice, human_choice)
        AI_turn(computer_choice, human_choice)
        
    
    # game over
    if Wins(board, HUMAN):
        clean()
        print(f'Human turn [{human_choice}]')
        Render(board, computer_choice, human_choice)
        print('YOU WIN!')
        
    elif Wins(board, COMP):
        clean()
        print(f'Computer turn [{computer_choice}]')
        Render(board, computer_choice, human_choice)
        print('YOU LOSE!')
    else:
        clean()
        Render(board, computer_choice, human_choice)
        print('DRAW!')
    exit()


if __name__ == '__main__':
    main()