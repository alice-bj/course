# -*- coding:utf-8 -*-
import os
import random
import string
from conf import settings
from libs.my_pickle import Mypickle


class Classes:
    def __init__(self,name,time,school_name,course_name):
        self.name = ''.join(random.sample(string.ascii_letters,3))+'_'+name
        self.time = time
        self.school = school_name
        self.course = course_name
        self.teacher = None  # 一个班级 一个老师
        self.student = []  # student对象


class Course:
    def __init__(self,name,price,period):
        self.name = name
        self.price = price
        self.period = period
        self.classes = []  # classes 名称

    def create_classes(self,school_obj):
        print('学校：%s  课程：%s -->正在创建班级：'%(school_obj.name,self.name))
        name = input('classes_name:').strip()
        time = input('classes_time(开课时间):').strip()
        class_obj=Classes(name,time,school_obj.name,self.name)
        self.classes.append(class_obj.name)
        Mypickle(settings.SCHOOL_PATH).edit(school_obj)  # 更新school.pkl
        class_path = os.path.join(settings.CLASSES_PATH,class_obj.name+'.pkl')
        Mypickle(class_path).dump(class_obj)
        print('创建成功'.center(30, '-'))


class School:
    def __init__(self,name):
        self.name = name
        self.course = [] # course对象

    def create_course(self):
        print('%s -->正在创建课程：'%self.name)
        name = input('course_name：').strip()
        price = input('course_price：').strip()
        period = input('course_period：').strip()
        cour = Course(name,price,period)
        self.course.append(cour)
        Mypickle(settings.SCHOOL_PATH).edit(self)
        print('创建成功'.center(30, '-'))