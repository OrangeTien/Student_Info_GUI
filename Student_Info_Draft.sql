
// 建立数据库
CREATE DATABASE Student_Info charset=utf8;
SHOW DATABASES;
use Student_Info;

// 建立若干表
CREATE TABLE student( 
     sid VARCHAR(30) PRIMARY KEY NOT NULL,
     sname VARCHAR(20)
  );
 
CREATE TABLE course 
  ( 
     cid VARCHAR(20) PRIMARY KEY NOT NULL, 
     cname VARCHAR(40)
  );
 
CREATE TABLE grade
  ( 
     sid VARCHAR(30) NOT NULL, 
     cid VARCHAR(20) NOT NULL, 
     score INT 
  );

SHOW TABLES;

// 检查满足几范式

// 添加数据
student:
insert into student values('1909853A-I011-0011','andrew'),('1909853B-I011-0022','bench'),('1909853T-I011-0077','tony'),('1909853J-I011-0033','jakcy');

course:
insert into course values('MATH001','calculus1'),('ENG004','English4'),('CS002','OOP');

grade:
insert into grade values('1909853A-I011-0011','MATH001',73),('1909853A-I011-0011','ENG004',70),('1909853A-I011-0011','CS002',75),
                        ('1909853B-I011-0022','MATH001',55),('1909853B-I011-0022','ENG004',95),('1909853B-I011-0022','CS002',79),
                        ('1909853T-I011-0077','MATH001',81),('1909853T-I011-0077','ENG004',84),('1909853T-I011-0077','CS002',72),
                        ('1909853J-I011-0033','MATH001',87),('1909853J-I011-0033','ENG004',51),('1909853J-I011-0033','CS002',89);


// 删除操作失误的数据
delete from student where sid='CS002' or sid='ENG004' or sid='MATH001';

// 开始查询
查询班级学生学号、姓名、课程名称，成绩信息：
select student.sid AS Student_No , sname As Name,cid As Course_Name,score As Score from 
grade join student on grade.sid=student.sid;


//查询课程分数总和最高的学生姓名和学号

// 这是第一句，这个可以找出最大值，但是找不出student.id
SELECT MAX(score_total.total_score) FROM 
(SELECT SUM(score) AS total_score FROM  grade GROUP BY sid) AS score_total;

// 这是第二句，这个可以找出最大值，也可以找出student.id,但是where不支持limit操作

SELECT sid,sum(score) AS total_score FROM  grade GROUP BY sid order by total_score desc limit 1;

// 这是最后的答案，经过google发现，再嵌套一层select即可绕开limit问题
SELECT student.sid,sname,cid,score from grade join student on grade.sid=student.sid
where student.sid in(
  select test.sid from 
  (SELECT sid,sum(score) AS total_score FROM  grade GROUP BY sid order by total_score desc limit 1) as test
);


// 这句话可以找出总分最低的学生
SELECT sid,sum(score) AS total_score FROM  grade GROUP BY sid order by total_score limit 1;

// 这个句子目前有点小问题，它只能删除一次数据，这是因为只删除了student里面的信息，而没有删除其他表的信息
delete from student where sid in (
  SELECT test.sid from(
  SELECT sid,sum(score) AS total_score FROM grade GROUP BY sid order by total_score limit 1) as test
);

// 添加数据,

insert into student values("%s","%S");
insert into course values(%s,%s);

// 根据sid和cid删除所有表中所有相关信息
delete from student where sid=%s 
delete from grade where sid=%s and cid=%s






