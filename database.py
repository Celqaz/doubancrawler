import sqlite3

# 打开数据库
try:
    print('连接数据库中')
    conn = sqlite3.connect('database/dbdb.sqlite')
    cur = conn.cursor()
    print('数据库连接成功')
except Exception as e:
    print('!!!数据库连接失败!!!')

def add_data():
    cur.execute('''INSERT INTO File(name, file_type, project_id, type_id, employee_id, date, arcID) VALUES(?,?,?,?,?,?,?)''',
                (fname, file_type, int_project_id, int_type_id, int_employee_id, date, arc_id))
    print('\n开始向Evernote同步\n')
# add_file.add_record(conn, cur)