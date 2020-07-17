from flask import Flask, request, send_file, jsonify, abort, render_template
from ininal import IninalScraper

ininal_scraper = IninalScraper()
app = Flask("ininal_scraper")


@app.route('/ininal_scraper/api/get_transactions', methods=['GET'])
def get_transactions():
    try:
        start_date = request.json["start_date"]
        end_date = request.json["end_date"]
    except:
        start_date = None
        end_date = None

    transactions = ininal_scraper.get_all_transactions(start_date, end_date)
    if transactions:
        return jsonify(dict(success=True, transactions=transactions))
    else:
        return jsonify(dict(success=False))


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=1339)