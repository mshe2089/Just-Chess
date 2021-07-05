def rook_moves(board, team, x, y, epc, castle):
    movelist = []
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
    return movelist