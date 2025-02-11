#FUNÇÃO TESTE PARA ESTUDAR PASSAGEM DE PARAMETRO POR VALOR VS POR REFERENCIA
# 
# 
# 
# # Autor: MIGUEL 


import ctypes


def test_fortran_dll():
    # Carrega a DLL
    fortran_dll = ctypes.CDLL("./fortran_codes/dll_example.dll")
    
    # Configura os tipos dos argumentos
    calculo = fortran_dll.MINHA_FUNCAO
    calculo.argtypes = [
        ctypes.c_double,                    # entrada (por valor)
        ctypes.POINTER(ctypes.c_double)     # saida (por referência)
    ]
    
    # Teste
    entrada = ctypes.c_double(5.0)
    saida = ctypes.c_double()
    
    calculo(entrada, ctypes.byref(saida))
    print(f"Entrada: {entrada.value}")  # Permanece 5.0
    print(f"Saída: {saida.value}")     # Será 10.0

if __name__ == "__main__":
    test_fortran_dll()

'''
Discussão:
1. Passagem por Valor (entrada):
   - utiliza ctypes.c_double
   - Valor é copiado para Fortran
   - Alterações em Fortran não são refletidas em Python

2. Passagem por Referência (saida):
   - utiliza POINTER(ctypes.c_double)
   - Memória é compartilhada com Fortran
   - Alterações em Fortran são refletidas em Python

'''