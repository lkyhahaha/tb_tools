from selenium import webdriver
from selenium.webdriver import ChromeOptions
from time import sleep
from pymysql import *
from qianniu1688 import tools

mysql_obj = connect(host='localhost', user='root', password='', db='taobao_data', port=3306,
                        charset='utf8mb4')
print("数据库连接成功")
option = ChromeOptions()
option.add_experimental_option('excludeSwitches', ['enable-automation'])
option.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(options=option)
url = 'https://item.taobao.com/item.htm?spm=a1z10.3-c.w4002-24537816225.9.6bfd6f73yJ9Wts&id=682628841629'
driver.get(url)
# 账号
username = driver.find_element_by_id("fm-login-id")
username.click()
sql_un='select v_value from variable where v_key="albb_username"'
us = tools.readdb(mysql_obj, sql_un)
un = str(us).replace("(('","").replace("',),)","")
username.send_keys(un)
# 密码
password = driver.find_element_by_id("fm-login-password")
password.click()
sql_pw = 'select v_value from variable where v_key="albb_password"'
pa = tools.readdb(mysql_obj, sql_pw)
pw = str(pa).replace("(('", "").replace("',),)", "")
password.send_keys(pw)
submit = driver.find_element_by_xpath("//*[@id='login-form']/div[4]/button")
submit.click()
sleep(10)

cookieset = []
i = 1
while i < 6:
    driver.get(url)
    cookie_list = driver.get_cookies()
    cookie = [item["name"] + "=" + item["value"] for item in cookie_list]
    cookiestr = ';'.join(item for item in cookie)
    # print(cookie_list)
    # print(cookiestr)
    cookie_dict = {}
    cookie_dict['Cookies'] = cookiestr
    cookieset.append(cookie_dict)
    # print("\n")
    # print(cookieset)
    print("第" + str(i) + "个cookie抓取成功")
    i += 1

    sleep(3)
print(cookieset)
driver.quit()
mysql_obj.close()
