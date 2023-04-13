from flask import Flask, jsonify
from waitress import serve
import time

app = Flask(__name__)

count_by_guid = {}

@app.route('/checkin/<guid>/<server_id>')
def checkin(guid, server_id):
    # Used at server start.
    count_by_guid[guid] = {'count': 0, 'server_id': server_id, 'last_updated': time.time()}

@app.route('/update/<guid>/<count>')
def update(guid, count):
    # Used every time an user logs into the world server.
    count_by_guid[guid]['count'] = count
    count_by_guid[guid]['last_updated'] = time.time()

@app.route('/query')
def query():
    # If the server has not updated its user count in the last 5 minutes reset it to zero.    
    for guid in count_by_guid:
        if time.time() - count_by_guid[guid]['last_updated'] >= 300:
            count_by_guid[guid]['count'] = 0
            count_by_guid[guid]['last_updated'] = time.time()
    return jsonify(count_by_guid)

@app.route('/checkout/<guid>')
def checkout(guid):
    # Used at server shutdown.
    count_by_guid[guid]['count'] = 0
    count_by_guid[guid]['last_updated'] = time.time()

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=8000)

