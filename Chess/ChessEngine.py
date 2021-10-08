"""
Engine Script
"""


# notata ca "gs" in main (statusul jocului in fiecare moment)
class GameState():
    def __init__(self):
        """
        tabla: 8x8, lista 2d;
        primul caracter din fiecare string reprezinta culoarea (w -> white, b -> black);
        al doilea caracter din fiecare string reprezinta numele piesei de sah:
            ( K -> king, Q -> queen, R -> rook, P -> pawn, B -> bishop, N -> knight)
        """
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]

        self.whiteToMove = True
        self.moveLog = []

    # preia mutarea si o executa
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove  # pastreaza randul jucatorilor

    # rectifica mutarea
    def undoMove(self):
        # verifica daca exista o mutare
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            # paseaza tura celuilalt jucator
            self.whiteToMove = not self.whiteToMove

    # miscari valide CU mat-uri
    def getValidMoves(self):
        return self.getAllPossibleMoves()  # ! NU LUAM IN CALCUL MAT-URILE MOMENTAN

    # miscari valide FARA mat-uri
    def getAllPossibleMoves(self):
        moves = [Move((6, 4), (4, 4), self.board)] # (6, 4)(4, 4) EXEMPLU DE MUTARE LEGALA
        for r in range(len(self.board)):  # numarul de randuri
            for c in range(len(self.board[r])):  # numarul de coloane
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) and (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    # PION
                    if piece == 'p':
                        self.getPawnMove(r, c, moves)
                    elif piece == 'R':
                        self.getRookMoves(r, c, moves)
        return moves

    # mutarile pionilor (PAWN)
    def getPawnMoves(self, r, c, moves):
        pass

    # mutarile turelor (ROOK)
    def getRookMoves(self, r, c, moves):
        pass


class Move():
    # Sursa: https://www.dummies.com/games/chess/naming-ranks-and-files-in-chess/
    # Tabla: https://www.dummies.com/wp-content/uploads/281905.image0.jpg
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    # reverse key in value
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    # reverse key in value
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        """
            'moveID' = orice mutare va avea un ID anume cum ar fi "6444";
            (6*1000 + 4*100 + 4*10 + 4 = 6000 + 400 + 40 + 4 = 6444);
            Pentru simplificarea notatiilor in baza tablei de joc non-legala (doar pentru robot);
            Interfata legala este cea cu Ranks and Files pentru care exista dictionar.
        """
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
        print(f"Mutare ID: {self.moveID}")

    # skip rule
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChassNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
