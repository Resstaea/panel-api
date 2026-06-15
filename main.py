from flask import Flask, request, jsonify
import os
import requests
from datetime import datetime

app = Flask(__name__)

UPSTREAM_URL = "http://147.135.212.197/crapi/had/viewstats"

# Token untuk akses Flask kamu (parameter)
MY_TOKEN = os.environ.get('MY_TOKEN', 'hYuwoskkkaw28kss')

# Token API upstream ke 147.135.212.197
UPSTREAM_TOKEN = os.environ.get('UPSTREAM_TOKEN', 'Qk5YQUVBUzRkeJVjR4CId0GDlFVBc2Bia4CFU0qAWHRbZZaGXmGHUw==')

@app.route('/crapi/had/viewstats', methods=['GET'])
def viewstats():
    token = request.args.get('token')

    if token != MY_TOKEN:
        return jsonify({"status": "error", "msg": "Invalid token"}), 401

    now = datetime.now()
    today = now.strftime('%Y-%m-%d')

    dt1 = request.args.get('dt1', f'{today}-00:00:00')
    dt2 = request.args.get('dt2', f'{today}-23:59:59')
    records = request.args.get('records', '100')
    sEcho = request.args.get('sEcho', '1')

    try:
        resp = requests.get(UPSTREAM_URL, params={
            'token': UPSTREAM_TOKEN,  # pakai token API upstream
            'dt1': dt1,
            'dt2': dt2,
            'records': records,
            'sEcho': sEcho,
        }, timeout=10)

        data = resp.json()
        return jsonify(data)

    except requests.exceptions.Timeout:
        return jsonify({"status": "error", "msg": "Upstream timeout"}), 504
    except Exception as e:
        return jsonify({"status": "error", "msg": str(e)}), 500


@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "time": datetime.now().isoformat()})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)
