from flask import Flask, jsonify, request, abort
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

# Creating a route for create task.
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

# Creating a route to remove task by id.
@app.route('/task/<int:id_tasks>',methods=['DELETE'])
def remove(id_tasks):
    task = [task for task in tasks if task['id'] == id_tasks]
    if not task:
        abort(404)
    tasks.remove(task[0])
    return '', 204

# Creating a route detail task
@app.route('/task/<int:id_task>', methods=['GET'])
def detail(id_task):
    task = [task for task in tasks if task['id'] == id_task]
    if not task:
        abort(404)
    return jsonify(task[0])

# Creating a route for update task
@app.route('/task/<int:id_task>', methods=['PUT'])
def update(id_task):
    task = [task for task in tasks if task['id'] == id_task]
    title = request.json.get('titulo')
    description = request.json.get('descricao')
    entregue = request.json.get('estado')
    if not task:
        abort(404)
    if not description or not title or entregue is None:
        abort(400)
    task_chosen = task[0]
    task_chosen['titulo'] = title or task_chosen['titulo']
    task_chosen['descricao'] = description or task_chosen['descricao']
    task_chosen['estado'] = entregue or task_chosen['estado']
    return jsonify(task_chosen)

