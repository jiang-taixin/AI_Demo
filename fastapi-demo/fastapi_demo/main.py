import uvicorn
from fastapi import FastAPI
from fastapi import Request, Response

from ORM_Example.api.user import user
from ORM_Example.api.chat import chat
from example.views import example
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from tortoise.contrib.fastapi import register_tortoise
from ORM_Example.settings import orm_setting

app = FastAPI()
# fastapi启动 register_tortoise就会执行
register_tortoise(app=app, config=orm_setting)

app.include_router(example, prefix='/example', tags=['Example'])
app.include_router(user, prefix='/user', tags=['用户'])
app.include_router(chat, prefix='/chat', tags=['对话'])


# 中间件  按照函数声明顺序倒序执行  先middleware_method1后middleware_method2
origins = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)


@app.middleware('http')
async def middleware_method2(request: Request, next_call):
    # print('------- middleware_method2 request')
    response = await next_call(request)
    response.headers['auther'] = 'admin'
    # print('------- middleware_method2 response')
    return response


@app.middleware('http')
async def middleware_method1(request: Request, next_call):
    # print('------- middleware_method1 request', request.client.host)
    # if request.client.host not in ['127.0.0.1']:
    #     return Response(content='forbidden', status_code=403)
    # if request.url.path in ['/user/user_list']:
    #     return Response(content='forbidden', status_code=403)
    response = await next_call(request)
    # print('------- middleware_method1 response')
    return response


# 静态文件  path是访问路径  directory='static'实际路径
# http://localhost:8000/static/index.html
app.mount('/static', StaticFiles(directory='static'))

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', reload=True, port=8000)
