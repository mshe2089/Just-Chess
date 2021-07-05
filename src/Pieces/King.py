def king_moves(board, team, x, y, epc, castle):
    movelist = []

    def in_bounds(x, y):
        if x <= 7 and x >= 0 and y <=7 and y >= 0:
            return True
        return False

    for i in [-1,0,1]:
        for j in [-1,0,1]:
            if (i == 0 and j == 0):
                continue
            elif in_bounds(x+i, y+j) and (board[y+j][x+i] == "-" or ((board[y+j][x+i].isupper() and team == 1) or (board[y+j][x+i].islower() and team == 0))):
                movelist.append([x+i, y+j])


    return movelist