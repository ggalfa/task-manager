from flask import Flask,jsonify

app = Flask('Manager')

tasks = []

@app.route('/tasks')
def list():
    return jsonify(tasks)