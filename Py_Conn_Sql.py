# py_conn_sql.py
# 本文件是使用pymysql来连接数据库的模版

# 1.导入 PyMySQL 包
import pymysql

# 2.创建连接对象 - 桥梁
# pymysql.connect(host='主机',port=端口号,user='用户名',password='密码',database='数据库名',charset='编码方式')
conn = pymysql.connect(host='localhost',port=3306,user='root',password='12345678',database='Library_sys',charset='utf8')

# 3.创建游标对象 - 搬运工
# cursors函数是连接对象的方法，游标对象带有 execute() 方法可以执行sql语句
cur = conn.cursor()

# 4.增删改查 - 搬运工工作
sql_1 = "select * from Rent_book;"
cur.execute(sql_1)
content_one = cur.fetchone() # fetchone方法用来获取一条数据,反会类型是元组

# 注意看打印结果，content_all并没有包含第一条数据，这是因为我们使用的是游标操作，第一条数据读取完了之后，游标会往下面走
content_all = cur.fetchall()

print(content_one)
print(content_all)


# 5.关闭游标和连接对象（关闭有先后顺序） - 解雇搬运工，拆除桥梁
cur.close()
conn.close()


# # 增删改查具体操作示例
# # 增加数据,虽然最后的打印结果表明已经插入了数据，但是实际上在数据库中并没有插入，因为python开启了事务，所以需要提交
# sql_add = "insert into Book values(6,'Python插入','XXXX-OOOO-XXXXX-6','free','N','M_6');"
# cur.execute(sql_add)
#
# # 删除数据
# sql_del = "delete from Book where ID_book=6; "
# # cur.execute(sql_del)
#
# # 修改数据
# sql_modify = "update Book set Name_b='Python_insert' where ID_book=6;"
# cur.execute(sql_modify)




