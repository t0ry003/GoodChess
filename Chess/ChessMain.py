"""
Main Script
"""

# Imports
import json
import os
import random
import sys
import tkinter as t
import webbrowser
from tkinter import ttk

import ntkutils
import pygame as p
from pypresence import Presence
from tkmessagebox import *

import ChessEngine

# Constants
BOARD_WIDTH = BOARD_HEIGHT = 784
MOVE_LOG_PANEL_WIDTH = 250
MOVE_LOG_PANEL_HEIGHT = BOARD_HEIGHT
DIMENSION = 8
SQ_SIZE = BOARD_HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}
WINDOW_ICON = p.image.load('images/GAME/icon.png')
ANIMATE = True
SCROLL_OFFSET = 1
SCROLL_SPEED = 1
FRAMES_PER_SQUARE = 9
PRACTICE_MODE = False
SKIN = 'Default'
THEME = 'Default'
COLORS = 0
MOVES_LOG = []
PROMOTION_PIECE = 'Queen'
CLIENT_ID = '1187143441830912150'
DRP = True
RPC = Presence(CLIENT_ID)

try:
    RPC.connect()
except Exception as ex:
    print(f"Error connecting to Discord RPC: {ex}")
    DRP = False

if DRP:
    RPC.update(
        details="Playing Good Chess",
        small_image="icon",
        buttons=[{"label": "⭐ Github", "url": "https://github.com/t0ry003/GoodChess"}]
    )


def menu():
    """
        Display a GUI window to allow the user to choose the skin and theme for the chessboard.

        Updates global variables SKIN, THEME, and COLORS.

        This function uses a Tkinter window to prompt the user for skin and theme preferences and updates global
        variables accordingly.
    """

    def load_chess_data(file_path):
        with open(file_path, 'r') as file:
            chess_data = json.load(file)
        return chess_data

    def show_last_moves():
        file_path = ".moves_log.json"
        if not os.path.isfile(file_path):
            showerror("ERROR", "No data to show.")
            return

        chess_data = load_chess_data(file_path)
        if chess_data:
            show_chess_data(chess_data)
        else:
            print("Error loading chess data from the file or no data to show.")

    def apply_selection():
        global SKIN, THEME, COLORS, FRAMES_PER_SQUARE, PRACTICE_MODE
        SKIN = skin_combo.get()
        THEME = theme_combo.get()

        if THEME == 'Default':
            COLORS = [p.Color(240, 217, 181), p.Color(181, 136, 99)]
        elif THEME == 'Dark':
            COLORS = [p.Color(150, 150, 150), p.Color(50, 50, 50)]
        elif THEME == 'Green':
            COLORS = [p.Color(238, 238, 210), p.Color(118, 150, 86)]

        FRAMES_PER_SQUARE = int(anim_combo.get()[0])
        PRACTICE_MODE = var_practice_mode.get()

        save_settings_to_cfg()

        shutdown_ttk_repeat()

    def shutdown_ttk_repeat():
        root.eval('::ttk::CancelRepeat')
        root.destroy()
        root.quit()

    def open_github():
        webbrowser.open("https://github.com/t0ry003/GoodChess")

    def show_chess_data(chess_data):
        top = t.Toplevel()
        ntkutils.dark_title_bar(top)
        top.title("Data Viewer")
        top.iconbitmap("images/game/icon.ico")

        top_window_width = 280
        top_window_height = 250
        top_screen_width = top.winfo_screenwidth()
        top_screen_height = top.winfo_screenheight()
        top_x_position = (top_screen_width - top_window_width) // 2
        top_y_position = (top_screen_height - top_window_height) // 2
        top.geometry(f"{top_window_width}x{top_window_height}+{top_x_position}+{top_y_position}")

        tree = ttk.Treeview(top, columns=('No', 'Player', 'Move'), show='headings', style='Treeview')
        tree.heading('No', text='No', anchor='center')
        tree.heading('Player', text='Player', anchor='center')
        tree.heading('Move', text='Move', anchor='center')
        # make a scroll bar that moves the treeview up and down
        scroll = ttk.Scrollbar(top, orient='vertical', command=tree.yview)

        for move in chess_data:
            tree.insert('', 'end', values=(move['number'], move['player'], move['move']))

        tree.column('No', width=30)
        tree.column('Player', width=100)
        tree.column('Move', width=100)

        tree.configure(yscrollcommand=scroll.set)
        scroll.pack(side='right', fill='y')
        tree.pack(side='left', fill='both', expand=True)

        top.mainloop()

    global SKIN, THEME, COLORS, FRAMES_PER_SQUARE, PRACTICE_MODE
    root = t.Tk()
    ntkutils.dark_title_bar(root)

    root.title("Good Chess")
    root.iconbitmap("images/game/icon.ico")

    window_width = 350
    window_height = 650
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    main_logo = ImageTk.PhotoImage(Image.open("./images/GAME/icon.ico").resize((150, 150)))

    play_icon = t.PhotoImage(file='./images/GAME/play-icon.png')

    skin_label = ttk.Label(root, text="Choose Skin:")
    skin_combo = ttk.Combobox(root, values=["Default", "Fantasy", "Minimalist"])
    skin_combo.set(SKIN)

    theme_label = ttk.Label(root, text="Choose Theme:")
    theme_combo = ttk.Combobox(root, values=["Default", "Dark", "Green"])
    theme_combo.set(THEME)

    anim_label = ttk.Label(root, text="Choose Animation Speed:")
    anim_combo = ttk.Combobox(root, width=4, values=["1 (FAST)", "2", "3", "4", "5", "6", "7", "8", "9 (SLOW)"])
    anim_combo.set(FRAMES_PER_SQUARE)

    var_practice_mode = t.IntVar(value=0)
    if PRACTICE_MODE == '1':
        var_practice_mode = t.IntVar(value=1)
    practice_mode_checkbox = ttk.Checkbutton(root, text="Practice Mode", variable=var_practice_mode)

    logo_label = ttk.Label(root, image=main_logo)

    apply_button = ttk.Button(root, command=apply_selection, image=play_icon)
    show_moves_button = ttk.Button(root, text="Show Last Moves", command=show_last_moves)

    github_button = ttk.Button(root, text="\u2B50 GitHub", command=open_github)

    logo_label.pack(pady=10)
    skin_label.pack(pady=0)
    skin_combo.pack(pady=10)
    theme_label.pack(pady=0)
    theme_combo.pack(pady=10)
    anim_label.pack(pady=0)
    anim_combo.pack(pady=10)
    practice_mode_checkbox.pack(pady=10)
    apply_button.pack(pady=20)
    show_moves_button.pack(pady=10)
    github_button.pack(side=t.LEFT, padx=10, pady=10)

    root.tk.call('source', './images/THEME/sun-valley.tcl')
    root.tk.call('set_theme', 'dark')
    root.protocol("WM_DELETE_WINDOW", shutdown_ttk_repeat)
    root.mainloop()


def ask_pawn_promotion():
    """
    Ask the player which piece to promote the pawn to.

    This function uses a Tkinter window to prompt the player for a piece to promote the pawn to.
    """

    def on_closing():
        global PROMOTION_PIECE
        PROMOTION_PIECE = 'Queen'
        popup.destroy()
        popup.quit()

    def apply_selection():
        global PROMOTION_PIECE
        PROMOTION_PIECE = promotion_combo.get()
        popup.destroy()
        popup.quit()

    global PROMOTION_PIECE
    popup = t.Tk()
    ntkutils.dark_title_bar(popup)

    popup.tk.call('source', './images/THEME/sun-valley.tcl')
    popup.tk.call('set_theme', 'dark')

    popup.title("Pawn Promotion")
    popup.iconbitmap("images/GAME/icon.ico")

    window_width = 350
    window_height = 200
    screen_width = popup.winfo_screenwidth()
    screen_height = popup.winfo_screenheight()
    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2
    popup.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    promotion_label = ttk.Label(popup, text="Choose a piece to promote the pawn to:")
    promotion_combo = ttk.Combobox(popup, values=["Queen", "Rook", "Bishop", "Knight"])
    promotion_combo.set("Queen")

    apply_button = ttk.Button(popup, text="APPLY", command=apply_selection)

    promotion_label.pack(pady=10)
    promotion_combo.pack(pady=10)
    apply_button.pack(pady=20)

    popup.protocol("WM_DELETE_WINDOW", on_closing)
    popup.mainloop()
    return PROMOTION_PIECE[0]


def load_images():
    """
    Load chess piece images based on the chosen skin.

    This function loads images of chess pieces based on the global variable SKIN and scales them to the appropriate size
    """

    pieces = ["wP", "wR", "wN", "wB", "wQ", "wK", "bP", "bR", "bN", "bB", "bQ", "bK"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/SKIN_" + SKIN + "/" + piece + ".png"),
                                          (SQ_SIZE, SQ_SIZE))


def highlight_squares(screen, gs, validMoves, sqSelected):
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
            s.set_alpha(130)

            if gs.in_check():
                s.fill(p.Color('red'))
                screen.blit(s, (SQ_SIZE * c, SQ_SIZE * r))
            else:
                s.fill(p.Color('blue'))
                screen.blit(s, (SQ_SIZE * c, SQ_SIZE * r))

            s.fill(p.Color('yellow'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (move.endCol * SQ_SIZE, move.endRow * SQ_SIZE))


def draw_game_state(screen, gs, validMoves, sqSelected, moveLogFont):
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

    draw_board(screen)
    highlight_squares(screen, gs, validMoves, sqSelected)
    draw_pieces(screen, gs.board)
    draw_move_log(screen, gs, moveLogFont)


def draw_board(screen):
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


def draw_pieces(screen, board):
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


def draw_move_log(screen, gs, font):
    """
    Draw the move log on the right side of the chessboard.

    Args:
    - screen: The Pygame display surface.
    - gs: The current game state.
    - font: Pygame font for the move log.

    This function draws the move log on the right side of the chessboard.
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
        text = f"{move_number}. {moveTexts[i].get_chess_notation()}"
        textObject = font.render(text, True, p.Color('white'))
        textLocation = moveLogRect.move(padding, textY)
        screen.blit(textObject, textLocation)
        textY += textObject.get_height() + lineSpacing

        if i >= len(MOVES_LOG):
            MOVES_LOG.append(moveTexts[i].get_chess_notation())

    if len(moveTexts) > visible_lines:
        SCROLL_OFFSET += SCROLL_SPEED
        if SCROLL_OFFSET > (len(moveTexts) - visible_lines) * (font.get_height() + lineSpacing):
            SCROLL_OFFSET = 0


def animate_move(move, screen, board, clock):
    """
    Animate a chess move on the chessboard.

    Args:
    - move: The move to animate.
    - screen: The Pygame display surface.
    - board: The current chessboard state.
    - clock: Pygame clock for controlling animation speed.

    This function animates a chess move on the chessboard, updating the screen and clock accordingly.
    """

    global COLORS, FRAMES_PER_SQUARE
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    frameCount = (abs(dR) + abs(dC)) * FRAMES_PER_SQUARE
    for frame in range(frameCount + 1):
        r, c = (move.startRow + dR * frame / frameCount, move.startCol + dC * frame / frameCount)
        draw_board(screen)
        draw_pieces(screen, board)
        color = COLORS[(move.endRow + move.endCol) % 2]
        endSquare = p.Rect(move.endCol * SQ_SIZE, move.endRow * SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endSquare)
        if move.pieceCaptured != '--':
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        screen.blit(IMAGES[move.pieceMoved], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60)


def draw_text(screen, text, font_size=60, font_color='Black', shadow_color='White'):
    """
    Draw enhanced text on the screen.

    Args:
    - screen: The Pygame display surface.
    - text: The text to display.
    - font_size: The size of the font.
    - font_color: The color of the text.
    - shadow_color: The color of the text shadow.
    """

    font = p.font.SysFont("Arial", font_size, True, False)

    textObject = font.render(text, True, p.Color(shadow_color))
    textLocation = p.Rect(0, 0, BOARD_WIDTH, BOARD_HEIGHT).move(
        BOARD_WIDTH / 2 - textObject.get_width() / 2,
        BOARD_HEIGHT / 2 - textObject.get_height() / 2
    )

    screen.blit(textObject, textLocation)

    textObject = font.render(text, True, p.Color(font_color))
    shadow_location = textLocation.move(2, 2)

    screen.blit(textObject, shadow_location)


def save_moves_to_json(moves_log):
    """
    Save the moves log to a JSON file with timestamps.

    Args:
    - moves_log: List of chess moves.

    This function converts the moves log to a JSON format, including timestamps, and saves it to a file named
    'moves_log.json'.
    """
    player_moves = []
    white_name = "White"
    black_name = "Black"
    for i in range(len(moves_log)):
        if i % 2 == 0:
            player_moves.append({
                "number": i + 1,
                "player": white_name,
                "move": moves_log[i]
            })
        else:
            player_moves.append({
                "number": i + 1,
                "player": black_name,
                "move": moves_log[i]
            })

    with open('.moves_log.json', 'w') as json_file:
        json.dump(player_moves, json_file)


def save_settings_to_cfg():
    """
    Save the current settings to a config file.

    This function saves the current settings to a config file named 'settings.cfg'.
    """

    global SKIN, THEME, FRAMES_PER_SQUARE, PRACTICE_MODE
    with open('settings.cfg', 'w') as file:
        file.write(f"SKIN={SKIN}\n")
        file.write(f"THEME={THEME}\n")
        file.write(f"FRAMES_PER_SQUARE={FRAMES_PER_SQUARE}\n")
        file.write(f"PRACTICE_MODE={PRACTICE_MODE}\n")


def load_settings_from_cfg():
    """
    Load the current settings from a config file.

    This function loads the current settings from a config file named 'settings.cfg'.
    """

    global SKIN, THEME, FRAMES_PER_SQUARE, PRACTICE_MODE
    try:
        with open('settings.cfg', 'r') as file:
            lines = file.readlines()
            SKIN = lines[0].split('=')[1].strip()
            THEME = lines[1].split('=')[1].strip()
            FRAMES_PER_SQUARE = lines[2].split('=')[1].strip()
            PRACTICE_MODE = lines[3].split('=')[1].strip()
    except FileNotFoundError:
        print("Settings file not found. Using default settings.")
        set_default_settings()
    except IndexError:
        print("Error loading settings file. Using default settings.")
        set_default_settings()
    except Exception as e:
        print(f"Error loading settings file: {e}")
        set_default_settings()


def set_default_settings():
    """
    Set the default settings.

    This function sets the default settings.
    """

    global SKIN, THEME, FRAMES_PER_SQUARE, PRACTICE_MODE
    SKIN = 'Default'
    THEME = 'Default'
    FRAMES_PER_SQUARE = 9
    PRACTICE_MODE = False


def main():
    """
    Run the main chess game loop.

    This function initializes the chess game and runs the main game loop, handling player input and updating the game
    state accordingly.
    """

    global SKIN, THEME, COLORS, MOVES_LOG, ANIMATE, PRACTICE_MODE, RPC
    menu()
    if COLORS == 0:
        sys.exit("Game did not start. Please choose a skin and theme and press START.")
    p.init()
    p.display.set_icon(WINDOW_ICON)
    p.display.set_caption('Good Chess')
    screen = p.display.set_mode((BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    moveLogFont = p.font.SysFont("Arial", 25, False, False)
    gs = ChessEngine.GameState()
    load_images()
    validMoves = gs.get_valid_moves()
    moveMade = False
    running = True
    sqSelected = ()
    playerClicks = []
    gameOver = False

    while running:
        for e in p.event.get():
            if e.type != p.MOUSEMOTION:
                if DRP:
                    RPC.update(
                        details="Playing Good Chess",
                        state=f"Moves: {len(MOVES_LOG)}",
                        large_image="icon",
                        small_image=f"{random.choices(['wb', 'wk', 'wn', 'wp', 'wq', 'wr'])[0]}",
                        buttons=[{"label": "⭐ Github", "url": "https://github.com/t0ry003/GoodChess"}]
                    )

            if e.type == p.QUIT:
                running = False

            elif e.type == p.MOUSEBUTTONDOWN and e.button == 1:
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
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                if validMoves[i].isPawnPromotion:
                                    piece = ask_pawn_promotion()
                                    gs.promotionChoice = piece
                                gs.make_move(validMoves[i])
                                moveMade = True
                                ANIMATE = True
                                sqSelected = ()
                                playerClicks = []
                        if not moveMade:
                            playerClicks = [sqSelected]

            elif (e.type == p.KEYDOWN and PRACTICE_MODE) or (e.type == p.KEYDOWN and gameOver):
                if e.key == p.K_z:
                    gs.undo_move()
                    if len(MOVES_LOG) > 0:
                        MOVES_LOG.pop()
                    moveMade = True
                    ANIMATE = False
                    gameOver = False
                if e.key == p.K_r:
                    gs = ChessEngine.GameState()
                    validMoves = gs.get_valid_moves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    ANIMATE = False
                    gameOver = False
                if e.key == p.K_ESCAPE:
                    PRACTICE_MODE = False

            elif e.type == p.KEYDOWN and e.key == p.K_ESCAPE:
                PRACTICE_MODE = True

            elif e.type == p.KEYDOWN:
                pass

        if moveMade:
            if ANIMATE:
                animate_move(gs.moveLog[-1], screen, gs.board, clock)
            validMoves = gs.get_valid_moves()
            moveMade = False
            ANIMATE = False

        draw_game_state(screen, gs, validMoves, sqSelected, moveLogFont)

        if gs.checkMate:
            gameOver = True
            if gs.whiteToMove:
                draw_text(screen, 'Black wins by checkmate', font_color='Black', shadow_color='Red')
            else:
                draw_text(screen, 'White wins by checkmate', font_color='White', shadow_color='Green')
        elif gs.staleMate:
            gameOver = True
            draw_text(screen, 'Stalemate')

        clock.tick(MAX_FPS)
        p.display.flip()


if __name__ == "__main__":
    load_settings_from_cfg()

    main()

    if len(MOVES_LOG) >= 2:
        save_moves_to_json(MOVES_LOG)

    if DRP:
        RPC.close()
