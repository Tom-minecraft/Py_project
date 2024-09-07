import pymysql
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

db = pymysql.connect(host="localhost", port=3306, user="root", passwd="chqteng1234")
cursor = db.cursor()
# cursor.execute('select version()')
# data = cursor.fetchone()
# print("Database version",data)
# cursor.execute("create database spider default character set utf8mb4")
# db.close()

# db = pymysql.connect(host="localhost", port=3306, user="root", passwd="chqteng1234")
# cursor_2 = db.cursor()
# cursor_2.execute('use spider')
# cursor_2.execute(
#     "create table if not exists students(id varchar(255) not null,name varchar(255) not null,age int not null,primary key (id))")
# db.close()

"""----------------------动态存储-------------------------"""
# id = "20120001"
# user = "Bob"
# age = 20
#
# db = pymysql.connect(host="localhost", port=3306, user="root", passwd="chqteng1234")
# cursor_3 = db.cursor()
# cursor_3.execute("use spider")
# sql = 'insert into students (id, name, age) values (%s, %s, %s)'
# try:
#     cursor_3.execute(sql, (id, user, age))
#     db.commit()
# except Exception as e:
#     db.rollback()
#     logging.error(e)
# db.close()

data = {
    'id':'11111dfds112222222',
    'name':'Aobsdfdfsf',
    'age':185423234,
}
table = 'students'
keys = ','.join(data.keys())
values = ','.join(['%s']*len(data))
sql = f'INSERT INTO {table} ({keys}) VALUES ({values}) ON DUPLICATE KEY UPDATE '
update = ','.join([f'{key}=%s' for key in data])
sql += update
try:
    cursor.execute("use spider")
    cursor.execute(sql, tuple(data.values())*2)
    db.commit()
except Exception as e:
    logging.error(e)
    db.rollback()
db.close()


"""-----------更新------------"""


# sql_update = 'update students set age = %s where name = %s'
# try:
#     cursor_3.execute("use spider")
#     cursor_3.execute(sql_update,(25,"Bob"))
#     db.commit()
# except Exception as e:
#     logging.error(e)
#     db.rollback()

"""--------------更新插入----------------"""

# data = {
#     'id':'20240901',
#     'name':'Aob',
#     'age':18,
# }
# table = 'students'
# keys = ','.join(data.keys())
# values = ','.join(['%s']*len(data))
# sql = 'insert into {table} ({keys}) values ({values}) on duplicate key update '.format(table=table, keys=keys, values=values)
# update = ','.join(['{key}=%s'.format(key=key) for key in data])
# sql += update
# data_values = tuple(data.values())*2
# try:
#     cursor_3.execute("use spider")
#     cursor_3.execute(sql,data_values)
#     db.commit()
# except Exception as e:
#     logging.error(e)
#     db.rollback()

"""----------------删除---------------------"""
# table = 'students'
# condition = 'age > 20'
# sql = 'delete from {table} where {condition}'.format(table=table, condition=condition)
# try:
#     cursor_3.execute("use spider")
#     cursor_3.execute(sql)
#     db.commit()
# except Exception as e:
#     logging.error(e)
#     db.rollback()
# db.close()

# """-----------查询(全部取出)--------------"""

# sql = 'select * from students where age > 10'
# try:
#     cursor_3.execute("use spider")
#     cursor_3.execute(sql)
#     print(cursor_3.rowcount)
#     result_one = cursor_3.fetchone()
#     print(result_one)
#     result_all = cursor_3.fetchall()
#     print(result_all)
#     print("Type:", type(result_all))
#     for each in result_all:
#         print(each)
# except Exception as e:
#     print(e)



# sql = 'select * from students where age > 10'
# try:
#     cursor.execute("use spider")
#     cursor.execute(sql)
#     print(cursor.rowcount)
#     one = cursor.fetchone()
#     while one:
#         print(one)
#         one = cursor.fetchone()
# except Exception as e:
#     logging.error(e)

