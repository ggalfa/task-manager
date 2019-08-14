from manager import app, tasks

def test_list_tasks_return_status_200():
    app.config['TESTING'] = True
    with app.test_client() as cliente:
        response = cliente.get('/tasks')
        assert response.status_code == 200

def test_list_tasks_return_format_jason():
    app.config['TESTING'] = True
    with app.test_client() as cliente:
        response = cliente.get('/tasks')
        assert response.content_type == 'application/json'

def test_list_of_task_empty_return_list_empty():
    app.config['TESTING'] = True
    with app.test_client() as cliente:
        response = cliente.get('/tasks')
        assert response.json == []

def test_list_of_tasks_not_empty_return_content():
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