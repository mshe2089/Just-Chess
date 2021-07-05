import copy
from tkinter import *
from tkinter import ttk
from Pieces.Rook import rook_moves
from Pieces.Bishop import bishop_moves
from Pieces.Pawn import pawn_moves
from Pieces.Knight import knight_moves
from Pieces.King import king_moves
from Pieces.Queen import queen_moves

#Game supervisor, Move validator
key = { "p":pawn_moves,
        "P":pawn_moves,
        "b":bishop_moves,
        "B":bishop_moves,
        "n":knight_moves,
        "N":knight_moves,
        "r":rook_moves,
        "R":rook_moves,
        "q":queen_moves,
        "Q":queen_moves,
        "k":king_moves,
        "K":king_moves,
}
alphanumerics =    {0:"a",
          1:"b",
          2:"c",
          3:"d",
          4:"e",
          5:"f",
          6:"g",
          7:"h",
}
class game:

    #castling
    #enpassant
    #pawn promotion
    #50 move

    def __init__(self, turn) -> None:
        self.reset()

    def reset(self):
        self.to_promote = None#location of piece to promote
        self.check = False#unused
        self.log = []#unused
        self.w_captures = []
        self.b_captures = []
        self.turn = 0
        self.HMC = 0 #half move counter unused
        self.FMC = 0 #full move counter unused
        self.EPC = None #en passant target
        self.castles = ['K','Q','k','q']
        self.positions = [["r","n","b","q","k","b","n","r"],["p","p","p","p","p","p","p","p"],["-","-","-","-","-","-","-","-"],["-","-","-","-","-","-","-","-"],["-","-","-","-","-","-","-","-"],["-","-","-","-","-","-","-","-"],["P","P","P","P","P","P","P","P"],["R","N","B","Q","K","B","N","R"]]
        #self.oldpositions - a stack we could use to push old positions to
        #self.positions = [["r","n","b","q","k","b","-","-"],["p","p","p","p","p","p","P","-"],["-","-","-","-","-","-","-","P"],["-","-","-","-","-","-","-","-"],["-","-","-","-","-","-","-","-"],["-","-","-","-","-","-","-","-"],["p","p","p","P","P","P","P","P"],["R","-","-","-","K","-","-","R"]]

    def undo(self):
        pass

    def export(self):
        exportmsg = ""
        empty = 0
        for i in self.positions:
            for j in i:
                if j != "-":
                    if empty != 0:
                        exportmsg = (exportmsg + str(empty))
                    exportmsg = (exportmsg + j)
                    empty = 0
                else:
                    empty += 1
            if empty != 0:
                exportmsg = (exportmsg + str(empty))
            empty = 0
            exportmsg = (exportmsg + "/")
        if empty != 0:
            exportmsg = (exportmsg + str(empty))
        empty = 0
        
        exportmsg = (exportmsg + " ")
        if self.turn == 1:
            exportmsg = (exportmsg + "b")
        else:
            exportmsg = (exportmsg + "w")
        exportmsg = (exportmsg + " ")

        exportmsg = (exportmsg + "".join(self.castles))
        exportmsg = (exportmsg + " ")

        if self.EPC != None:
            exportmsg = (exportmsg + alphanumerics[self.EPC[0]])
            exportmsg = (exportmsg + 8-self.EPC[1])
        else:
            exportmsg = (exportmsg + "-")
        exportmsg = (exportmsg + " ")
        exportmsg = (exportmsg + str(self.HMC))
        exportmsg = (exportmsg + " ")
        exportmsg = (exportmsg + str(self.FMC))
        return exportmsg


    def get_w_captures(self):
        return self.w_captures

    def get_b_captures(self):
        return self.b_captures    

    def get_turn(self):
        return self.turn

    def get_board(self):
        return self.positions

    def in_check(self, board, team):#Checks if (team) is being checked
        if team == 1:
            king = "k"
        else:
            king = "K"
        for i in range(8):
            for j in range(8):
                if board[i][j] == king:
                    if self.under_attack(board, team, j, i):
                        return True
                    return False

    def kingside_castles(self, king, team):
        if team == 0:
            side = "K"
        else:
            side = "k"
        if (side in self.castles):
            for i in range(8):
                for j in range(8):
                    if self.positions[i][j] == king:
                        if self.positions[i][j+1] == "-" and self.positions[i][j+2] == "-" and not self.under_attack(self.positions, team, j, i) and not self.under_attack(self.positions, team, j+1, i) and not self.under_attack(self.positions, team, j+2, i):
                            return [j+2,i]
                        return None

    def queenside_castles(self, king, team):
        if team == 0:
            side = "Q"
        else:
            side = "q"
        if (side in self.castles):
            for i in range(8):
                for j in range(8):
                    if self.positions[i][j] == king:
                        if self.positions[i][j-1] == "-" and self.positions[i][j-2] == "-" and self.positions[i][j-3] == "-" and not self.under_attack(self.positions, team, j, i) and not self.under_attack(self.positions, team, j-1, i) and not self.under_attack(self.positions, team, j-2, i) and not self.under_attack(self.positions, team, j-3, i):
                            return [j-2,i]
                        return None
        
    def castle(self, startx, starty, endx, endy):#performs castle move
        king = self.positions[starty][startx]
        if endx > startx:
            rook = self.positions[endy][endx+1]
            self.positions[starty][startx] = "-"
            self.positions[endy][endx+1] = "-"
            self.positions[endy][endx-1] = rook
        else:
            rook = self.positions[endy][endx-2]
            self.positions[starty][startx] = "-"
            self.positions[endy][endx-2] = "-"
            self.positions[endy][endx+1] = rook
        self.positions[endy][endx] = king

    def disallow_castle(self, piece, x):#removes castling availability based on piece moved and piece position
        if piece == "K":
            if "K" in self.castles:
                self.castles.remove("K") 
            if "Q" in self.castles:
                self.castles.remove("Q")
        elif piece == "k":
            if "k" in self.castles:
                self.castles.remove("k") 
            if "q" in self.castles:
                self.castles.remove("q")
        elif piece == "R":
            if "K" in self.castles and x == 7:
                self.castles.remove("K")
            elif "Q" in self.castles and x == 0:
                self.castles.remove("Q")
        elif piece == "r":
            if "k" in self.castles and x == 7:
                self.castles.remove("k")
            elif "q" in self.castles and x == 0:
                self.castles.remove("q")

    def enpassant(self, startx, starty, endx, endy):#performs castle move
        pawn = self.positions[starty][startx]
        if pawn == "P":
            self.positions[starty][startx] = "-"
            self.positions[endy][endx] = pawn
            self.positions[endy+1][endx] = "-"
            self.w_captures.append("p")
            enemy_pawn = "p"
        else:
            self.positions[starty][startx] = "-"
            self.positions[endy][endx] = pawn
            self.positions[endy-1][endx] = "-"
            self.b_captures.append("P")
            enemy_pawn = "P"
        self.EPC = None
        return enemy_pawn

    def checkmated(self, team):#check if (team) has checkmated opponent
        for i in range(8):
            for j in range(8):
                if self.positions[i][j] != "-":
                    if (self.positions[i][j].islower() and team == 0) or (self.positions[i][j].isupper() and team == 1):
                        if self.get_moves(j, i) != []:
                            return False
        return True

    def get_moves(self, x, y): #get all valid moves of piece at x, y
        team = 1
        king = "k"
        if self.positions[y][x].isupper():
            team = 0
            king = "K"
        moveset = key[self.positions[y][x]](self.positions, team, x, y, self.EPC, self.castles)

        ### add castle moves
        if self.positions[y][x] == "K" or self.positions[y][x] == "k":
            kingside_castle = self.kingside_castles(king, team)
            queenside_castle = self.queenside_castles(king, team)
            if kingside_castle != None:
                moveset.append(kingside_castle)
            if queenside_castle != None:
                moveset.append(queenside_castle)

        ### remove all moves that would lead to check
        i = 0
        while i < (len(moveset)):
            testmove = copy.deepcopy(self.positions)
            testmove[y][x] = "-"
            testmove[moveset[i][1]][moveset[i][0]] = self.positions[y][x]
            if self.in_check(testmove, team):
                moveset.pop(i)
                i-=1
            i+=1

        return moveset
        

    def move(self, startx, starty, endx, endy): #moves piece in position matrix and inverts turn
        self.oldpositions = copy.deepcopy(self.positions)
        piece = self.positions[starty][startx]
        #Move validation
        capture = None
        moveset = self.get_moves(startx, starty)
        for i in moveset:
            if i[0] == endx and i[1] == endy:#if is valid move
                
                
                #if castle move
                if piece.upper() == "K" and abs(endx - startx) >= 2:
                    self.castle(startx, starty, endx, endy)

                #if enpassant
                elif piece.upper() == "P" and startx != endx and [endx, endy] == self.EPC:
                    capture = self.enpassant(startx, starty, endx, endy)

                #if normal move 
                else:
                    capturer = self.rm_piece(startx, starty)
                    captured = self.rm_piece(endx, endy)
                    if captured != "-":
                        if capturer.isupper():
                            self.w_captures.append(captured)
                        else:
                            self.b_captures.append(captured)
                        capture = captured
                    self.add_piece(piece, endx, endy)

                ###label EPC tile
                if piece.upper() == "P" and abs(endy - starty) >= 2:
                    if piece == "P":
                        self.EPC = [endx, endy+1]
                    else:
                        self.EPC = [endx, endy-1]
                else:
                    self.EPC = None

                ###Check if pawn was moved into promotion zone
                if piece.upper() == "P" and (endy == 0 or endy == 7):
                    self.promotion(endx, endy)

                ###increment full move counter
                if self.turn == 1:
                    self.FMC += 1
                
                ###increment full move counter
                if piece.upper() == "P" or capture:
                    self.HMC == 0
                else:
                    self.HMC += 0

                self.disallow_castle(piece, startx)
                self.turn = 1 - self.turn
                return capture
        return capture

    def add_piece(self, piece, x, y): #adds a piece to x, y
        self.positions[y][x] = piece

    def rm_piece(self, x, y): #remove a piece from x, y and returns it
        piece = self.positions[y][x]
        self.positions[y][x] = "-"
        return piece

    def piece_selectable(self, x, y):#check whether a turn valid piece was selected
        if self.to_promote != None:
            return False
        if self.positions[y][x] != "-" and ((self.turn == 0 and self.positions[y][x].isupper()) or (self.turn == 1 and self.positions[y][x].islower())):#if piece selected and turn is correct
            return True
        return False

    def promotion(self, x, y):
        self.to_promote = [x,y]

    def promote_queen(self):
        if self.positions[self.to_promote[1]][self.to_promote[0]].isupper():
            self.positions[self.to_promote[1]][self.to_promote[0]] = "Q"
            team = 0
        else:
            self.positions[self.to_promote[1]][self.to_promote[0]] = "q"
            team = 1
        self.to_promote = None
        return team

    def promote_bishop(self):
        if self.positions[self.to_promote[1]][self.to_promote[0]].isupper():
            self.positions[self.to_promote[1]][self.to_promote[0]] = "B"
            team = 0
        else:
            self.positions[self.to_promote[1]][self.to_promote[0]] = "b"
            team = 1
        self.to_promote = None
        return team

    def promote_rook(self):
        if self.positions[self.to_promote[1]][self.to_promote[0]].isupper():
            self.positions[self.to_promote[1]][self.to_promote[0]] = "R"
            team = 0
        else:
            self.positions[self.to_promote[1]][self.to_promote[0]] = "r"
            team = 1
        self.to_promote = None
        return team

    def promote_knight(self):
        if self.positions[self.to_promote[1]][self.to_promote[0]].isupper():
            self.positions[self.to_promote[1]][self.to_promote[0]] = "N"
            team = 0
        else:
            self.positions[self.to_promote[1]][self.to_promote[0]] = "n"
            team = 1
        self.to_promote = None
        return team


    def under_attack(self, board, team, x, y):#check whether a square is under attack by opponent of team

        def in_bounds(x, y):
            if x <= 7 and x >= 0 and y <=7 and y >= 0:
                return True
            return False

        def ishostile(piece):
            if team == 1 and piece.isupper():
                return True
            elif team == 0 and piece.islower():
                return True
            else:
                return False
        
        def isrook(piece):
            if piece == "r" or piece == "R":
                return True
            return False

        def isqueen(piece):
            if piece == "q" or piece == "Q":
                return True
            return False

        def isknight(piece):
            if piece == "n" or piece == "N":
                return True
            return False

        def isbishop(piece):
            if piece == "b" or piece == "B":
                return True
            return False
        
        def isking(piece):
            if piece == "k" or piece == "K":
                return True
            return False

        def ispawn(piece):
            if piece == "p" or piece == "P":
                return True
            return False

        #Vertical, horizontal checks
        for i in range(x-1, -1, -1):
            if board[y][i] != "-":
                if ishostile(board[y][i]) and (isrook(board[y][i]) or isqueen(board[y][i])):
                    return True
                break
        for i in range(x+1, 8, 1):
            if board[y][i] != "-":
                if ishostile(board[y][i]) and (isrook(board[y][i]) or isqueen(board[y][i])):
                    return True
                break
        for i in range(y-1, -1, -1):
            if board[i][x] != "-":
                if ishostile(board[i][x]) and (isrook(board[i][x]) or isqueen(board[i][x])):
                    return True
                break
        for i in range(y+1, 8, 1):
            if board[i][x] != "-":
                if ishostile(board[i][x]) and (isrook(board[i][x]) or isqueen(board[i][x])):
                    return True
                break
        #Diagonal checks
        i = 1
        while x+i <= 7 and y+i <= 7:
            if board[y+i][x+i] != "-":
                if ishostile(board[y+i][x+i]) and (isbishop(board[y+i][x+i]) or isqueen(board[y+i][x+i])):
                    return True
                break
            i += 1
        i = 1
        while x+i <= 7 and y-i >= 0:
            if board[y-i][x+i] != "-":
                if ishostile(board[y-i][x+i]) and (isbishop(board[y-i][x+i]) or isqueen(board[y-i][x+i])):
                    return True
                break
            i += 1
        i = 1
        while x-i >= 0 and y+i <= 7:
            if board[y+i][x-i] != "-":
                if ishostile(board[y+i][x-i]) and (isbishop(board[y+i][x-i]) or isqueen(board[y+i][x-i])):
                    return True
                break
            i += 1
        i = 1
        while x-i >= 0 and y-i >= 0:
            if board[y-i][x-i] != "-":
                if ishostile(board[y-i][x-i]) and (isbishop(board[y-i][x-i]) or isqueen(board[y-i][x-i])):
                    return True
                break
            i += 1
        #Knight checks
        if in_bounds(x+2, y-1) and ishostile(board[y-1][x+2]) and isknight(board[y-1][x+2]):
            return True
        if in_bounds(x+2, y+1) and ishostile(board[y+1][x+2]) and isknight(board[y+1][x+2]):
            return True
        if in_bounds(x+1, y-2) and ishostile(board[y-2][x+1]) and isknight(board[y-2][x+1]):
            return True
        if in_bounds(x+1, y+2) and ishostile(board[y+2][x+1]) and isknight(board[y+2][x+1]):
            return True
        if in_bounds(x-1, y-2) and ishostile(board[y-2][x-1]) and isknight(board[y-2][x-1]):
            return True
        if in_bounds(x-1, y+2) and ishostile(board[y+2][x-1]) and isknight(board[y+2][x-1]):
            return True
        if in_bounds(x-2, y-1) and ishostile(board[y-1][x-2]) and isknight(board[y-1][x-2]):
            return True
        if in_bounds(x-2, y+1) and ishostile(board[y+1][x-2]) and isknight(board[y+1][x-2]):
            return True
        #Pawn checks
        if team == 0:
            if in_bounds(x-1, y-1) and ishostile(board[y-1][x-1]) and ispawn(board[y-1][x-1]):
                return True
            if in_bounds(x+1, y-1) and ishostile(board[y-1][x+1]) and ispawn(board[y-1][x+1]):
                return True
        else:
            if in_bounds(x-1, y+1) and ishostile(board[y+1][x-1]) and ispawn(board[y+1][x-1]):
                return True
            if in_bounds(x+1, y+1) and ishostile(board[y+1][x+1]) and ispawn(board[y+1][x+1]):
                return True
        #King checks
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                if (i == 0 and j == 0):
                    continue
                elif in_bounds(x+i, y+j) and board[y+j][x+i] != "-" and ishostile(board[y+j][x+i]) and isking(board[y+j][x+i]):
                    return True
        return False


