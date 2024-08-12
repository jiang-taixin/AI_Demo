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
            'models': ['ORM_Example.models', 'aerich.models'],
            'default_connection': 'default'
        }
    },
}
