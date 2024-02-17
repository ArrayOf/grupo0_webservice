from http import HTTPStatus
from os.path import join, dirname, realpath
from json import loads

from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from redis.asyncio import Redis
from uvicorn import run

app = FastAPI()

dir_templates = join(dirname(realpath(__file__)), 'templates')
TEMPLATES = Jinja2Templates(directory=dir_templates)

REDIS = Redis(
    host='<endereço ip ou host>',
    port=17639,
    password='<senha>'
)


@app.get('/', response_class=HTMLResponse)
async def get_index(
        request: Request
):
    dados = []

    cursor = 0
    while True:
        cursor, keys = await REDIS.scan(cursor, 'GRUPO0:ALUNOS:*', 1_000)
        if keys:
            for key in keys:
                data = await REDIS.get(key)
                dados.append(loads(data))

        if not cursor:
            break

    dados = sorted(dados, key=lambda x: x['id'], reverse=False)

    return TEMPLATES.TemplateResponse(
        name='index.html',
        context={'request': request, 'dados': dados}
    )


@app.delete('/delete', status_code=HTTPStatus.NO_CONTENT)
async def delete_aluno(
        aluno_id: int = Query(),
):
    await REDIS.delete(f'GRUPO0:ALUNOS:{aluno_id}')


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
