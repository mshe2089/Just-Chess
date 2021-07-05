def pawn_moves(board, team, x, y, epc, castle):
    movelist = []

    def in_bounds(x, y):
        if x <= 7 and x >= 0 and y <=7 and y >= 0:
            return True
        return False

    if team == 0:
        if in_bounds(x, y-1) and board[y-1][x] == "-":
            movelist.append([x,y-1])
            if in_bounds(x, y-2) and board[y-2][x] == "-" and y == 6:
                movelist.append([x,y-2])
        if in_bounds(x-1, y-1):
            if board[y-1][x-1].islower() or [x-1, y-1] == epc:
                movelist.append([x-1,y-1])
        if in_bounds(x+1, y-1):
            if board[y-1][x+1].islower() or [x+1, y-1] == epc:
                movelist.append([x+1,y-1])
    else:
        if in_bounds(x, y+1) and board[y+1][x] == "-":
            movelist.append([x,y+1])
            if in_bounds(x, y+2) and board[y+2][x] == "-" and y == 1:
                movelist.append([x,y+2])
        if in_bounds(x-1, y+1):
            if board[y+1][x-1].isupper() or [x-1, y+1] == epc:
                movelist.append([x-1,y+1])
        if in_bounds(x+1, y+1):
            if board[y+1][x+1].isupper() or [x+1, y+1] == epc:
                movelist.append([x+1,y+1])

    return movelist