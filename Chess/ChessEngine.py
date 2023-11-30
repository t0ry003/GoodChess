"""
Engine Script
"""


class GameState:
    """
            Initialize a new chess game state.

            Attributes:
            - board: The chessboard represented as a 2D list.
            - moveFunctions: Dictionary mapping piece types to their respective move functions.
            - whiteToMove: Boolean flag indicating if it's White's turn.
            - moveLog: A list to keep track of the moves made in the game.
            - whiteKingLocation: Tuple representing the current location of the White King.
            - blackKingLocation: Tuple representing the current location of the Black King.
            - checkMate: Boolean flag indicating if the game is in a checkmate condition.
            - staleMate: Boolean flag indicating if the game is in a stalemate condition.
    """

    def __init__(self):

        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        self.moveFunctions = {'P': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves,
                              'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}

        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.checkMate = False
        self.staleMate = False

    def makeMove(self, move):
        """
                Make a move on the chessboard and update the game state accordingly.

                Args:
                - move: An instance of the Move class representing the move to be made.

                This method updates the board, move log, and other game state attributes.
        """

        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow, move.endCol)
        if move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow, move.endCol)

    def undoMove(self):
        """
        Undo the last move made in the game.

        This method reverts the game state to the previous state by removing the last move made.
        """

        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove
            if move.pieceMoved == 'wK':
                self.whiteKingLocation = (move.startRow, move.startCol)
            if move.pieceMoved == 'bK':
                self.blackKingLocation = (move.startRow, move.startCol)

    def getValidMoves(self):
        """
        Get a list of valid moves for the current player.

        Returns:
        A list of valid Move objects that can be made by the current player.

        This method calculates all possible moves and filters out those that would leave the player's own King in check.
        If there are no valid moves, it also checks for checkmate and stalemate conditions.
        """

        moves = self.getAllPossibleMoves()
        for i in range(len(moves) - 1, -1, -1):
            self.makeMove(moves[i])
            self.whiteToMove = not self.whiteToMove
            if self.inCheck():
                moves.remove(moves[i])
            self.whiteToMove = not self.whiteToMove
            self.undoMove()
        if len(moves) == 0:
            if self.inCheck():
                self.checkMate = True
            else:
                self.staleMate = True
        else:
            self.checkMate = False
            self.staleMate = False
        return moves

    def inCheck(self):
        """
        Check if the current player's King is in check.

        Returns:
        True if the current player's King is in check, False otherwise.
        """

        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])

    def squareUnderAttack(self, r, c):
        """
        Check if a square on the chessboard is under attack by the opponent.

        Args:
        - r: The row of the square to check.
        - c: The column of the square to check.

        Returns:
        True if the square is under attack, False otherwise.

        This method temporarily simulates the opponent's moves to check if they can attack the specified square.
        """

        self.whiteToMove = not self.whiteToMove
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove
        for move in oppMoves:
            if move.endRow == r and move.endCol == c:
                return True
        return False

    def getAllPossibleMoves(self):
        """
        Get all possible moves for the current player.

        Returns:
        A list of all possible Move objects that can be made by the current player, including legal and illegal moves.

        This method generates all possible moves for the current player's pieces, regardless of whether they are legal.
        """

        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves)
        return moves

    def getPawnMoves(self, r, c, moves):
        """
        Get possible moves for a pawn at a given square.

        Args:
        - r: The row of the pawn.
        - c: The column of the pawn.
        - moves: A list to append the generated moves to.

        This method generates all possible moves for a pawn at the specified square.
        """

        if self.whiteToMove:
            if self.board[r - 1][c] == "--":
                moves.append(Move((r, c), (r - 1, c), self.board))
                if r == 6 and self.board[r - 2][c] == "--":
                    moves.append(Move((r, c), (r - 2, c), self.board))
            if c - 1 >= 0:
                if self.board[r - 1][c - 1][0] == 'b':
                    moves.append(Move((r, c), (r - 1, c - 1), self.board))
            if c + 1 <= 7:
                if self.board[r - 1][c + 1][0] == 'b':
                    moves.append(Move((r, c), (r - 1, c + 1), self.board))
        else:
            if self.board[r + 1][c] == "--" and self.board[r + 1][c] != None:
                moves.append(Move((r, c), (r + 1, c), self.board))
                if r == 1 and self.board[r + 2][c] == "--":
                    moves.append(Move((r, c), (r + 2, c), self.board))
            if c - 1 >= 0:
                if self.board[r + 1][c - 1][0] == 'w':
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))
            if c + 1 <= 7:
                if self.board[r + 1][c + 1][0] == 'w':
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))

    def getRookMoves(self, r, c, moves):
        """
        Get possible moves for a rook at a given square.

        Args:
        - r: The row of the rook.
        - c: The column of the rook.
        - moves: A list to append the generated moves to.

        This method generates all possible moves for a rook at the specified square.
        """

        directie = ((-1, 0), (0, -1), (1, 0), (0, 1))
        culoareInamic = 'b' if self.whiteToMove else 'w'
        for d in directie:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if (0 <= endRow < 8) and (0 <= endCol < 8):
                    endPiece = self.board[endRow][endCol]
                    if endPiece == '--':
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == culoareInamic:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break

    def getKnightMoves(self, r, c, moves):
        """
        Get possible moves for a knight at a given square.

        Args:
        - r: The row of the knight.
        - c: The column of the knight.
        - moves: A list to append the generated moves to.

        This method generates all possible moves for a knight at the specified square.
        """

        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        allyColor = 'w' if self.whiteToMove else 'b'
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((r, c), (endRow, endCol), self.board))

    def getBishopMoves(self, r, c, moves):
        """
        Get possible moves for a bishop at a given square.

        Args:
        - r: The row of the bishop.
        - c: The column of the bishop.
        - moves: A list to append the generated moves to.

        This method generates all possible moves for a bishop at the specified square.
        """

        directie = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        culoareInamic = 'b' if self.whiteToMove else 'w'
        for d in directie:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == '--':
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == culoareInamic:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break

    def getQueenMoves(self, r, c, moves):
        """
        Get possible moves for a queen at a given square.

        Args:
        - r: The row of the queen.
        - c: The column of the queen.
        - moves: A list to append the generated moves to.

        This method generates all possible moves for a queen at the specified square.
        """

        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)

    def getKingMoves(self, r, c, moves):
        """
        Get possible moves for a king at a given square.

        Args:
        - r: The row of the king.
        - c: The column of the king.
        - moves: A list to append the generated moves to.

        This method generates all possible moves for a king at the specified square.
        """

        kingMoves = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        allyColor = 'w' if self.whiteToMove else 'b'
        for i in range(8):
            endRow = r + kingMoves[i][0]
            endCol = c + kingMoves[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((r, c), (endRow, endCol), self.board))


class Move():
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = dict(a=0, b=1, c=2, d=3, e=4, f=5, g=6, h=7)
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        """
        Create a Move object representing a chess move.

        Args:
        - startSq: Tuple representing the starting square of the move.
        - endSq: Tuple representing the ending square of the move.
        - board: The current chessboard state.

        This constructor initializes a Move object with the provided information.
        """

        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    def __eq__(self, other):
        """
        Compare two Move objects for equality.

        Args:
        - other: Another Move object to compare with.

        Returns:
        True if the moves are equal, False otherwise.

        This method compares two Move objects based on their move IDs.
        """

        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        """
        Get the standard algebraic notation (SAN) for the move.

        Returns:
        A string representing the SAN notation of the move.

        This method returns the SAN notation for the move, e.g., "Nf3" for a knight move to f3.
        """

        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        """
        Convert row and column indices to chess notation.

        Args:
        - r: The row index.
        - c: The column index.

        Returns:
        A string in the format 'file' + 'rank', representing the chess square notation (e.g., 'a1' for (0, 0)).

        This function takes a row and column index and converts them into a chess square notation, where 'file' represents
        the column and 'rank' represents the row in algebraic notation (e.g., 'a1', 'h8', etc.).
        """

        return self.colsToFiles[c] + self.rowsToRanks[r]
