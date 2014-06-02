"""
Created on Sat May 31 18:50:41 2014

@author: TheRussEquilibrium
"""
import random
import pickle
import operator

TicTacToe = [['-']*3 for i in range(3)]
squares = [[0,0],[0,1],[0,2],[1,0],[1,1],[1,2],[2,0],[2,1],[2,2]]
currentBoard = {1:1,2:1,3:1,4:1,5:1,6:1,7:1,8:1,9:1}
lookup = {(0,0):1,(0,1):2,(0,2):3,(1,0):4,(1,1):5,(1,2):6,(2,0):7,(2,1):8,(2,2):9}
reverselookup = {1:[0,0],2:[0,1],3:[0,2],4:[1,0],5:[1,1],6:[1,2],7:[2,0],8:[2,1],9:[2,2]}
#Q = {111111111:0}
#pickle.dump(Q,open("save.p","wb"))
Q = pickle.load(open("save.p","rb"))
gamma = .8

def PrintBoard():
    for row in TicTacToe:
        print row

def CompOneMove():
    x = random.choice(squares)
    squares.remove(x)
    currentBoard[lookup[(x[0],x[1])]] = 3

def CompTwoMove():
    o = random.choice(squares)
    squares.remove(o)
    currentBoard[lookup[(o[0],o[1])]] = 2
    
def CompMove(bestMove):
    y = None
    bestMove = bestMove
    board = 'a'
    for key,value in currentBoard.iteritems():
        board = board + str(value)
    board = board[1:]
    for i in xrange(len(board)):
        if board[i] != bestMove[i]:
            y = i
    x = reverselookup[y+1]
    squares.remove(x)
    TicTacToe[x[0]][x[1]] = "X"
    currentBoard[lookup[(x[0],x[1])]] = 3

def PlayerMove():
    o = reverselookup[input("Player make a move: ")]
    squares.remove(o)
    TicTacToe[o[0]][o[1]] = "O"
    currentBoard[lookup[(o[0],o[1])]] = 2

def startGame():
    global squares, currentBoard
    PrintBoard()
    squares = [[0,0],[0,1],[0,2],[1,0],[1,1],[1,2],[2,0],[2,1],[2,2]]
    currentBoard = {1:1,2:1,3:1,4:1,5:1,6:1,7:1,8:1,9:1}
    gameContinue = True
    print ""
    while(gameContinue) and (len(squares) > 1):
        status = win(currentBoard)
        if(status == 1) or (status == 0):
            gameContinue = False
            break
        bestMove = str(LegalMoves())
        print bestMove[0],bestMove[1],bestMove[2]
        print bestMove[3],bestMove[4],bestMove[5]
        print bestMove[6],bestMove[7],bestMove[8]
        CompMove(bestMove)
        PrintBoard()
        print ""
        status = win(currentBoard)
        if(status == 1) or (status == 0):
            gameContinue = False
            break
        PlayerMove()
        PrintBoard()
        print ""
        status = win(currentBoard)
        if(status == 1) or (status == 0):
            gameContinue = False
            break

def LegalMoves():
    QValue = newQValue(currentBoard)
    legalMoves = []
    legalMovesValue = {}
    for i in xrange(len(str(QValue))):
        s = list(str(QValue))
        if s[i] == '1':
            s[i] = '3'
            legalMoves.append(int("".join(s)))
    for move in legalMoves:
        legalMovesValue[move] = Q[move]
    for key,value in legalMovesValue.iteritems():
        print key, value
    return max(legalMovesValue.iteritems(), key=operator.itemgetter(1))[0]

def startLearning():
    global squares, currentBoard
    squares = [[0,0],[0,1],[0,2],[1,0],[1,1],[1,2],[2,0],[2,1],[2,2]]
    currentBoard = {1:1,2:1,3:1,4:1,5:1,6:1,7:1,8:1,9:1}
    Didwin = None
    all_values = []
    while(len(squares) > 1) and (Didwin == None):
        CompOneMove()
        Didwin = win(currentBoard)
        values = newQValue(currentBoard)
        all_values.append(values)
        CompTwoMove()
        Didwin = win(currentBoard)

    if Didwin == 1:
        for value in all_values:
            Q_Update = reward(value,100)
            Q[value] = Q_Update
    if Didwin == 0:
        for value in all_values:
            Q_Update = reward(value,-200)
            Q[value] = Q_Update
    else:
        for value in all_values:
            Q_Update = reward(value, -1)
            Q[value] = Q_Update


def reward(values, x):
    z = Q[values]
    return (z + (gamma * x))

def newQValue(currentBoard):
    x = currentBoard
    values = 'a'
    for key,value in x.iteritems():
        values = values + str(value)
    values = int(values[1:])
    if values not in Q.keys():
        Q[values] = 0
    return values
    
def win(currentBoard):
    if(currentBoard[1] == currentBoard[2]) and (currentBoard[1] == currentBoard[3]) and (currentBoard[1] == 3):
        return 1
    if(currentBoard[4] == currentBoard[5]) and (currentBoard[4] == currentBoard[6]) and (currentBoard[4] == 3):
        return 1
    if(currentBoard[7] == currentBoard[8]) and (currentBoard[7] == currentBoard[9]) and (currentBoard[7] == 3):
        return 1
    if(currentBoard[1] == currentBoard[4]) and (currentBoard[1] == currentBoard[7]) and (currentBoard[1] == 3):
        return 1
    if(currentBoard[2] == currentBoard[5]) and (currentBoard[2] == currentBoard[8]) and (currentBoard[2] == 3):
        return 1
    if(currentBoard[3] == currentBoard[6]) and (currentBoard[3] == currentBoard[9]) and (currentBoard[3] == 3):
        return 1
    if(currentBoard[1] == currentBoard[5]) and (currentBoard[1] == currentBoard[9]) and (currentBoard[1] == 3):
        return 1
    if(currentBoard[3] == currentBoard[5]) and (currentBoard[3] == currentBoard[7]) and (currentBoard[3] == 3):
        return 1
        
    if(currentBoard[1] == currentBoard[2]) and (currentBoard[1] == currentBoard[3]) and (currentBoard[1] == 2):
        return 0
    if(currentBoard[4] == currentBoard[5]) and (currentBoard[4] == currentBoard[6]) and (currentBoard[4] == 2):
        return 0
    if(currentBoard[7] == currentBoard[8]) and (currentBoard[7] == currentBoard[9]) and (currentBoard[7] == 2):
        return 0
    if(currentBoard[1] == currentBoard[4]) and (currentBoard[1] == currentBoard[7]) and (currentBoard[1] == 2):
        return 0
    if(currentBoard[2] == currentBoard[5]) and (currentBoard[2] == currentBoard[8]) and (currentBoard[2] == 2):
        return 0
    if(currentBoard[3] == currentBoard[6]) and (currentBoard[3] == currentBoard[9]) and (currentBoard[3] == 2):
        return 0
    if(currentBoard[1] == currentBoard[5]) and (currentBoard[1] == currentBoard[9]) and (currentBoard[1] == 2):
        return 0
    if(currentBoard[3] == currentBoard[5]) and (currentBoard[3] == currentBoard[7]) and (currentBoard[3] == 2):
        return 0

def main():
    for i in xrange(5000):
        startLearning()
    pickle.dump(Q,open("save.p","wb"))
    startGame()       
main()
