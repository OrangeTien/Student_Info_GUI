# Student_Info_Demo.py
# 此文件是对学生管理系统GUI界面的一个简单演示

from tkinter import *
from tkinter.ttk import *
from tkinter.messagebox import *
import pymysql
# import tkinter as tk
# from tkinter import ttk
# from tkinter.ttk import *
# from nltk.tag import str2tuple
# import os
# from PIL import Image, ImageTk


# 部署GUI界面

# 1.设置窗口对象
window = Tk()
window.geometry("920x680+200+100")
window.title('Student_Info')
window.resizable(0,0)
window["bg"]="Coral" # 珊瑚色 Coral

# 2.设置最上面的图片,这个不是很好弄，先是要弄一张合适的图片，要去修改分辨率
# 905*115比较好
top_image = PhotoImage(file="imgs/mai2.png")
top_label = Label(window,image=top_image)
top_label.place(x=3,y=3)


# 3.设置容器 / 分区
# 此处采用 panedWindow 和 LabelFrame 容器控件
window.left_pane = PanedWindow(width=201,height=670)  # 这里是规定容器的长宽
window.right_pane = PanedWindow(width=702,height=670)
window.left_pane.place(x=5,y=125) # 这里是决定将这个容器放在哪个位置
window.right_pane.place(x=211,y=125) # 这个坐标应该指的是左上角的点的位置
window.right_top_frame = LabelFrame(window.right_pane,text="Please add student information here!",width = 650,height = 150)
window.right_top_frame.place(x = 14,y = 10) # 注意，这里的坐标是相对坐标，是相对于当前所属控件的坐标


# 4.设置若干按钮
# window.style_button = ttk.Style()
# window.style_button.configure('s_button',width=10,font=("Helvetica",17,"bold"))

window.button_show = Button(window,text=" SHOW ALL",width=10)
window.button_show.place(x = 40, y = 200)
window.button_best = Button(window,text="BEST STU",width=10)
window.button_best.place(x = 40 , y = 250 )
window.button_delete = Button(window,text="DELETE ONE",width=10,state=DISABLED)
window.button_delete.place(x = 40 , y = 300)
window.button_clear = Button(window,text="CLEAR ALL",width=10)
window.button_clear.place(x = 40 , y = 350)


# 5.在LabelFrame容器内设置若干控件
# 提前定义好相应变量，后面可以作为连接数据库的参数
sid = StringVar()
sname = StringVar()
cid = StringVar()
score = StringVar()

window.label_sid = Label(window.right_top_frame,text="Student No.")
window.label_sid.place(x = 5, y = 20)
window_input_sid = Entry(window.right_top_frame,width=16,textvariable=sid).place(x = 85, y = 18 )
# sid = window_input_sid.get()

window.label_sname = Label(window.right_top_frame,text="Student Name")
window.label_sname.place(x = 350, y = 20 )
window_input_sname = Entry(window.right_top_frame,width=16,textvariable=sname).place(x = 447, y = 18)
# Entry(window,textvariable=sid)
# sname = window_input_sname.get()
#

window.label_cid = Label(window.right_top_frame,text="Course No.")
window.label_cid.place(x = 5, y = 60 )
window_input_cid = Entry(window.right_top_frame,width=16,textvariable=cid).place(x = 85 , y = 58)
# cid = window_input_cid.get()
#

window.label_score = Label(window.right_top_frame,text="Score")
window.label_score.place(x = 350 , y = 60)
window_input_score = Entry(window.right_top_frame,width=16,textvariable=score).place(x = 447, y = 58 )
# score = window_input_score.get()

# window.button_append = Button(window.right_top_frame,width=10,text='ADD').place(x = 250, y = 95 )


# 6.添加 TreeView 控件
window.tree = Treeview(window.right_pane,show="headings",columns=("sid","sname","cid","score"),height=18)
window.tree.column("sid",width=100,anchor="center")
window.tree.column("sname",width=100,anchor="center")
window.tree.column("cid",width=80,anchor="center")
window.tree.column("score",width=80,anchor="center")

window.tree.heading("sid",text="Student No.")
window.tree.heading("sname",text="Student Name")
window.tree.heading("cid",text="Course No.")
window.tree.heading("score",text="Score")

window.tree.place(rely= 0.26, relwidth= 0.96 )
# .place(rely=0.3, relwidth=0.97)  .place(x=10,y=80)


# 至此，GUI界面设置完成

# 接下来需要对各个按钮进行逻辑实现

# 1.sql_query 是负责连接数据库并且执行一些简单操作的函数
def sql_query(sql):
    # query and return the result tuple

    conn = pymysql.connect(host='localhost', port=3306, user='root', password='12345678', database='Student_Info',
                           charset='utf8')
    cur = conn.cursor()
    # sql = "select student.sid AS Student_No, sname As Name,cid As Course_Name,score As Score " \
    #       "from grade join student on grade.sid=student.sid;"

    cur.execute(sql)
    content = cur.fetchall()
    cur.close()
    conn.close()
    return content

# 2.tree_clear 这是用来清空TreeView控件里面的已存在的内容的函数
def tree_clear(*args):
    temp_list= window.tree.get_children()
    for i in temp_list:
            window.tree.delete(i)   # 先清空，再插入

# window.button_clear = Button(window,text="CLEAR ALL",width=10,command=tree_clear)
# window.button_clear.place(x = 40 , y = 350)
window.button_clear.bind('<Button-1>',tree_clear)

# 3.load_tree 这是用来在TreeView控件中展示内容的函数
def load_tree(list):
    for item in list:
            window.tree.insert("",1,text="line",values=item)


# 4."SHOW ALL" button 实现
def Show_All(*args):
    # 1.每一次展现 TreeView 内容之前，都要清空之前的内容
    tree_clear()

    # 2.获取查询结果，类型为元组
    sql = "select student.sid AS Student_No, sname As Name,cid As Course_Name,score As Score " \
          "from grade join student on grade.sid=student.sid;"
    query_result = sql_query(sql)

    # 加载数据到 TreeView 控件 ， 如果 load_treeview 方法不可用，则可以尝试 inset 方法
    # window.tree.load_treeview(query_result)

    # 3.加载数据 insert 方法
    load_tree(query_result)


# "SHOW ALL" button
# window.button_show = Button(window,text=" SHOW ALL",width=10,command=Show_All)
# window.button_show.place(x = 40, y = 200)
window.button_show.bind("<Button-1>",Show_All)


# 5."BEST STU" button 实现
def Best_Stu(*args):
    tree_clear()

    sql = """SELECT student.sid,sname,cid,score from grade join student on grade.sid=student.sid
             where student.sid in(
             select test.sid from 
             (SELECT sid,sum(score) AS total_score FROM  grade GROUP BY sid order by total_score desc limit 1) as test);
"""

    query_result = sql_query(sql)
    load_tree(query_result)

# "BEST STU" button
# window.button_best = Button(window,text="BEST STU",width=10,command=Best_Stu)
# window.button_best.place(x = 40 , y = 250 )
window.button_best.bind('<Button-1>',Best_Stu)

# 6.sql_insert_del 是用来增删数据库中的数据的函数
def sql_insert_del(sql,arg_list):
    conn = pymysql.connect(host='localhost', port=3306, user='root', password='12345678', database='Student_Info',
                           charset='utf8')
    cur = conn.cursor()

    try:
        cur.execute(sql,arg_list)
        conn.commit()
        Show_All()

    except:
        conn.rollback()

    cur.close()
    conn.close()

# 7."ADD" button 实现
def Add_Student(*args):

    # 要先判断用户是否把每个空都填了
    if sid.get() == "":
        showerror(title='ERROR', message="Student No. Can\'t be Empty!")
    elif sname.get() == "":
        showerror(title='ERROR', message="Student Name Can\'t be Empty!")
    elif cid.get() == "":
        showerror(title='ERROR', message="Course No. Can\'t be Empty!")
    elif score.get() == "":
        showerror(title='ERROR', message="Score. Can\'t be Empty!")
    else:
        # 1.清空
        tree_clear()

        # 2.拿到源数据
        s_sid = sid.get()
        s_sname = sname.get()
        c_cid = cid.get()
        c_cname = cid.get()
        g_score = score.get()

        # 2.1 debug 过程中发现一个问题，就是数据可能会重复的问题
        # 用户可能会插入一个新的学生，但是它的课和其他学生的课是一样的，这个时候课程是不能插入的
        # 这个时候，就要解决重复数据的问题

        # 2.2 找出所有学生列表，课程列表
        sql = "select sid from student;"
        sql_query_student = sql_query(sql)

        sql = "select cid from course;"
        sql_query_course = sql_query(sql)

        tuple_s_sid = tuple((s_sid,))

        tuple_c_cid = tuple((c_cid,))

        # sql_query_course = list(sql_query_student)
        # 3.判断用户的输入属于哪种情况，总共四种情况
        # 学生，课程都不同；学生课程都相同；学生同，课程不同；学生不同，课程同
        # 仍然有问题：同一个学生，插入两节不同的课时候，就会出问题了
        if tuple_s_sid in sql_query_student:
                if tuple_c_cid in sql_query_course: # 插入的学生信息和课程信息都是现有的，直接showinfo了
                    showerror(title="REPEAT",message="THIS INFORMATION ALREADY EXISTS")

                else: # 学生同，课程不同，course和grade新增
                    sql = "insert into course values(%s,%s);"
                    arg_list = [c_cid,c_cname]
                    sql_insert_del(sql,arg_list)

                    sql = "insert into grade values(%s,%s,%s)"
                    arg_list = [s_sid,c_cid,g_score]
                    sql_insert_del(sql,arg_list)
                    showinfo(title="SUCCESS", message="course %s was ADDED for student %s!" % (c_cid,s_sname))

        else:
                if tuple_c_cid in sql_query_course: # 课程同，学生不同,student和grade新增
                    sql = "insert into student values(%s,%s);"
                    arg_list = [s_sid,s_sname]
                    sql_insert_del(sql,arg_list)

                    sql = "insert into grade values(%s,%s,%s)"
                    arg_list = [s_sid,c_cid,g_score]
                    sql_insert_del(sql,arg_list)

                    showinfo(title="SUCCESS", message="student %s was ADDED to the course %s!" % (s_sname,c_cid))

                else: # 新同学，新课程，三表同增
                    sql_student = "insert into student values(%s,%s);"
                    arg_list = [s_sid, s_sname]
                    sql_insert_del(sql_student, arg_list)

                    sql_course = "insert into course values(%s,%s);"
                    arg_list = [c_cid, c_cname]
                    sql_insert_del(sql_course, arg_list)

                    sql_grade = "insert into grade values(%s,%s,%s);"
                    arg_list = [s_sid, c_cid, g_score]
                    sql_insert_del(sql_grade, arg_list)
                    showinfo(title="SUCCESS", message="student %s \n course %s \n was ADDED!" % (s_sname ,c_cid))

        # 3.写入数据到数据库
        # conn = pymysql.connect(host='localhost', port=3306, user='root', password='12345678', database='Student_Info',
        #                        charset='utf8')
        # cur = conn.cursor()
        # sql_student = "insert into student values(%s,%s);"
        # sql_course = "insert into course values(%s,%s);"
        # sql_grade = "insert into grade values(%s,%s,%s)"
        #
        # print(c_cid,c_cname)
        #     ## 使用事务
        # try:
        #     cur.execute(sql_student, [s_sid, s_sname])
        #     cur.execute(sql_course, [c_cid, c_cname])
        #     cur.execute(sql_grade, [s_sid, c_cid, g_score])
        #     conn.commit()
        #     showinfo(title="SUCCESS", message="STUDENT %s WAS ADDED!" % s_sname)
        #     Show_All()
            # showinfo(title="HINT", message="PLEASE CLICK THE \"SHOW ALL\" BUTTON AGAIN!")
        #
        # except:
        #     showinfo(title="ERROR", message="ADD FAILED! ROLLBACK")
        #     conn.rollback()
        #
        # cur.close()
        # conn.close()


# ADD" button
window.button_append = Button(window.right_top_frame,width=10,text='ADD',command=Add_Student).place(x = 250, y = 95 )


# 8.switchButtonState 这个是用来禁用 delete 按钮的方法（详见下面的注释）
"""
一开始，delete按钮被禁用，只有当用户选中了数据的时候，delete才被启用，如何判断用户有没有选中数据？
tree.bind('<<TreeviewSelect>>',fuc)
"""
def switchButtonState(*args):
    if (window.button_delete['state'] == NORMAL):
        window.button_delete['state'] = DISABLED
    else:
        window.button_delete['state'] = NORMAL

window.tree.bind('<<TreeviewSelect>>',switchButtonState) # 这个 <<TreeviewSelect>> 可以判断是否被选中

# 9."DELETE ONE" button 实现
def Delete_One(*args):

    # 先获取要删除的那一条数据，筛选出 sid 和 cid ，因为根据 sid 和 cid 能在三张表中唯一确定一条数据
    item = window.tree.selection()
    selected_student = window.tree.item(item,"values")
    # print("sid is %s and cid is %s" % (selected_student[0],selected_student[2]))
    sid = selected_student[0]
    sname = selected_student[1]
    cid = selected_student[2]


    # 连接数据库，根据 sid 和 cid 删除三表中所有相关的内容
    conn = pymysql.connect(host='localhost', port=3306, user='root', password='12345678', database='Student_Info',
                           charset='utf8')
    cur = conn.cursor()
    sql_del_student = "delete from student where sid=%s"
    sql_del_grade = "delete from grade where sid=%s and cid=%s"

    flag = 0
    try:
        cur.execute(sql_del_student,[sid])
        cur.execute(sql_del_grade,[sid,cid])
        conn.commit()
        showinfo(title="SUCCESS",message="student %s WAS DELETED!"% sname)
        Show_All()
        flag = 1
    except:
        conn.rollback()
        showerror(title="ERROR",message="DELETE FAILED! ROLL BACK!")

    cur.close()
    conn.close()

    # if flag == 1:
    #     tree_clear()
    #     showinfo(title="HINT",message="PLEASE CLICK THE \"SHOW ALL\" BUTTON AGAIN!")

window.button_delete.bind('<Button-1>',Delete_One)


# 启动UI界面
window.mainloop()

