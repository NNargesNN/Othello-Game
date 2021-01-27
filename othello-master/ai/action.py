class Action:
    def __init__(self, board, choice, minimax, heuristic=0):
        self.board = board
        self.choice = choice
        self.minimax = minimax
        self.heuristic = heuristic
        self.score = 0

    def get_score(self):
        return self.score


class Scorer:
    def __init__(self, func, mn, mx, weight):
        self.func = func
        self.mn = mn
        self.mx = mx
        self.weight = weight

    def score(self, actions):
        sorted_actions = sorted(actions, key=self.func)
        for i in range(len(sorted_actions)):
            current_score = 0
            if i > 0:
                current_score += self.func(sorted_actions[i]) - self.func(sorted_actions[i - 1])
            if i + 1 < len(sorted_actions):
                current_score += self.func(sorted_actions[i + 1]) - self.func(sorted_actions[i])
            if i == 0 or i == len(sorted_actions) - 1:
                current_score += 0.4 * (self.mx - self.mn)
            current_score += 0.4 * (self.mx - self.mn)
            sorted_actions[i].score += 100 * (current_score - self.mn) / (self.mx - self.mn) * self.weight
        # sort konim bad taghsim bar tedad konim be har nafar bar axe faselash ba nazidk tarin cut emtiaz bedim
        # -inf [list] +inf