from flask import jsonify, request
from app import app, celery
from app.tasks import reverse_string
from app.tasks import solver_fortran , write_xy_task , write_xy_em_memoria_task
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

