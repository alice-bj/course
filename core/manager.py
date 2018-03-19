# -*- coding:utf-8 -*-
import os

from libs import salt
from conf import settings
from core.school import School
from core.teacher import Teacher
from core.student import Student
from libs.my_pickle import Mypickle


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
        """
        创建学校
        输入学校名称 eg:luffy_shanghai
        利用：Mypickle 存到school.pkl 文件中
        """
        school_name = input('school_name>>>:').strip()
        sch = School(school_name)
        self.school_path.dump(sch)
        print('创建学校成功'.center(30,'-'))

    def choice_school(self):
        """
        选择学校
        读取 school.pkl 文件，显示学校列表，供用户选择学校
        :return: 用户选择学校的序号，学校对象，学校下所有课程对象的集合列表
        """
        data = self.school_path.load()
        num_school_dic = {}
        num_course_dic = {}
        for index, i in enumerate(data,1):
            print('%s. %s'%(index,i.name))
            num_school_dic[str(index)]  = i
            # i.course 学校下的所有课程对象的列表
            num_course_dic[str(index)] = i.course
        choice_school_num = input('先选择学校 num>>>:').strip()
        return choice_school_num,num_school_dic,num_course_dic

    def choice_course(self):
        """
        选择课程
        选好学校之后，展示学校下的所有课程，供用户选择课程
        :return:用户选择的课程序号，课程对象，用户选择的学校序号，学校对象
        """
        choice_school_num, school_obj, course_obj = self.choice_school()
        num_course_dic = {}
        if choice_school_num in course_obj:
            for index, i in enumerate(course_obj[choice_school_num], 1):
                print('%s. %s' % (index, i.name))
                num_course_dic[str(index)] = i
            choice_course_num = input('再选择课程 num>>:').strip()
            return choice_course_num, num_course_dic, choice_school_num, school_obj
        else:
            print('\033[1;31m选择的学校不存在\033[0m')

    def choice_classes(self):
        """
        选择班级
        选好课程之后，展示课程下的所有班级，供用户选择班级
        :return: 班级对象，班级路径
        """
        choice_course_num, num_course_dic, choice_school_num, school_obj = self.choice_course()
        num_classes_dic = {}
        if choice_course_num in num_course_dic:
            for index, i in enumerate(num_course_dic[choice_course_num].classes, 1):
                print('%s. %s' % (index, i))
                num_classes_dic[str(index)] = i
            choice_class_num = input('最后选择班级 num>>:').strip()
            if choice_class_num in num_classes_dic:  # 拿到 班级名 找到对象 修改
                print(num_classes_dic[choice_class_num])  # 班级名
                # 根据班级名 拼接班级文件存放的路径 读取班级文件
                class_path = os.path.join(self.classes_path, num_classes_dic[choice_class_num] + '.pkl')
                class_obj = Mypickle(class_path).load()
                return class_obj, class_path
            else:
                print('\033[1;31m选择的班级不存在\033[0m')
        else:
            print('\033[1;31m选择的课程不存在\033[0m')

    def create_course(self):
        """
        创建课程
        展示学校列表，选择具体在哪一个学校下创建课程，利用学校对象去创建课程
        """
        choice_school_num, school_obj, course_obj = self.choice_school()
        if choice_school_num in school_obj:
            school_obj[choice_school_num].create_course()
        else:
            print('\033[1;31m选择的学校不存在\033[0m')

    def create_classes(self):
        """
        创建班级
        展示学校，选择，展示学校下的课程，再选择，选择具体在哪一个课程下创建班级，利用课程对象去创建班级
        """
        choice_course_num, num_course_dic, choice_school_num, school_obj = self.choice_course()
        if choice_course_num in num_course_dic:
            num_course_dic[choice_course_num].create_classes(school_obj[choice_school_num])  # 需要把学校对象传进去
        else:
            print('\033[1;31m选择的课程不存在\033[0m')

    def common_school_course_classes(self):
        """
        所有学校，学校下的课程，课程下的所有班级
        :return: 字典形式的所有班级名
        """
        classes_dic = {}
        data = self.school_path.load()
        for school_index, i in enumerate(data,1):
            if len(i.course) > 0:
                print('%s. %s' % (school_index, i.name))
                for course_index, j in enumerate(i.course,1):
                    print('%4s.%s. %s - %s - %s'%(school_index,course_index,j.name,j.price,j.period))
                    if len(j.classes) > 0:
                        for class_index,k in enumerate(j.classes,1):
                            print('%8s.%s.%s  班级：%s'%(school_index,course_index,class_index,k))
                            classes_dic['%s.%s.%s'%(str(school_index),str(course_index),str(class_index))] = k
            else:
                print('%s. %s'%(school_index,i.name))
        return classes_dic

    def show_school_course_classes(self):
        """
        展示学校/课程/班级
        展示所有学校，学校下的课程，课程下的所有班级
        """
        self.common_school_course_classes()
        print('end'.center(20, '-'))

    def show_detail_classes(self):
        """
        查看班级的详细信息
        展示学校，课程，班级，选择班级，展示班级下的详细信息
        """
        classes_dic = self.common_school_course_classes()
        class_num = input('选择班级eg:(1.1.1) num>>>:').strip()
        if class_num in classes_dic:
            print('班级:%s' % (classes_dic[class_num]))
            class_name = classes_dic[class_num]
            # 根据班级名 拼接班级文件的路径
            class_path = os.path.join(self.classes_path, class_name + '.pkl')
            if os.path.isfile(class_path):
                class_obj = Mypickle(class_path).load()
                for i in class_obj:
                    print(i.__dict__)
        else:
            print('\033[1;31m选择的班级不存在\033[0m')

    def create_teacher(self):
        """
        创建讲师
        输入讲师的名称，
        1.讲师对象存到 userinfo.pkl 用来登录判断
        2.讲师对象存到 teacher.pkl 用来后续使用 eg:添加班级  一个讲师可以有多个班级
        """
        password_salt = salt.create_salt()
        name = input('teacher_name>>>:').strip()
        tea = Teacher(name,password_salt)
        self.userinfo_path.dump(tea)
        self.teacher_path.dump(tea)
        print('讲师:%s 创建成功'.center(30, '-')%name)

    def bound_classes_teacher(self):
        """
        为讲师绑定班级
        读取 teacher_path.pkl 文件，列出所有讲师列表，供管理员选择为哪个讲师指定班级
        如果，班级已经绑定过讲师，不允许再次绑定其他讲师
        绑定成功后，更新 teacher.pkl 文件 和 class.pkl. 文件
        """
        tea_data = self.teacher_path.load()
        data = {}
        for index,i in enumerate(tea_data,1):
            print('%s. %s'%(index,i.name))
            data[str(index)] = i
        print('-----为讲师指定班级-----')
        tea_num = input('先选择讲师 num>>>:').strip()
        if tea_num in data:
            print('讲师:%s 正在分配班级'%data[tea_num].name)
            classes_dic = self.common_school_course_classes()
            class_num = input('再选择班级eg:(1.1.1) num>>>:').strip()
            if class_num in classes_dic:
                print('讲师:%s 班级:%s'%(data[tea_num].name,classes_dic[class_num]))  # 这里得到 讲师对象 和 班级名称
                teacher_obj,class_name = data[tea_num],classes_dic[class_num]
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
            else:
                print('\033[1;31m选择的班级不存在\033[0m')
        else:
            print('\033[1;31m选择的讲师不存在\033[0m')

    def create_student(self):
        """
        创建学员
        输入学员的名称，
        1.学员对象存到 userinfo.pkl 用来登录判断
        2.学员对象存到 student.pkl  用来使用 eg:添加班级  一个学员一个班级
        学员指定班级后，更新 student.pkl 文件 和 class.pkl. 文件
        """
        password_salt = salt.create_salt()
        name = input('student_name>>>:').strip()
        stu = Student(name,password_salt)
        self.userinfo_path.dump(stu) # 先把学员的 账号 密码 存起来
        self.student_path.dump(stu)  # 生成学员的文件
        print('-----为学员指定班级-----')
        classes_dic = self.common_school_course_classes()
        class_num = input('再选择班级eg:(1.1.1) num>>>:').strip()
        if class_num in classes_dic:
            print('学员:%s 班级:%s' % (name, classes_dic[class_num]))  # 这里得到 讲师对象 和 班级名称
            student_obj, class_name = stu, classes_dic[class_num]
            student_obj.classes = class_name
            class_path = os.path.join(self.classes_path, class_name + '.pkl')
            if os.path.isfile(class_path):
                class_obj = Mypickle(class_path).load()
                class_temp_obj = None
                for i in class_obj:
                    i.student.append(student_obj)
                    class_temp_obj = i
                Mypickle(class_path).edit(class_temp_obj)  # 更新了班级文件
                self.student_path.edit(student_obj)  # 更新了学生文件  这里应该 在创建学员时 就先生成文件
                print('创建学员:%s 成功'.center(20, '-')%student_obj.name)
        else:
            print('\033[1;31m选择的班级不存在\033[0m')

    def show_teacher(self):
        """
        查看讲师
        展示所有讲师的详细信息，所带的班级...
        """
        data = self.teacher_path.load()
        for i in data:
            print(i.__dict__)

    def show_student(self):
        """
        查看学员
        展示所有学员详细信息，班级，成绩...
        """
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