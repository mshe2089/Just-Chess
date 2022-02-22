from random import randint

class randomBot:

    def __init__(self, team, game) -> None:
        self.team = team
        self.game = game

    def decide(self):#decides on move based on game
        validpieces = []
        if self.team == 0:
            for i in range(8):
                for j in range(8):
                    if self.game.positions[i][j] != "-" and self.game.positions[i][j].isupper() and self.game.get_moves(j, i) != []:
                        validpieces.append([j,i])
        elif self.team == 1:
            for i in range(8):
                for j in range(8):
                    if self.game.positions[i][j] != "-" and self.game.positions[i][j].islower() and self.game.get_moves(j, i) != []:
                        validpieces.append([j,i])
        piece = validpieces[randint(0, len(validpieces)-1)]
        validmoves = self.game.get_moves(piece[0], piece[1])
        move = validmoves[randint(0, len(validmoves)-1)]
        return (piece + move)

    def decidePromotion(self):#decides on promotion target
        decision = randint(2, 5)
        return ([decision, 3, decision, 3])

