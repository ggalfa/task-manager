from flask import Flask,jsonify

app = Flask('Manager')

tasks = []
tasks.append({'id': 1, 'titulo': 'Python', 'descricao': 'Curso de Python e Flask'})

@app.route('/tasks')
def list():
    return jsonify(tasks)