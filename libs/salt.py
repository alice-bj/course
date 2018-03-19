# -*- coding:utf-8 -*-
import random
import string


def create_salt():
    password_salt = ''.join(random.sample(string.ascii_letters + string.digits, 6))
    return password_salt