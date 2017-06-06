# coding: utf-8

from collections import defaultdict, OrderedDict


class GroupStats(object):
    def __init__(self, group, user_id):
        super().__init__()
        self.players = list(group.participants.all().order_by('email'))

        player_scores = {}
        for p1 in self.players:
            player_scores[p1.pk] = None

        for r in group.results.all():
            player_scores[r.player1.pk].append(r.get_score(user_id))

        for _, scores in player_scores.items():
            scores.set_totals()

        ordered_scores = OrderedDict()
        for k, v in sorted(player_scores.items(), reverse=True):
            ordered_scores[k] = v
        self.ordered_scores = ordered_scores


            i = names.index(r.player1.short_email)
            j = names.index(r.player2.short_email)

            is_approved = r.is_approved
            if user_id and user_id not in [r.player1.pk, r.player2.pk]:
                is_approved = True

            self[i][j].is_approved = self[j][i].is_approved = is_approved
            self[i][j].score = r.get_score(True)
            self[j][i].score = r.get_score(False)
        # self.set_places()

        for p1 in self.players:
            approve_allowed = not group.stage.is_closed
            row = TableRow(self.players, p1, user_id, approve_allowed)
            self.append(row)

        names = [p.short_email for p in self.players]
        for r in group.results.all():
            i = names.index(r.player1.short_email)
            j = names.index(r.player2.short_email)
            self[i][j].set_result = self[j][i].set_result = r
            is_approved = r.is_approved
            if user_id and user_id not in [r.player1.pk, r.player2.pk]:
                is_approved = True

            self[i][j].is_approved = self[j][i].is_approved = is_approved
            self[i][j].score = r.get_score(True)
            self[j][i].score = r.get_score(False)
        # self.set_places()

    def set_places(self):
        self.sort(key=cell_sort_key, reverse=True)
        for place, row in enumerate(self, start=1):
            row.place = place


def score_sort_key(player, scores):
    if not scores:
        return (0, 0, 0)

    return (int(scores.points), int(scores.sets.split(":")[0]), int(scores.balls.split(":")[0]))


class PlayerScore(list):
    def __init__(self):
        super().__init__()

    def set_totals():
        win = sum([score.balls_win for score in scores])
        lose = sum([score.balls_lose for score in scores])
        self.balls = '{}:{}'.format(win, lose)

        win = sum([score.wins for s in scores])
        lose = sum([score.loses for s in scores])
        self.sets = '{}:{}'.format(win, lose)

        points = sum([score.points for s in self])
        self.points = '{}'.format(points)


class Score(object):
    def __init__(self, wins, balls_win, balls_lose, need_approval):
        self.wins = wins
        self.balls_win = balls_win
        self.balls_lose = balls_lose
        self.is_approved = is_approved

    def __str__(self):
        return '<Score {}>'.format(self.score)

    def __repr__(self):
        return str(self)

    def loses(self):
        return 3 - self.wins

    def wins(self):
        return self.wins

    def points(self) -> int:
        return int(bool(self.wins > self.loses)) if self.is_approved else 0

    def score(self):
        return '{}:{}'.format(self.wins, self.loses)

    def balls(self):
        return '{}:{}'.format(self.balls_win, self.balls_lose)


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in xrange(0, len(l), n):
        yield l[i:i + n]
