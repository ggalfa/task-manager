from flask import Flask, jsonify, request
from operator import itemgetter
import json


app = Flask('Manager')

tasks = []
# tasks.append({
#             'id': 1,
#             'titulo': 'tarefa 1',
#             'descricao': 'tarefa numero 1',
#             'estado': False})

@app.route('/tasks')
def listed():
    return jsonify(sorted(tasks, key=itemgetter('estado')))


@app.route('/task', methods=['POST'])
def create():
    # titulo = request.json.get('titulo')
    # descricao = request.json.get('descricao')
    titulo = request.get_json('titulo')
    descricao = request.get_json('descricao')
    if not descricao or not titulo:
        abort(400)

    task = {
        'id': len(tasks) + 1,
        'titulo': titulo,
        'descricao': descricao,
        'estado': False
    }
    tasks.append(task)
    return jsonify(task), 201