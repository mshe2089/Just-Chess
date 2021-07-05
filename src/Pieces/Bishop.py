def bishop_moves(board, team, x, y, epc, castle):
    movelist = []
    i = 1
    while x+i <= 7 and y+i <= 7:
        if board[y+i][x+i] == "-":
            movelist.append([x+i,y+i])
        elif board[y+i][x+i].isupper():
            if team == 0:
                break
            else:
                movelist.append([x+i,y+i])
            break
        else:
            if team == 1:
                break
            else:
                movelist.append([x+i,y+i])
            break
        i += 1
    i = 1
    while x+i <= 7 and y-i >= 0:
        if board[y-i][x+i] == "-":
            movelist.append([x+i,y-i])
        elif board[y-i][x+i].isupper():
            if team == 0:
                break
            else:
                movelist.append([x+i,y-i])
            break
        else:
            if team == 1:
                break
            else:
                movelist.append([x+i,y-i])
            break
        i += 1
    i = 1
    while x-i >= 0 and y+i <= 7:
        if board[y+i][x-i] == "-":
            movelist.append([x-i,y+i])
        elif board[y+i][x-i].isupper():
            if team == 0:
                break
            else:
                movelist.append([x-i,y+i])
            break
        else:
            if team == 1:
                break
            else:
                movelist.append([x-i,y+i])
            break
        i += 1
    i = 1
    while x-i >= 0 and y-i >= 0:
        if board[y-i][x-i] == "-":
            movelist.append([x-i,y-i])
        elif board[y-i][x-i].isupper():
            if team == 0:
                break
            else:
                movelist.append([x-i,y-i])
            break
        else:
            if team == 1:
                break
            else:
                movelist.append([x-i,y-i])
            break
        i += 1
    return movelist