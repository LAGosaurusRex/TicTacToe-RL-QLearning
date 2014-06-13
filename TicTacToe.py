# -*- coding: utf-8 -*-
"""
Created on Sat May 31 18:50:41 2014

@author: TheRussEquilibrium a.k.a LAGosaurus.Rex
"""

import random
import pickle
import operator
import os.path

TicTacToe = [['-']*3 for i in range(3)]
squares = [[0,0],[0,1],[0,2],[1,0],[1,1],[1,2],[2,0],[2,1],[2,2]] #board coordinates
currentBoard = {1:1,2:1,3:1,4:1,5:1,6:1,7:1,8:1,9:1} #board labeled 1-9, each square initially set to 1. 3 == "X" and 2 == "O".
lookup = {(0,0):1,(0,1):2,(0,2):3,(1,0):4,(1,1):5,(1,2):6,(2,0):7,(2,1):8,(2,2):9} #helps with updating currentBoard as moves are made.
reverselookup = {1:[0,0],2:[0,1],3:[0,2],4:[1,0],5:[1,1],6:[1,2],7:[2,0],8:[2,1],9:[2,2]} #helps with allowing the computer to move on its own vs humans.
'''Checks to see if the Q dictionary exists on your computer.
   If not it initializes one with the starting postion and saves
   a copy to your computer'''
if os.path.isfile("save.p"):
    Q = pickle.load(open("save.p","rb"))
else:
    Q = {111111111:0}
    pickle.dump(Q,open("save.p","wb"))

def PrintBoard():
    '''Prints the Tic-Tac-Toe Game Board.'''
    for row in TicTacToe:
        print row

def CompOneMove():
    '''For the learning function. "X" moves randomly.'''
    x = random.choice(squares) #chooses a random value from the squares list
    squares.remove(x) #removes that value from the list
    currentBoard[lookup[(x[0],x[1])]] = 3 #sets that value on the Current Board to 3, i.e "X"

def CompTwoMove():
    '''For the learning function. "O" moves randomly.'''
    o = random.choice(squares) #chooses a random value from the squares list
    squares.remove(o) #removes that value from the list
    currentBoard[lookup[(o[0],o[1])]] = 2 #sets that value on the Current Board to 2, i.e "O"
    
def CompMove(shape,bestMove):
    '''For computer vs human playing. It takes 2 values:
        shape is obviously the shape the computer playes as, i.e "X" or "O".
        And bestMove is exactly what it says, it's the estimated best move
        from the given position based on prior evaluations of the algorithm.'''
    y = None
    bestMove = bestMove
    board = 'a'
    #Iterates over the currentBoard dict and creates a number for
    #the position, i.e the current position would be 111111111.
    for key,value in currentBoard.iteritems():
        board = board + str(value)
    board = board[1:]
    #Iterates over each value in board and bestMove looking for the
    #difference between the 2 lists. Once it finds the difference it uses
    #the reverselookup table to then find the correct square to mark.
    for i in xrange(len(board)):
        if board[i] != bestMove[i]:
            y = i
    x = reverselookup[y+1]
    squares.remove(x)
    TicTacToe[x[0]][x[1]] = shape
    if shape == "X":
        currentBoard[lookup[(x[0],x[1])]] = 3
    else:
        currentBoard[lookup[(x[0],x[1])]] = 2

def PlayerMove(shape):
    '''Function for player movement.'''
    o = reverselookup[input("Player make a move: ")]
    squares.remove(o)
    TicTacToe[o[0]][o[1]] = shape
    if shape == "O":
        currentBoard[lookup[(o[0],o[1])]] = 2
    else:
        currentBoard[lookup[(o[0],o[1])]] = 3

def startGame():
    '''Probably a way to combine startGame and startGame2 into one function.
       But this seemed easiest at the time. startGame() playes a game vs the
       computer with the computer being first move("X")'''
    global squares, currentBoard
    squares = [[0,0],[0,1],[0,2],[1,0],[1,1],[1,2],[2,0],[2,1],[2,2]]
    currentBoard = {1:1,2:1,3:1,4:1,5:1,6:1,7:1,8:1,9:1}
    gameContinue = True
    print ""
    while(gameContinue) and (len(squares) > 1):
        status = win(currentBoard)
        if(status == 1) or (status == 0):
            gameContinue = False
            return 0
        bestMove = str(LegalMoves("X"))
        '''This commented out part will print out what the computer believes to
           be the best move given the current board.'''
#        print bestMove[0],bestMove[1],bestMove[2]
#        print bestMove[3],bestMove[4],bestMove[5]
#        print bestMove[6],bestMove[7],bestMove[8]
        CompMove("X",bestMove)
        PrintBoard()
        print ""
        status = win(currentBoard)
        if(status == 1):
            print("Computer Wins, you suck.")
            gameContinue = False
            return 0
        PlayerMove("O")
        status = win(currentBoard)
        if(status == 0):
            print("Oh, this can't be right. You won? Are you hacking my program? Don't you feel cool, hacking to win Tic-Tac-Toe.")
            gameContinue = False
            return 0
            
def startGame2():
    '''Same as startGame() but the human player goes first("X").'''
    global squares, currentBoard
    squares = [[0,0],[0,1],[0,2],[1,0],[1,1],[1,2],[2,0],[2,1],[2,2]]
    currentBoard = {1:1,2:1,3:1,4:1,5:1,6:1,7:1,8:1,9:1}
    gameContinue = True
    PrintBoard()
    while(gameContinue) and (len(squares) >= 1):
        print ""
        PlayerMove("X")
        PrintBoard()
        print ""
        status = win(currentBoard)
        if(status == 1):
            print("Oh, this can't be right. You won? Are you hacking my program? Don't you feel cool, hacking to win Tic-Tac-Toe.")
            gameContinue = False
            return 0
        bestMove = str(LegalMoves("O"))
        '''This commented out part will print out what the computer believes to
           be the best move given the current board.'''
#        print bestMove[0],bestMove[1],bestMove[2]
#        print bestMove[3],bestMove[4],bestMove[5]
#        print bestMove[6],bestMove[7],bestMove[8]
        CompMove("O",bestMove)
        PrintBoard()
        print ""
        status = win(currentBoard)
        if(status == 0):
            print("Computer Wins, you suck.")
            gameContinue = False
            return 0

def LegalMoves(x):
    '''This function finds all legal moves for the computer, along with 
       their estimated values. Then returns either the highest value or
       lowest value based on whether or not the computer is "X" or "O".'''
    if x == "X":
        y = ["1","3"]
    if x == "O":
        y = ["1","2"]
    QValue = newQValue(currentBoard) #gets a numeric representation of the current position, i.e 111111111
    legalMoves = []
    legalMovesValue = {}
    #this loops over QValue and creates a list of all possible moves in a numeric representation, i.e 311111111, 131111111, etc
    for i in xrange(len(str(QValue))):
        s = list(str(QValue))
        if s[i] == y[0]:
            s[i] = y[1]
            legalMoves.append(int("".join(s)))
    #places those moves into a dictionary with their previous evaluated values from the Q dict
    for move in legalMoves:
        legalMovesValue[move] = Q[move]
    '''The commented part below will print out the possible moves in the 
       given position along with a value tied to that move.'''
#    for key,value in legalMovesValue.iteritems():
#        print key, value
    # returns the best move by returning the max or min key depending on if "X" or "O" 
    if x == "X":
        return max(legalMovesValue.iteritems(), key=operator.itemgetter(1))[0]
    if x == "O":
        return min(legalMovesValue.iteritems(), key=operator.itemgetter(1))[0]

def startLearning():
    '''The learning function plays out a game, computer vs computer. Each game
       played updates the values in the Q dictionary. Enough games need to be 
       played to allow each new position to be put into the dictionary; if you 
       don't do this and play the computer it will throw an error because the 
       position isn't in the dictionary. I could just initialize the dictionary
       with all possible positions, but, you need the algorithm to run and learn
       anyways so I don't see the necessity.'''
    global squares, currentBoard
    squares = [[0,0],[0,1],[0,2],[1,0],[1,1],[1,2],[2,0],[2,1],[2,2]]
    currentBoard = {1:1,2:1,3:1,4:1,5:1,6:1,7:1,8:1,9:1}
    Didwin = None
    all_values = []
    while(len(squares) >= 1) and (Didwin == None):
        CompOneMove()
        values = newQValue(currentBoard)
        all_values.append(values)
        Didwin = win(currentBoard)
        if Didwin or len(squares) == 0:
            break
        CompTwoMove()
        values = newQValue(currentBoard)
        all_values.append(values)
        Didwin = win(currentBoard)

    if Didwin == 1:
        for value in all_values:
            Q_Update = reward(value,50)
            Q[value] = Q_Update
        #This allows the algorithm to quickly learn from moves that lead
        #to a loss on the next opponent move.
        #I feel like I should be able to do some sort of depth search
        #Which looks forward like a chess algorithm and can help set
        #move evaluations.            
            all_values.reverse()
            Q_Update = reward(all_values[1],10000)
            Q[all_values[1]] = Q_Update
    if Didwin == 0:
        for value in all_values:
            Q_Update = reward(value,-50)
            Q[value] = Q_Update
        #This allows the algorithm to quickly learn from moves that lead
        #to a loss on the next opponent move.
        #I feel like I should be able to do some sort of depth search
        #Which looks forward like a chess algorithm and can help set
        #move evaluations.
        all_values.reverse()
        Q_Update = reward(all_values[1],-10000)
        Q[all_values[1]] = Q_Update
    else:
        for value in all_values:
            Q_Update = reward(value,0)
            Q[value] = Q_Update

def reward(values, x):
    '''This updates the evaluation in the Q dict of the position.'''
    z = Q[values]
    return (z + x)

def newQValue(currentBoard):
    '''This returns a numeric representation of the current position.
       It also puts each newly found position into the Q dictionary and
       sets its initial value to 0.'''
    x = currentBoard
    values = 'a'
    for key,value in x.iteritems():
        values = values + str(value)
    values = int(values[1:])
    if values not in Q.keys():
        Q[values] = 0
    return values
    
def win(currentBoard):
    '''My method of checking to see if someone has won. 
       There has to be a better approach.'''
    if(currentBoard[1] == currentBoard[2] == currentBoard[3] == 3):
        return 1
    if(currentBoard[4] == currentBoard[5] == currentBoard[6] == 3):
        return 1
    if(currentBoard[7] == currentBoard[8] == currentBoard[9] == 3):
        return 1
    if(currentBoard[1] == currentBoard[4] == currentBoard[7] == 3):
        return 1
    if(currentBoard[2] == currentBoard[5] == currentBoard[8] == 3):
        return 1
    if(currentBoard[3] == currentBoard[6] == currentBoard[9] == 3):
        return 1
    if(currentBoard[1] == currentBoard[5] == currentBoard[9] == 3):
        return 1
    if(currentBoard[3] == currentBoard[5] == currentBoard[7] == 3):
        return 1
        
    if(currentBoard[1] == currentBoard[2] == currentBoard[3] == 2):
        return 0
    if(currentBoard[4] == currentBoard[5] == currentBoard[6] == 2):
        return 0
    if(currentBoard[7] == currentBoard[8] == currentBoard[9] == 2):
        return 0
    if(currentBoard[1] == currentBoard[4] == currentBoard[7] == 2):
        return 0
    if(currentBoard[2] == currentBoard[5] == currentBoard[8] == 2):
        return 0
    if(currentBoard[3] == currentBoard[6] == currentBoard[9] == 2):
        return 0
    if(currentBoard[1] == currentBoard[5] == currentBoard[9] == 2):
        return 0
    if(currentBoard[3] == currentBoard[5] == currentBoard[7] == 2):
        return 0

def main():
    global TicTacToe
    #maybe it's best to be the loop in the startLearning() function?
    for i in xrange(50000):
        startLearning()
    #after it runs the learning iterations it saves a new updated value of
    #the Q dict to your computer
    pickle.dump(Q,open("save.p","wb"))
    print("When asked for a move it expects an input, an integer 1-9. The board is labeled left to right, 1-9")
    startGame()
    TicTacToe = [['-']*3 for i in range(3)]
    startGame2()
main()
