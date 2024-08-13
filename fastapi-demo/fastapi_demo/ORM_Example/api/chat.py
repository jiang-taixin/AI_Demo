import io
import json
import time
from typing import List

from fastapi import APIRouter, HTTPException
from fastapi import Request
from pydantic import BaseModel, field_validator
from fastapi.responses import JSONResponse, StreamingResponse
from ORM_Example.models import User, ChatRecord, MulTestModel

import random
from http import HTTPStatus
# 建议dashscope SDK 的版本 >= 1.14.0
from dashscope import Generation
import dashscope
dashscope.api_key = 'sk-efee0fffd69a433c918c5bea4183056c'

chat = APIRouter()


@chat.get('/chat_list', description='获取对话列表')
async def get_chat_list():
    # user__user_name  user一对多属性名 __关联对象属性名
    chats = await ChatRecord.all().values('request_id', 'user__user_name', 'mul__name')
    return chats


@chat.get('/{chat_id}', description='通过id获取对话')
async def get_chat(chat_id: int):
    chat_record = await ChatRecord.get(id=chat_id)

    # 一对多查询
    print(await chat_record.user.values('user_name'))
    # 多对多查询
    print(await chat_record.mul.all().values('name'))

    return chat_record


class ChatData(BaseModel):
    content: str


async def get_chat_message(user_id: int, question: ChatData):
    messages = [{'role': 'user', 'content': question.content}]
    responses = Generation.call(
        model="qwen-max",
        messages=messages,
        result_format='message',
        stream=True,
        incremental_output=True)
    input_tokens = 0
    output_tokens = 0
    total_tokens = 0
    request_id = ''
    for response in responses:
        if response.status_code == HTTPStatus.OK:
            print(f'input: {response.usage.input_tokens}, output: {response.usage.output_tokens}, total :{response.usage.total_tokens}')
            input_tokens = response.usage.input_tokens
            output_tokens = response.usage.output_tokens
            total_tokens = response.usage.total_tokens
            request_id = response.request_id
            yield response.output.choices[0].message.content
        else:
            pass
    await ChatRecord.create(request_id=request_id,
                            input_tokens=input_tokens,
                            output_tokens=output_tokens,
                            total_tokens=total_tokens,
                            user_id=user_id)  # 一对多关系绑定


@chat.post('/get_chat/{user_id}', description='用通义进行对话')
async def start_chat(user_id: int, question: ChatData):
    # 流式输出
    # return StreamingResponse(get_chat_message(user_id, question), media_type='text/plain')

    messages = [{'role': 'user', 'content': question.content}]
    response = Generation.call(model="qwen-max",
                               messages=messages,
                               # 设置随机数种子seed，如果没有设置，则随机数种子默认为1234
                               seed=random.randint(1, 10000),
                               temperature=0.8,
                               top_p=0.8,
                               top_k=50,
                               # 将输出设置为"message"格式
                               result_format='message')
    if response.status_code == HTTPStatus.OK:
        print(response.output.choices[0].message.content)
        await ChatRecord.create(request_id=response.request_id,
                                input_tokens=response.usage.input_tokens,
                                output_tokens=response.usage.output_tokens,
                                total_tokens=response.usage.total_tokens,
                                user_id=user_id)  # 一对多关系绑定
        data = {'content': response.output.choices[0].message.content}
        return JSONResponse(status_code=200, content={'message': 'success', 'code': 200, 'output': data})
    else:
        return JSONResponse(status_code=200, content={'message': 'fail', 'code': 200})


class ChatIn(BaseModel):
    request_id: str
    input_tokens: int
    output_tokens: int
    total_tokens: int
    user_id: str
    mul: List[int]


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


@chat.put('/{chat_id}', description='修改对话')
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


@chat.delete('/{chat_id}', description='删除对话')
async def delete_chat(chat_id: int):
    result = await ChatRecord.filter(id=chat_id).delete()
    # 多对多关联不用删除    会自动删除
    if not result:
        return HTTPException(status_code=404, detail=f'主键为{chat_id}的对话记录不存在')
    else:
        return {'message': 'delete success'}
