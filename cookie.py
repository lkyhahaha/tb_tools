from time import sleep
import time
import pymysql
from selenium import webdriver


# 定义登录方法
def login(username, password):
    # 用户名
    driver.find_element_by_name('username').click()
    driver.find_element_by_name('username').clear()
    driver.find_element_by_name('username').send_keys(username)
    # 密码
    driver.find_element_by_name('password').click()
    driver.find_element_by_name('password').clear()
    driver.find_element_by_name('password').send_keys(password)

    driver.find_element_by_class_name('form__submit').click()


# 格式化当前时间
def getupdatetime():
    updatetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(updatetime)


# 查表记录
def listdb():
    db = pymysql.connect(host="", port=, user="", passwd="", db="")
    cursor = db.cursor()
    sql = "select * from ad_cookie"
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            loginUser = row[0]
            token = row[1]
            update = row[2]
            evn = row[3]
            # 打印结果
            print(
                "loginUser=%s,token=%s,update=%s,evn=%s" % (loginUser, token, update, evn))
    except:
        print(
            "Error: unable to fecth data")
    db.close()


# 插入一条记录
def insertdb():
    db = pymysql.connect(host="", port=, user="", passwd="", db="")
    cursor = db.cursor()
    insertsql = "insert into ad_cookie (loginUser,token,updatetime,evn) values ('%s','%s','%s','%s')" % (
        username, cookiestr, updatetime, 'market')
    cursor.execute(insertsql)
    db.commit()
    db.close()


# 更新表记录
def updatedb():
    db = pymysql.connect(host="", port=, user="", passwd="", db="")
    cursor = db.cursor()
    updatesql = "update ad_cookie set token='%s',updatetime='%s' where loginUser='%s' and evn='market'" % (
        cookiestr, updatetime, username)
    cursor.execute(updatesql)
    db.commit()
    db.close()


driver = webdriver.Chrome()
base_url = ""
driver.get(base_url)
username = ""
password = ""
sleep(1)
login(username, password)
driver.refresh()
sleep(1)
cookie_list = driver.get_cookies()
cookie = [item["name"] + "=" + item["value"] for item in cookie_list]
cookiestr = ';'.join(item for item in cookie)
print(cookie_list)
print(cookiestr)
updatetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
print(updatetime)
updatedb()
driver.close()