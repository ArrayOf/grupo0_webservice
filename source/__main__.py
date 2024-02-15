from http import HTTPStatus
from os.path import join, dirname, realpath

from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from uvicorn import run

app = FastAPI()

dir_templates = join(dirname(realpath(__file__)), 'templates')
TEMPLATES = Jinja2Templates(directory=dir_templates)


@app.get('/', response_class=HTMLResponse)
async def get_index(
        request: Request
):
    dados = [
        {'id': 1, 'nome': 'Mario', 'idade': 46},
        {'id': 2, 'nome': 'Thiago', 'idade': 38},
        {'id': 3, 'nome': 'Vitor', 'idade': 26},
        {'id': 4, 'nome': 'Thayra', 'idade': 25},
    ]

    return TEMPLATES.TemplateResponse(
        name='index.html',
        context={'request': request, 'dados': dados}
    )


@app.delete('/delete', status_code=HTTPStatus.NO_CONTENT)
async def delete_aluno(
        aluno_id: int = Query(),
):
    print(f'DELETOU DO BANCO DE DADOS O ALUNO {aluno_id}')


@app.get('/details', response_class=HTMLResponse)
async def details(
        request: Request,
        aluno_id: int = Query(),
):
    return TEMPLATES.TemplateResponse(
        name='details.html',
        context={'request': request, 'aluno_id': aluno_id}
    )


if __name__ == '__main__':
    run(app, host='0.0.0.0', port=8080)
