# -*- coding:utf-8 -*-
import os
import random
import string

from conf import settings
from libs.my_pickle import Mypickle


class Classes:
    def __init__(self,name,class_time,school_name,course_name):
        self.name = ''.join(random.sample(string.ascii_letters,3))+'_'+name
        self.time = class_time
        self.school = school_name
        self.course = course_name
        self.teacher = None  # 一个班级 一个老师
        self.student = []   # student对象


class Course:
    def __init__(self,name,price,period):
        self.name = name
        self.price = price
        self.period = period
        self.classes = []  # classes 名称

    def create_classes(self,school_obj):
        """
        输入：班级名，开课时间，创建班级，将班级对象存到一个以班级名命名的文件中 eg:fdj_py_1.pkl  输入py_1 生成 fdj_py_1 为了唯一性
        创建成功后，更新 school.pkl 文件，生成班级名命名的文件
        :param school_obj: 学校对象
        :return:
        """
        print('学校：%s  课程：%s -->正在创建班级：'%(school_obj.name,self.name))
        name = input('classes_name:').strip()
        class_time = input('classes_time(开课时间):').strip()
        class_obj=Classes(name,class_time,school_obj.name,self.name)
        self.classes.append(class_obj.name)
        Mypickle(settings.SCHOOL_PATH).edit(school_obj)  # 更新school.pkl
        class_path = os.path.join(settings.CLASSES_PATH,class_obj.name+'.pkl')
        Mypickle(class_path).dump(class_obj)
        print('创建成功'.center(30, '-'))


class School:
    def __init__(self,name):
        self.name = name
        self.course = []  # course对象

    def create_course(self):
        """
        输入：课程名，价钱，周期，创建课程，将课程对象存到文件 school.pkl 学校对象中
        创建成功后，更新 school.pkl 文件
        """
        print('%s -->正在创建课程：'%self.name)
        name = input('course_name：').strip()
        price = input('course_price：').strip()
        period = input('course_period：').strip()
        cour = Course(name,price,period)
        self.course.append(cour)
        Mypickle(settings.SCHOOL_PATH).edit(self)
        print('创建成功'.center(30, '-'))