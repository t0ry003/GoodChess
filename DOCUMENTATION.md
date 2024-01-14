# Good Chess Documentation

<a href="#chessmain">ChessMain.py</a></br>
<a href="#chessengine">ChessEngine.py</a></br>
<a href="#credits">Credits</a>

## ChessMain

### Imports

- `json`: Used for handling JSON data.
- `os`: Provides a way of interacting with the operating system.
- `sys`: Provides access to some variables used or maintained by the interpreter.
- `pygame`: Library for creating games and multimedia applications.
- `tkinter`: GUI library for creating interfaces.
- `ttk`: Tkinter themed widgets.
- `webbrowser`: Module for displaying Web-based documents to users.
- `tkmessagebox`: Module for creating standard Tkinter dialogs.
- `ntkutils`: Custom utilities related to Tkinter.
- `pypresence`: Discord Rich Presence library.
- `ChessEngine`: Module containing the chess game logic.

### Constants

- `BOARD_WIDTH` and `BOARD_HEIGHT`: Dimensions of the chessboard.
- `MOVE_LOG_PANEL_WIDTH` and `MOVE_LOG_PANEL_HEIGHT`: Dimensions of the move log panel.
- `DIMENSION`: Number of rows and columns on the chessboard.
- `SQ_SIZE`: Size of each square on the chessboard.
- `MAX_FPS`: Maximum frames per second for the game loop.
- `IMAGES`: Dictionary to store images of chess pieces.
- `WINDOW_ICON`: Icon for the game window.
- `ANIMATE`: Flag to control animation.
- `SCROLL_OFFSET`: Offset for scrolling the move log.
- `SCROLL_SPEED`: Speed of scrolling in the move log.
- `FRAMES_PER_SQUARE`: Number of frames per square for animation.
- `PRACTICE_MODE`: Flag indicating whether the game is in practice mode.
- `SKIN` and `THEME`: Variables for storing the chosen skin and theme.
- `COLORS`: Color scheme based on the chosen theme.
- `MOVES_LOG`: List to store chess moves.
- `PROMOTION_PIECE`: Default pawn promotion piece.
- `CLIENT_ID`: Discord client ID for Rich Presence.
- `RPC`: Discord Rich Presence client.

### Function: `menu()`

Display a GUI window to allow the user to choose the skin and theme for the chessboard. Updates global
variables `SKIN`, `THEME`, and `COLORS`. Uses a Tkinter window to prompt the user for skin and theme preferences.

### Function: `ask_pawn_promotion()`

Ask the player which piece to promote the pawn to using a Tkinter window.

### Function: `load_images()`

Load chess piece images based on the chosen skin and scale them to the appropriate size.

### Function: `highlight_squares(screen, gs, validMoves, sqSelected)`

Highlight the selected square and valid moves on the chessboard.

### Function: `draw_game_state(screen, gs, validMoves, sqSelected, moveLogFont)`

Draw the chessboard, pieces, and move log on the screen based on provided parameters.

### Function: `draw_board(screen)`

Draw the chessboard grid on the screen.

### Function: `draw_pieces(screen, board)`

Draw the chess pieces on the chessboard based on the provided board state.

### Function: `draw_move_log(screen, gs, font)`

Draw the move log on the right side of the chessboard.

### Function: `animate_move(move, screen, board, clock)`

Animate a chess move on the chessboard, updating the screen and clock accordingly.

### Function: `draw_text(screen, text, font_size=60, font_color='Black', shadow_color='White')`

Draw enhanced text on the screen.

### Function: `save_moves_to_json(moves_log)`

Save the moves log to a JSON file with timestamps. Converts the moves log to JSON format, including timestamps, and
saves it to a file named 'moves_log.json'.

### Function: `save_settings_to_cfg()`

Save the current skin and theme to a configuration file. Saves the current skin and theme to a configuration file

### Function: `load_settings_from_cfg()`

Load the skin and theme from a configuration file. Loads the skin and theme from a configuration file.

### Function: `main()`

Run the main chess game loop. Initializes the chess game and runs the main game loop, handling player input and updating
the game state accordingly.

Note: Save moves log to JSON after the game ends.

## ChessEngine

## `GameState` Class

### Description

The `GameState` class represents the state of a chess game. It includes the current chessboard, move functions for each
piece, information about whose turn it is, a move log, and additional details such as the locations of kings, checkmate,
and stalemate conditions.

### Attributes

- `board`: 2D list representing the chessboard.
- `moveFunctions`: Dictionary mapping piece types to their move functions.
- `whiteToMove`: Boolean indicating if it's White's turn.
- `moveLog`: List to keep track of the moves made in the game.
- `promotionChoice`: Default pawn promotion choice.
- `whiteKingLocation`: Tuple representing the location of the White King.
- `blackKingLocation`: Tuple representing the location of the Black King.
- `checkMate`: Boolean indicating if the game is in a checkmate condition.
- `staleMate`: Boolean indicating if the game is in a stalemate condition.
- `enpassantPossible`: Tuple representing the square where en passant is possible.
- `currentCastlingRights`: Instance of the `CastleRights` class representing current castling rights.
- `castleRightsLog`: List to keep track of castling rights during the game.

### Methods

#### `__init__(self)`

Initialize a new chess game state with default values.

#### `make_move(self, move)`

Make a move on the chessboard and update the game state accordingly.

#### `undo_move(self)`

Undo the last move made in the game.

#### `update_castling_rights(self, move)`

Update the castling rights after a move is made.

#### `get_valid_moves(self)`

Get a list of valid moves for the current player.

#### `in_check(self)`

Check if the current player's King is in check.

#### `square_under_attack(self, r, c)`

Check if a square on the chessboard is under attack by the opponent.

#### `get_all_possible_moves(self)`

Get all possible moves for the current player, including legal and illegal moves.

#### `get_pawn_moves(self, r, c, moves)`

Get possible moves for a pawn at a given square.

#### `get_rook_moves(self, r, c, moves)`

Get possible moves for a rook at a given square.

#### `get_knight_moves(self, r, c, moves)`

Get possible moves for a knight at a given square.

#### `get_bishop_moves(self, r, c, moves)`

Get possible moves for a bishop at a given square.

#### `get_queen_moves(self, r, c, moves)`

Get possible moves for a queen at a given square.

#### `get_king_moves(self, r, c, moves)`

Get possible moves for a king at a given square.

#### `get_castle_moves(self, r, c, moves)`

Get possible castle moves for a king at a given square.

#### `get_kingside_castle_moves(self, r, c, moves)`

Get possible kingside castle moves for a king at a given square.

#### `get_queen_side_castle_moves(self, r, c, moves)`

Get possible queenside castle moves for a king at a given square.

## `CastleRights` Class

### Description

The `CastleRights` class keeps track of the castling rights for each player.

### Attributes

- `wks`: Boolean flag indicating if White can castle kingside.
- `wqs`: Boolean flag indicating if White can castle queenside.
- `bks`: Boolean flag indicating if Black can castle kingside.
- `bqs`: Boolean flag indicating if Black can castle queenside.

## `Move` Class

### Description

The `Move` class represents a chess move.

### Attributes

- `startRow`: Starting row of the move.
- `startCol`: Starting column of the move.
- `endRow`: Ending row of the move.
- `endCol`: Ending column of the move.
- `pieceMoved`: Piece that was moved.
- `pieceCaptured`: Piece that was captured during the move.
- `isPawnPromotion`: Boolean indicating if the move involves a pawn promotion.
- `isEnpassantMove`: Boolean indicating if the move is an en passant capture.
- `isCastleMove`: Boolean indicating if the move is a castling move.
- `moveID`: Unique identifier for the move.

### Methods

#### `__eq__(self, other)`

Compare two Move objects for equality based on their move IDs.

#### `get_chess_notation(self)`

Get the standard algebraic notation (SAN) for the move.

#### `getRankFile(self, r, c)`

Convert row and column indices to chess notation.


## Credits

- Chess pieces: https://commons.wikimedia.org/wiki/Category:SVG_chess_pieces
