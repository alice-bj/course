# -*- coding:utf-8 -*-
import os
import pickle
import random
import string
import hashlib

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANAGER_PATH = os.path.join(BASE_DIR, 'db', 'userinfo.pkl')

password_salt = ''.join(random.sample(string.ascii_letters + string.digits, 6))

class Manager:
    def __init__(self,password_salt):
        self.name = 'admin'
        self.password = hashlib.md5(('123'+password_salt).encode('utf-8')).hexdigest()
        self.salt = password_salt
        self.identity = 'manager'

# admin = Manager(password_salt)
# print(MANAGER_PATH)
# with open(MANAGER_PATH, 'wb') as f:
#     pickle.dump(admin, f)