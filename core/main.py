# -*- coding:utf-8 -*-
import os

from conf import settings
from libs.login import login
from core.manager import Manager
from libs.my_pickle import Mypickle

func_dic = {}


def make_route(num):
    def inner(fun):
        func_dic[num] = fun
    return inner


@make_route('1')
def manager():
    """
    管理员登录，从管理员对象的数据属性中展示可操作的选项，选择序号，使用getattr()映射到管理员类的具体函数属性上
    :return:
    """
    user = login('manager')
    if user and user['identity'] == 'manager':
        mana = Manager('admin')
        while True:
            for index, i in enumerate(mana.manager_dic,1):
                print('%s. %s'%(index,i[0]))
            num = input('num>>>:').strip()
            if num.isdigit() and int(num) > 0:
                try:
                    getattr(mana,mana.manager_dic[int(num)-1][1])()
                except Exception as e:
                    print(e)
                    print('\033[1;31m请输入正确的序号\033[0m')
            else:
                print('\033[1;31m请输入整数型序号\033[0m')


@make_route('2')
def teacher():
    """
    讲师登录，读取 teacher.pkl 展示讲师下的所有班级，选择班级，展示班级下的所有学生，选择学生序号，为某个学生修改成绩，
    找到班级里的某个学生，修改成绩，更新班级文件
    """
    user = login('teacher')
    if user and user['identity'] == 'teacher':
        print('%s 讲师登录: '%user['user'])
        teacher_name = user['user']
        teacher_path = Mypickle(settings.TEACHER_PATH)
        data = teacher_path.load()
        classes_dic = {}
        for i in data:
            if i.name == teacher_name:
                for index,j in enumerate(i.classes,1):
                    classes_dic[str(index)] = j
        print('讲师:%s 管理的班级有:' % teacher_name)
        for i in classes_dic:
            print('%s. %s'%(i,classes_dic[i]))
        num = input('num>>>:').strip()
        if num in classes_dic:
            classes_path = settings.CLASSES_PATH
            class_temp_path = os.path.join(classes_path,classes_dic[num]+'.pkl')  # 去班级文件里面查找 班级信息
            class_path = Mypickle(class_temp_path)
            data = class_path.load()
            print('班级里的学生有:')
            score_dic = {}
            for i in data:
                if i.teacher == teacher_name:
                    for index,j in enumerate(i.student,1):
                        print('%s. student_name: %s  score: %s'%(index,j.name,j.score))
                        score_dic[str(index)] = j.name  # 把课程的对象 存起来
            print('选择序号为学员修改成绩:')
            score_num = input('num>>>:').strip()
            if score_num in score_dic:
                student_name=  score_dic[score_num]
                new_score = input('new_score>>>:').strip()
                class_obj = None
                again_data = class_path.load()
                for k in again_data:
                    if k.teacher == teacher_name:
                        for m in k.student:
                            if m.name == student_name:
                                m.score = new_score    # 把新的成绩赋值 给对象
                                class_obj = k
                class_path.edit(class_obj)
                print('修改学员: %s 成绩成功'%student_name)
                print('end'.center(20,'-'))
            else:
                print('\033[1;31m选择的序号不存在\033[0m')
        else:
            print('\033[1;31m选择的班级不存在\033[0m')


@make_route('3')
def student():
    """
    学员登录，读取 student.pkl 文件 知道班级名，查找班级文件 读取学员的成绩
    """
    user = login('student')
    if user and user['identity'] == 'student':
        print('%s 学员登录：'%user['user'])
        student_name = user['user']
        student_path = Mypickle(settings.STUDENT_PATH)
        data = student_path.load()
        class_name = None
        for i in data:
            if i.name == student_name:
                class_name = i.classes
        print('学员:%s 班级是:%s' % (student_name,class_name))
        if class_name != None:
            classes_path = settings.CLASSES_PATH
            class_temp_path = os.path.join(classes_path, class_name + '.pkl')  # 去班级文件里面查找 班级信息
            class_path = Mypickle(class_temp_path)
            data = class_path.load()
            for i in data:
                for j in i.student:
                    if j.name == student_name:
                        print('student_name: %s  score: %s' %(j.name,j.score))
            print('end'.center(20,'-'))


@make_route('4')
def register_student():
    print('欢迎注册'.center(20,'-'))  # 学费默认都交了 O(∩_∩)O
    mana = Manager('admin')
    mana.create_student()


@make_route('5')
def quit_fun():
    quit('bye bye')


def run():
    msg = '''
    1.管理员登录 
    2.讲师登录 
    3.学员登录 
    4.学员注册 
    5.退出 
    '''
    while True:
        print(msg)
        num = input('num>>>:').strip()
        if num in func_dic:
            func_dic[num]()
        else:
            print('\033[1;31m请重新输入正确的序号！\033[0m')