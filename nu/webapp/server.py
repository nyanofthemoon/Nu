# sudo python3.7 app.py

import redis
from flask import Flask, request, jsonify, render_template
app = Flask(__name__)

pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
storage = redis.Redis(connection_pool=pool)

@app.route('/')
def index():
    data = {
        'title': 'Meta Dashboard'
    }
    return render_template('index.html', data=data)

@app.route('/status')
def status():
    data = {
        'name': 'Meta'
    }
    return render_template('status.html', data=data)

@app.route('/speech', methods=['GET', 'POST'])
def speech():
    if request.method == 'GET':
        data = {
        }
        return render_template('speech.html', data=data)
    else:
        data = request.get_json()
        storage.publish('sense.brain.webspeech2text', str(data))
        return jsonify({})

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port='80')
