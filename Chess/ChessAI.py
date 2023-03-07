import random
import time
import numpy as np

pieceScore_mg = {"p": 82, "N": 337, "B": 365, "R": 477, "Q": 1025, "K": 0}
pieceScore_eg = {"p": 94, "N": 281, "B": 297, "R": 512, "Q": 936, "K": 0}

wKnight_mg = [
     [-167, -89, -34, -49,  61, -97, -15, -107],
     [-73, -41,  72,  36,  23,  62,   7,  -17],
     [-47,  60,  37,  65,  84, 129,  73,   44],
     [-9,  17,  19,  53,  37,  69,  18,   22],
     [-13,   4,  16,  13,  28,  19,  21,   -8],
     [-23,  -9,  12,  10,  19,  17,  25,  -16],
     [-29, -53, -12,  -3,  -1,  18, -14,  -19],
    [-105, -21, -58, -33, -17, -28, -19,  -23]
]
wKnight_eg = [
[-58, -38, -13, -28, -31, -27, -63, -99],
    [-25,  -8, -25,  -2,  -9, -25, -24, -52],
    [-24, -20,  10,   9,  -1,  -9, -19, -41],
    [-17,   3,  22,  22,  22,  11,   8, -18],
    [-18,  -6,  16,  25,  16,  17,   4, -18],
    [-23,  -3,  -1,  15,  10,  -3, -20, -22],
    [-42, -20, -10,  -5,  -2, -20, -23, -44],
    [-29, -51, -23, -15, -22, -18, -50, -64]
]

np.array(wKnight_mg)
np.array(wKnight_eg)
bKnight_mg = np.flip(wKnight_mg)
bKnight_eg = np.flip(wKnight_eg)
bKnight_mg = bKnight_mg.tolist()
bKnight_eg = bKnight_eg.tolist()

wBishop_mg = [
[-29,   4, -82, -37, -25, -42,   7,  -8],
    [-26,  16, -18, -13,  30,  59,  18, -47],
    [-16,  37,  43,  40,  35,  50,  37,  -2],
     [-4,   5,  19,  50,  37,  37,   7,  -2],
     [-6,  13,  13,  26,  34,  12,  10,   4],
      [0,  15,  15,  15,  14,  27,  18,  10],
      [4,  15,  16,   0,   7,  21,  33,   1],
    [-33,  -3, -14, -21, -13, -12, -39, -21]
]
wBishop_eg = [
[-14, -21, -11,  -8, -7,  -9, -17, -24],
     [-8,  -4,   7, -12, -3, -13,  -4, -14],
      [2,  -8,   0,  -1, -2,   6,   0,   4],
     [-3,   9,  12,   9, 14,  10,   3,   2],
     [-6,   3,  13,  19,  7,  10,  -3,  -9],
    [-12,  -3,   8,  10, 13,   3,  -7, -15],
    [-14, -18,  -7,  -1,  4,  -9, -15, -27],
    [-23,  -9, -23,  -5, -9, -16,  -5, -17]
]
np.array(wBishop_mg)
np.array(wBishop_eg)
bBishop_mg = np.flip(wBishop_mg)
bBishop_eg = np.flip(wBishop_eg)
bBishop_mg = bBishop_mg.tolist()
bBishop_eg = bBishop_eg.tolist()

wRook_mg = [
[32,  42,  32,  51, 63,  9,  31,  43],
     [27,  32,  58,  62, 80, 67,  26,  44],
     [-5,  19,  26,  36, 17, 45,  61,  16],
    [-24, -11,   7,  26, 24, 35,  -8, -20],
    [-36, -26, -12,  -1,  9, -7,   6, -23],
    [-45, -25, -16, -17,  3,  0,  -5, -33],
    [-44, -16, -20,  -9, -1, 11,  -6, -71],
    [-19, -13,   1,  17, 16,  7, -37, -26]
]
wRook_eg = [
[13, 10, 18, 15, 12,  12,   8,   5],
    [11, 13, 13, 11, -3,   3,   8,   3],
    [7,  7,  7,  5,  4,  -3,  -5,  -3],
     [4,  3, 13,  1,  2,   1,  -1,   2],
     [3,  5,  8,  4, -5,  -6,  -8, -11],
    [-4,  0, -5, -1, -7, -12,  -8, -16],
    [-6, -6,  0,  2, -9,  -9, -11,  -3],
    [-9,  2,  3, -1, -5, -13,   4, -20]
]
np.array(wRook_mg)
np.array(wRook_eg)
bRook_mg = np.flip(wRook_mg)
bRook_eg = np.flip(wRook_eg)
bRook_mg = bRook_mg.tolist()
bRook_eg = bRook_eg.tolist()

wQueen_mg = [
[-28,   0,  29,  12,  59,  44,  43,  45],
    [-24, -39,  -5,   1, -16,  57,  28,  54],
    [-13, -17,   7,   8,  29,  56,  47,  57],
    [-27, -27, -16, -16,  -1,  17,  -2,   1],
     [-9, -26,  -9, -10,  -2,  -4,   3,  -3],
    [-14,   2, -11,  -2,  -5,   2,  14,   5],
    [-35,  -8,  11,   2,   8,  15,  -3,   1],
     [-1, -18,  -9,  10, -15, -25, -31, -50]
]
wQueen_eg = [
[-9,  22,  22,  27,  27,  19,  10,  20],
    [-17,  20,  32,  41,  58,  25,  30,   0],
    [-20,   6,   9,  49,  47,  35,  19,   9],
      [3,  22,  24,  45,  57,  40,  57,  36],
    [-18,  28,  19,  47,  31,  34,  39,  23],
    [-16, -27,  15,   6,   9,  17,  10,   5],
    [-22, -23, -30, -16, -16, -23, -36, -32],
    [-33, -28, -22, -43,  -5, -32, -20, -41]
]
np.array(wQueen_mg)
np.array(wQueen_eg)
bQueen_mg = np.flip(wQueen_mg)
bQueen_eg = np.flip(wQueen_eg)
bQueen_mg = bQueen_mg.tolist()
bQueen_eg = bQueen_eg.tolist()

wKing_mg = [
[-65,  23,  16, -15, -56, -34,   2,  13],
     [29,  -1, -20,  -7,  -8,  -4, -38, -29],
     [-9,  24,   2, -16, -20,   6,  22, -22],
    [-17, -20, -12, -27, -30, -25, -14, -36],
    [-49,  -1, -27, -39, -46, -44, -33, -51],
    [-14, -14, -22, -46, -44, -30, -15, -27],
      [1,   7,  -8, -64, -43, -16,   9,   8],
    [-15,  36,  12, -54,   8, -28,  24,  14]
]
wKing_eg = [
[-74, -35, -18, -18, -11,  15,   4, -17],
    [-12,  17,  14,  17,  17,  38,  23,  11],
     [10,  17,  23,  15,  20,  45,  44,  13],
     [-8,  22,  24,  27,  26,  33,  26,   3],
    [-18,  -4,  21,  24,  27,  23,   9, -11],
    [-19,  -3,  11,  21,  23,  16,   7,  -9],
    [-27, -11,   4,  13,  14,   4,  -5, -17],
    [-53, -34, -21, -11, -28, -14, -24, -43]
]
np.array(wKing_mg)
np.array(wKing_eg)
bKing_mg = np.flip(wKing_mg)
bKing_eg = np.flip(wKing_eg)
bKing_mg = bKing_mg.tolist()
bKing_eg = bKing_eg.tolist()

wPawn_mg = [
[0,   0,   0,   0,   0,   0,  0,   0],
     [98, 134,  61,  95,  68, 126, 34, -11],
     [-6,   7,  26,  31,  65,  56, 25, -20],
    [-14,  13,   6,  21,  23,  12, 17, -23],
    [-27,  -2,  -5,  12,  17,   6, 10, -25],
    [-26,  -4,  -4, -10,   3,   3, 33, -12],
    [-35,  -1, -20, -23, -15,  24, 38, -22],
      [0,   0,   0,   0,   0,   0,  0,   0]
]
wPawn_eg = [
[0,   0,   0,   0,   0,   0,   0,   0],
    [178, 173, 158, 134, 147, 132, 165, 187],
     [94, 100,  85,  67,  56,  53,  82,  84],
     [32,  24,  13,   5,  -2,   4,  17,  17],
     [13,   9,  -3,  -7,  -7,  -8,   3,  -1],
      [4,   7,  -6,   1,   0,  -5,  -1,  -8],
     [13,   8,   8,  10,  13,   0,   2,  -7],
      [0,   0,   0,   0,   0,   0,   0,   0]
]
np.array(wPawn_mg)
np.array(wPawn_eg)
bPawn_mg = np.flip(wPawn_mg)
bPawn_eg = np.flip(wPawn_eg)
bPawn_mg = bPawn_mg.tolist()
bPawn_eg = bPawn_eg.tolist()


piecePositionScores_mg = {"wN": wKnight_mg, "bN": bKnight_mg,
                       "wB": wBishop_mg, "bB": bBishop_mg,
                       "wQ": wQueen_mg, "bQ": bQueen_mg,
                       "wR": wRook_mg, "bR": bRook_mg,
                       "wp": wPawn_mg, "bp": bPawn_mg,
                       "wK": wKing_mg, "bK": bKing_mg}

piecePositionScores_eg = {"wN": wKnight_eg, "bN": bKnight_eg,
                       "wB": wBishop_eg, "bB": bBishop_eg,
                       "wQ": wQueen_eg, "bQ": bQueen_eg,
                       "wR": wRook_eg, "bR": bRook_eg ,
                       "wp": wPawn_eg, "bp": bPawn_eg,
                       "wK": wKing_eg, "bK": bKing_eg}

CHECKMATE = 10000
STALEMATE = 0
DEPTH = 4


def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves)-1)]

'''
helper method to make first recursive call
'''

def findBestMove(gameState, returnQueue):
    start = time.time()
    global nextMove, counter, counter2
    nextMove = None
    #random.shuffle(validMoves)
    counter, counter2 = 0, 0
    findMoveNegaMaxAlphaBeta(gameState, DEPTH, -CHECKMATE, CHECKMATE)
    end = time.time()
    print(counter)
    print(counter2, "quiescence")
    print(end-start)
    returnQueue.put(nextMove)

def findMoveNegaMaxAlphaBeta(gameState, depth, alpha, beta): # alpha upper bound, beta lower bound
    global nextMove, counter
    counter += 1
    foundPV_flag = False
    if depth == 0:
        #return scoreBoard(gameState)
        return quiescence(gameState, 8, alpha, beta)

    validMoves = gameState.getValidMoves()
    validMoves = orderMoves(gameState, validMoves)

    for move in validMoves:
        gameState.makeMove(move)
        if foundPV_flag:
            score = -findMoveNegaMaxAlphaBeta(gameState, depth-1, -alpha-1, -alpha)
            if score > alpha and score < beta:
                score = -findMoveNegaMaxAlphaBeta(gameState, depth-1, -beta, -alpha)
        else:
            score = -findMoveNegaMaxAlphaBeta(gameState, depth-1, -beta, -alpha)
        gameState.undoMove()
        if score >= beta:
            return beta
        if score > alpha:
            alpha = score
            foundPV_flag = True
            if depth == DEPTH:
                nextMove = move
                print(move, score/100)

    # if gameState.staleMate:
    #     alpha = 0

    return alpha

'''
quiescent search
'''
def quiescence(gameState, depth, alpha, beta):
    global counter2
    counter2 += 1

    score = scoreBoard(gameState)

    if depth == 0:
        return alpha

    captureMoves = gameState.getCaptureMoves()
    captureMoves = orderMoves(gameState, captureMoves)

    if score >= beta:
        return beta
    if score > alpha:
        alpha = score

    for move in captureMoves:
        gameState.makeMove(move)
        score = -quiescence(gameState, depth-1, -beta, -alpha)
        gameState.undoMove()
        if score >= beta:
            return beta
        if score > alpha:
            alpha = score

    return alpha


'''
move ordering
'''
def orderMoves(gameState, validMoves):


    moveOrderScoreList = []
    captureMultiplier = 100
    isEndGame = getGamePhase(gameState)

    # move order
    for move in validMoves:
        piece = move.pieceMoved # stores "**"
        capturedPiece = move.pieceCaptured # stores "**"
        endRow, endCol = move.endRow, move.endCol
        moveOrderScore = 0

        if not isEndGame:

            # mvv_lva
            if capturedPiece != "--":
                moveOrderScore += captureMultiplier * (pieceScore_mg[capturedPiece[1]] - pieceScore_mg[piece[1]])

            if piece[1] == "p" and (endRow == 0 or endRow == 7):
                moveOrderScore += pieceScore_mg["Q"]*100

        else: # it is endgame
            if capturedPiece != "--":
                moveOrderScore += captureMultiplier * (pieceScore_eg[capturedPiece[1]] - pieceScore_eg[piece[1]])

            if piece[1] == "p" and (endRow == 0 or endRow == 7):
                moveOrderScore += pieceScore_eg["Q"]*100

        # implement hanging piece to pawn later

        moveOrderScoreList.append(moveOrderScore)


    # sort using numpy
    moveOrderScoreList = np.array(moveOrderScoreList)
    validMoves = np.array(validMoves)

    idx = np.argsort(moveOrderScoreList)

    moveOrderScoreList = np.array(moveOrderScoreList)[idx]
    validMoves = np.array(validMoves)[idx]

    moveOrderScoreList = moveOrderScoreList.tolist()
    validMoves = validMoves.tolist()

    moveOrderScoreList.reverse()
    validMoves.reverse()

    return validMoves

'''
positive score good for white (white winning)
negative score good for black (black winning)
'''
def scoreBoard(gameState):
    if gameState.checkMate:
        if gameState.whiteToMove:
            return -CHECKMATE # black wins
        else:
            return CHECKMATE # white wins
    elif gameState.staleMate:
        return STALEMATE # draw


    score = 0
    isEndGame = getGamePhase(gameState)

    for row in range(len(gameState.board)):
        for col in range(len(gameState.board[row])):
            square = gameState.board[row][col]

            if not isEndGame:
                if square != "--":
                    piecePositionScore = piecePositionScores_mg[square][row][col]

                    if square[0] == "w":
                        score += pieceScore_mg[square[1]] + piecePositionScore
                    elif square[0] == "b":
                        score -= pieceScore_mg[square[1]] + piecePositionScore
            else: # it is endgame
                if square != "--":
                    piecePositionScore = piecePositionScores_eg[square][row][col]

                    if square[0] == "w":
                        score += pieceScore_mg[square[1]] + piecePositionScore
                    elif square[0] == "b":
                        score -= pieceScore_mg[square[1]] + piecePositionScore

    turnMultiplier = 1 if gameState.whiteToMove else -1
    return score * turnMultiplier


def getGamePhase(gameState):
    wMajorPieceCount = 0
    bMajorPieceCount = 0
    for row in range(len(gameState.board)):
        for col in range(len(gameState.board[row])):
            square = gameState.board[row][col]

            if square == "wN" or square == "wB" or square == "wR" or square == "wQ":
                wMajorPieceCount += 1
            if square == "bN" or square == "bB" or square == "bR" or square == "bQ":
                bMajorPieceCount += 1
    if wMajorPieceCount <= 4 and bMajorPieceCount <= 4:
        return True # it is end game
    return False # it is middle game


#******************************************************************
#******************************************************************
#******************************************************************
'''
OLD search algorithms
'''
# minmax no recursion
def findBestMoveNoRecur(gameState, validMoves):

    turnMultiplier = 1 if gameState.whiteToMove else -1
    oppMinMaxScore = CHECKMATE
    bestPlayerMove = None
    random.shuffle(validMoves)
    for playerMove in validMoves:
        gameState.makeMove(playerMove)
        oppMoves = gameState.getValidMoves()
        if gameState.checkMate:
            oppMaxScore = -CHECKMATE
        elif gameState.staleMate:
            oppMaxScore = STALEMATE
        else:
            oppMaxScore = -CHECKMATE
            for opponentsMove in oppMoves:
                gameState.makeMove(opponentsMove)
                gameState.getValidMoves()
                if gameState.checkMate:
                    score = CHECKMATE
                elif gameState.staleMate:
                    score = STALEMATE
                else:
                    score = -turnMultiplier * scoreMaterial(gameState.board)
                if score > oppMaxScore:
                    oppMaxScore = score
                gameState.undoMove()
        if oppMaxScore < oppMinMaxScore:
            oppMinMaxScore = oppMaxScore
            bestPlayerMove = playerMove
        gameState.undoMove()
    return bestPlayerMove

def findMoveMinMax(gameState, validMoves, depth, whiteToMove):
    global nextMove
    random.shuffle(validMoves)
    if depth == 0: # after depth recursion (final state)
        return scoreMaterial(gameState.board)

    if whiteToMove:
        maxScore = -CHECKMATE # worst score possible
        for move in validMoves:
            gameState.makeMove(move)
            nextValidMoves = gameState.getValidMoves()
            score = findMoveMinMax(gameState, nextValidMoves, depth - 1, False)
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move
            gameState.undoMove()
        return maxScore

    else: # black's turn
        minScore = CHECKMATE
        for move in validMoves:
            gameState.makeMove(move)
            nextValidMoves = gameState.getValidMoves()
            score = findMoveMinMax(gameState, nextValidMoves, depth - 1, True)
            if score < minScore:
                minScore = score
                if depth == DEPTH:
                    nextMove = move
            gameState.undoMove()
        return minScore

def findMoveNegaMax(gameState, validMoves, depth, turnMultiplier):
    global nextMove
    if depth == 0:
        return turnMultiplier * scoreBoard(gameState)

    maxScore = -CHECKMATE
    random.shuffle(validMoves)
    for move in validMoves:
        gameState.makeMove(move)
        nextValidMoves = gameState.getValidMoves()
        score = -findMoveNegaMax(gameState, nextValidMoves, depth-1, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gameState.undoMove()
    return maxScore



