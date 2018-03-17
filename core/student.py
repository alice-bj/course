# -*- coding:utf-8 -*-
import hashlib


class Student:
    def __init__(self,name,salt):
        self.name = name
        self.password = hashlib.md5(('123'+salt).encode('utf-8')).hexdigest()  # 123
        self.salt = salt
        self.identity = 'student'
        self.score = '0'
        self.classes = None