# Configurando um projeto com Flask

## Passo 01

Gere um ambiente virtual com o Python, garantindo que ele está instalado em seu computador.
Execute o seguinte comando no diretorio do projeto:

> python -m venv venv

## Passo 02

Acesse o terminal do venv e baixe todas as dependências que estão no arquivo requirements.txt. Execute o seguinte comando:

> venv\Scripts\activate

> pip install -r requirements.txt

## passo 03

Inicie o servidor Redis. No Windows, você pode fazer isso executando o seguinte comando no diretório onde o Redis está instalado:

>cd '.\Program Files\Redis\'
> .\redis-server.exe

## passo 04
Inicie o worker do Celery em um terminal separado ( no diretorio raiz
C:\Users\Miguel\Desktop\Lamce\meu_projeto_flask) :

>cd C:\Users\Miguel\Desktop\Lamce\meu_projeto_flask
>celery -A celery_worker worker --pool=solo --loglevel=info

## Passo 05

Opcionalmente, você pode iniciar o Flower, uma ferramenta de monitoramento para Celery, em outro terminal:

>celery -A celery_worker flower

# fortran e DLL

## Compilar e criar DLL ( cmd /k "C:\Program Files (x86)\Intel\oneAPI\setvars.bat")

Para compilar e criar uma DLL a partir de um código Fortran, você pode usar o compilador `gfortran`. Execute o seguinte comando no terminal:


> gfortran -shared -o write_xy.dll write_xy.f90

Para compilar com o Intel Fortran sem dependências adicionais, você pode usar o seguinte comando:


No PowerShell utilize para utilizar o compilador intel :

cmd /k "C:\Program Files (x86)\Intel\oneAPI\setvars.bat"

>ifx /dll /MT /o write_xy_teste.dll write_xy_teste.f90 

Isso garantirá que todas as bibliotecas necessárias sejam vinculadas estaticamente, evitando dependências externas.

No WSL:

> gfortran -shared -fPIC -o write_xy_em_memoria.so write_xy_em_memoria.f90



## Verificando a DLL com dumpbin

Para verificar as exportações de uma DLL, você pode usar a ferramenta `dumpbin` que vem com o Visual Studio. Execute o seguinte comando no terminal:

> dumpbin /exports write_xy.dll


dumpbin /dependents write_xy.dll (para verificar dependencias )

No Wsl:
> ldd write_xy_em_memoria.so
NEEDED:  
        NEEDED               libgfortran.so.5
        NEEDED               libm.so.6

Isso exibirá uma lista de todas as funções exportadas pela DLL, permitindo que você verifique se a compilação foi bem-sucedida e se todas as funções esperadas estão presentes.

## Utilizando o Flower

Para acessar a interface do Flower, abra seu navegador e vá para o seguinte endereço:

> [http://127.0.0.1:5555/](http://127.0.0.1:5555/)

Isso permitirá que você monitore as tarefas do Celery, visualize estatísticas e gerencie workers de forma fácil e intuitiva.