# 获取店铺所有商品id

# 问题1：通过url实现翻页(打印n=2，但url的n还是等于1？)
# 解决方法：
# 1.url和n的拼装在上面，拼装n+1后的结果要在重新给url赋值
# 2.通过获取并访问下一页的超链接实现翻页

# 问题2：想要在taobao.py运行这个问题，并引用最后productId的值

from selenium import webdriver
from time import sleep

from selenium.webdriver import ChromeOptions
from pymysql import *
from qianniu1688 import tools
from qianniu1688 import albb_item


# 获取每页的itemid
def getid():
    item = driver.find_elements_by_class_name("J_TCollect")
    global page_count
    page_count = len(item)
    print("第" + str(n) + "页商品数：" + str(page_count))

    for i in item:
        # 获取属性值
        id = i.get_attribute('data-item-id')
        # print(type(id))
        productId.append(id)


if __name__ == '__main__':
    option = ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    option.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(options=option)
    mysql_obj = connect(host='localhost', user='root', password='', db='taobao_data', port=3306,
                        charset='utf8mb4')
    print("数据库连接成功")

    sql_un = 'select v_value from variable where v_key="albb_username"'
    username = tools.readdb(mysql_obj, sql_un)
    un = str(username).replace("(('", "").replace("',),)", "")

    sql_pw = 'select v_value from variable where v_key="albb_password"'
    password = tools.readdb(mysql_obj, sql_pw)
    pw = str(password).replace("(('", "").replace("',),)", "")

    login_url="https://login.taobao.com/member/login.jhtml?spm=a1z10.3-c.754894437.1.7d576f737OTI4K&f=top&redirectURL=https%3A%2F%2Fshop330863453.taobao.com%2Fcategory.htm%3Fspm%3Da1z10.3-c.w4010-24537816223.2.23736f73EDmVlX%26search%3Dy"
    driver.get(login_url)
    username = driver.find_element_by_id("fm-login-id")
    username.click()
    username.send_keys(un)
    password = driver.find_element_by_id("fm-login-password")
    password.click()
    password.send_keys(pw)
    submit = driver.find_element_by_class_name("fm-submit")
    submit.click()
    # 休眠手动输入验证码
    sleep(10)

    n = 1
    url = "https://shop330863453.taobao.com/search.htm?spm=a1z10.3-c.w4002-24537816225.9.6d3f6f734UhVfz&_ksTS=1667309300936_121&callback=jsonp122&input_charset=gbk&mid=w-24537816225-0&wid=24537816225&path=%2Fsearch.htm&search=y&viewType=list&pageNo=" + str(
        n)
    driver.get(url)
    sql_wait = "select v_value from variable where v_key='tb_item_wait'"
    wt=tools.readdb(mysql_obj, sql_wait)
    wait = int(str(wt).replace("(('", "").replace("',),)", ""))
    # print(wait)
    # print(type(wait))
    sleep(wait)
    # 存放所有的itemid
    productId = []

    # 获取店铺所有商品总数
    total = int(driver.find_element_by_xpath("//*[@id='shop-search-list']/div/div[2]/span").text)
    print("店铺总商品数：" + str(total))
    getid()

    # 判断是否有下一页
    count = page_count
    while count < total:
        n += 1
        # # 通过url实现翻页(url和n的拼装在上面，拼装n+1后的结果要在重新给url赋值)
        # url = "https://shop330863453.taobao.com/search.htm?spm=a1z10.3-c.w4002-24537816225.9.6d3f6f734UhVfz&_ksTS=1667309300936_121&callback=jsonp122&input_charset=gbk&mid=w-24537816225-0&wid=24537816225&path=%2Fsearch.htm&search=y&viewType=list&pageNo=" + str(
        #     n)
        # print("n="+str(n))
        # print("url="+url)
        # driver.get(url)

        # 访问下一页按钮的超链接翻页
        nextpage = driver.find_element_by_xpath(
            "//*[@id='J_ShopSearchResult']/div/div[2]/div[1]/div[3]/a[2]").get_attribute("href")
        driver.get(nextpage)

        sleep(3)
        getid()
        count = count + page_count
        print("已抓取商品数：" + str(count))

    print(productId)

    update_time = tools.getCuurenttime()
    sql_update = "update variable set v_value=\"%s\" , update_time=\"%s\" where v_key='tb_item'" % (
    productId, update_time)
    tools.controldb(mysql_obj, sql_update)

    driver.quit()
    mysql_obj.close()
