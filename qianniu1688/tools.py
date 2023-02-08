import re
import json
import datetime


# response --> str --> json
def getJson(str):
    p1 = re.compile(r'[(](.*?)[)]', re.S)
    result_str = re.findall(p1, str)[0]
    result_json = json.loads(result_str)
    return result_json


# 获取当前时间
def getCuurenttime():
    now = datetime.datetime.now()
    current_time = datetime.datetime.strftime(now, '%Y-%m-%d %H:%M:%S')
    return current_time


# 数据库操作
def controldb(mysql_obj, sql):
    # print('1')
    # 创建游标对象
    cur_obj = mysql_obj.cursor()
    try:
        cur_obj.execute(sql)
        # 提交操作
        mysql_obj.commit()
        # print(sql)
        print('插入数据成功\n' + sql)
    except:
        mysql_obj.rollback()
        print('插入数据失败\n' + sql)

    cur_obj.close()


def readdb(mysql_obj, sql):
    cur_obj = mysql_obj.cursor()
    try:
        cur_obj.execute(sql)
        results = cur_obj.fetchall()
        # print(results)
        return results
    except:
        mysql_obj.rollback()
