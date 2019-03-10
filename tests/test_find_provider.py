import os
import pytest
from mmr import find_provider
from mmr import repositories as reps
from mmr.file_repositories_loader import get_repositories
from mmr import echidna


def get_hardcoded_repositories(url=None):
    programs = reps.Repository(
        "programs",
        [
            echidna.Program(
                code="ENETT_GWTTP",
                scheme="MC",
                currencies=["EUR"],
                rules=[echidna.GenerationFeeRule(percent=0.05)]
            ),
            echidna.Program(
                code="AMADEUS_B2BSAVE",
                scheme="VISA",
                currencies=["EUR", "SEK"],
            ),
        ]
    )
    channels = reps.Repository(
        "channels",
        [
            echidna.Channel(
                code="DY_AGENCY",
            )
        ]
    )
    airlines = reps.Repository(
        "airlines",
        [
            echidna.Airline(
                code="DY",
                rules=[
                    echidna.SchemeSurchargeRule(code="VISA_SCHEME_SURCHARGE", percent=0.1, scheme="VISA")
                ],
            )
        ]
    )
    return reps.Repositories(
        programs=programs,
        channels=channels,
        airlines=airlines
    )


def get_repositories_from_directory():
    url = os.path.join(os.path.dirname(__file__), 'simple_sample')
    return get_repositories(url)


@pytest.mark.parametrize("get_repositories", [get_hardcoded_repositories, get_repositories_from_directory])
def test_enett_gwttp_win(get_repositories):
    result = find_provider(
        purchase_currency_code="EUR",
        purchase_amount_eur=100,
        channel_code="DY_AGENCY",
        airline_code="DY",
        get_repositories=get_repositories
    )
    assert len(result) == 2

    item0 =  result[0]
    item1 =  result[1]
    for item in result:
        print(f"{item.rank} - {item.program_code}: {item.track_steps}")

    assert item0.rank == 0
    assert item0.score == 5
    assert item0.program_code == 'ENETT_GWTTP'

    assert item1.rank == 1
    assert item1.score == 10
    assert item1.program_code == 'AMADEUS_B2BSAVE'


@pytest.mark.parametrize("get_repositories", [get_hardcoded_repositories, get_repositories_from_directory])
def test_amadeus_b2bsave_win(get_repositories):
    result = find_provider(
        purchase_currency_code="SEK",
        purchase_amount_eur=100,
        channel_code="DY_AGENCY",
        airline_code="DY",
        get_repositories=get_repositories
    )
    assert len(result) == 2

    item0 =  result[0]
    item1 =  result[1]
    assert item0.rank == 0
    assert item0.score == 10
    assert item0.program_code == 'AMADEUS_B2BSAVE'

    assert item1.rank == 1
    assert item1.score == 15
    assert item1.program_code == 'ENETT_GWTTP'
    for item in result:
        print(f"{item.rank} - {item.program_code}: {item.track_steps}")
