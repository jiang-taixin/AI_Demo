from tortoise.models import Model
from tortoise import fields
from pydantic import BaseModel


class BaseModel(Model):
    create_time = fields.DatetimeField(auto_now_add=True, null=True)
    update_time = fields.DatetimeField(auto_now=True, null=True)


class User(BaseModel):
    id = fields.IntField(pk=True, description='用户ID')
    user_name = fields.CharField(max_length=32, description='用户名')
    password = fields.CharField(max_length=32, description='密码')
    telephone = fields.CharField(max_length=15, description='手机号')


class MulTestModel(BaseModel):    # 任意创建一个模型测试多对多
    id = fields.IntField(pk=True, description='ID')
    name = fields.CharField(max_length=255, description='名称')
    # 修改数据表测试 default=''
    comment = fields.CharField(max_length=255, description='备注', default='')


class ChatRecord(BaseModel):
    id = fields.IntField(pk=True, description='对话ID')
    request_id = fields.CharField(max_length=40, description=' 请求ID')
    input_tokens = fields.IntField(description='Input Tokens')
    output_tokens = fields.IntField(description='Output Tokens')
    total_tokens = fields.IntField(description='Total Tokens')

    # 一对多的关系 related_name反向查询关联   一个user对应多个chat  在表里生成user_id字段
    user = fields.ForeignKeyField('models.User', related_name='chats')
    # 多对多关系  生成多对多表
    mul = fields.ManyToManyField('models.MulTestModel', related_name='chats', description='测试多对多')
