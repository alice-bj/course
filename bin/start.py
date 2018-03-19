# -*- coding:utf-8 -*-
from os import path
from sys import path as sys_path

BASE_DIR = path.dirname(path.dirname(path.abspath(__file__)))
sys_path.append(BASE_DIR)

from db.manager import Manager
from core import main

if __name__ == "__main__":
    main.run()