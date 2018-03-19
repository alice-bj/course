# -*- coding:utf-8 -*-
import hashlib


class Teacher:
    def __init__(self,name,salt):
        self.name = name
        self.password = hashlib.md5(('123'+salt).encode('utf-8')).hexdigest()  # 123
        self.salt = salt
        self.identity = 'teacher'
        self.classes = []   # 班级名 列表