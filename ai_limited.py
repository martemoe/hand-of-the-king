#from sys import ps1

#from sklearn.preprocessing import PolynomialFeatures
from hand_of_the_king import getvalidmoves
import pdb
import random
import math

ROWS = 6
COLS = 6
COLORS = 8 

def get_computer_move(board, cards, banners, turn):
    print("Hello")
    return minimax(board,turn,cards)
    

def minimax(board, player,card):
    print(board)
    actions = getvalidmoves(board)
    next,cards = simulateboard(board, actions[0],card[player])

    heu = 0

    for i in cards:
        heu += i

    best = actions[0]
    value = minvalue(board,player,best,card)

    for action in actions:
        v = minvalue(board,player,best,card)

        if v > value:
            best = action
            value = v

    return best

#minvalue of the moves
def minvalue(board,player,action,card):
    state = board.copy()
    print(player)
    next,cards = simulateboard(state,action,card[player])

    heu = 0

    for i in cards:
        heu += i

    card[player] = cards

    nextplayer = 1 - player

    if len(getvalidmoves(next)) == 0:
        return heu

    value = math.inf

    for action in getvalidmoves(next):
        if maxvalue(next,nextplayer,action,card) > value:
            break
        value = min(value, maxvalue(next,nextplayer,action,card))

    return value


#Maxvalue of the moves
def maxvalue(board,player,action,card):
    state = board.copy()
    print(player)
    next,cards = simulateboard(state,action,card[player])

    heu = 0

    for i in cards:
        heu += i

    card[player] = cards
    nextplayer = 1 - player

    if len(getvalidmoves(next)) == 0:
        return heu

    value = -math.inf

    for action in getvalidmoves(next):
        value = min(value, minvalue(next,nextplayer,action,card))

    return value

#Simulate the move done to get the next state of the board and the cards won by the player
def simulateboard(board, action, cards):
    
    x1 = board.index(1)  # index of the 1-card on the board
    # print(f'moving from {x1} to {x}')

    # Remove captured cards from board

    print(action)
    color = board[action]  # color of the main captured card

    board[action] = 1  # the 1-card moves here

    #print("other")
    #print(color-2)
    #print(len(cards))
    #print(cards)
    cards[color - 2] += 1


    if abs(action - x1) < COLS:  # move is either left or right
        
        if action < x1:  # left
            possible = range(action + 1, x1)
        else:  # right
            possible = range(x1 + 1, action)
    else:  # move is either up or down
        
        if action < x1:  # up
            possible = range(action + COLS, x1, COLS)
        else:  # down
            possible = range(x1 + COLS, action, COLS)

    for i in possible:
        if board[i] == color:
            if i == action:
                continue


            board[i] = 0  # there is no card in this position anymore
            #print("loop")
            cards[color - 2] += 1

    # Move the 1-card to the correct position
    
    board[action] = 1
    board[x1] = 0

    print(board)

    board[action] = 1
    
    return board,cards


def simulateheuristics():
    pass