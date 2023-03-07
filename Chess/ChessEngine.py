import time
import numpy as np

'''
Responsible for storing all information about the current state of the game.
Reponsible for determining valid moves and keeping a move log.
'''

class GameState():
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]

        # self.board = [
        #     ["bR", "--", "--", "--", "bK", "--", "--", "bR"],
        #     ["bp", "--", "bp", "bp", "bQ", "bp", "bB", "--"],
        #     ["bB", "bN", "--", "--", "bp", "bN", "bp", "--"],
        #     ["--", "--", "--", "wp", "wN", "--", "--", "--"],
        #     ["--", "bp", "--", "--", "wp", "--", "--", "--"],
        #     ["--", "--", "wN", "--", "--", "wQ", "--", "bp"],
        #     ["wp", "wp", "wp", "wB", "wB", "wp", "wp", "wp"],
        #     ["wR", "--", "--", "--", "wK", "--", "--", "wR"]
        # ]

        # self.board = [
        #     ["--", "--", "--", "--", "--", "--", "--", "--"],
        #     ["--", "--", "--", "--", "--", "--", "--", "--"],
        #     ["--", "--", "--", "--", "--", "--", "--", "--"],
        #     ["--", "--", "--", "--", "--", "--", "--", "--"],
        #     ["--", "--", "--", "wK", "--", "--", "--", "--"],
        #     ["--", "--", "--", "--", "--", "--", "--", "--"],
        #     ["--", "--", "--", "--", "--", "--", "bK", "bQ"],
        #     ["--", "--", "--", "--", "--", "--", "--", "--"]
        # ]

        # self.board = [
        #     ["--", "--", "--", "--", "--", "wR", "--", "--"],
        #     ["--", "--", "--", "--", "--", "bp", "bp", "--"],
        #     ["--", "--", "--", "--", "bp", "--", "--", "wK"],
        #     ["--", "--", "--", "--", "--", "--", "--", "bp"],
        #     ["wQ", "--", "--", "--", "--", "--", "--", "--"],
        #     ["--", "wp", "--", "--", "--", "--", "--", "wp"],
        #     ["--", "--", "--", "bQ", "--", "wp", "wp", "--"],
        #     ["--", "--", "wR", "--", "--", "--", "wK", "--"]
        # ]

        self.moveFunction = {"p":self.getPawnMoves, "N":self.getKnightMoves, "R":self.getRookMoves,
                             "Q":self.getQueenMoves, "K":self.getKingMoves, "B":self.getBishopMoves}
        self.captureMoveFunction = {"p":self.getPawnCaptures, "N":self.getKnightCaptures, "R":self.getRookCaptures,
                                    "Q":self.getQueenCaptures, "K":self.getKingCaptures, "B":self.getBishopCaptures}
        self.whiteToMove = True
        self.isBoardFlipped = False
        self.moveLog = []
        self.wKingLocation = (7, 4)
        self.bKingLocation = (0, 4)
        self.inCheck = False
        self.pins = []
        self.checks = []

        self.checkMate = False
        self.staleMate = False
        self.enpassantPossible = () # coordinate of the sq where enpassant capture is possible
        self.enpassantPossibleLog = [self.enpassantPossible]
        self.currentCastleRight = CastleRights(True, True, True, True)
        self.castleRightLog = [CastleRights(self.currentCastleRight.wks, self.currentCastleRight.bks, self.currentCastleRight.wqs, self.currentCastleRight.bqs)]

    # def flipBoard(self):
    #     np.array(self.board)
    #     self.board = np.flip(self.board)
    #     self.board = self.board.tolist()
    #     self.isBoardFlipped = True
    #     print("*************************BOARD FLIPPED*************************")


    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove
        # update king's location
        if move.pieceMoved == "wK":
            self.wKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == "bK":
            self.bKingLocation = (move.endRow, move.endCol)

        # pawn promo
        if move.isPawnPromo:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + "Q"
            # add choice for promo

        # enpassant
        if move.isEnpassantMove:
             self.board[move.startRow][move.endCol] = "--" # capture pawn

        # update enpassanetPossible
        if move.pieceMoved[1] == "p" and abs(move.startRow-move.endRow) == 2: # for 2 sq pawn move
            self.enpassantPossible = ((move.startRow+move.endRow)//2, move.startCol)
        else:
            self.enpassantPossible = ()

        self.enpassantPossibleLog.append(self.enpassantPossible)

        # castle move
        if move.isCastleMove:
            if move.endCol-move.startCol == 2: # short castle
                self.board[move.endRow][move.endCol-1] = self.board[move.endRow][move.endCol+1] # moves rook to opposite side of king
                self.board[move.endRow][move.endCol+1] = "--" # erase old rook
            else: # long castle
                self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-2]
                self.board[move.endRow][move.endCol-2] = "--"

        # castling rights
        self.updateCastleRight(move)
        self.castleRightLog.append(CastleRights(self.currentCastleRight.wks, self.currentCastleRight.bks, self.currentCastleRight.wqs, self.currentCastleRight.bqs))



    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove
            # update king's location
            if move.pieceMoved == "wK":
                self.wKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == "bK":
                self.bKingLocation = (move.startRow, move.startCol)

            # undo enpassant
            if move.isEnpassantMove:
                self.board[move.endRow][move.endCol] = "--"
                self.board[move.startRow][move.endCol] = move.pieceCaptured

            self.enpassantPossibleLog.pop()
            self.enpassantPossible = self.enpassantPossibleLog[-1]

            # undo castle rights
            self.castleRightLog.pop() # delete new castle right
            newRights = self.castleRightLog[-1] # set current castle right to now last one in the list
            self.currentCastleRight = CastleRights(newRights.wks, newRights.bks, newRights.wqs, newRights.bqs)

            # undo castle move
            if move.isCastleMove:
                if move.endCol-move.startCol == 2: #short castle
                    self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-1]
                    self.board[move.endRow][move.endCol - 1] = "--"
                else: # long castle
                    self.board[move.endRow][move.endCol - 2] = self.board[move.endRow][move.endCol+1]
                    self.board[move.endRow][move.endCol + 1] = "--"

            # for AI algorithm
            self.checkMate = False
            self.staleMate = False

    def updateCastleRight(self, move):
        if move.pieceMoved == "wK":
            self.currentCastleRight.wks = False
            self.currentCastleRight.wqs = False
        elif move.pieceMoved == "bK":
            self.currentCastleRight.bks = False
            self.currentCastleRight.bqs = False
        elif move.pieceMoved == "wR":
            if move.startRow == 7:
                if move.startCol == 0:
                    self.currentCastleRight.wqs = False
                if move.startCol == 7:
                    self.currentCastleRight.wks = False
        elif move.pieceMoved == "bR":
            if move.startRow == 0:
                if move.startCol == 0:
                    self.currentCastleRight.bqs = False
                if move.startCol == 7:
                    self.currentCastleRight.bks = False

        # if rook is captured, don't allow castle
        if move.pieceCaptured == 'wR':
            if move.endRow == 7:
                if move.endCol == 0:
                    self.currentCastleRight.wqs = False
                elif move.endCol == 7:
                    self.currentCastleRight.wks = False
        elif move.pieceCaptured == 'bR':
            if move.endRow == 0:
                if move.endCol == 0:
                    self.currentCastleRight.bqs = False
                elif move.endCol == 7:
                    self.currentCastleRight.bks = False

    '''
    Moves considering checks
    '''
    def getValidMoves(self):
        tempEnpassantPossible = self.enpassantPossible
        tempCastleRight = CastleRights(self.currentCastleRight.wks, self.currentCastleRight.bks, self.currentCastleRight.wqs, self.currentCastleRight.bqs)
        possibleMoves = []
        self.inCheck, self.pins, self.checks = self.checkForPinsChecks()
        if self.whiteToMove:
            kingRow = self.wKingLocation[0]
            kingCol = self.wKingLocation[1]
        else:
            kingRow = self.bKingLocation[0]
            kingCol = self.bKingLocation[1]

        if self.inCheck:
            # case 1: only one check. capture, block, or move king
            if len(self.checks) == 1:
                possibleMoves = self.getAllPossibleMoves()
                check = self.checks[0]
                checkRow = check[0]
                checkCol = check[1]
                pieceChecking = self.board[checkRow][checkCol] # enemy piece attacking with check
                validSquares = [] # squares pieces can move to block check

                # if knight checking, either capture knight or move king
                if pieceChecking[1] == "N":
                    validSquares = [(checkRow, checkCol)]
                else: # not a knight
                    for i in range(1,8):
                        validSquare = (kingRow + check[2]*i, kingCol + check[3]*i) # check[2,3] are the check directions
                        validSquares.append(validSquare)
                        if validSquare[0] == checkRow and validSquare[1] == checkCol: # once get to attacking piece (the piece checking the king) then break
                            break

                # remove moves that don't block check or move king
                # when removing items from a list while iterating through, start from the end of the list
                for i in range(len(possibleMoves)-1, -1, -1):
                    if possibleMoves[i].pieceMoved[1] != "K": # does not move king so must block or capture
                        if not (possibleMoves[i].endRow, possibleMoves[i].endCol) in validSquares: # move doesn't block check or capture checking piece
                            possibleMoves.remove(possibleMoves[i])

            else: # for double checks
                self.getKingMoves(kingRow, kingCol, possibleMoves)
        else: # not check so all moves are fine
            possibleMoves = self.getAllPossibleMoves()

        if len(possibleMoves) == 0:
            if self.inCheck:
                self.checkMate = True
            else:
                self.staleMate = True
        else: # for undo moves
            self.checkMate = False
            self.staleMate = False

        if self.whiteToMove:
            self.getCastleMoves(self.wKingLocation[0], self.wKingLocation[1], possibleMoves)
        else:
            self.getCastleMoves(self.bKingLocation[0], self.bKingLocation[1], possibleMoves)

        self.enpassantPossible = tempEnpassantPossible
        self.currentCastleRight = tempCastleRight

        return possibleMoves

    def getCaptureMoves(self):
        tempEnpassantPossible = self.enpassantPossible
        possibleMoves = []
        self.inCheck, self.pins, self.checks = self.checkForPinsChecks()
        if self.whiteToMove:
            kingRow = self.wKingLocation[0]
            kingCol = self.wKingLocation[1]
        else:
            kingRow = self.bKingLocation[0]
            kingCol = self.bKingLocation[1]

        if self.inCheck:
            # case 1: only one check. capture, block, or move king
            if len(self.checks) == 1:
                possibleMoves = self.getAllPossibleCaptures()
                check = self.checks[0]
                checkRow = check[0]
                checkCol = check[1]
                pieceChecking = self.board[checkRow][checkCol] # enemy piece attacking with check
                validSquares = [] # squares pieces can move to block check

                # if knight checking, either capture knight or move king
                if pieceChecking[1] == "N":
                    validSquares = [(checkRow, checkCol)]
                else: # not a knight
                    for i in range(1,8):
                        validSquare = (kingRow + check[2]*i, kingCol + check[3]*i) # check[2,3] are the check directions
                        validSquares.append(validSquare)
                        if validSquare[0] == checkRow and validSquare[1] == checkCol: # once get to attacking piece (the piece checking the king) then break
                            break

                # remove moves that don't block check or move king
                # when removing items from a list while iterating through, start from the end of the list
                for i in range(len(possibleMoves)-1, -1, -1):
                    if possibleMoves[i].pieceMoved[1] != "K": # does not move king so must block or capture
                        if not (possibleMoves[i].endRow, possibleMoves[i].endCol) in validSquares: # move doesn't block check or capture checking piece
                            possibleMoves.remove(possibleMoves[i])

            else: # for double checks
                self.getKingMoves(kingRow, kingCol, possibleMoves)
        else: # not check so all moves are fine
            possibleMoves = self.getAllPossibleCaptures()

        if len(possibleMoves) == 0:
            if self.inCheck:
                self.checkMate = True
            else:
                self.staleMate = True
        else: # for undo moves
            self.checkMate = False
            self.staleMate = False

        self.enpassantPossible = tempEnpassantPossible
        return possibleMoves


    def checkForPinsChecks(self):
        pins = []
        checks = []
        inCheck = False

        if self.whiteToMove:
            enemyColor = "b"
            allyColor = "w"
            startRow = self.wKingLocation[0]
            startCol = self.wKingLocation[1]
        else:
            enemyColor = "w"
            allyColor = "b"
            startRow = self.bKingLocation[0]
            startCol = self.bKingLocation[1]

        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for j in range(len(directions)):
            d = directions[j]
            possiblePin = () # reset possible pins
            for i in range(1,8):
                endRow = startRow + d[0]*i
                endCol = startCol + d[1]*i
                if 0 <= endRow < 8 and 0 <= endCol < 8: # make sure not off the board
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] == allyColor and endPiece[1] != "K":
                        if possiblePin == (): # first possible pin
                            possiblePin = (endRow, endCol, d[0], d[1])
                        else: # second ally piece so no pin or check possible in that direction
                            break

                    elif endPiece[0] == enemyColor:
                        pieceType = endPiece[1]
                        # 5 cases + 1 more for knight
                        # 1) rook
                        # 2) bishop
                        # 3) diagonally a pawn attacking king
                        # 4) queen
                        # 5) any direction 1 sq away there is king
                        if (0 <= j <= 3 and pieceType == "R") or \
                                (4 <= j <= 7 and pieceType == "B") or \
                                (i == 1 and pieceType == "p" and ((enemyColor == "w" and 6 <= j <= 7) or (enemyColor == "b" and 4 <= j <= 5))) or \
                                (pieceType == "Q") or (i == 1 and pieceType == "K"):
                            if possiblePin == (): # no blocking pieces so check
                                inCheck = True
                                checks.append((endRow, endCol, d[0], d[1]))
                                break
                            else: # piece blocking so pin
                                 pins.append(possiblePin)
                        else: # enemy piece is not attacking with check
                            break
                else:
                    break # off board

        # knight moves
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for m in knightMoves:
            endRow = startRow + m[0]
            endCol = startCol + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:  # make sure not off the board
                endPiece = self.board[endRow][endCol]
                if endPiece[0] == enemyColor and endPiece[1] == "N": # enemy knight attacks king
                    inCheck = True
                    checks.append((endRow, endCol, m[0], m[1]))

        return inCheck, pins, checks


    # def inCheck(self):
    #     if self.whiteToMove:
    #         return self.sqUnderAttack(self.wKingLocation[0], self.wKingLocation[1])
    #     else:
    #         return self.sqUnderAttack(self.bKingLocation[0], self.bKingLocation[1])

    def sqUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove
        for move in oppMoves:
            if move.endRow == r and move.endCol == c:
                return True
        return False

    '''
    Moves w/o checks
    '''
    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])): # number of cols in given row
                turn = self.board[r][c][0]
                if (turn == "w" and self.whiteToMove) or (turn == "b" and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunction[piece](r, c, moves) # calls every get*Piece*Moves function
        return moves

    def getAllPossibleCaptures(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):  # number of cols in given row
                turn = self.board[r][c][0]
                if (turn == "w" and self.whiteToMove) or (turn == "b" and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.captureMoveFunction[piece](r, c, moves)  # calls every get*Piece*Moves function
        return moves

    '''
    Get all moves for piece at located row and col. Add these moves to the list
    '''
    def getPawnMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        enemyColor = "b" if self.whiteToMove else "w"
        if self.whiteToMove:
            if self.board[r-1][c] == "--": # 1 square move
                if not piecePinned or pinDirection == (-1, 0):
                    moves.append(MovePiece((r, c), (r-1, c), self.board))
                    if r == 6 and self.board[r-2][c] == "--": # 2 square move
                        moves.append(MovePiece((r, c), (r-2, c), self.board))

            # captures
            if c-1 >= 0:
                if self.board[r-1][c-1][0] == enemyColor:
                    if not piecePinned or pinDirection == (-1, -1):
                        moves.append(MovePiece((r, c), (r-1, c-1), self.board))
                elif (r-1,c-1) == self.enpassantPossible:
                    if not piecePinned or pinDirection == (-1,-1):
                        moves.append(MovePiece((r, c), (r - 1, c - 1), self.board, isEnpassantMove=True))

            if c+1 <= 7:
                if self.board[r-1][c+1][0] == enemyColor:
                    if not piecePinned or pinDirection == (-1, 1):
                        moves.append(MovePiece((r, c), (r-1, c+1), self.board))
                elif (r-1,c+1) == self.enpassantPossible:
                    if not piecePinned or pinDirection == (-1, 1):
                        moves.append(MovePiece((r, c), (r - 1, c+1), self.board, isEnpassantMove=True))

        else: # black pawn moves
            if self.board[(r+1)][c] == "--":
                if not piecePinned or pinDirection == (1, 0):
                    moves.append(MovePiece((r, c), ((r+1), c), self.board))
                    if r == 1 and self.board[r+2][c] == "--":
                        moves.append(MovePiece((r, c), (r+2, c), self.board))

            # captures
            if c-1 >= 0:
                if self.board[r+1][c-1][0] == enemyColor:
                    if not piecePinned or pinDirection == (1, -1):
                        moves.append(MovePiece((r, c), (r+1, c-1), self.board))
                elif (r+1,c-1) == self.enpassantPossible:
                    if not piecePinned or pinDirection == (1, -1):
                        moves.append(MovePiece((r, c), (r+1, c-1), self.board, isEnpassantMove=True))
            if c+1 <= 7:
                if self.board[r+1][c+1][0] == enemyColor:
                    if not piecePinned or pinDirection == (1, 1):
                        moves.append(MovePiece((r, c), (r+1, c+1), self.board))
                elif (r+1,c+1) == self.enpassantPossible:
                    if not piecePinned or pinDirection == (1, 1):
                        moves.append(MovePiece((r, c), (r+1, c+1), self.board, isEnpassantMove=True))

    def getPawnCaptures(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        enemyColor = "b" if self.whiteToMove else "w"
        if self.whiteToMove:
            # captures
            if c - 1 >= 0:
                if self.board[r - 1][c - 1][0] == enemyColor:
                    if not piecePinned or pinDirection == (-1, -1):
                        moves.append(MovePiece((r, c), (r - 1, c - 1), self.board))
                elif (r - 1, c - 1) == self.enpassantPossible:
                    if not piecePinned or pinDirection == (-1, -1):
                        moves.append(MovePiece((r, c), (r - 1, c - 1), self.board, isEnpassantMove=True))

            if c + 1 <= 7:
                if self.board[r - 1][c + 1][0] == enemyColor:
                    if not piecePinned or pinDirection == (-1, 1):
                        moves.append(MovePiece((r, c), (r - 1, c + 1), self.board))
                elif (r - 1, c + 1) == self.enpassantPossible:
                    if not piecePinned or pinDirection == (-1, 1):
                        moves.append(MovePiece((r, c), (r - 1, c + 1), self.board, isEnpassantMove=True))

        else:  # black pawn moves
            # captures
            if c - 1 >= 0:
                if self.board[r + 1][c - 1][0] == enemyColor:
                    if not piecePinned or pinDirection == (1, -1):
                        moves.append(MovePiece((r, c), (r + 1, c - 1), self.board))
                elif (r + 1, c - 1) == self.enpassantPossible:
                    if not piecePinned or pinDirection == (1, -1):
                        moves.append(MovePiece((r, c), (r + 1, c - 1), self.board, isEnpassantMove=True))
            if c + 1 <= 7:
                if self.board[r + 1][c + 1][0] == enemyColor:
                    if not piecePinned or pinDirection == (1, 1):
                        moves.append(MovePiece((r, c), (r + 1, c + 1), self.board))
                elif (r + 1, c + 1) == self.enpassantPossible:
                    if not piecePinned or pinDirection == (1, 1):
                        moves.append(MovePiece((r, c), (r + 1, c + 1), self.board, isEnpassantMove=True))


    def getKnightMoves(self, r, c, moves):
        piecePinned = False
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                self.pins.remove(self.pins[i])
                break

        directions = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))  # (row, col) -> left, right, up, down
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            endRow = r + d[0]
            endCol = c + d[1]
            if 0<=endRow<=7 and 0<=endCol<=7:
                if not piecePinned:
                    endPiece = self.board[endRow][endCol][0]
                    if self.board[endRow][endCol] == "--" or endPiece[0] == enemyColor:
                        moves.append(MovePiece((r, c), (endRow, endCol), self.board))

    def getKnightCaptures(self, r, c, moves):
        piecePinned = False
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                self.pins.remove(self.pins[i])
                break

        directions = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))  # (row, col) -> left, right, up, down
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            endRow = r + d[0]
            endCol = c + d[1]
            if 0<=endRow<=7 and 0<=endCol<=7:
                if not piecePinned:
                    endPiece = self.board[endRow][endCol][0]
                    if endPiece[0] == enemyColor:
                        moves.append(MovePiece((r, c), (endRow, endCol), self.board))



    def getBishopMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1)) # (row, col) -> top left, top right, bottom left, bottom right
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0]*i
                endCol = c + d[1] * i
                if 0 <= endRow <= 7 and 0 <= endCol <= 7:
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--":
                            moves.append(MovePiece((r, c), (endRow, endCol), self.board))
                        elif endPiece[0] == enemyColor:
                            moves.append(MovePiece((r, c), (endRow, endCol), self.board))
                            break
                        else: # friendly piece
                            break
                else: # off board
                    break

    def getBishopCaptures(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1)) # (row, col) -> top left, top right, bottom left, bottom right
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0]*i
                endCol = c + d[1] * i
                if 0 <= endRow <= 7 and 0 <= endCol <= 7:
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece[0] == enemyColor:
                            moves.append(MovePiece((r, c), (endRow, endCol), self.board))
                            break
                        else: # friendly piece
                            break
                else: # off board
                    break

    def getRookMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                if self.board[r][c][1] != "Q":
                    self.pins.remove(self.pins[i])
                break

        directions = ((0, -1), (0, 1), (-1, 0), (1, 0)) # (row, col) -> left, right, up, down
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0]*i
                endCol = c + d[1]*i
                if 0 <= endRow <= 7 and 0 <= endCol <= 7:
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--":
                            moves.append(MovePiece((r, c), (endRow, endCol), self.board))
                        elif endPiece[0] == enemyColor:
                            moves.append(MovePiece((r, c), (endRow, endCol), self.board))
                            break
                        else:  # friendly piece
                            break
                else:  # off board
                    break

    def getRookCaptures(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                if self.board[r][c][1] != "Q":
                    self.pins.remove(self.pins[i])
                break

        directions = ((0, -1), (0, 1), (-1, 0), (1, 0)) # (row, col) -> left, right, up, down
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0]*i
                endCol = c + d[1]*i
                if 0 <= endRow <= 7 and 0 <= endCol <= 7:
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece[0] == enemyColor:
                            moves.append(MovePiece((r, c), (endRow, endCol), self.board))
                            break
                        else:  # friendly piece
                            break
                else:  # off board
                    break


    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)

    def getQueenCaptures(self, r, c, moves):
        self.getRookCaptures(r, c, moves)
        self.getBishopCaptures(r, c, moves)

    def getKingMoves(self, r, c, moves):
        rowMoves = (-1, -1, -1, 0, 0, 1, 1, 1)
        colMoves = (-1, 0, 1, -1, 1, -1, 0, 1)
        allyColor = "w" if self.whiteToMove else "b"

        for i in range(8):
            endRow = r + rowMoves[i]
            endCol = c + colMoves[i]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    # place king on end square and check for checks
                    if allyColor == "w":
                        self.wKingLocation = (endRow, endCol)
                    else:
                        self.bKingLocation = (endRow, endCol)
                    inCheck, pins, checks = self.checkForPinsChecks()

                    if not inCheck:
                        moves.append(MovePiece((r, c), (endRow, endCol), self.board))

                    # place king back on original square
                    if allyColor == "w":
                        self.wKingLocation = (r,c)
                    else:
                        self.bKingLocation = (r,c)

    def getKingCaptures(self, r, c, moves):
        rowMoves = (-1, -1, -1, 0, 0, 1, 1, 1)
        colMoves = (-1, 0, 1, -1, 1, -1, 0, 1)
        allyColor = "w" if self.whiteToMove else "b"

        for i in range(8):
            endRow = r + rowMoves[i]
            endCol = c + colMoves[i]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor and endPiece != "--":
                    # place king on end square and check for checks
                    if allyColor == "w":
                        self.wKingLocation = (endRow, endCol)
                    else:
                        self.bKingLocation = (endRow, endCol)
                    inCheck, pins, checks = self.checkForPinsChecks()

                    if not inCheck:
                        moves.append(MovePiece((r, c), (endRow, endCol), self.board))

                    # place king back on original square
                    if allyColor == "w":
                        self.wKingLocation = (r,c)
                    else:
                        self.bKingLocation = (r,c)


    def getCastleMoves(self, r, c, moves):
        if self.sqUnderAttack(r, c):
            return #can't castle when in check
        if (self.whiteToMove and self.currentCastleRight.wks) or (not self.whiteToMove and self.currentCastleRight.bks):
            self.getKsCastleMoves(r, c, moves)
        if (self.whiteToMove and self.currentCastleRight.wqs) or (not self.whiteToMove and self.currentCastleRight.bqs):
            self.getQsCastleMoves(r, c, moves)

    def getKsCastleMoves(self, r, c, moves):
        if self.board[r][c+1] == "--" and self.board[r][c+2] == "--":
            if not self.sqUnderAttack(r, c+1) and not self.sqUnderAttack(r, c+2):
                 moves.append(MovePiece((r, c), (r, c+2), self.board, isCastleMove = True))


    def getQsCastleMoves(self, r, c, moves):
        if self.board[r][c-1] == "--" and self.board[r][c-2] == "--" and self.board[r][c-3] == "--":
            if not self.sqUnderAttack(r, c-1) and not self.sqUnderAttack(r, c-2) and not self.sqUnderAttack(r, c-3):
                 moves.append(MovePiece((r, c), (r, c-2), self.board, isCastleMove = True))


    def getControlledSquares(self):
        enemyControlledSquares = []
        enemyPiece = []
        playerControlledSquares = []
        playerPiece = []

        playerMoves = self.getValidMoves()

        self.whiteToMove = not self.whiteToMove
        oppMoves = self.getValidMoves()
        self.whiteToMove = not self.whiteToMove

        for move in playerMoves:
            endRow, endCol = move.endRow, move.endCol
            if self.board[endRow][endCol] == "--":
                playerControlledSquares.append((endRow, endCol))
                playerPiece.append(move.pieceMoved)

        for move in oppMoves:
            endRow, endCol = move.endRow, move.endCol
            if self.board[endRow][endCol] == "--":
                    enemyControlledSquares.append((endRow,endCol))
                    enemyPiece.append(move.pieceMoved)


        return playerPiece, playerControlledSquares, enemyPiece, enemyControlledSquares

    def getEnemyPawnAttackMap(self):
        pawnAttackSq = []

        for move in self.getValidMoves():
            if move.pieceMoved[1] == "p":
                pawnAttackSq.append((move.endRow, move.endCol))

        return pawnAttackSq

class CastleRights():
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs


class MovePiece():
    # key:value
    ranksToRows = {"1":7, "2":6, "3":5, "4":4, "5":3, "6":2, "7":1, "8":0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a":0, "b":1, "c":2, "d":3, "e":4, "f":5, "g":6, "h":7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSQ, endSQ, board, isEnpassantMove=False, isCastleMove=False):
        self.startRow = startSQ[0]
        self.startCol = startSQ[1]
        self.endRow = endSQ[0]
        self.endCol = endSQ[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]

        # pawn promo
        self.isPawnPromo = ((self.pieceMoved == "wp" and self.endRow == 0) or (self.pieceMoved == "bp" and self.endRow == 7))

        # enpassant
        self.isEnpassantMove = isEnpassantMove
        if self.isEnpassantMove:
            self.pieceCaptured = "wp" if self.pieceMoved == "bp" else "bp"

        self.isCapture = self.pieceCaptured != "--"

        # castle move
        self.isCastleMove = isCastleMove

        self.moveID = self.startRow*1000 + self.startCol*100 + self.endRow*10 + self.endCol

    '''
    Overriding the equals method
    '''
    def __eq__(self, other):
        if isinstance(other, MovePiece):
            return self.moveID == other.moveID
        return False


    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]

    def __str__(self): # overriding str() function
        # castle move
        if self.isCastleMove:
            return "O-O" if self.endCol == 6 else "O-O-O"

        endSquare = self.getRankFile(self.endRow, self.endCol)

        # pawn moves
        if self.pieceMoved[1] == "p":
            if self.isCapture:
                return self.colsToFiles[self.startCol] + "x" + endSquare
            else:
                return endSquare

            # pawn promo

        # two of same piece moving to a square ie. both knights move to same square

        # also adding + for check and '#' for checkmate

        # piece move
        moveString = self.pieceMoved[1]
        if self.isCapture:
            moveString += "x"
        return moveString + endSquare

    # debugging
    def __repr__(self):
        return (
            "<MovePiece"
            f" start=[{self.startRow},{self.startCol}]"
            f" end=[{self.endRow},{self.endCol}]"
            f" piece={self.pieceMoved}"
            ">"
        )
