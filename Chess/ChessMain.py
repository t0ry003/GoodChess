"""
Main Script
"""

import json
import pygame as p
import tkinter as t
from tkinter import ttk
from datetime import datetime
import ChessEngine

# Constants
BOARD_WIDTH = BOARD_HEIGHT = 784
MOVE_LOG_PANEL_WIDTH = 250
MOVE_LOG_PANEL_HEIGHT = BOARD_HEIGHT
DIMENSION = 8
SQ_SIZE = BOARD_HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}
WINDOW_ICON = p.image.load('images/game/icon.png')
ANIMATE = True
SCROLL_OFFSET = 0
SCROLL_SPEED = 1

# Global variables
global SKIN, THEME, COLORS, MOVES_LOG
SKIN = 'Default'
THEME = 'Default'
MOVES_LOG = []


def choose_skin_theme():
    """
        Display a GUI window to allow the user to choose the skin and theme for the chessboard.

        Updates global variables SKIN, THEME, and COLORS.

        This function uses a Tkinter window to prompt the user for skin and theme preferences and updates global variables accordingly.
    """

    global SKIN, THEME, COLORS
    root = t.Tk()
    root.title("Good Chess | Settings")
    root.iconbitmap("images/game/icon.ico")

    window_width = 350
    window_height = 300
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    dark_bg = "#1E1E1E"
    dark_fg = "white"
    dark_highlight_bg = "#353535"

    style = ttk.Style()
    style.theme_use("clam")

    style.configure("TLabel", background=dark_bg, foreground=dark_fg)
    style.configure("TCombobox", fieldbackground=dark_bg, background=dark_highlight_bg, foreground=dark_fg)
    style.configure("TButton", background=dark_bg, foreground=dark_fg)

    skin_label = ttk.Label(root, text="Choose Skin:")
    skin_combo = ttk.Combobox(root, values=["Default", "Fantasy", "Minimalist"])
    skin_combo.set(SKIN)

    theme_label = ttk.Label(root, text="Choose Theme:")
    theme_combo = ttk.Combobox(root, values=["Default", "Dark", "Green"])  # Add more theme options if needed
    theme_combo.set(THEME)

    def apply_selection():
        global SKIN, THEME, COLORS
        SKIN = skin_combo.get()
        THEME = theme_combo.get()

        if THEME == 'Default':
            COLORS = [p.Color(240, 217, 181), p.Color(181, 136, 99)]
        elif THEME == 'Dark':
            COLORS = [p.Color(150, 150, 150), p.Color(50, 50, 50)]
        elif THEME == 'Green':
            COLORS = [p.Color(238, 238, 210), p.Color(118, 150, 86)]

        root.destroy()

    apply_button = ttk.Button(root, text="Apply", command=apply_selection)

    skin_label.pack(pady=10)
    skin_combo.pack(pady=10)
    theme_label.pack(pady=10)
    theme_combo.pack(pady=10)
    apply_button.pack(pady=20)

    root.configure(background=dark_bg)
    root.mainloop()


def loadImages():
    """
    Load chess piece images based on the chosen skin.

    This function loads images of chess pieces based on the global variable SKIN and scales them to the appropriate size.
    """

    pieces = ["wP", "wR", "wN", "wB", "wQ", "wK", "bP", "bR", "bN", "bB", "bQ", "bK"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/SKIN_" + SKIN + "/" + piece + ".png"),
                                          (SQ_SIZE, SQ_SIZE))


def main():
    """
    Run the main chess game loop.

    This function initializes the chess game and runs the main game loop, handling player input and updating the game state accordingly.
    """

    global SKIN, THEME, COLORS
    choose_skin_theme()
    p.init()
    p.display.set_icon(WINDOW_ICON)
    p.display.set_caption('Good Chess')
    screen = p.display.set_mode((BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    moveLogFont = p.font.SysFont("Arial", 25, False, False)
    gs = ChessEngine.GameState()
    loadImages()
    validMoves = gs.getValidMoves()
    moveMade = False
    running = True
    sqSelected = ()
    playerClicks = []
    gameOver = False

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False

            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver:
                    location = p.mouse.get_pos()
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE
                    if sqSelected == (row, col) or col >= 8:
                        sqSelected = ()
                        playerClicks = []
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)
                    if len(playerClicks) == 2:
                        move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                        if move in validMoves:
                            gs.makeMove(move)
                            moveMade = True
                            animate = True
                            sqSelected = ()
                            playerClicks = []
                        else:
                            playerClicks = [sqSelected]


            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()
                    moveMade = True
                    animate = False
                    gameOver = False
                if e.key == p.K_r:
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


def highlightSquares(screen, gs, validMoves, sqSelected):
    """
    Highlight valid moves on the chessboard.

    Args:
    - screen: The Pygame display surface.
    - gs: The current game state.
    - validMoves: List of valid moves.
    - sqSelected: The selected square.

    This function highlights the selected square and valid moves on the chessboard.
    """

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


def drawGameState(screen, gs, validMoves, sqSelected, moveLogFont):
    """
    Draw the current state of the chessboard.

    Args:
    - screen: The Pygame display surface.
    - gs: The current game state.
    - validMoves: List of valid moves.
    - sqSelected: The selected square.
    - moveLogFont: Pygame font for the move log.

    This function draws the chessboard, pieces, and move log on the screen based on the provided parameters.
    """

    drawBoard(screen)
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board)
    drawMoveLog(screen, gs, moveLogFont)


def drawBoard(screen):
    """
    Draw the chessboard grid on the screen.

    Args:
    - screen: The Pygame display surface.

    This function draws the grid of the chessboard on the provided Pygame display surface.
    """

    global COLORS
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = COLORS[((r + c) % 2)]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawPieces(screen, board):
    """
    Draw the chess pieces on the chessboard.

    Args:
    - screen: The Pygame display surface.
    - board: The current chessboard state.

    This function draws the chess pieces on the chessboard based on the provided board state.
    """

    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawMoveLog(screen, gs, font):
    """
    Draw the move log on the right side of the chessboard.

    Args:
    - screen: The Pygame display surface.
    - gs: The current game state.
    - font: Pygame font for the move log.

    This function draws the move log on the right side of the chessboard, including timestamps for each move.
    """

    global SCROLL_OFFSET, MOVES_LOG
    moveLogRect = p.Rect(BOARD_WIDTH, 0, MOVE_LOG_PANEL_WIDTH, MOVE_LOG_PANEL_HEIGHT)
    p.draw.rect(screen, p.Color('black'), moveLogRect)
    moveLog = gs.moveLog
    moveTexts = moveLog
    padding = 5
    textY = padding - SCROLL_OFFSET
    lineSpacing = 2
    visible_lines = MOVE_LOG_PANEL_HEIGHT // (font.get_height() + lineSpacing)

    for i in range(len(moveTexts)):
        move_number = i + 1
        text = f"{move_number}. {moveTexts[i].getChessNotation()}"
        textObject = font.render(text, True, p.Color('white'))
        textLocation = moveLogRect.move(padding, textY)
        screen.blit(textObject, textLocation)
        textY += textObject.get_height() + lineSpacing

        if i >= len(MOVES_LOG):
            MOVES_LOG.append(moveTexts[i].getChessNotation())

    if len(moveTexts) > visible_lines:
        SCROLL_OFFSET += SCROLL_SPEED
        if SCROLL_OFFSET > (len(moveTexts) - visible_lines) * (font.get_height() + lineSpacing):
            SCROLL_OFFSET = 0


def animateMove(move, screen, board, clock):
    """
    Animate a chess move on the chessboard.

    Args:
    - move: The move to animate.
    - screen: The Pygame display surface.
    - board: The current chessboard state.
    - clock: Pygame clock for controlling animation speed.

    This function animates a chess move on the chessboard, updating the screen and clock accordingly.
    """

    global COLORS
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 10
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare
    for frame in range(frameCount + 1):
        r, c = (move.startRow + dR * frame / frameCount, move.startCol + dC * frame / frameCount)
        drawBoard(screen)
        drawPieces(screen, board)
        color = COLORS[(move.endRow + move.endCol) % 2]
        endSquare = p.Rect(move.endCol * SQ_SIZE, move.endRow * SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endSquare)
        if move.pieceCaptured != '--':
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        screen.blit(IMAGES[move.pieceMoved], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60)


def drawText(screen, text):
    """
    Draw text on the screen.

    Args:
    - screen: The Pygame display surface.
    - text: The text to display.

    This function draws text on the screen using a specified font.
    """

    font = p.font.SysFont("Helvitca", 45, True, False)
    textObject = font.render(text, 0, p.Color('Gray'))
    textLocation = p.Rect(0, 0, BOARD_WIDTH, BOARD_HEIGHT).move(BOARD_WIDTH / 2 - textObject.get_width() / 2,
                                                                BOARD_HEIGHT / 2 - textObject.get_height() / 2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, 0, p.Color('Black'))
    screen.blit(textObject, textLocation.move(2, 2))


def save_moves_to_json(moves_log):
    """
    Save the moves log to a JSON file with timestamps.

    Args:
    - moves_log: List of chess moves.

    This function converts the moves log to a JSON format, including timestamps, and saves it to a file named 'moves_log.json'.
    """

    timestamped_moves = [{'timestamp': str(datetime.now()), 'move': move} for move in moves_log]

    with open('moves_log.json', 'w') as json_file:
        json.dump(timestamped_moves, json_file)


if __name__ == "__main__":
    main()
    save_moves_to_json(MOVES_LOG)
