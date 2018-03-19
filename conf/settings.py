# -*- coding:utf-8 -*-
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

USERINFO_PATH = os.path.join(BASE_DIR, 'db', 'userinfo.pkl')
SCHOOL_PATH = os.path.join(BASE_DIR, 'db', 'school.pkl')
CLASSES_PATH = os.path.join(BASE_DIR, 'db', 'classes')
TEACHER_PATH = os.path.join(BASE_DIR, 'db', 'teacher.pkl')
STUDENT_PATH = os.path.join(BASE_DIR, 'db', 'student.pkl')