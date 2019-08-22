from manager import app, tasks
import json
# from collections import Mapping


def test_listed_tasks_return_status_200():
    app.config['TESTING'] = True
    with app.test_client() as cliente:
        response = cliente.get('/tasks')
        assert response.status_code == 200

def test_listed_tasks_return_format_jason():
    app.config['TESTING'] = True
    with app.test_client() as cliente:
        response = cliente.get('/tasks')
        assert response.content_type == 'application/json'

def test_listed_of_task_empty_return_list_empty():
    app.config['TESTING'] = True
    with app.test_client() as cliente:
        response = cliente.get('/tasks')
        assert response.json == []

def test_listed_of_tasks_not_empty_return_content():
    tasks.append({'id': 1, 'titulo': 'tarefa 1',
                   'descricao': 'tarefa numero 1', 'estado': False})
    app.config['TESTING'] = True
    with app.test_client() as cliente:
        response = cliente.get('/tasks')
        assert response.json == [{
            'id': 1,
            'titulo': 'tarefa 1',
            'descricao': 'tarefa numero 1',
            'estado': False
        }]
    tasks.clear()

def test_create_task_accept_post():
    with app.test_client() as cliente:
        response = cliente.post('/task')
        assert response.status_code != 405

def test_create_task_return_task_inserted():
    tasks.clear()
    cliente = app.test_client()
    # performs the request using the verb POST
    response = cliente.post('/task', data=json.dumps({
        # 'id': 'id',
        'titulo': 'titulo',
        'descricao': 'descricao'}),
        content_type='application/json')
    # analysis and transformation to python object of the answer is performed
    data = json.loads(response.data.decode('utf-8'))
    assert data['id'] == 1
    # assert data['titulo'] == 'titulo'
    # assert data['descricao'] == 'descricao'
    # when the comparison is with True, False or None, is 'is'
    assert data['estado'] is False

def test_create_task_status_code_return_201():
    with app.test_client() as cliente:
        response = cliente.post('/task', data=json.dumps({
            'titulo': 'titulo',
            'descricao': 'descricao',}),
            content_type='application/json')
        assert response.status_code == 201

def test_create_task_insert_element_in_blank():
        tasks.clear()
        with app.test_client() as cliente:
            # make a request using the POST verb
            cliente.post('/task', data=json.dumps({
                'titulo': 'titulo',
                'descricao': 'descricao'}),
                content_type='application/json')
            assert len(tasks) > 0

# def test_listed_tasks_must_present_tasks_not_finished_first():
#     tasks.clear()
#     tasks.append({'id': 1, 'titulo': 'tarefa 1', 'descricao': 'tarefa de numero 1',
#                   'estado': True})
#     tasks.append({'id': 2, 'titulo': 'tarefa 2', 'descricao': 'tarefa de numero 2',
#                   'estado': False})
#     with app.test_client() as cliente:
#         response = cliente.get('/task')
#         data = json.loads(response.data.decode('UTF-8'))
#         first_task, second_task = data
#         assert first_task['titulo'] == 'tarefa 2'
#         assert second_task['titulo'] == 'tarefa 1'

def test_delete_task_uses_verb_delete():
    tasks.clear()
    with app.test_client() as cliente:
        response = cliente.delete('/tasks/1')
        assert response.status_code != 405

def test_remove_task_exists_return_204():
    tasks.clear()
    tasks.append({'id': 1, 'titulo': 'titulo',
                   'descricao': 'descricao', 'estado': False})
    cliente = app.test_client()
    response = cliente.delete('/task/1', content_type='application/json')
    assert response.status_code == 204
    assert response.data == b''

def test_to_remove_task_exists_remove_task_from_list():
    tasks.clear()
    tasks.append({'id': 1, 'titulo': 'titulo',
                   'descricao': 'descricao', 'estado': False})
    cliente = app.test_client()
    cliente.delete('/task/1', content_type='application/json')
    assert len(tasks) == 0

def test_to_remove_task_not_exists():
    tasks.clear()
    cliente = app.test_client()
    response =  cliente.delete('/task/1', content_type='application/json')
    assert response.status_code == 404

def test_detail_task_exists():
    tasks.clear()
    tasks.append({'id': 1, 'titulo': 'titulo',
                   'descricao': 'descricao', 'entregue': False})
    cliente = app.test_client()
    response = cliente.get('/task/1', content_type='application/json')
    data = json.loads(response.data.decode('utf-8'))
    assert response.status_code == 200
    assert data['id'] == 1
    assert data['titulo'] == 'titulo'
    assert data['descricao'] == 'descricao'
    assert data['entregue'] == False

def test_detail_task_not_exists():
    tasks.clear()
    cliente = app.test_client()
    response = cliente.get('/task/1', content_type='application/json')
    assert response.status_code == 404

def test_update_a_task_existing():
    tasks.clear()
    tasks.append({'id': 1, 'titulo': 'titulo',
                   'descricao': 'descricao', 'estado': False})
    cliente = app.test_client()
    response = cliente.put('/task/1', data=json.dumps(
        {'titulo': 'titulo atualizado',
          'descricao': 'descricao atualizada', 'estado': True}
    ),
        content_type='application/json')
    data = json.loads(response.data.decode('utf-8'))
    assert response.status_code == 200
    assert data['id'] == 1
    assert data['titulo'] == 'titulo atualizado'
    assert data['descricao'] == 'descricao atualizada'
    assert data['estado'] is True

def test_update_a_task_not_existing():
    tasks.clear()
    cliente = app.test_client()
    response = cliente.put('/task/1', data=json.dumps({
        'titulo': 'titulo atualizado',
        'descricao': 'descricao atualizada', 'estado': True
    }),
        content_type='application/json')
    assert response.status_code ==  404

def test_updating_a_task_with_fields_invalids():
    tasks.clear()
    tasks.append({'id': 1, 'titulo': 'titulo',
                    'descricao': 'descricao', 'estado': False})
    cliente = app.test_client()
    # sem estado
    response = cliente.put('/taskfa/1', data=json.dumps(
        {'titulo': 'titulo atualizado',
         'decricao': 'descricao atualizada'}
    ),
        content_type='application/json')
    if response.status_code == 400:
        assert response.status_code == 400
    assert response.status_code == 404
    # sem descrição
    response = cliente.put('/task/1', data=json.dumps(
        {'titulo': 'titulo atualizado',
         'estado': False}
    ),
        content_type='application/json')
    assert response.status_code == 400
    # sem titulo
    response = cliente.put('/task/1', data=json.dumps(
        {'descricao': 'descricao atualizado',
         'estado': False}
    ),
        content_type='application/json')
    assert response.status_code == 400
