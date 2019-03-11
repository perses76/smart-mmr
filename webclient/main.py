import os
import mmr
from flask import Flask, render_template, request
app = Flask(__name__)

@app.route("/control-panel")
def control_panel():
    data = {}
    return render_template('control_panel.html', **data)


@app.route("/")
def search():
    data = {
        "purchase_currency_code": 'EUR',
        "purchase_amount_eur": 100,
        "channel_code": 'DY_AGENCY',
        "airline_code": 'DY',
    }
    if request.args.get("do_search"):
        data.update({
            "purchase_currency_code": request.args.get("purchase_currency_code"),
            "purchase_amount_eur": float(request.args.get("purchase_amount_eur")),
            # "channel_code": request.args.get("channel_code"),
            # "airline_code": request.args.get("airline_code"),
        })
        result = mmr.find_provider(**data)
        data['result'] = result
    return render_template('search.html', **data)


def get_searcher():
    import importlib.util
    path = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            '..',
            'mmr',
            'main.py'
        )
    )
    spec = importlib.util.spec_from_file_location("smartmmr.main", path)
    main_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(main_module)
    return main_module.find_provider
