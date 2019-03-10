import engine as eng


def run_test(program_rules=None, channel_airline=eng.Airline('dy'), purchase_currency='USD', program_volume=1, program_scheme="mc", channel_rules=None):
    airline = eng.Airline("dy")
    enett = eng.Program(
        code="enett",
        scheme=program_scheme,
        currencies=['USD'],
        volume=program_volume,
        rules=program_rules
    )
    dy_agency = eng.Channel(
        code="dy_agency",
        airlines=[channel_airline],
        rules=channel_rules
    )
    ctx = eng.Context(program=enett, channel=dy_agency, amount=100, airline=airline, purchase_currency=purchase_currency)
    return eng.evaluate(ctx, [enett, dy_agency])


def test_no_rules():
    score = run_test()
    assert score == eng.Score(0)


def test_no_channel_support_airline():
    score = run_test(
        program_rules=[eng.SupportAirlineRule()],
        channel_airline=eng.Airline('s7')
    )
    assert score == eng.HALT


def test_exchange_required():
    score = run_test(
        purchase_currency='CZK',
        program_rules=[eng.FxFeeRule()]
    )
    assert score == eng.Score(-0.4)


def test_with_kickback_rule():
    kickback_rule = eng.KickbackRule(code="less8", min_volume=0, max_volume=8, percent=0.1)
    score = run_test(
        program_volume=4,
        program_rules=[kickback_rule]
    )
    assert score == eng.Score(10)


def test_evaluate_rule_returns_None():
    class MyRule():
        def evaluate(self, ctx):
            return None
    expected_score = eng.Score(16)
    score = eng.evaluate(None, [MyRule()], init_score=expected_score)
    assert score == expected_score


def test_scheme_surcharge_rule():
    score = run_test(
        program_scheme="visa",
        program_volume=4,
        channel_rules=[eng.SchemeSurchargeRule(code="mc_only", percent=-0.1, accepted_scheme="mc")]
    )
    assert score == eng.Score(-10)
