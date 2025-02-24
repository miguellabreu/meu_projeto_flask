from flask import jsonify, request
from app import app, celery , redis_client
from app.tasks import reverse_string
from app.tasks import solver_fortran , write_xy_task , write_xy_em_memoria_task , write_xy_em_memoria_so
import subprocess

@app.route('/')
def home():
    return "Hello, Flask!"

@app.route('/reverse', methods=['POST'])
def reverse():
    data = request.get_json()
    string = data['string']
    task = reverse_string.delay(string)
    return jsonify({"task_id": task.id})

@app.route('/compile_fortran', methods=['POST'])
def compile_fortran():
    result = subprocess.run(['gfortran', 'xy.f90', '-o', 'exec.exe'], capture_output=True, text=True)
    if result.returncode != 0:
        return jsonify({"error": result.stderr}), 500
    return jsonify({"message": "Fortran code compiled successfully."})


@app.route('/run_fortran', methods=['POST'])
def run_fortran():
    task = solver_fortran.delay()
    return jsonify({"task_id": task.id})

'''
Rota para verificar o status de uma tarefa
args:
    task_id: str - ID da tarefa
returns:
    JSON - status da tarefa
'''
@app.route('/task_status/<task_id>', methods=['GET'])
def task_status(task_id):
    task = celery.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'current': 0,
            'total': 1,
            'status': 'Pending...'
        }
    elif task.state == 'PROGRESS':
        response = {
            'state': task.state,
            'current': task.info.get('current', 0),
            'total': task.info.get('total', 1),
            'status': 'In progress...'
        }
    elif task.state == 'SUCCESS':
        response = {
            'state': task.state,
            'current': 1,
            'total': 1,
            'status': 'Task completed!',
            'result': task.get()
        }
    else:
        response = {
            'state': task.state,
            'current': 1,
            'total': 1,
            'status': str(task.info)
        }
    return jsonify(response)


@app.route('/write_xy', methods=['POST'])
def write_xy():
    n = request.json.get('n')
    print('n', n)
    task = write_xy_task.delay(n)
    return jsonify({
            "status": "Task started",
            "task_id": task.id  
        })


@app.route('/write_xy_em_memoria', methods=['POST'])
def write_xy_em_memoria():
    n = request.json.get('n')
    print('n', n)
    task = write_xy_em_memoria_task.delay(n)
    return jsonify({
            "status": "Task started",
            "task_id": task.id  
        })

@app.route('/get_xy_data/<task_id>', methods=['GET'])
def get_xy_data(task_id):
    print(f"Fetching data for Task ID: {task_id}")
    # Recupere os dados do Redis usando o task_id
    x_data = redis_client.get(f'x_data_{task_id}')
    y_data = redis_client.get(f'y_data_{task_id}')

    if not x_data or not y_data:
        print(f"Data not found for Task ID: {task_id}")
        return jsonify({"status": "error", "message": "Data not found in Redis"}), 404

    # Converta os dados de volta para listas
    x_list = eval(x_data.decode('utf-8'))  # Converte string para lista
    y_list = eval(y_data.decode('utf-8'))  # Converte string para lista

    return jsonify({
        "status": "success",
        "task_id": task_id,
        "data": {"x": x_list, "y": y_list}
    })

@app.route('/write_xy_em_memoria_so', methods=['POST'])
def write_xy_em_memoria_so_route():
    n = request.json.get('n')
    print('n', n)
    task = write_xy_em_memoria_so.delay(n)
    return jsonify({
        "status": "Task started",
        "task_id": task.id  
    })