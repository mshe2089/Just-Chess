def queen_moves(board, team, x, y, epc, castle):
    movelist = []
#============================
    for i in range(x-1, -1, -1):
        if board[y][i] == "-":
            movelist.append([i,y])
        elif board[y][i].isupper():
            if team == 0:
                break
            else:
                movelist.append([i,y])
            break
        else:
            if team == 1:
                break
            else:
                movelist.append([i,y])
            break
    for i in range(x+1, 8, 1):
        if board[y][i] == "-":
            movelist.append([i,y])
        elif board[y][i].isupper():
            if team == 0:
                break
            else:
                movelist.append([i,y])
            break
        else:
            if team == 1:
                break
            else:
                movelist.append([i,y])
            break
    for i in range(y-1, -1, -1):
        if board[i][x] == "-":
            movelist.append([x,i])
        elif board[i][x].isupper():
            if team == 0:
                break
            else:
                movelist.append([x,i])
            break
        else:
            if team == 1:
                break
            else:
                movelist.append([x,i])
            break    
    for i in range(y+1, 8, 1):
        if board[i][x] == "-":
            movelist.append([x,i])
        elif board[i][x].isupper():
            if team == 0:
                break
            else:
                movelist.append([x,i])
            break
        else:
            if team == 1:
                break
            else:
                movelist.append([x,i])
            break    
#============================
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
#============================
    return movelist