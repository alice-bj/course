角色:学校、学员、课程、讲师
要求:
1. 创建北京、上海 2 所学校
2. 创建linux , python , go 3个课程 ， linux\py 在北京开， go 在上海开
3. 课程包含，周期，价格，通过学校创建课程
4. 通过学校创建班级， 班级关联课程、讲师
5. 创建学员时，选择学校，关联班级
5. 创建讲师角色时要关联学校，
6. 提供两个角色接口
    6.1 学员视图， 可以注册， 交学费， 选择班级，
    6.2 讲师视图， 讲师可管理自己的班级， 上课时选择班级，查看班级学员列表 ， 修改所管理的学员的成绩
    6.3 管理视图，创建讲师， 创建班级，创建课程
7. 上面的操作产生的数据都通过pickle序列化保存到文件里 

------------------------------------------------------
结构说明：
course_sys
    bin
        start.py        启动文件
    conf
        settings.py     配置文件
    core
        main.py         主模块
        manager.py      管理员类
        school.py       学校类 课程类 班级类
        student.py      学员类
        teacher.py      讲师类
    db
        classes         班级对象 一个对象 一个文件 唯一 
            fdj_py_1.pkl      
            OhX_go_1.pkl
            TVB_linux_2.pkl
            zPX_linux_1.pkl      
        manager.py      用来生成 初始的管理员
        school.pkl      学校对象的集合   
        student.pkl     学员对象的集合  
        teacher.pkl     讲师对象的集合
        userinfo.pkl    用来生成 管理员 讲师 学员 的登录文件  
    libs
        login.py        公用的登录模块   
        my_pickle.py    公用的pickle处理模块 
    course_sys.png      选课系统的 UML 图  
    README   

------------------------------------------------------
学校课程班级的关系: 
1. luffy_beijing
   1.1. linux - 4000 - 3mons
       1.1.1  班级：zPX_linux_1
       1.1.2  班级：TVB_linux_2
   1.2. python - 5000 - 8monx
       1.2.1  班级：fdj_py_1
2. luffy_shanghai
   2.1. go - 9000 - 9mons
       2.1.1  班级：OhX_go_1
3. luffy_shanxi

------------------------------------------------------
用户:
    管理员: admin 123   
    讲师: alex 123   egon 123 
    学员: alice 123  lily 123  alice_a 123  lily_a 123   