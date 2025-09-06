# -*- coding:utf-8 -*-
# AUTHOR: Sun

from os import name, getenv

def set_constant[T](env_name: str, default: T) -> T:
    if name =='nt':
        return default
    elif name == 'posix':
        return getenv(env_name)
    else:
        raise Exception('Unsupported OS')

USERNAME = set_constant('USERNAME', 'root')
PASSWORD = set_constant('PASSWORD', '123456')
HOST = set_constant('HOST', 'localhost')
PORT = set_constant('PORT', '3306')

DB_URI: str = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/anime'

ENABLE_INNER_PICTURE: str = set_constant('ENABLE_INNER_PICTURE', 'true')
if ENABLE_INNER_PICTURE.lower() == 'true':
    ENABLE_INNER_PICTURE: bool = True
elif ENABLE_INNER_PICTURE.lower() == 'false':
    ENABLE_INNER_PICTURE: bool = False
else:
    raise Exception('Invalid value for ENABLE_INNER_PICTURE')

PICTURE_PATH: str = set_constant('PICTURE_PATH', 'picture')


if __name__ == '__main__':
    pass
