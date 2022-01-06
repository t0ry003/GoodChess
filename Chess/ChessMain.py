"""
Main Script
"""

import pygame as p
import ChessEngine

BOARD_WIDTH = BOARD_HEIGHT = 784
MOVE_LOG_PANEL_WIDTH = 250
MOVE_LOG_PANEL_HEIGHT = BOARD_HEIGHT
# tabla este de tipul 8x8
DIMENSION = 8
# marimea unui patrat
SQ_SIZE = BOARD_HEIGHT // DIMENSION
# numarul de fps-uri la care ruleaza jocul
MAX_FPS = 15
# pentru a adauga seturi de saj (skins)
IMAGES = {}
# window icon
WINDOW_ICON = p.image.load('images/icon.png')
# animate
animate = True


# incarcarea imaginilor intr-o lista IMAGES["culoarePiesa"]
def loadImages():
    pieces = ["wP", "wR", "wN", "wB", "wQ", "wK", "bP", "bR", "bN", "bB", "bQ", "bK"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))


# functia principala(main)
def main():
    p.init()
    p.display.set_icon(WINDOW_ICON)
    p.display.set_caption('Good Chess')
    screen = p.display.set_mode((BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    moveLogFont = p.font.SysFont("Arial", 25, False, False)
    gs = ChessEngine.GameState()  # gs = game state (statusul jocului in fiecare moemnt)
    loadImages()  # importam imaginile o singura data
    validMoves = gs.getValidMoves()
    moveMade = False  # semafor
    running = True
    sqSelected = ()  # nu este selectat nimic ((row, col))
    playerClicks = []  # memoria click-urilor(mutarilor). Ex: [(6,4), (4,4)]
    gameOver = False
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False

            # MOUSE BINDS
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver:
                    location = p.mouse.get_pos()  # pozitia (x,y)
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE
                    # pentru a nu muta in acelasi loc
                    if sqSelected == (row, col) or col >= 8:
                        sqSelected = ()  # reset
                        playerClicks = []  # reset
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)  # pentru primul si al doilea click
                    if len(playerClicks) == 2:  # dupa al doilea click
                        move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                        # DEBUG PRINT
                        # print(move.getChessNotation())
                        if move in validMoves:
                            gs.makeMove(move)
                            moveMade = True
                            animate = True
                            sqSelected = ()  # reset
                            playerClicks = []
                        else:
                            playerClicks = [sqSelected]


            # KEY BINDS
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()
                    moveMade = True
                    animate = False
                    gameOver = False
                if e.key == p.K_r:  # reset the board
                    gs = ChessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False
                    gameOver = False

        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1], screen, gs.board, clock)
            validMoves = gs.getValidMoves()
            moveMade = False
            animate = False

        drawGameState(screen, gs, validMoves, sqSelected, moveLogFont)

        if gs.checkMate:
            gameOver = True
            if gs.whiteToMove:
                drawText(screen, 'Black wins by checkmate')
            else:
                drawText(screen, 'Black wins by stalemate')
        elif gs.staleMate:
            gameOver = True
            drawText(screen, 'Stalemate')

        clock.tick(MAX_FPS)
        p.display.flip()


# functia care arata mutarile pe tabla
def highlightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'):
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)
            s.fill(p.Color('blue'))
            screen.blit(s, (SQ_SIZE * c, SQ_SIZE * r))
            s.fill(p.Color('yellow'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (move.endCol * SQ_SIZE, move.endRow * SQ_SIZE))


# pentru a adauga seturi de sah (skins)
def drawGameState(screen, gs, validMoves, sqSelected, moveLogFont):
    drawBoard(screen)
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board)
    drawMoveLog(screen, gs, moveLogFont)


# functia care afiseaza tabla de sah (drawBoard())
def drawBoard(screen):
    # BOARD COLORS
    global colors
    colors = [p.Color(240, 217, 181), p.Color(181, 136, 99)]
    # END BOARD COLORS

    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r + c) % 2)]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


# functia care afiseaza piesele in forma tablei de sah (drawPieces())
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            # verificam daca nu este loc gol (notat in lista ca "--")
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


# functie pentru log-ul de mutari
def drawMoveLog(screen, gs, font):
    moveLogRect = p.Rect(BOARD_WIDTH, 0, MOVE_LOG_PANEL_WIDTH, MOVE_LOG_PANEL_HEIGHT)
    p.draw.rect(screen, p.Color('black'), moveLogRect)
    moveLog = gs.moveLog
    moveTexts = moveLog
    padding = 5
    textY = padding
    lineSpacing = 2
    for i in range(len(moveTexts)):
        text = moveTexts[i].getChessNotation()
        textObject = font.render(text, True, p.Color('white'))
        textLocation = moveLogRect.move(padding, textY)
        screen.blit(textObject, textLocation)
        textY += textObject.get_height() + lineSpacing


# functia de animare a mutarii
def animateMove(move, screen, board, clock):
    global colors
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 10  # pentru un patrat
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare
    for frame in range(frameCount + 1):
        r, c = (move.startRow + dR * frame / frameCount, move.startCol + dC * frame / frameCount)
        drawBoard(screen)
        drawPieces(screen, board)
        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = p.Rect(move.endCol * SQ_SIZE, move.endRow * SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endSquare)
        # draw capture piece
        if move.pieceCaptured != '--':
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        # draw moving piece
        screen.blit(IMAGES[move.pieceMoved], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60)  # frame count for animation


def drawText(screen, text):
    font = p.font.SysFont("Helvitca", 45, True, False)
    textObject = font.render(text, 0, p.Color('Gray'))
    textLocation = p.Rect(0, 0, BOARD_WIDTH, BOARD_HEIGHT).move(BOARD_WIDTH / 2 - textObject.get_width() / 2,
                                                                BOARD_HEIGHT / 2 - textObject.get_height() / 2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, 0, p.Color('Black'))
    screen.blit(textObject, textLocation.move(2, 2))


# apelarea functiei principale
if __name__ == "__main__":
    main()
