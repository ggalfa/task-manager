from flask import Flask,jsonify

app = Flask('Manager')

tasks = []
tasks.append({'id': 1, 'titulo': 'Python', 'descricao': 'Curso de Python e Flask'})
tasks.append({'id': 2, 'titulo': 'Python e Django', 'descricao': 'Curso de Python e Django'})

@app.route('/tasks')
def list():
    return jsonify(tasks)