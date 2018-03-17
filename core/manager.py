# -*- coding:utf-8 -*-
import os
import random
import string
from core.school import School
from core.teacher import Teacher
from core.student import Student
from libs.my_pickle import Mypickle
from conf import settings


class Manager:
    manager_dic = [('创建学校','create_school'),('创建课程','create_course'),('创建班级','create_classes'),
                   ('展示学校/课程/班级', 'show_school_course_classes'),('查看班级的详细信息','show_detail_classes'),
                   ('创建讲师','create_teacher'),('为讲师绑定班级','bound_classes_teacher'),('创建学员','create_student'),
                   ('查看讲师','show_teacher'),('查看学员','show_student'),('退出','quit_fun')]

    def __init__(self,name):
        self.name = name
        self.userinfo_path = Mypickle(settings.USERINFO_PATH)
        self.school_path = Mypickle(settings.SCHOOL_PATH)
        self.classes_path = settings.CLASSES_PATH
        self.teacher_path = Mypickle(settings.TEACHER_PATH)
        self.student_path = Mypickle(settings.STUDENT_PATH)

    def create_school(self):
        # 创建学校
        school_name = input('school_name>>>:').strip()
        sch = School(school_name)
        self.school_path.dump(sch)
        print('创建成功'.center(30,'-'))

    def choice_school(self):
        # 选择学校
        data = self.school_path.load()
        num_school_dic = {}
        num_course_dic = {}
        for index, i in enumerate(data,1):
            print('%s. %s'%(index,i.name))
            num_school_dic[str(index)]  = i
            num_course_dic[str(index)] = i.course
        num = input('先选择学校 num>>>:').strip()
        return num,num_school_dic,num_course_dic

    def choice_course(self):
        # 选择课程
        num, school_obj, course_obj = self.choice_school()
        num_course_dic = {}
        if num in course_obj:
            for index, i in enumerate(course_obj[num], 1):
                print('%s. %s' % (index, i.name))
                num_course_dic[str(index)] = i
        num2 = input('再选择课程 num>>:').strip()
        return num2,num_course_dic,num,school_obj

    def choice_classes(self):
        # 选择班级
        num2, num_course_dic, num, school_obj = self.choice_course()
        num_classes_dic = {}
        if num2 in num_course_dic:
            for index, i in enumerate(num_course_dic[num2].classes, 1):
                print('%s. %s' % (index, i))
                num_classes_dic[str(index)] = i
        num3 = input('最后选择班级 num>>:').strip()
        if num3 in num_classes_dic:  # 拿到 班级名 找到对象 修改
            print(num_classes_dic[num3])  # 班级名
            class_path = os.path.join(self.classes_path, num_classes_dic[num3] + '.pkl')
            class_obj = Mypickle(class_path).load()
            return class_obj,class_path

    def create_course(self):
        # 创建课程
        num,school_obj,course_obj = self.choice_school()
        if num in school_obj:
            school_obj[num].create_course()

    def create_classes(self):
        # 创建班级
        num2, num_course_dic, num, school_obj = self.choice_course()
        if num2 in num_course_dic:
            num_course_dic[num2].create_classes(school_obj[num])  # 需要把学校对象传进去

    def common_school_course_classes(self):
        # 展示学校 课程 班级 的列表 并返回班级 列表
        classes_dic = {}
        data = self.school_path.load()
        for index, i in enumerate(data,1):
            if len(i.course) > 0:
                print('%s. %s' % (index, i.name))
                for index1, j in enumerate(i.course,1):
                    print('%4s.%s. %s - %s - %s'%(index,index1,j.name,j.price,j.period))
                    if len(j.classes) > 0:
                        for index2,k in enumerate(j.classes,1):
                            print('%8s.%s.%s  班级：%s'%(index,index1,index2,k))
                            classes_dic['%s.%s.%s'%(str(index),str(index1),str(index2))] = k
            else:
                print('%s. %s'%(index,i.name))
        return classes_dic

    def show_school_course_classes(self):
        # 展示学校及课程和班级
        self.common_school_course_classes()
        print('end'.center(20, '-'))

    def show_detail_classes(self):
        # 查看班级的详细信息
        classes_dic = self.common_school_course_classes()
        class_num2 = input('选择班级eg:(1.1.1) num>>>:').strip()
        if class_num2 in classes_dic:
            print('班级:%s' % (classes_dic[class_num2]))
            class_name = classes_dic[class_num2]
            class_path = os.path.join(self.classes_path, class_name + '.pkl')
            if os.path.isfile(class_path):
                class_obj = Mypickle(class_path).load()
                for i in class_obj:
                    print(i.__dict__)

    def create_teacher(self):
        # 创建讲师
        salt = ''.join(random.sample(string.ascii_letters + string.digits, 6))
        name = input('teacher_name>>>:').strip()
        tea = Teacher(name,salt)
        self.userinfo_path.dump(tea)  # 先把讲师的 账号 密码 存起来
        self.teacher_path.dump(tea)  # 生成老师的文件
        print('讲师:%s 创建成功'.center(30, '-')%name)

    def bound_classes_teacher(self):
        # 为讲师绑定多个班级
        tea_data = self.teacher_path.load()
        data = {}
        for index,i in enumerate(tea_data,1):
            print('%s. %s'%(index,i.name))
            data[str(index)] = i
        print('-----为讲师指定班级-----')
        num = input('先选择讲师 num>>>:').strip()
        if num in data:
            print('讲师:%s 正在分配班级'%data[num].name)
            classes_dic = self.common_school_course_classes()
            class_num2 = input('再选择班级eg:(1.1.1) num>>>:').strip()
            if class_num2 in classes_dic:
                print('讲师:%s 班级:%s'%(data[num].name,classes_dic[class_num2]))  # 这里得到 讲师对象 和 班级名称
                teacher_obj,class_name = data[num],classes_dic[class_num2]
                # teacher_obj.classes.append(class_name)
                # self.teacher_path.edit(teacher_obj)  # 更新了老师文件  这里应该 在创建讲师时 就先生成文件
                class_path = os.path.join(self.classes_path,class_name+'.pkl')
                if os.path.isfile(class_path):
                    class_obj = Mypickle(class_path).load()
                    class_temp_obj = None
                    temp_teacher = None
                    for i in class_obj:
                        if i.teacher == None:  # 如果已经绑定过 不允许再次绑定
                            i.teacher = teacher_obj.name
                            class_temp_obj = i
                        else:
                            temp_teacher = i.teacher
                    if class_temp_obj != None:
                        teacher_obj.classes.append(class_name)
                        self.teacher_path.edit(teacher_obj)  # 更新了老师文件  这里应该 在创建讲师时 就先生成文件
                        Mypickle(class_path).edit(class_temp_obj)  # 更新了班级文件
                        print('绑定成功'.center(20, '-'))
                    else:
                        print('绑定失败,已经绑定了讲师 %s'%temp_teacher)

    def create_student(self):
        # 创建学员
        salt = ''.join(random.sample(string.ascii_letters + string.digits, 6))
        name = input('student_name>>>:').strip()
        stu = Student(name,salt)
        self.userinfo_path.dump(stu) # 先把学员的 账号 密码 存起来
        self.student_path.dump(stu)  # 生成学员的文件
        print('-----为学员指定班级-----')
        classes_dic = self.common_school_course_classes()
        class_num2 = input('再选择班级eg:(1.1.1) num>>>:').strip()
        if class_num2 in classes_dic:
            print('学员:%s 班级:%s' % (name, classes_dic[class_num2]))  # 这里得到 讲师对象 和 班级名称
            student_obj, class_name = stu, classes_dic[class_num2]
            student_obj.classes = class_name
            class_path = os.path.join(self.classes_path, class_name + '.pkl')
            if os.path.isfile(class_path):
                class_obj = Mypickle(class_path).load()
                class_temp_obj = None
                for i in class_obj:
                    i.student.append(student_obj)
                    class_temp_obj = i
                Mypickle(class_path).edit(class_temp_obj)  # 更新了班级文件
                self.student_path.edit(student_obj)  # 更新了学生文件  这里应该 在创建讲师时 就先生成文件

                print('创建学员:%s 成功'.center(20, '-')%student_obj.name)

    def show_teacher(self):
        # 展示讲师
        data = self.teacher_path.load()
        for i in data:
            print(i.__dict__)

    def show_student(self):
        # 展示学员
        data = self.student_path.load()
        class_temp_name = []
        for i in data:
            class_name = i.classes
            class_temp_name.append(class_name)
        set_class_name = set(class_temp_name)  # 学生的班级名 会重名 需要集合过滤
        for i in set_class_name:
            class_path = os.path.join(self.classes_path,i+'.pkl')
            data = Mypickle(class_path).load()
            for i in data:
                for j in i.student:
                    print(j.__dict__)

    @staticmethod
    def quit_fun():
        quit('bye bye...')