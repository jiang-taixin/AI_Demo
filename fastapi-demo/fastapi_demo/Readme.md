### Fastapi

#### PyCharm创建Fastapi项目

* pip install fastapi
* pip install uvicorn
* --reload --port 8001 

#### 路径操作

* 装饰器方法
```
@user.get()
@user.post()
@user.put()
@user.patch()
@user.delete()
@user.options()
@user.head()
@user.trace()
```

* 装饰器参数
```python
from fastapi import APIRouter
'''
创建路由
prefix 前缀 如prefix='/example' 则请求url为/example/example/3   tags标签--下面接口不加的话都在当前标签下
在这里设置参数和在include_router设置效果相同
'''
user = APIRouter(prefix='', tags=['用户管理'])
'''
装饰器参数
加tags的话如果和路由tags一致则合并，不一致则额外创建新的标签
deprecated=True是否废弃
response_description='响应description'
'''
@user.get('/user', summary='通过id查询用户 summary',
          description='通过id查询用户 description',
          tags=['用户管理'],
          response_description='响应description',
          deprecated=True)
def get_user():
    return {'message': 'get response'}
```

* include_router路由分发

```python
from fastapi import FastAPI
from example.views import example

app = FastAPI()
app.include_router(example, prefix='/example', tags=['用户管理'])
```

#### 路径参数
```python
from fastapi import APIRouter
user = APIRouter()
# 路径参数名和变量名对应
@user.get('/{user_id}', summary='获取路径参数')
async def get_path_arg(user_id: int):    # 类型不声明默认str
    return {'message': f'example id = {user_id}'}
```

#### 查询参数  url?a=xx&b=xx
```python
# 获取url参数  路径函数中声明不属于路径参数的其他函数参数时    它们将被自动解释为查询字符串参数
# 这时arg1是路径参数  arg2是查询参数 http://localhost:8000/example/get_url_arg/22?arg2=22
@example.get('/get_url_arg/{arg1}', summary='获取url参数')
async def get_url_arg(arg1: str, arg2: str):
    return {'message': f'get url arguments--arg1:{arg1}, arg2:{arg2}'}
```
* 参数非必填   建议第一种
```python
@example.get('/get_url_arg/{arg1}', summary='获取url参数')
async def get_url_arg(arg1: str, arg2: str = Query(default=None, description='查询参数2')):
    return {'message': f'get url arguments--arg1:{arg1}, arg2:{arg2}'}
```
或
```python
@example.get('/get_url_arg/{arg1}', summary='获取url参数')
async def get_url_arg(arg1: str, arg2: str = ''):
    return {'message': f'get url arguments--arg1:{arg1}, arg2:{arg2}'}
```

* Union & Optional  Optional是Union的简写
```python
@example.get('/get_url_arg/{arg1}', summary='获取url参数')
async def get_url_arg(arg1: str,
                      arg2: Union[str, None] = Query(default=None, description='查询参数2'),
                      arg3: Optional[str] = None):
    return {'message': f'get url arguments--arg1:{arg1}, arg2:{arg2}, arg3:{arg3}'}
```

#### 请求体数据
* pydantic 用来做类型强制检查 pip install pydantic
* 定义model model字段有默认值非必填
```python
from datetime import date
from pydantic import BaseModel, Field
class User(BaseModel):
    name: str = Field(pattern='^a')  # 正则表达式
    age: int = Field(default=20, gt=0, lt=100)  # 范围约束
    birthday: date

```
* 定义接口
```python
@example.post('/post_data', summary='post请求发送请求体数据')
async def post_data(data: User):
    print(data.dict(), type(data))     # 会将请求体数据转换成User对象   数据类型不一致会尝试转换   转换失败报错
    return {'message': 'post response'}
```

* validators
```python
from datetime import date
from pydantic import BaseModel, Field ,field_validator


class User(BaseModel):
    # name: str = Field(pattern='^a')  # 正则表达式
    name: str
    age: int = Field(default=20, gt=0, lt=100)  # 范围约束
    birthday: date

    @field_validator('name')  # 限定校验字段
    def name_validator(self, value):  # cls当前对象   value当前字段值
        assert value.isalpha(), 'name must be alpha'
        return value
```

* 类型嵌套
```python
from datetime import date
from pydantic import BaseModel, Field ,field_validator


class Address(BaseModel):
    province: str
    city: str


class User(BaseModel):
    # name: str = Field(pattern='^a')  # 正则表达式
    name: str
    age: int = Field(default=20, gt=0, lt=100)  # 范围约束
    birthday: date
    address: Address

    @field_validator('name')  # 限定校验字段
    def name_validator(cls, value):  # cls当前对象   value当前字段值
        assert value.isalpha(), 'name must be alpha'
        return value
```

#### Form表单数据
FastApi使用Form组件接收表单数据，需要先安装python-multipart  pip install python-multipart

```python
from fastapi import Form
@example.post('/post_form_data', summary='post请求发送form表单')
async def post_form_data(arg1: str = Form(), arg2: str = Form()):

    return {'message': f'arg1 = {arg1}, arg2 = {arg2}'}
```

#### 文件上传

* File方式

```python
from fastapi import File
@example.post('/upload_file', summary='文件上传')
async def upload_file(file: bytes = File()):
    return {'message': f'file name:{file.title}, file length:{len(file)}'}

@example.post('/upload_files', summary='文件上传')
async def upload_files(files: List[bytes] = File()):
    return {'message': f'upload files'}
```

* UploadFile方式

```python
import os.path
from fastapi import UploadFile
@example.post('/upload_file_n', summary='使用UploadFile上传文件')
async def upload_file_n(file: UploadFile):
    # 将文件进行保存
    path = os.path.join('example/files', file.filename)
    with open(path, 'wb') as f:
        for line in file.file:
            f.write(line)

    return {'message': f'file name:{file.filename}'}
```

#### Request对象
```python
from fastapi import Request
@example.get('/', summary='get example summary',
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

```

#### 静态文件访问
```python
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
app = FastAPI()
app.mount('/static', StaticFiles(directory='static'))
```

#### 响应模型参数

* response_model
```python

# 这里将请求数据反序列化成User对象，进行操作后再用UserRes过滤后进行返回
@example.post('/response_model', response_model=UserRes, summary='响应模型参数')
async def response_model(user: User):
    return user
```

* response_model_exclude_unset 数据本身没有的字段不会包含Model设定的字段
```python
@example.get('response_model_exclude/{name}',
             response_model=Item,
             summary='response_model_exclude_unset参数',
             response_model_exclude_unset=True)
async def response_model_exclude(name: str):
    print(name)
    item = items[name]
    return item
```

#### ORM 推荐使用tortoise ORM   1.异步 2.简单
* 安装tortoise ORM
```
pip install tortoise-orm
```
* 创建关系模型  其中User对应多个ChatRecord  
```python
from tortoise.models import Model
from tortoise import fields


class BaseModel(Model):
    create_time = fields.DatetimeField(auto_now_add=True, null=True)
    update_time = fields.DatetimeField(auto_now=True, null=True)


class User(BaseModel):
    id = fields.IntField(pk=True, description='用户ID')
    user_name = fields.CharField(max_length=32, description='用户名')
    password = fields.CharField(max_length=32, description='密码')
    telephone = fields.CharField(max_length=15, description='手机号')


class MulTestModel(BaseModel):
    id = fields.IntField(pk=True, description='ID')
    name = fields.CharField(max_length=255, description='名称')


class ChatRecord(BaseModel):
    id = fields.IntField(pk=True, description='对话ID')
    request_id = fields.CharField(max_length=40, description=' 请求ID')
    input_tokens = fields.IntField(description='Input Tokens')
    output_tokens = fields.IntField(description='Output Tokens')
    total_tokens = fields.IntField(description='Total Tokens')

    # 一对多的关系 related_name反向查询关联   一个user对应多个chat
    user = fields.ForeignKeyField('models.User', related_name='chats')
    # 多对多关系
    mul = fields.ManyToManyField('models.MulTestModel', related_name='chats', description='测试多对多')
```
* 迁移命令 aerich迁移工具
```python
# 在main.py 导入
from tortoise.contrib.fastapi import register_tortoise
```
```python
from ORM_Example.settings import orm_setting

# fastapi启动 register_tortoise就会执行
register_tortoise(app=app, config=orm_setting)
```
```python
# config配置
orm_setting = {
    'connections': {
        'default': {
            'engine': 'tortoise.backends.mysql',
            'credentials': {
                'host': '127.0.0.1',
                'port': '3306',
                'user': 'root',
                'password': 'Accenture123',
                'database': 'fastapi',
                'minsize': 1,
                'maxsize': 5,
                'charset': 'utf8',
                'echo': True
            }
        }
    },
    'apps': {
        'models': {
            'models': ['ORM_Example.models'],
            'default_connection': 'default'
        }
    },
}
```
* 连接完成 此时数据库没有数据表  安装aerich
```
pip install aerich
```
* 初始化配置，只需要使用一次
```
执行前切换目录  把earich自带的模型类添加进去'models': ['ORM_Example.models', 'aerich.models'],
aerich init -t ORM_Example.settings.orm_setting
```
* 初始化完成会在当前目录生成pyprojexct.toml文件和migrations文件夹 migrations保存迁移文件 pyproject.toml保存配置文件路径
* 初始化数据库  执行完数据库里会生成数据表
```
aerich init-db
```
* 更新模型并进行迁移
```python
class MulTestModel(BaseModel):    # 任意创建一个模型测试多对多
    id = fields.IntField(pk=True, description='ID')
    name = fields.CharField(max_length=255, description='名称')
    # 修改数据表测试 default=''
    comment = fields.CharField(max_length=255, description='备注', default='')
```
* 执行migrate命令 --name 给这次改动增加名称 aerich migrate --name add_column   这时只生成迁移文件并没有修改数据库
```
aerich migrate
```
```python
from tortoise import BaseDBAsyncClient

# 执行后生成迁移文件  升级和降级
async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `multestmodel` ADD `comment` VARCHAR(255) NOT NULL  COMMENT '备注' DEFAULT '';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `multestmodel` DROP COLUMN `comment`;"""
```

* 执行upgrade命令  这时才真正修改数据库   撤销执行downgrade
```
aerich upgrade
```

#### tortoise ORM查询

* 导入模型类
```python
from ORM_Example.models import User
```
* 查询
```python
@user.get('/user_list', description='获取用户列表')
async def get_user_list():
    # 查询所有
    # users = await User.all()   # queryset [User(), User(), ...]
    # for u in users:
    #     print(u.user_name)
    # return users

    # filter
    # users = await User.filter(user_name='test')
    # for u in users:
    #     print(u.user_name)
    # return users

    # get
    # users = await User.get(user_name='test')
    # return users

    # 模糊查询
    # users = await User.filter(id__gt=1)  # id__gt=1 id>1  id__in=[2, 3]  id__range=[1, 1000]
    # return users

    # values查询
    users = await User.all().values('user_name', 'id')  # 只返回数据name id字段
    return users

@user.get('/{user_id}', description='通过id获取用户')
async def get_user(user_id: int):
    usr = await User.get(id=user_id)
    return usr
```

#### tortoise ORM添加数据

* 数据校验模型
```python
from pydantic import BaseModel, field_validator
# 数据校验模型
class UserIn(BaseModel):
    user_name: str
    password: str
    telephone: str

    @field_validator('user_name')
    def name_validator(cls, value):
        assert value.isalpha(), 'name must be alpha'
        return value

    @field_validator('password')
    def pwd_validator(cls, value):
        assert len(value) > 5, 'password length must more than 5'
        return value

    @field_validator('telephone')
    def tel_validator(cls, value):
        assert len(value) == 11, 'telephone length must be 11'
        return value
```

* 数据添加  单表
```python
@user.post('/', description='创建用户')
async def create_user(user_in: UserIn):
    # 方式1
    # usr = User(user_name=user_in.user_name, password=user_in.password, telephone=user_in.telephone)
    # await usr.save()  #

    # 方式2
    usr = await User.create(user_name=user_in.user_name, password=user_in.password, telephone=user_in.telephone)
    return usr
```
* 数据添加   一对多多对多
```python
@chat.post('/', description='记录对话信息')
async def create_chat(chat_in: ChatIn):
    chat_record = await ChatRecord.create(request_id=chat_in.request_id, input_tokens=chat_in.input_tokens,
                                          output_tokens=chat_in.output_tokens, total_tokens=chat_in.total_tokens,
                                          user_id=chat_in.user_id)    # 一对多关系绑定
    # 多对多关系绑定  先把chat传入的对多数组取出对象
    choose_mul = await MulTestModel.filter(id__in=chat_in.mul)
    # choose_mul 数组打散插入
    # await chat_record.mul.clear()   # 清空关联信息
    await chat_record.mul.add(*choose_mul)
    return chat_record
```

#### 多对多查询
```python
@chat.get('/chat_list', description='获取对话列表')
async def get_chat_list():
    # user__user_name  user一对多属性名 __关联对象属性名
    chats = await ChatRecord.all().values('request_id', 'user__user_name', 'mul__name')  
    return chats
```

```python
@chat.get('/{chat_id}', description='通过id获取对话')
async def get_chat(chat_id: int):
    chat_record = await ChatRecord.get(id=chat_id)

    # 一对多查询
    print(await chat_record.user.values('user_name'))
    # 多对多查询
    print(await chat_record.mul.all().values('name'))

    return chat_record
```

#### 数据更新

* 单表更新
```python
@user.put('/{id}', description='修改用户')
async def update_user(user_id: int, user_in: UserIn):
    data = user_in.dict()
    result = await User.filter(id=user_id).update(**data)
    if result == 1:
        return await User.get(id=user_id)
    else:
        return {'message': 'update failed'}
```

* 多表关联更新
```python
@chat.put('/{chat_id: int}', description='修改对话')
async def update_chat(chat_id: int, chat_in: ChatIn):
    print('chat in:', chat_in)
    data = chat_in.dict()
    print('data:', data)

    # chat in: request_id='string' input_tokens=0 output_tokens=0 total_tokens=0 user_id='string' mul=[0]
    # data: {'request_id': 'string', 'input_tokens': 0, 'output_tokens': 0, 'total_tokens': 0, 'user_id': 'string', 'mul': [0]}

    # 此时执行filter update会报错    因为chat表没有mul字段  先将mul pop出来
    mul = data.pop('mul')
    print('mul:', mul)    # [0]

    # 更新chat表
    result = await ChatRecord.filter(id=chat_id).update(**data)
    if result == 1:
        edit_chat = await ChatRecord.get(id=chat_id)
    else:
        return {'message': 'update failed'}

    # 更新多对多的关系
    choose_mul = await MulTestModel.filter(id__in=mul)
    # 先清除原有关联
    await edit_chat.mul.clear()
    await edit_chat.mul.add(*choose_mul)
    return edit_chat
```

#### 删除数据

* 单表数据删除
```python
@user.delete('/{user_id}', description='删除用户')
async def delete_user(user_id: int):
    result = await User.filter(id=user_id).delete()  # result 删除条数
    if not result:
        raise HTTPException(status_code=404, detail=f'主键为{user_id}的用户不存在')
    else:
        return {'message': 'delete success'}
```

* 有关联表数据删除
```python
@chat.delete('/{chat_id}', description='删除对话')
async def delete_chat(chat_id: int):
    result = await ChatRecord.filter(id=chat_id).delete()
    # 多对多关联不用删除    会自动删除
    if not result:
        raise HTTPException(status_code=404, detail=f'主键为{chat_id}的对话记录不存在')
    else:
        return {'message': 'delete success'}
```

#### 中间件

* 中间件是一个函数，在每个请求被特定的路径操作处理之前，以及每个响应之后工作
* 创建中间件
```python
# 中间件  按照函数声明顺序倒序执行  先middleware_method1后middleware_method2
@app.middleware('http')
async def middleware_method2(request: Request, next_call):
    print('------- middleware_method2 request')
    response = await next_call(request)
    response.headers['auther'] = 'admin'
    print('------- middleware_method2 response')
    return response


@app.middleware('http')
async def middleware_method1(request: Request, next_call):
    print('------- middleware_method1 request', request.client.host)
    if request.client.host not in ['127.0.0.1']:
        return Response(content='forbidden', status_code=403)
    if request.url.path in ['/user/user_list']:
        return Response(content='forbidden', status_code=403)
    response = await next_call(request)
    print('------- middleware_method1 response')
    return response
```
* 跨域  下面代码是fastapi封装的中间件
```python
# 这个是自定义示例   只能处理简单请求
@app.middleware('http')
async def cors_middleware(request: Request, next_call):
    response = await next_call(request)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response
```

```python
from fastapi.middleware.cors import CORSMiddleware

origins = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['GET', 'POST', 'PUT', 'DELETE'],
    allow_headers=['*']
)
```


#### Docker
* 启动 launchctl start docker 
* 