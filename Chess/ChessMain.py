'''
MAIN DRIVER FILE.
Responsible for handling user input and displaying current GameState object.
'''
import pygame as p
from Chess import ChessEngine, ChessAI
from multiprocessing import Process, Queue

p.init()

BOARD_WIDTH = 512
BOARD_HEIGHT = 512
MOVELOG_WIDTH = 300
MOVELOG_HEIGHT = BOARD_HEIGHT
DIMENSION = 8  # 8x8 chess board
SQ_SIZE = BOARD_WIDTH // DIMENSION
MAX_FPS = 75
IMAGES = {}


def loadImages():
    pieces = ["bR", "bN", "bB", "bQ", "bK", "bp", "wR", "wN", "wB", "wQ", "wK", "wp"]
    for i in pieces:
        IMAGES[i] = p.transform.scale(p.image.load("chess_pieces/" + i + ".png"), (SQ_SIZE, SQ_SIZE))


'''
responsible for graphics of current game state
'''
def drawGameState(gameDisplay, gameState, validMoves, sqSelected, moveLogFont):
    drawBoard(gameDisplay) # draw board
    hightlightSquares(gameDisplay, gameState, validMoves, sqSelected, gameState.inCheck, gameState.moveLog) # highlighting
    drawPieces(gameDisplay, gameState.board) # draw pieces on the board
    drawMoveLog(gameDisplay, gameState, moveLogFont)


def drawBoard(gameDisplay):
    global colours
    colours = [p.Color("white"), p.Color("gray")]
    even = colours[0]
    odd = colours[1]
    for r in range(0,DIMENSION):
        for c in range(0,DIMENSION):
            colour = colours[((r+c)%2)]
            p.draw.rect(gameDisplay, colour, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


'''
responsible for highlighting selected piece and its moves
'''
def hightlightSquares(gameDisplay, gameState, validMoves, sqSelected, inCheck, moveLog):
    # highlight from where to where that the piece moved to
    if len(moveLog) != 0:
        lastMove = moveLog[-1]
        surfaceLastMove = p.Surface((SQ_SIZE, SQ_SIZE))
        surfaceLastMove.set_alpha(75)
        surfaceLastMove.fill(p.Color(0, 255, 0))
        gameDisplay.blit(surfaceLastMove, (lastMove.startCol * SQ_SIZE, lastMove.startRow * SQ_SIZE))
        gameDisplay.blit(surfaceLastMove, (lastMove.endCol * SQ_SIZE, lastMove.endRow * SQ_SIZE))

    if sqSelected != ():
        r, c = sqSelected
        # highlighting piece
        if gameState.board[r][c][0] == ("w" if gameState.whiteToMove else "b"):
            surface = p.Surface((SQ_SIZE, SQ_SIZE))
            surface.set_alpha(100) # transparency -> transparent 0-225 opaque
            surface.fill(p.Color(4, 217, 255))
            gameDisplay.blit(surface, (c*SQ_SIZE, r*SQ_SIZE))

            # highlight possible moves
            surface.fill(p.Color(255, 255, 59))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    gameDisplay.blit(surface, (move.endCol*SQ_SIZE, move.endRow*SQ_SIZE))

    # highlight checks
    if inCheck:
        r, c = gameState.wKingLocation if gameState.whiteToMove else gameState.bKingLocation
        surfaceInCheck = p.Surface((SQ_SIZE, SQ_SIZE))
        surfaceInCheck.set_alpha(130)
        surfaceInCheck.fill(p.Color(255,0,0))
        gameDisplay.blit(surfaceInCheck, (c * SQ_SIZE, r * SQ_SIZE))


def drawPieces(gameDisplay, board):
    for r in range(0, DIMENSION):
        for c in range(0, DIMENSION):
            piece = board[r][c]
            if piece != "--":
                gameDisplay.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawMoveLog(gameDisplay, gameState, font):
    moveLogRect = p.Rect(BOARD_WIDTH, 0, MOVELOG_WIDTH, MOVELOG_HEIGHT)
    p.draw.rect(gameDisplay, p.Color("white"), moveLogRect)
    moveLog = gameState.moveLog
    moveText = []
    if len(moveLog) != 0:
        for i in range(0, len(moveLog), 2):
            moveString = str(i//2 + 1) + ". " + str(moveLog[i]) + "  "
            if i+1 < len(moveLog): # make sure black made a move
                moveString += str(moveLog[i+1]) + "  "
            moveText.append(moveString)

        movesPerRow = 2
        padding = 5
        textY = padding
        lineSpacing = 5
        for i in range(0, len(moveText), movesPerRow):
            text = ""
            for j in range(movesPerRow):
                if i+j<len(moveText):
                    text += moveText[i+j]
            textObject = font.render(text, True, p.Color("black"))
            textLocation = moveLogRect.move(padding, textY)
            gameDisplay.blit(textObject, textLocation)
            textY += textObject.get_height() + lineSpacing


'''
animating move
'''
def animateMove(move, gameDisplay, board, clock):
    global colours
    dRow = move.endRow-move.startRow
    dCol = move.endCol-move.startCol
    framesPerSqaure = 6 # frames to move one square for animation
    frameCount = (abs(dRow) + abs(dCol))*framesPerSqaure
    for frame in range(frameCount+1):
        r, c = (move.startRow+dRow*frame/frameCount, move.startCol+dCol*frame/frameCount)
        drawBoard(gameDisplay)
        drawPieces(gameDisplay, board)
        # erase the piece moved from ending square
        color = colours[(move.endRow+move.endCol)%2]
        endSquare = p.Rect(move.endCol*SQ_SIZE, move.endRow*SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(gameDisplay, color, endSquare)
        # draw captured piece onto rectangle
        if move.pieceCaptured != "--":
            if move.isEnpassantMove:
                enpassantRow = move.endRow+1 if move.pieceCaptured[0] == "b" else move.endRow-1
                endSquare = p.Rect(move.endCol * SQ_SIZE, enpassantRow * SQ_SIZE, SQ_SIZE, SQ_SIZE)
            gameDisplay.blit(IMAGES[move.pieceCaptured], endSquare)
        # draw moving piece
        gameDisplay.blit(IMAGES[move.pieceMoved], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(75)

def drawEndGameText(gameDisplay, text):
    font = p.font.SysFont("Arial", 32, True, False)
    textObject = font.render(text, 0, p.Color("red"))
    textLocation = p.Rect(0, 0, BOARD_WIDTH, BOARD_HEIGHT).move(BOARD_WIDTH / 2 - textObject.get_width() / 2, BOARD_HEIGHT / 2 - textObject.get_height() / 2)
    gameDisplay.blit(textObject, textLocation)

'''
Main code driver.
Handle user input and update graphics.
'''
def main():
    #global returnQueue
    gameDisplay = p.display.set_mode((BOARD_WIDTH + MOVELOG_WIDTH, BOARD_HEIGHT))
    clock = p.time.Clock()
    moveLogFont = p.font.SysFont("Arial", 20, False, False)
    gameState = ChessEngine.GameState()
    validMoves = gameState.getValidMoves()
    moveMade = False
    loadImages()  # only load it once
    gameLoop = True
    sqSelected = () # last user click, (row, col) tuple
    playerClicks = [] # 2 tuples
    animate = False # flag for when to animate a move
    gameOver = False
    turnCounter = 0

    # Human or AI
    humanPlayerOne = 0 # FOR WHITE: if human playing true, if AI playing false
    humanPlayerTwo = 0 # FOR BLACK: same as above

    isAI_Thinking = False
    moveFinderProcess = None
    moveUndone = False


    while gameLoop:
        isHumanTurn = (gameState.whiteToMove and humanPlayerOne) or (not gameState.whiteToMove and humanPlayerTwo)

        for event in p.event.get():
            if event.type == p.QUIT:
                gameLoop = False

            # mouse press

            elif event.type == p.MOUSEBUTTONDOWN:
                if not gameOver:
                    mouse_location = p.mouse.get_pos() # (x,y) location of mouse
                    col = mouse_location[0] // SQ_SIZE
                    row = mouse_location[1] // SQ_SIZE
                    if sqSelected == (row, col) or col >= 8: # clicked twice or clicked on movelog
                        sqSelected = () # deselect
                        playerClicks = [] # clear previous click
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)
                    if len(playerClicks) == 2 and isHumanTurn:
                        move = ChessEngine.MovePiece(playerClicks[0], playerClicks[1], gameState.board)
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gameState.makeMove(validMoves[i]) # move created by engine not by player clicks
                                moveMade = True
                                animate = True
                                # resets to make 2nd move
                                sqSelected = ()
                                playerClicks = []
                        if not moveMade:
                            playerClicks = [sqSelected]

            # key press
            elif event.type == p.KEYDOWN:
                if event.key == p.K_LEFT: # undo when left arrow is pressed
                    gameState.undoMove()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = True
                    animate = False
                    gameOver = False
                    if isAI_Thinking:
                        moveFinderProcess.terminate()
                        isAI_Thinking = False
                    moveUndone = True

                if event.key == p.K_r: # reset board when "r" is pressed
                    # reset variables
                    gameState = ChessEngine.GameState()
                    validMoves = gameState.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False
                    gameOver = False
                    if isAI_Thinking:
                        moveFinderProcess.terminate()
                        isAI_Thinking = False
                    moveUndone = True

            # if moveMade: # flip board every turn
            #     gameState.flipBoard()
            #     turnCounter += 1
            #     if turnCounter%2 == 0:
            #         gameState.isBoardFlipped = False

        # AI move
        if not gameOver and not isHumanTurn and not moveUndone:
            if not isAI_Thinking:
                isAI_Thinking = True
                print("THINKING...")
                returnQueue = Queue() # used to pass data through threads
                moveFinderProcess = Process(target=ChessAI.findBestMove, args=(gameState, returnQueue))
                moveFinderProcess.start() # call

            if not moveFinderProcess.is_alive():
                print("DONE THINKING")
                AI_move = returnQueue.get()
                if AI_move is None:
                    AI_move = ChessAI.findRandomMove(validMoves)
                gameState.makeMove(AI_move)
                moveMade = True
                animate = True
                isAI_Thinking = False

        if moveMade:
            if animate:
                animateMove(gameState.moveLog[-1], gameDisplay, gameState.board, clock)
            validMoves = gameState.getValidMoves()
            moveMade = False
            animate = False
            moveUndone = False

        drawGameState(gameDisplay, gameState, validMoves, sqSelected, moveLogFont)

        if gameState.checkMate or gameState.staleMate:
            gameOver = True
            drawEndGameText(gameDisplay, "STALEMATE" if gameState.staleMate else "BLACK WINS BY CHECKMATE" if gameState.whiteToMove else "WHITE WINS BY CHECKMATE")


        clock.tick(MAX_FPS)
        p.display.flip()  # updates entire screen


# run the game
if __name__ == "__main__":  # allows main to run if main is imported
    main()