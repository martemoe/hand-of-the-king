#from sys import ps1

#from sklearn.preprocessing import PolynomialFeatures
from hand_of_the_king import getvalidmoves
import pdb
import random
import math

ROWS = 6
COLS = 6
COLORS = 8 
MAXDEPTH = 5
MIN = 0
MaxValue = 0

# Starting method
def get_computer_move(board, cards, banners, turn):
    
    #Calling the minimax function
    return minimax(board,turn,cards,banners)
    
# Methond for the minimax 
def minimax(board, player,card,banners):
    #print(board)

    #Getting the valid moves the ai can take from the starting point to get a list of the actions to begin with
    actions = getvalidmoves(board)
    random.shuffle(actions)

    #Set a variable for the current depth
    currentdepth = 0

    #The beginning starting best action
    best = actions[0]

    #The beginning best value
    value = minvalue(board,player,best,card,currentdepth+1,banners)

    #Looping through all the actions
    for action in actions:

        #Getting the next min value
        v = minvalue(board,player,best,card,currentdepth+1,banners)

        #If the next min value is greater than the last one, update the best action and value
        if v > value:
            best = action
            value = v

    #Return the best action
    return best

#minvalue of the moves
def minvalue(board,player,action,card,currentdepth,banners):
    global MIN
    # copy the current state of the board
    state = board.copy()
    #print(player)
    #simulate the next state of the board based on the acton passed and get the next board, what color it would pick up and the amount picked up
    next,color, amount = simulateboard(state,action,card[player])


    card[player][color-2] += amount

    # Check to see if current player should capture a banner
    if card[player][color - 2] >= card[abs(1-player)][color - 2]:
        banners[player][color - 2] = 1  # add the banner to the player's collection
        banners[abs(1-player)][color - 2] = 0

    #calculating utility
    heu = 0

    for i in banners[player]:
        heu += i

    #getting the next player
    nextplayer = 1 - player

    # limiting the depth
    if currentdepth == MAXDEPTH:
        return heu

    #returning if there are no more moves
    if len(getvalidmoves(next)) == 0:
        return heu

    value = math.inf

    #adding to the depth
    currentdepth += 1

    #getting the next valid moves based on the next state of the board and getting the min of current value and the value from the max
    for action in getvalidmoves(next):

        value = min(value, maxvalue(next,nextplayer,action,card,currentdepth+1,banners))
        
        valuemin = MIN
        if value < MIN:
            MIN = value

    return value


#Maxvalue of the moves
def maxvalue(board,player,action,card,currentdepth,banners):
    # copy the current state of the board
    state = board.copy()
    print(player)
    #simulate the next state of the board based on the acton passed and get the next board, what color it would pick up and the amount picked up
    next,color, amount = simulateboard(state,action,card[player])


    card[player][color-2] += amount

    # Check to see if current player should capture a banner
    if card[player][color - 2] >= card[abs(1-player)][color - 2]:
        banners[player][color - 2] = 1  # add the banner to the player's collection
        banners[abs(1-player)][color - 2] = 0

    #calculating utility
    heu = 0

    for i in banners[player]:
        heu += i

    #getting the next player
    nextplayer = 1 - player

    # limiting the depth
    if currentdepth == MAXDEPTH:
        return heu

    #returning if there are no more moves
    if len(getvalidmoves(next)) == 0:
        return heu

    value = -math.inf

    #adding to the depth
    currentdepth += 1

    #getting the next valid moves based on the next state of the board and getting the min of current value and the value from the max
    valuemin = MIN
    for action in getvalidmoves(next):

        # pruning if the 
        # current utility is bigger than the smallest
        if heu > valuemin:
            break

        value = min(value, minvalue(next,nextplayer,action,card,currentdepth+1,banners))

    return value

#Simulate the move done to get the next state of the board and the cards won by the player
def simulateboard(board, action, cards):
    
    x1 = board.index(1)  # index of the 1-card on the board
    # print(f'moving from {x1} to {x}')

    # Remove captured cards from board

    print(action)
    color = board[action]  # color of the main captured card

    board[action] = 1  # the 1-card moves here
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

    amount = 0
    for i in possible:
        if board[i] == color:
            if i == action:
                continue

            amount += 1
            board[i] = 0  # there is no card in this position anymore
            #print("loop")
            cards[color - 2] += 1

    # Move the 1-card to the correct position
    board[action] = 1
    board[x1] = 0

    #print(board)


    #print (amount+1)
    
    return board,color, amount + 1
