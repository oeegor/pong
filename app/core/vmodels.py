# coding: utf-8


class Table(list):
    def __init__(self, group, user_id):
        super().__init__()
        self.players = list(group.participants.all())
        for p1 in self.players:
            can_add_approve = not group.stage.is_closed
            row = TableRow(self.players, p1, user_id, can_add_approve)
            self.append(row)

    def set_places(self):
        def key(i):
            return (int(i.points), int(i.sets.split(":")[0]), int(i.balls.split(":")[0]))
        self.sort(key=key, reverse=True)
        for place, row in enumerate(self, start=1):
            row.place = place


class TableRow(list):
    def __init__(self, players, player1, user_id, can_add_approve):
        super().__init__()
        self.player1 = player1
        self.place = None
        for player2 in players:
            is_current_user = user_id in [player1.pk, player2.pk]
            can_add_approve = is_current_user and can_add_approve
            self.append(TableCell(None, player1, player2, can_add_approve))

    @property
    def balls(self):
        win = sum([s.score.balls_win for s in self if s.score])
        lose = sum([s.score.balls_lose for s in self if s.score])
        return '{}:{}'.format(win, lose)

    @property
    def sets(self):
        win = sum([s.score.wins for s in self if s.score])
        lose = sum([s.score.loses for s in self if s.score])
        return '{}:{}'.format(win, lose)

    @property
    def points(self):
        points = sum([s.score.points for s in self if s.score])
        return '{}'.format(points)


class TableCell(object):
    def __init__(self, score, player1, player2, can_add_approve):
        self.score = score
        self.player1 = player1
        self.player2 = player2
        self.is_approved = None
        self.can_add_approve = can_add_approve
        self.is_filler = player1.pk == player2.pk

    def __str__(self):
        return '<Cell {}>'.format(self.score)

    def __repr__(self):
        return str(self)


class Score(object):
    def __init__(self, wins, balls_win, balls_lose, is_approved):
        self.wins = wins
        self.balls_win = balls_win
        self.balls_lose = balls_lose
        self.is_approved = is_approved

    def __str__(self):
        return '<Score {}>'.format(self.score)

    def __repr__(self):
        return str(self)

    @property
    def loses(self):
        return 3 - self.wins

    @property
    def points(self):
        return int(bool(self.wins > self.loses)) if self.is_approved else 0

    @property
    def score(self):
        return '{}:{}'.format(self.wins, self.loses)

    @property
    def balls(self):
        return '{}:{}'.format(self.balls_win, self.balls_lose)


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in xrange(0, len(l), n):
        yield l[i:i+n]
