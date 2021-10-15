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
        # dictionar pentru metode simplificate (mai simplu)
        self.moveFunctions = {'P': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves,
                              'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}

        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (7, 4)  # locatia de start "wK"
        self.blackKingLocation = (0, 4)  # locatia de start "bK"
        self.checkMate = False
        self.staleMate = False

    # preia mutarea si o executa
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove  # pastreaza randul jucatorilor
        # update king's pos
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow, move.endCol)
        if move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow, move.endCol)

    # rectifica mutarea
    def undoMove(self):
        # verifica daca exista o mutare
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            # paseaza tura celuilalt jucator
            self.whiteToMove = not self.whiteToMove
            # update king's pos
            if move.pieceMoved == 'wK':
                self.whiteKingLocation = (move.startRow, move.startCol)
            if move.pieceMoved == 'bK':
                self.blackKingLocation = (move.startRow, move.startCol)

    # miscari valide CU mat-uri
    def getValidMoves(self):
        # 1) generam toate mutarile posibile
        moves = self.getAllPossibleMoves()
        # 2) pentru fiecare mutare, face mutarea
        for i in range(len(moves) - 1, -1, -1):  # parcurgem invers
            self.makeMove(moves[i])
            # 3) generarea mutarilor oponentului
            # 4) pentru fiecare mutare a oponentului, verifica daca iti poat ataca regele
            self.whiteToMove = not self.whiteToMove  # schimbam jucatorii deoarece functia makeMove() a schimbat deja jucatorii
            if self.inCheck():
                moves.remove(moves[i])  # 5) daca ataca regele nu este o mutare valida
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

    # verifica daca jucatorul este in check
    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])

    # verifica daca inamicul poate ataca patratul (r, c)
    def squareUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove  # schimba jucatorii pentru a afla mutarile
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove  # schimba inapoi jucatorii
        for move in oppMoves:
            if move.endRow == r and move.endCol == c:  # patratul este atacat
                return True
        return False

    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):  # numarul de randuri
            for c in range(len(self.board[r])):  # numarul de coloane
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    # metoda simplificate pe dictionar
                    self.moveFunctions[piece](r, c, moves)
        return moves

    # mutarile pionilor (PAWN)
    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove:
            if self.board[r - 1][c] == "--":  # mutare 1 in fata
                moves.append(Move((r, c), (r - 1, c), self.board))
                if r == 6 and self.board[r - 2][c] == "--":  # mutare 2 in fata
                    moves.append(Move((r, c), (r - 2, c), self.board))
            if c - 1 >= 0:  # eliminare stanga
                if self.board[r - 1][c - 1][0] == 'b':
                    moves.append(Move((r, c), (r - 1, c - 1), self.board))
            if c + 1 <= 7:  # eliminare la dreapta
                if self.board[r - 1][c + 1][0] == 'b':
                    moves.append(Move((r, c), (r - 1, c + 1), self.board))
        else:
            if self.board[r + 1][c] == "--":  # mutare 1 in fata
                moves.append(Move((r, c), (r + 1, c), self.board))
                if r == 1 and self.board[r + 2][c] == "--":  # mutare 2 in fata
                    moves.append(Move((r, c), (r + 2, c), self.board))
            if c - 1 >= 0:  # eliminare stanga
                if self.board[r + 1][c - 1][0] == 'w':
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))
            if c + 1 <= 7:  # eliminare la dreapta
                if self.board[r + 1][c + 1][0] == 'w':
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))

    # mutarile turelor (ROOK)
    def getRookMoves(self, r, c, moves):
        directie = ((-1, 0), (0, -1), (1, 0), (0, 1))
        culoareInamic = 'b' if self.whiteToMove else 'w'
        for d in directie:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                # verfica daca este pe tabla
                if (0 <= endRow < 8) and (0 <= endCol < 8):
                    endPiece = self.board[endRow][endCol]
                    if endPiece == '--':
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == culoareInamic:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:  # piesa din echipa
                        break
                else:  # nu e pe tabla
                    break

    # mutarile cailor (KNIGHT)
    def getKnightMoves(self, r, c, moves):
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        allyColor = 'w' if self.whiteToMove else 'b'
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:  # nu este piesa din echipa
                    moves.append(Move((r, c), (endRow, endCol), self.board))

    # mutarile nebunilor (BISHOP)
    def getBishopMoves(self, r, c, moves):
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
                    else:  # piesa din echipa
                        break
                else:  # nu e pe tabla
                    break

    # mutarile reginelor (QUEEN)
    def getQueenMoves(self, r, c, moves):
        # mutarile reginei sunt mutarile turelor (ROOK) si mutarile nebunilor (BISHOP)
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)

    # mutarile regilor (KING)
    def getKingMoves(self, r, c, moves):
        kingMoves = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        allyColor = 'w' if self.whiteToMove else 'b'
        for i in range(8):
            endRow = r + kingMoves[i][0]
            endCol = c + kingMoves[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:  # nu este piesa din echipa
                    moves.append(Move((r, c), (endRow, endCol), self.board))


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

    # skip rule
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChassNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
