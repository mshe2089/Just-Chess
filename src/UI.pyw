from tkinter import *
from tkinter import ttk
from Game import game
from tkinter.filedialog import asksaveasfile
import os
import sys

#Pyinstaller resource code stolen from stackoverflow
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

#Chess renderer
#================================================================================

#Opening and formatting window

#NEXT: expand moveset ,full move log, numpy, pytorch, ab tree ai


#TO add bot: 1. add to menu in UI 2.add bot init to game 3. implement bot decide function same as randombot

window = Tk(screenName=None,  baseName=None,  className="new_window",  useTk=1) #where m is the name of the main window object
window.title("Literally just chess")
window.resizable(0, 0)
window.rowconfigure(0, weight=1)
window.columnconfigure(0, weight=1)

board_frame = Frame(master = window, bg ="saddlebrown")
board_frame.grid(column=0, row=0)
board_frame.rowconfigure(0, weight=1)
board_frame.columnconfigure(0, weight=1)

label_frame = Frame(master = window, bg ="saddlebrown")
label_frame.grid(column=0, row=1, sticky = 'ew')

statusmsg_frame = Frame(master = label_frame, bg ="saddlebrown")
statusmsg_frame.grid(column=0, row=0, sticky = 'ew')
botWhite_frame = Frame(master = label_frame, bg ="saddlebrown")
botWhite_frame.grid(column=1, row=0, sticky = 'ew')
botBlack_frame = Frame(master = label_frame, bg ="saddlebrown")
botBlack_frame.grid(column=2, row=0, sticky = 'ew')

buttons_frame = Frame(master = window, bg ="saddlebrown")
buttons_frame.grid(column=0, row=2, sticky='ew')#rm sticky for still buttons

#Starting game
game = game(0)


#================================================================================

#Variables
selected_piece = None
promoting = False
selected_x = -1
selected_y = -1
targets = []
delay = 1
ggdelay = 10000

#================================================================================

key =    {"K":"wKing",
          "k":"bKing",
          "Q":"wQueen",
          "q":"bQueen",
          "P":"wPawn",
          "p":"bPawn",
          "N":"wKnight",
          "n":"bKnight",
          "B":"wBishop",
          "b":"bBishop",
          "R":"wRook",
          "r":"bRook",
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

#================================================================================

#DRAW COMMANDS
def draw_piece(piece, x, y):
    canvas.create_image(x*75, y*75, anchor=NW, image=assets[piece], tags="pieces")

def draw_bkg():
    canvas.create_image(0, 0, anchor=NW, image=assets["Board"])

def clear_board():
    canvas.delete("pieces")

def draw_board():
    clear_board()
    positions = game.get_board()
    for i in range(8):
        for j in range(8):
            if positions[i][j] != '-':
                draw_piece(key[positions[i][j]],j,i)

def draw_tips():
    for i in targets:
        canvas.create_image(i[0]*75, i[1]*75, anchor=NW, image=assets["Tip1"], tags="tips")

def draw_tip_selected(x, y):
    clear_tips()
    canvas.create_image(x*75, y*75, anchor=NW, image=assets["Tip2"], tags="tips")
    canvas.tag_raise("pieces")
    draw_tips()

def draw_selector(team):
    canvas.create_image(150, 225, anchor=NW, image=assets["Tip3"], tags="select")
    if team == 0:
        canvas.create_image(150, 225, anchor=NW, image=assets["wKnight"], tags="select")
        canvas.create_image(225, 225, anchor=NW, image=assets["wBishop"], tags="select")
        canvas.create_image(300, 225, anchor=NW, image=assets["wRook"], tags="select")
        canvas.create_image(375, 225, anchor=NW, image=assets["wQueen"], tags="select")
    else:
        canvas.create_image(150, 225, anchor=NW, image=assets["bKnight"], tags="select")
        canvas.create_image(225, 225, anchor=NW, image=assets["bBishop"], tags="select")
        canvas.create_image(300, 225, anchor=NW, image=assets["bRook"], tags="select")
        canvas.create_image(375, 225, anchor=NW, image=assets["bQueen"], tags="select")

def clear_selector():
    canvas.delete("select")

def clear_tips():
    canvas.delete("tips")

def undo():
    pass    #TODO

def reset():
    end_promotion()
    statusmsg.set("White's turn")
    selected_x = -1
    selected_y = -1
    targets = []
    clear_tips()
    clear_selector()
    botWhiteVar.set("Human")
    botBlackVar.set("Human")
    game.reset()
    draw_board()

def resetKeepBot():
    game.reset()
    end_promotion()
    statusmsg.set("White's turn")
    selected_x = -1
    selected_y = -1
    targets = []
    clear_tips()
    clear_selector()
    draw_board()
    newbotBlack(botBlackVar.get())
    newbotWhite(botWhiteVar.get())

def select(x, y):
    global selected_x
    global selected_y
    global targets
    global selected_piece
    selected_x = x#select new
    selected_y = y
    selected_piece = key[game.get_board()[y][x]]
    targets = game.get_moves(selected_x, selected_y)
    draw_tip_selected(selected_x, selected_y)#draw tips

def unselect():
    global selected_x
    global selected_y
    global targets
    global selected_piece
    selected_x = -1#unselect
    selected_y = -1
    selected_piece = None
    targets = []
    clear_tips()#undraw tips

def is_move(x, y):
    for i in targets:
        if i[0] == x and i[1] == y:
            return True
    return False

def start_promotion(team):
    global promoting
    promoting = True
    game.turn = 1-game.turn
    draw_selector(team)
    if (team == 0 and game.whiteBot != None) or (team == 1 and game.blackBot != None):
        game.ponderPromotion(team)
        doBotPromote(team)

def end_promotion():
    global promoting
    promoting = False
    game.turn = 1-game.turn
    clear_selector()

def export():
    files = [('Text Document', '*.txt')]
    file = asksaveasfile(filetypes = files, defaultextension = files)
    file.write(game.export())#Write contents
    file.close

def newbotBlack(bot):
    game.newbotBlack(bot)
    if game.turn == 1 and game.blackBot != None and game.checkmated(0) == 0:
        game.ponder(1)
        doBotMove(1)

def newbotWhite(bot):
    game.newbotWhite(bot)
    if game.turn == 0 and game.whiteBot != None and game.checkmated(1) == 0:
        game.ponder(0)
        doBotMove(0)

def doBotMove(team):
    if team == 1:
        window.after(delay, choose, game.blackBotMove[0], game.blackBotMove[1], True)
        window.after(2*delay, choose, game.blackBotMove[2], game.blackBotMove[3], True)

    elif team == 0:
        window.after(delay, choose, game.whiteBotMove[0], game.whiteBotMove[1], True)
        window.after(2*delay, choose, game.whiteBotMove[2], game.whiteBotMove[3], True)

def doBotPromote(team):
    if team == 1:
        window.after(delay, choose, game.blackBotMove[0], game.blackBotMove[1], True)

    elif team == 0:
        window.after(delay, choose, game.whiteBotMove[0], game.whiteBotMove[1], True)


def choose(grid_x, grid_y, isbot):
    new_status = ""
    print("\nGrid " + str(grid_x) + ", " + str(grid_y), end = "")
    #print(game.castles)

    if game.under_attack(game.get_board(), game.get_turn(), grid_x, grid_y):
        print(" ,under attack from ", end = "")
    else:
        print(" ,not under attack from ", end = "")
    if game.get_turn() == 0:
        print("black")
    else:
        print("white")

    if game.piece_selectable(grid_x, grid_y, isbot):#if piece selected and turn is correct
        if selected_x != grid_x or selected_y != grid_y:#if new piece selected
            select(grid_x, grid_y)

            new_status=("Selected " + str(selected_piece) + " on " + str(alphanumerics[selected_x]) + str(8-selected_y))

            print("Selected " + key[game.get_board()[grid_y][grid_x]], end = "")
            print(", valid moves: ", end = "")
            print(targets)
        else:#if same piece selected

            new_status=("Unselected " + str(selected_piece) + " on " + str(alphanumerics[selected_x]) + str(8-selected_y))

            unselect()
            print("Unselected " + key[game.get_board()[grid_y][grid_x]])

    elif is_move(grid_x, grid_y):#move made
        capture = game.move(selected_x, selected_y, grid_x, grid_y)

        # msg = ("Moved " + str(selected_piece) + " from " + str(alphanumerics[selected_x]) + str(8-selected_y) + " to " + str(alphanumerics[grid_x]) + str(8-grid_y))
        msg = (str(alphanumerics[selected_x]) + str(8-selected_y) + " to " + str(alphanumerics[grid_x]) + str(8-grid_y))

        if game.get_board()[grid_y][grid_x].upper() == "K" and abs(grid_x-selected_x) >= 2:
            if (grid_x-selected_x) >= 2:
                msg = (msg + ", castling kingside")
            else:
                msg = (msg + ", castling queenside")

        if capture != None:
            msg = (msg + ", capturing " + key[capture])
        new_status=msg

        unselect()
        draw_board()
        game.whiteBotMove = []
        game.blackBotMove = []
        print("Moved to this grid")

        #bring up menu if promotion occurs
        if game.to_promote != None:
            if game.positions[game.to_promote[1]][game.to_promote[0]].isupper():
                start_promotion(0)
            else:
                start_promotion(1)

    #Promotion selection made
    elif promoting == True and grid_y == 3 and grid_x >= 2 and grid_x <= 5:
        if grid_x == 2:
            team = game.promote_knight()
            if team == 0:
                new_status = "Promoted wPawn to wKnight"
            else:
                new_status = "Promoted bPawn to bKnight"
        elif grid_x == 3:
            team = game.promote_bishop()
            if team == 0:
                new_status = "Promoted wPawn to wBishop"
            else:
                new_status = "Promoted bPawn to bBishop"
        elif grid_x == 4:
            team = game.promote_rook()
            if team == 0:
                new_status = "Promoted wPawn to wRook"
            else:
                new_status = "Promoted bPawn to bRook"
        elif grid_x == 5:
            team = game.promote_queen()
            if team == 0:
                new_status = "Promoted wPawn to wQueen"
            else:
                new_status = "Promoted bPawn to bQueen"
        end_promotion()
        draw_board()
        game.whiteBotMove = []
        game.blackBotMove = []

    else:
        if selected_piece != None:
            new_status = ("Unselected " + str(selected_piece) + " on " + str(alphanumerics[selected_x]) + str(8-selected_y))
        unselect()

    if game.in_check(game.get_board(), game.get_turn()):
        if new_status != "":
            new_status = new_status + ", "
        new_status = new_status + "Check"

    if not promoting:
        if new_status != "":
            new_status = new_status + ", "
        if game.get_turn() == 0:
            new_status = new_status + "White's turn"
        else:
            new_status = new_status + "Black's turn"

    if game.checkmated(1-game.get_turn()) != 0:
        if game.checkmated(1-game.get_turn()) == 1:
            if game.get_turn() == 1:
                new_status = "Checkmate! White wins."
            else:
                new_status = "Checkmate! Black wins."
        else:
            new_status = "Stalemate!"
        window.after(ggdelay, resetKeepBot)

    if game.FMC > 300:
        game.turn = 2
        new_status = "Game has gone on too long."
        window.after(ggdelay, resetKeepBot)

    if (len(game.w_captures) >= 15) and (len(game.b_captures) >= 15):
        game.turn = 2
        new_status = "Only kings remain."
        window.after(ggdelay, resetKeepBot)

    else:#CALL BOT MOVE
        if game.turn == 1 and game.blackBot != None and not game.checkmated(0) and game.blackBotMove == []:
            print("Called blackbot")
            game.ponder(1)
            doBotMove(1)

        elif game.turn == 0 and game.whiteBot != None and not game.checkmated(1) and game.whiteBotMove == []:
            print("Called whitebot")
            game.ponder(0)
            doBotMove(0)

    statusmsg.set(new_status)

    print("White has captured: ", end = "")
    print(game.get_w_captures())
    print("Black has captured: ", end = "")
    print(game.get_b_captures())


#================================================================================

#Button drawer
Button(master = buttons_frame, text="Undo (Feature unavailable)", command=undo, bg = "LightSalmon3").grid(column=0, row=0)
Button(master = buttons_frame, text="Reset", command=reset, bg = "LightSalmon3").grid(column=1, row=0)
Button(master = buttons_frame, text="Export", command=export, bg = "LightSalmon3").grid(column=2, row=0)

#Button frame config
buttons_frame.rowconfigure(0, weight=1, minsize = 50)
buttons_frame.columnconfigure([0,1,2], weight=1)

#Messages drawer
statusmsg = StringVar()
statusmsg.set("White's turn")
Label(master = statusmsg_frame, text="Status:").grid(column=0, row=0, sticky = 'e')
Label(master = statusmsg_frame, textvariable=statusmsg).grid(column=1, row=0, sticky = 'w')

#Message frame config
label_frame.rowconfigure(0, weight=1, minsize = 50)
label_frame.columnconfigure([0,1], weight=1)

statusmsg_frame.rowconfigure(0, weight=1, minsize = 50)
statusmsg_frame.columnconfigure([0,1], weight=1)


botWhite_frame.rowconfigure(0, weight=1, minsize = 50)
botWhite_frame.columnconfigure([0,1], weight=1)
botWhiteVar = StringVar()
botWhiteVar.set("Human") # default value
Label(master = botWhite_frame, text="White:").grid(column=0, row=0, sticky = 'e')
OptionMenu(botWhite_frame, botWhiteVar, "Human", "Random",command=newbotWhite).grid(column=1, row=0, sticky = 'w')

botBlack_frame.rowconfigure(0, weight=1, minsize = 50)
botBlack_frame.columnconfigure([0,1], weight=1)
botBlackVar = StringVar()
botBlackVar.set("Human") # default value
Label(master = botBlack_frame, text="Black:").grid(column=0, row=0, sticky = 'e')
OptionMenu(botBlack_frame, botBlackVar, "Human", "Random",command=newbotBlack).grid(column=1, row=0, sticky = 'w')


#Canvas drawer
canvas = Canvas(window, width=600, height=600)
canvas.grid(column=0, row=0)

#Assets loading
assets = {"Board": PhotoImage(file=resource_path("Textures\\Chess.png")),
          "wKing": PhotoImage(file=resource_path("Textures\\wKing.png")),
          "bKing": PhotoImage(file=resource_path("Textures\\bKing.png")),
          "wQueen": PhotoImage(file=resource_path("Textures\\wQueen.png")),
          "bQueen": PhotoImage(file=resource_path("Textures\\bQueen.png")),
          "wPawn": PhotoImage(file=resource_path("Textures\\wPawn.png")),
          "bPawn": PhotoImage(file=resource_path("Textures\\bPawn.png")),
          "wKnight": PhotoImage(file=resource_path("Textures\\wKnight.png")),
          "bKnight": PhotoImage(file=resource_path("Textures\\bKnight.png")),
          "wBishop": PhotoImage(file=resource_path("Textures\\wBishop.png")),
          "bBishop": PhotoImage(file=resource_path("Textures\\bBishop.png")),
          "wRook": PhotoImage(file=resource_path("Textures\\wRook.png")),
          "bRook": PhotoImage(file=resource_path("Textures\\bRook.png")),
          "Tip1": PhotoImage(file=resource_path("Textures\\Tip.png")),
          "Tip2": PhotoImage(file=resource_path("Textures\\Tip_selected.png")),
          "Tip3": PhotoImage(file=resource_path("Textures\\Tip_promotion.png")),
}

#================================================================================

#Board drawer, game starter
draw_bkg()

#test draws
#|00|01|......
#|10|11|......
#.............
clear_board()
draw_board()

#================================================================================

def Button_1(click):
    #Click parser

    global selected_x, selected_y
    global targets
    border = 10
    grid_x = -1
    grid_y = -1
    for i in range(8):
        if click.x > i*75 + border and click.x < (i+1)*75 - border:
            grid_x = i
    for i in range(8):
        if click.y > i*75 + border and click.y < (i+1)*75 - border:
            grid_y = i

    if grid_x != -1 and grid_y != -1 and not ((game.turn == 0 and game.whiteBot != None) or  (game.turn == 1 and game.blackBot != None)):#if square clicked and not bot turn
        choose(grid_x, grid_y, False)



#Binds
canvas.bind("<Button-1>", Button_1)

#================================================================================
window.mainloop()
