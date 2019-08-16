from manager import app, tasks
import json


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
        'id': 'id',
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

# def test_crete_task_without_description():
#     with app.test_client() as cliente:
#         # status code must be 400 indicating a client error
#         response = cliente.post('/task', data=json.dumps({'titulo': 'titulo'}),
#                                 content_type='application/json')
#         assert response.status_code == 400
#     assert response.status_code == 201
