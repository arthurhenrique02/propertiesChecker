# Comandos:

##### python -m venv .venv
##### (ative a venv)
##### pip install -r requirements.txt
##### python .\main.py (roda o servidor em flask)
##### celery -A main.celery beat -l INFO (roda o celery para a task async)
##### celery -A main.celery beat -l INFO (roda o celery beat para achamar a task 1 vez no dia)

##### (importante manter um terminal para cada 'servidor' (flask, celery e celery beat), pois o projeto não está rodando no docker)
