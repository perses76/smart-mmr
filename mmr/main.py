from .file_repositories_loader import get_repositories
from . import echidna


def find_provider(purchase_currency_code, purchase_amount_eur, channel_code, airline_code, get_repositories=get_repositories):
    reps = get_repositories()
    channel = reps.channels[channel_code]
    airline = reps.airlines[airline_code]
    ctx = echidna.Context(
        purchase_currency=purchase_currency_code,
        amount=purchase_amount_eur,
        channel=channel,
        airline=airline,
        repositories=reps
    )
    result = []
    fxfee_rule = echidna.FxFeeRule()
    for program in reps.programs:
        tracker = echidna.Tracker()
        ctx.program = program
        ctx.tracker = tracker
        score = echidna.evaluate(ctx, [program, channel, airline, fxfee_rule])
        result.append(
            ResultItem(score=score.value, program_code=program.code, track_steps=tracker.steps)
        )
    result = sorted(result, key=lambda it: it.score)
    for idx, item in enumerate(result):
        item.rank = idx
    return result


class ResultItem():
    def __init__(self, score, program_code, rank=0, track_steps=None):
        self.score = score
        self.program_code = program_code
        self.rank = rank
        self.track_steps = track_steps
