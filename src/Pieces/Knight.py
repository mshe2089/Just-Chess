def knight_moves(board, team, x, y, epc, castle):
    movelist = []
    def in_bounds(x, y):
        if x <= 7 and x >= 0 and y <=7 and y >= 0:
            return True
        return False

    if in_bounds(x+2, y-1) and (board[y-1][x+2] == "-" or ((board[y-1][x+2].isupper() and team == 1) or (board[y-1][x+2].islower() and team == 0))):
        movelist.append([x+2, y-1])
    if in_bounds(x+2, y+1) and (board[y+1][x+2] == "-" or ((board[y+1][x+2].isupper() and team == 1) or (board[y+1][x+2].islower() and team == 0))):
        movelist.append([x+2, y+1])
    if in_bounds(x+1, y-2) and (board[y-2][x+1] == "-" or ((board[y-2][x+1].isupper() and team == 1) or (board[y-2][x+1].islower() and team == 0))):
        movelist.append([x+1, y-2])
    if in_bounds(x+1, y+2) and (board[y+2][x+1] == "-" or ((board[y+2][x+1].isupper() and team == 1) or (board[y+2][x+1].islower() and team == 0))):
        movelist.append([x+1, y+2])
    if in_bounds(x-1, y-2) and (board[y-2][x-1] == "-" or ((board[y-2][x-1].isupper() and team == 1) or (board[y-2][x-1].islower() and team == 0))):
        movelist.append([x-1, y-2])
    if in_bounds(x-1, y+2) and (board[y+2][x-1] == "-" or ((board[y+2][x-1].isupper() and team == 1) or (board[y+2][x-1].islower() and team == 0))):
        movelist.append([x-1, y+2])
    if in_bounds(x-2, y-1) and (board[y-1][x-2] == "-" or ((board[y-1][x-2].isupper() and team == 1) or (board[y-1][x-2].islower() and team == 0))):
        movelist.append([x-2, y-1])
    if in_bounds(x-2, y+1) and (board[y+1][x-2] == "-" or ((board[y+1][x-2].isupper() and team == 1) or (board[y+1][x-2].islower() and team == 0))):
        movelist.append([x-2, y+1])
    return movelist