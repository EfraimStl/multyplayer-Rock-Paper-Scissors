class Game:
    def __init__(self, id):
        self.p1went = False
        self.p2went = False
        self.ready = False
        self.id = id
        self.moves = [None, None]
        self.wins = [0, 0]
        self.ties = 0

    def get_player_move(self, p):
        return self.moves[p]

    def play(self, player, move):
        self.moves[player] = move
        if player == 0:
            self.p1went = True
        else:
            self.p2went = True

    def connected(self):
        return self.ready

    def both_went(self):
        return self.p1went and self.p2went

    def winner(self):
        p1 = self.moves[0].upper()[0]
        p2 = self.moves[1].upper()[0]

        if p1 == p2:
            winner = 2
        elif (p1 == "R" and p2 == "S") or (p1 == "P" and p2 == "R") or (p1 == "S" and p2 == "P"):
            winner = 0
        else:
            winner = 1

        return winner

    def reset_moves(self):
        self.p1went = False
        self.p2went = False

    def reset(self):
        self.p1went = False
        self.p2went = False
        self.ready = False
        self.moves = [None, None]
        self.wins = [0, 0]
        self.ties = 0


