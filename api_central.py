from fastapi import FastAPI
import random

app = FastAPI(title='Core API')

@app.get('/')
def check():
    return {'status': 'Online'}

@app.get('/solicitar-viagem')
def trip():
    return {'sucesso': True, 'motorista': 'Roberto Cruz', 'preco': 8.53}
