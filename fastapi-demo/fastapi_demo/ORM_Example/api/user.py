import json

from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel, field_validator
from fastapi.responses import JSONResponse
from tortoise.exceptions import DoesNotExist, MultipleObjectsReturned

from ORM_Example.models import User, ChatRecord, MulTestModel

user = APIRouter()


class LoginIn(BaseModel):
    user_name: str
    password: str


class LoginOut(BaseModel):
    user_name: str
    id: int
    telephone: str


@user.post('/login', description='用户登录')
async def login(login_in: LoginIn):
    try:
        usr = await User.get(user_name=login_in.user_name)
        if usr.password == login_in.password:
            usr_out = {'user_name': usr.user_name, 'id': usr.id, 'telephone': usr.telephone}
            return JSONResponse(status_code=200, content={'message': 'login success', 'code': 200, 'user': usr_out})
        else:
            return JSONResponse(status_code=200, content={'message': 'password error', 'code': 400})
    except MultipleObjectsReturned as e:
        return JSONResponse(status_code=200, content={'message': 'Multiple users', 'code': 400})
    except DoesNotExist as e:
        return JSONResponse(status_code=200, content={'message': 'user does not exist', 'code': 400})


@user.get('/test', description='测试连通')
async def test():
    print('test')
    return {'message': 'connect success'}


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
    try:
        usr = await User.get(id=user_id)
        usr_out = {'user_name': usr.user_name, 'id': usr.id, 'telephone': usr.telephone, 'password': usr.password}
        return JSONResponse(status_code=200, content={'message': 'login success', 'code': 200, 'user': usr_out})
    except DoesNotExist as e:
        return JSONResponse(status_code=200, content={'message': 'user does not exist', 'code': 400})


# 数据校验模型
class UserIn(BaseModel):
    user_name: str
    password: str
    telephone: str

    @field_validator('user_name')
    def name_validator(cls, value):
        assert len(value) > 3, 'name length must more than 3'
        return value

    @field_validator('password')
    def pwd_validator(cls, value):
        assert len(value) > 5, 'password length must more than 5'
        return value

    @field_validator('telephone')
    def tel_validator(cls, value):
        assert len(value) == 11, 'telephone length must be 11'
        return value


@user.post('/', description='创建用户')
async def create_user(user_in: UserIn):
    # 方式1
    # usr = User(user_name=user_in.user_name, password=user_in.password, telephone=user_in.telephone)
    # await usr.save()  #

    try:
        # 方式2
        num = await User.filter(user_name=user_in.user_name).count()
        if num > 0:
            return JSONResponse(status_code=200, content={'message': 'user exist', 'code': 400})
        usr = await User.create(user_name=user_in.user_name, password=user_in.password, telephone=user_in.telephone)
        usr_out = {'user_name': usr.user_name, 'id': usr.id, 'telephone': usr.telephone}
        return JSONResponse(status_code=200, content={'message': 'register success', 'code': 200, 'user': usr_out})
    except:
        return JSONResponse(status_code=200, content={'message': 'register fail', 'code': 400})


@user.put('/{user_id}', description='修改用户')
async def update_user(user_id: int, user_in: UserIn):

    try:
        data = user_in.dict()
        result = await User.filter(id=user_id).update(**data)
        if result == 1:
            usr = await User.get(id=user_id)
            usr_out = {'user_name': usr.user_name, 'id': usr.id, 'telephone': usr.telephone, 'password': usr.password}
            return JSONResponse(status_code=200, content={'message': 'login success', 'code': 200, 'user': usr_out})
        else:
            return JSONResponse(status_code=200, content={'message': 'edit fail', 'code': 400})

    except Exception as e:
        return JSONResponse(status_code=200, content={'message': 'edit fail', 'code': 400})


@user.delete('/{user_id}', description='删除用户')
async def delete_user(user_id: int):
    result = await User.filter(id=user_id).delete()  # result 删除条数
    if not result:
        raise HTTPException(status_code=404, detail=f'主键为{user_id}的用户不存在')
    else:
        return {'message': 'delete success'}
