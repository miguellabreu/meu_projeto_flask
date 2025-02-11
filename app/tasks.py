from app import celery
import subprocess
import pandas as pd
import os
import ctypes


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
        dll_path = os.path.abspath('./write_xy_em_memoria.dll')
        
        if not os.path.exists(dll_path):
            return {
                "status": "error",
                "message": f"DLL not found at {dll_path}"
            }

        # Load DLL
        fortran_dll = ctypes.CDLL(dll_path)
        
        # Create arrays to store the results
        x_array = (ctypes.c_float * n)()
        y_array = (ctypes.c_float * n)()
        
        # Define argument types and return type
        fortran_dll.write_xy_em_memoria.argtypes = [
            ctypes.c_int,
            ctypes.POINTER(ctypes.c_float),
            ctypes.POINTER(ctypes.c_float)
        ]
        fortran_dll.write_xy_em_memoria.restype = None
        
        # Call Fortran function
        fortran_dll.write_xy_em_memoria(
            ctypes.c_int(n), 
            x_array,
            y_array
        )
        
        # Convert results to Python lists
        x_list = [x_array[i] for i in range(n)]
        y_list = [y_array[i] for i in range(n)]
        
        # Create DataFrame and convert to JSON
        df = pd.DataFrame({
            'x': x_list,
            'y': y_list
        })
        
        return {
            "status": "success",
            "message": f"Successfully generated {n} points",
            "data": df.to_dict(orient='records')
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }