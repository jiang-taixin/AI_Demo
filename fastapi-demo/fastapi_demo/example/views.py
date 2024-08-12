import os.path
from typing import Union, Optional, List

from fastapi import APIRouter, Query, Form, File, UploadFile, Request
import uvicorn

from example.models import User, UserRes, Item, items

'''
创建路由
prefix 前缀 如prefix='/example' 则请求url为/example/example/3   tags标签--下面接口不加的话都在当前标签下
'''
example = APIRouter()


'''
装饰器参数
加tags的话如果和路由tags一致则合并，不一致则额外创建新的标签
deprecated=True是否废弃
response_description='响应description'
'''


@example.get('/', summary='请求模型',
             description='get example description',
             response_description='get example response description')
async def example_get(request: Request):
    print(request.url, request.client.host, request.client.port)
    return {'request message': {
        'url': request.url,
        'ip': request.client.host,
        'port': request.client.port,
        'user-agent': request.headers.get('user-agent'),
        'cookie': request.cookies
    }}


# 路径参数名和变量名对应
@example.get('/get_path_arg/{input_id}', summary='获取路径参数')
async def get_path_arg(input_id: int):
    return {'message': f'example id = {input_id}'}


# 获取url参数  路径函数中声明不属于路径参数的其他函数参数时    它们将被自动解释为查询字符串参数
@example.get('/get_url_arg/{arg1}', summary='获取url参数')
async def get_url_arg(arg1: str,
                      arg2: Union[str, None] = Query(default=None, description='查询参数2'),
                      arg3: Optional[str] = None):
    return {'message': f'get url arguments--arg1:{arg1}, arg2:{arg2}, arg3:{arg3}'}


''' post 
    会将请求体数据转换成User对象   数据类型不一致会尝试转换   转换失败报错
    如 name='23' 转成name=23    name='ww'报错
    '''


@example.post('/post_data', summary='post请求发送请求体数据')
async def post_data(data: User):
    print(data.dict(), type(data))
    return data


@example.post('/post_form_data', summary='post请求发送form表单')
async def post_form_data(arg1: str = Form(), arg2: str = Form()):
    return {'message': f'arg1 = {arg1}, arg2 = {arg2}'}


@example.post('/upload_file', summary='文件上传')
async def upload_file(file: bytes = File()):
    return {'message': f'file name:{file.title}, file length:{len(file)}'}


@example.post('/upload_files', summary='多个文件上传')
async def upload_files(files: List[bytes] = File()):
    return {'message': f'upload files'}


@example.post('/upload_file_n', summary='使用UploadFile上传文件')
async def upload_file_n(file: UploadFile):
    # 将文件进行保存
    path = os.path.join('example/files', file.filename)
    with open(path, 'wb') as f:
        for line in file.file:
            f.write(line)

    return {'message': f'file name:{file.filename}'}


@example.post('/response_model', response_model=UserRes, summary='响应模型参数')
async def response_model(user: User):
    return user


# response_model_exclude_defaults,response_model_exclude_none,response_model_exclude
# response_model_include
@example.get('response_model_exclude/{name}',
             response_model=Item,
             summary='response_model_exclude_unset参数',
             response_model_exclude_unset=True)
async def response_model_exclude(name: str):
    print(name)
    item = items[name]
    return item


if __name__ == '__main__':
    uvicorn.run('views:example', reload=True, port=8989)
