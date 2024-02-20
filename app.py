import os
from flask import Flask, request, Response, send_from_directory
from multiprocessing import Process
import subprocess

from funcs import notify_close_cars

# For local testing Only:
from dotenv import load_dotenv
load_dotenv()

subprocess.run(["playwright", "install", "chromium"])

# Check keys when program start
KEYS = os.getenv('KEYS')
if not KEYS:
    print('Missing KEYS environment variable.')
    os._exit(1)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def main_function():
    # import keys from environment variables
    keys = dict(item.split(':') for item in KEYS.split(','))

    if request.method == 'GET':
        if request.args.get('key') not in keys.values():
            return 'API key is needed'

        return Response(open('index.html').read())

    if request.method == 'POST':
        if request.args.get('key') not in keys.values():
            return 'API key is needed'

        loc = [float(request.form.get('latitude')), float(request.form.get('longitude'))]
        max_dis = float(request.form.get('radius'))
        api_key = request.form.get('key')
        login_cred = request.form.get('login_cred')
        autobook = request.form.get('autobook')
        ethical = request.form.get('ethical')

        p = Process(target=notify_close_cars, args=(loc, max_dis, api_key,autobook,login_cred, ethical,))
        p.start()

        if login_cred=='' and autobook is not None:
            return Response(open('requested_warn.html').read())
        else:
            return Response(open('requested.html').read())

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(app.root_path, 'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
    app.run(debug=False)
