from flask import Flask, jsonify
from waitress import serve
import time

app = Flask(__name__)

count_by_guid = {}

@app.route('/checkin/<guid>/<server_id>')
def checkin(guid, server_id):
    """
    Adds a new GUID to the dictionary with a count of 0 and the server ID it checked in from.
    """
    count_by_guid[guid] = {'count': 0, 'server_id': server_id, 'last_updated': time.time()}

@app.route('/update/<guid>/<count>')
def update(guid, count):
    """
    Updates the count for a given GUID.
    """
    count_by_guid[guid]['count'] = count
    count_by_guid[guid]['last_updated'] = time.time()

@app.route('/query')
def query():
    """
    Queries the dictionary for all GUIDs and their associated counts. If a GUID has not been updated in the last 5 minutes,
    its count is reset to 0.
    """
    for guid in count_by_guid:
        if time.time() - count_by_guid[guid]['last_updated'] >= 300:
            count_by_guid[guid]['count'] = 0
            count_by_guid[guid]['last_updated'] = time.time()
    return jsonify(count_by_guid)

@app.route('/checkout/<guid>')
def checkout(guid):
    """
    Resets the count for a given GUID to 0.
    """
    count_by_guid[guid]['count'] = 0
    count_by_guid[guid]['last_updated'] = time.time()

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=8000)

