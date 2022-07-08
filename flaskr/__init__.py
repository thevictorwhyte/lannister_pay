import os
from flask import Flask, request, abort, jsonify
from utils.filters import filter_flat_type, filter_ratio_type, filter_percentage_type
import sys


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='dev'
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/split-payments/compute', methods=['POST'])
    def compute():
        body = request.get_json()
        request_id = body.get('ID', None)
        amount = body.get('Amount', None)
        currency = body.get('currency', None)
        customer_email = body.get('CustomerEmail', None)
        split_info = body.get('SplitInfo', None)

        try:
            balance = amount
            split_breakdown = []
            flat_split_type = list(filter(filter_flat_type, split_info))
            percentage_split_type = list(
                filter(filter_percentage_type, split_info))
            ratio_split_type = list(filter(filter_ratio_type, split_info))

            if(len(flat_split_type) > 0):
                for item in flat_split_type:
                    balance -= item['SplitValue']
                    split_breakdown.append({
                        'SplitEntityId': item['SplitEntityId'],
                        'Amount': item['SplitValue']
                    })

            if(len(percentage_split_type) > 0):
                for item in percentage_split_type:
                    val = (item['SplitValue'] / 100) * balance
                    balance -= val
                    split_breakdown.append({
                        'SplitEntityId': item['SplitEntityId'],
                        'Amount': val
                    })

            if(len(ratio_split_type) > 0):
                total_ratio = 0
                ratio_balance = balance
                for item in ratio_split_type:
                    total_ratio += item['SplitValue']

                for item in ratio_split_type:
                    split_amount = (item['SplitValue'] / total_ratio) * balance
                    ratio_balance -= split_amount
                    split_breakdown.append({
                        'SplitEntityId': item['SplitEntityId'],
                        'Amount': split_amount
                    })

            return jsonify({
                'success': True,
                'Balance': ratio_balance,
                'SplitBreakdown': split_breakdown,
                'ID': request_id
            })

        except Exception as e:
            print(sys.exc_info())
            print(e)
            abort(422)

    return app
