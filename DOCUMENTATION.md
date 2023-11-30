# Good Chess Documentation

## ChessMain.py

### Main Script

The `ChessMain.py` file contains the main script for the chess game. It utilizes the Pygame library for the graphical interface and includes functions for initializing the game, handling player input, and updating the game state.

#### Constants

- `BOARD_WIDTH` and `BOARD_HEIGHT`: Dimensions of the chessboard.
- `MOVE_LOG_PANEL_WIDTH` and `MOVE_LOG_PANEL_HEIGHT`: Dimensions of the move log panel.
- `DIMENSION`: Size of the chessboard.
- `SQ_SIZE`: Size of each square on the chessboard.
- `MAX_FPS`: Maximum frames per second for the game.
- `IMAGES`: Dictionary to store chess piece images.
- `WINDOW_ICON`: Icon for the game window.
- `ANIMATE`: Boolean flag to enable or disable animation.
- `SCROLL_OFFSET`: Offset for scrolling the move log.
- `SCROLL_SPEED`: Speed of the scrolling animation.
- `SCROLL_WAIT_TIME`: Waiting time before resetting the scroll.

#### Global Variables

- `SKIN`, `THEME`, `COLORS`, `MOVES_LOG`: Global variables for the game skin, theme, colors, and move log.

#### Functions

- `choose_skin_theme()`: Display a GUI window for choosing the skin and theme for the chessboard.
- `loadImages()`: Load chess piece images based on the chosen skin.
- `main()`: Run the main chess game loop, handling player input and updating the game state.
- `highlightSquares(screen, gs, validMoves, sqSelected)`: Highlight valid moves on the chessboard.
- `drawGameState(screen, gs, validMoves, sqSelected, moveLogFont)`: Draw the current state of the chessboard.
- `drawBoard(screen)`: Draw the chessboard grid on the screen.
- `drawPieces(screen, board)`: Draw the chess pieces on the chessboard.
- `drawMoveLog(screen, gs, font)`: Draw the move log on the right side of the chessboard.
- `animateMove(move, screen, board, clock)`: Animate a chess move on the chessboard.
- `drawText(screen, text)`: Draw text on the screen.
- `save_moves_to_json(moves_log)`: Save the moves log to a JSON file with timestamps.

### ChessEngine.py

#### Engine Script

The `ChessEngine.py` file contains the engine script for managing the game state, valid moves, and chess piece movements.

#### `GameState` Class

- `__init__(self)`: Initialize a new chess game state.
- `makeMove(self, move)`: Make a move on the chessboard and update the game state.
- `undoMove(self)`: Undo the last move made in the game.
- `getValidMoves(self)`: Get a list of valid moves for the current player.
- `inCheck(self)`: Check if the current player's King is in check.
- `squareUnderAttack(self, r, c)`: Check if a square on the chessboard is under attack by the opponent.
- `getAllPossibleMoves(self)`: Get all possible moves for the current player.
- `getPawnMoves(self, r, c, moves)`: Get possible moves for a pawn at a given square.
- `getRookMoves(self, r, c, moves)`: Get possible moves for a rook at a given square.
- `getKnightMoves(self, r, c, moves)`: Get possible moves for a knight at a given square.
- `getBishopMoves(self, r, c, moves)`: Get possible moves for a bishop at a given square.
- `getQueenMoves(self, r, c, moves)`: Get possible moves for a queen at a given square.
- `getKingMoves(self, r, c, moves)`: Get possible moves for a king at a given square.

#### `Move` Class

- `__init__(self, startSq, endSq, board)`: Create a Move object representing a chess move.
- `__eq__(self, other)`: Compare two Move objects for equality.
- `getChessNotation(self)`: Get the standard algebraic notation (SAN) for the move.
- `getRankFile(self, r, c)`: Convert row and column indices to chess notation.

---

## How to Run

1. Ensure Python is installed on your system.
2. Install the required libraries: `pygame` and `tkinter`.
3. Run the `ChessMain.py` script to start the chess game.

---

## Additional Notes

- The game allows players to choose the skin and theme for the chessboard.
- Moves are displayed in the move log on the right side of the chessboard.
- The game supports undoing moves, and the moves log is saved to a JSON file with timestamps after the game ends.

