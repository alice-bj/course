# -*- coding:utf-8 -*-
import os
import hashlib
from conf import settings
from libs.my_pickle import Mypickle


def login(type):
    while True:
        username = input('username>>>:').strip()
        password = input('password>>>:').strip()
        path = settings.USERINFO_PATH
        if os.path.isfile(path):
            data = Mypickle(path).load()
            for i in data:
                if i.identity == type:
                    if i.name == username:
                        if i.password == hashlib.md5((password+i.salt).encode('utf-8')).hexdigest():
                            print('welcome'.center(20,'-'))
                            return {'user':username,'identity':i.identity}
                        else:
                            print('\033[1;31m密码有误\033[0m')
                            break
        else:
            print('\033[1;31m不存在该文件\033[0m')