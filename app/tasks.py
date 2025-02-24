from app import celery , redis_client
import subprocess
import pandas as pd
import os
import ctypes
import uuid

@celery.task(bind=True)
def reverse_string(self, string):
    self.update_state(state='PROGRESS', meta={'current': 0, 'total': len(string)})
    result = string[::-1]
    self.update_state(state='PROGRESS', meta={'current': len(string), 'total': len(string)})
    return result

@celery.task(bind=True)
def solver_fortran(self):
    #self.update_state(state='PROGRESS', meta={'current': 0, 'total': 2})
    result = subprocess.run(['./exec.exe'], capture_output=True, text=True)
    if result.returncode != 0:
        return {"error": result.stderr}
    
    #self.update_state(state='PROGRESS', meta={'current': 1, 'total': 2})
    output = readCSV('output_xy.csv')

    #self.update_state(state='PROGRESS', meta={'current': 2, 'total': 2})
    return {"message": "Fortran executable ran successfully.", "output": output}

def readCSV(filename):
    df = pd.read_csv(filename)
    return df.to_json()

def compile_fortran():
    result = subprocess.run(['gfortran', 'xy.f90', '-o', 'exec.exe'], capture_output=True, text=True)
    if result.returncode != 0:
        return {"error": result.stderr}
    return {"message": "Fortran code compiled successfully."}

print("path" , os.path.join(os.path.dirname(os.path.dirname(__file__)), 'write_xy.dll'))

@celery.task(bind=True)
def write_xy_task(self, n):
    """
    Celery task to call Fortran DLL function.
    
    Args:
        self: Task instance (auto-injected by Celery when bind=True)
        n: Number of points to generate
        
    Returns:
        dict: Status information
    """
    try:
        # Get absolute path to DLL
        dll_path = os.path.abspath('./write_xy_teste.dll')
        
        if not os.path.exists(dll_path):
            return {
                "status": "error",
                "message": f"DLL not found at {dll_path}"
            }

        # Load DLL and set argument types   
        fortran_dll = ctypes.CDLL(dll_path)
        fortran_dll.write_xy.argtypes = [ctypes.c_int]
        fortran_dll.write_xy.restype = None
        
        # Execute Fortran function
        fortran_dll.write_xy(n)
        
        # conveterndo o df em json
        df_json = readCSV('output_xy.csv')

        return {
            "status": "success", 
            "message": f"Successfully generated {n} points",
            "output": df_json
        }
        
    except Exception as e:
        return {
            "status": "error Exeption write_xy_task",
            "message": str(e)
        }

# task para rodar write_xy_em_memoria
@celery.task(bind=True)
def write_xy_em_memoria_task(self, n):
    try:
        # Código para chamar a função Fortran e gerar os dados
        dll_path = os.path.abspath('./fortran_codes/write_xy_em_memoria.dll')
        fortran_dll = ctypes.CDLL(dll_path)
        x_array = (ctypes.c_float * n)()
        y_array = (ctypes.c_float * n)()
        fortran_dll.write_xy_em_memoria.argtypes = [
            ctypes.c_int,
            ctypes.POINTER(ctypes.c_float),
            ctypes.POINTER(ctypes.c_float)
        ]
        fortran_dll.write_xy_em_memoria.restype = None
        fortran_dll.write_xy_em_memoria(ctypes.c_int(n), x_array, y_array)

        # Converta os resultados para listas Python
        x_list = [x_array[i] for i in range(n)]
        y_list = [y_array[i] for i in range(n)]

        # Gerar um ID único para esta execução
        task_id = self.request.id
        print(f"Task ID: {task_id}")

        # Salvar os dados no Redis com chaves únicas
        redis_client.set(f'x_data_{task_id}', str(x_list))  # Salva a lista x
        redis_client.set(f'y_data_{task_id}', str(y_list))  # Salva a lista y

        return {
            "status": "success",
            "message": f"Successfully generated {n} points",
            "data": {"x": x_list, "y": y_list},
            "task_id": task_id  # Retorna o ID único
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
    
@celery.task(bind=True)
def write_xy_em_memoria_so(self, n):
    try:
        # Código para chamar a função Fortran e gerar os dados
        so_path = os.path.abspath('./fortran_codes/write_xy_em_memoria.so')
        fortran_so = ctypes.CDLL(so_path)
        x_array = (ctypes.c_float * n)()
        y_array = (ctypes.c_float * n)()
        fortran_so.write_xy_em_memoria.argtypes = [
            ctypes.c_int,
            ctypes.POINTER(ctypes.c_float),
            ctypes.POINTER(ctypes.c_float)
        ]
        fortran_so.write_xy_em_memoria.restype = None
        fortran_so.write_xy_em_memoria(ctypes.c_int(n), x_array, y_array)

        # Converta os resultados para listas Python
        x_list = [x_array[i] for i in range(n)]
        y_list = [y_array[i] for i in range(n)]

        # Gerar um ID único para esta execução
        task_id = self.request.id
        print(f"Task ID: {task_id}")

        # Salvar os dados no Redis com chaves únicas
        redis_client.set(f'x_data_{task_id}', str(x_list))  # Salva a lista x
        redis_client.set(f'y_data_{task_id}', str(y_list))  # Salva a lista y

        return {
            "status": "success",
            "message": f"Successfully generated {n} points",
            "data": {"x": x_list, "y": y_list},
            "task_id": task_id  # Retorna o ID único
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }