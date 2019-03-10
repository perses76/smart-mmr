class Score():
    def __init__(self, value=0):
        self.value = value

    def __add__(self, other):
        return Score(self.value + other.value)

    def __eq__(self, other):
        return self.value == other.value

    def __repr__(self):
        return f"Score: {self.value}"

HALT = Score("halt")
BINGO = Score("bingo")
ZERO = Score(0)

class NullTracker():
    def log(self, message):
        pass


class Tracker():
    def __init__(self):
        self._steps = []

    def log(self, message):
        self._steps.append(message)

    @property
    def steps(self):
        return self._steps


def evaluate(ctx, rules, init_score=ZERO):
    total_score = init_score
    for rule in rules:
        score = rule.evaluate(ctx)
        ctx.tracker.log({"rule": rule.code, "score": score})
        if score is not None:
            if score == HALT or score == BINGO:
                return score
            total_score = score + total_score
    return total_score


class Context():
    def __init__(self, channel, amount, airline, purchase_currency, repositories=None, program=None, tracker=NullTracker()):
        self.program = program
        self.channel = channel
        self.amount = amount
        self.airline = airline
        self.purchase_currency = purchase_currency
        self.tracker = tracker
        self.respositories = repositories


class Program():
    def __init__(self, code, scheme, currencies, rules=None):
        self.code = code
        self.scheme = scheme
        self.currencies = currencies
        self.rules = rules if rules else []

    def evaluate(self, ctx):
        return evaluate(ctx, self.rules)


class Channel():
    def __init__(self, code, rules=None):
        self.code = code
        self.rules = rules if rules else []

    def evaluate(self, ctx):
        return evaluate(ctx, self.rules)


class Airline():
    def __init__(self, code, name=None, rules=None):
        self.code = code
        self.name = name
        self.rules = rules if rules else []

    def __eq__(self, other):
        return self.code == other.code

    def evaluate(self, ctx):
        return evaluate(ctx, self.rules)


class KickbackRule():
    def __init__(self, code, min_volume, max_volume, percent):
        self.code = code
        self.min_volume = min_volume
        self.max_volume = max_volume
        self.percent = percent

    def evaluate(self, ctx):
        if ctx.program.volume > self.min_volume and ctx.program.volume < self.max_volume:
            return Score(ctx.amount * self.percent)


class SchemeSurchargeRule():
    def __init__(self, code, percent, scheme):
        self.code = code
        self.percent = percent
        self.scheme = scheme

    def evaluate(self, ctx):
        if ctx.program.scheme == self.scheme:
            return Score(ctx.amount * self.percent)


class FxFeeRule():
    code = "fxfee"
    percent = 0.1
    def __init__(self):
        pass

    def evaluate(self, ctx):
        if ctx.purchase_currency in ctx.program.currencies:
            return ZERO
        return Score(ctx.amount * self.percent)


class GenerationFeeRule():
    code="GENERATION_FEE"
    def __init__(self, percent):
        self.percent  = percent

    def evaluate(self, ctx):
        return Score(ctx.amount * self.percent)
