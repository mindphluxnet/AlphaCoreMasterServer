from flask import Flask, jsonify
from waitress import serve
import time

app = Flask(__name__)

count_by_server = {}

@app.route('/report/<server_id>/<count>')
def update(server_id, count):    
    # Server reports player count once a minute.
    if server_id not in count_by_server:
        count_by_server[server_id] = {'count': count, 'last_updated': time.time()}
    else:
        count_by_server[server_id]['count'] = count
        count_by_server[server_id]['last_updated'] = time.time()

@app.route('/query')
def query():
    # If a server has not updated its user count in the last 5 minutes reset it to zero.    
    for server_id in count_by_server:
        if time.time() - count_by_server[server_id]['last_updated'] >= 300:
            count_by_server[server_id]['count'] = 0
            count_by_server[server_id]['last_updated'] = time.time()
    return jsonify(count_by_server)

@app.route('/checkout/<server_id>')
def checkout(server_id):
    # Used at server shutdown.
    if server_id not in count_by_server:
        count_by_server[server_id] = {'count': 0, 'last_updated': time.time()}
    else:
        count_by_server[server_id]['count'] = 0
        count_by_server[server_id]['last_updated'] = time.time()

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=8000)

