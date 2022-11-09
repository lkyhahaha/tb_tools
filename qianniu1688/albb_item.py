# 功能一：从淘管家-已铺货商品列表中导出商品id
# 实现方式：
# 1.访问淘管家自动跳转至登录界面，利用webdriver登录后，再次访问淘管家url
# 遇到的问题：直接用add_cookie()注入cookie方法程序报错，最后利用selenium完成登录操作（安全性低）
# 2.利用xpath和classname等方法定位元素，获取商品id和销售状态，处理成字典（product={itemid:status}）
# 3.通过判断“下一页”按钮是否可点击，while循环进入下一页，获取下一页的信息，继续存入product字典
# 4.利用for循环和if...else...对不同销售状态的商品id进行处理，存入不同的数组

# 问题1：
# 前4个商品的状态为空，后面的商品状态正常
# 问题2：
# 第4页页面渲染有问题，定位不到元素（已解决）
# 问题3：
# 修改规格的a标签href=“javascript:;” 无法直接点击（已解决）


# 功能二：导出规格匹配关系
from idlelib import browser

from selenium import webdriver
from time import sleep
from pymysql import *

from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.keys import Keys

# 登录
from qianniu1688 import taobao


def login():
    driver.switch_to.frame(0)
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


# 获取单页的商品id和销售状态，存入product字典
def getPageItem():
    # 单页的商品个数
    sleep(3)
    pagecount = len(driver.find_elements_by_class_name("item-title"))
    print("正在抓取第" + str(n) + "页 " + str(pagecount) + "个商品")
    for i in range(1, pagecount + 1):
        # print(i)
        offer = driver.find_element_by_xpath(
            "//*[@id='work_container']/div/div/div[2]/div[2]/div/div/div/div/div[3]/table/tbody/tr[{}]/td[2]/div[2]/p/a".format(
                i))
        offer_url = str(offer.get_attribute("href"))
        offer_id = offer_url.replace("https://detail.1688.com/offer/", "").replace(".html?sk=consignPrivate", "")
        # print(offer_id)
        # total_item.append(offer_id)
        # sleep(1)
        # 销售状态
        status = driver.find_element_by_xpath(
            "//*[@id='work_container']/div/div/div[2]/div[2]/div/div/div/div/div[3]/table/tbody/tr[{}]/td[6]".format(
                i)).text
        product[offer_id] = status
        try:
            mach = driver.find_element_by_xpath(
                "//*[@id='work_container']/div/div/div[2]/div[2]/div/div/div/div/div[3]/table/tbody/tr[{}]/td[4]/div/div".format(
                    i)).text
        except:
            mach = ""
        print(offer_id + ":" + status + "\t" + mach)

        if status in ("在售", "已下架"):
            if mach == '规格已匹配':
                product_mach.append(offer_id)
                item = driver.find_element_by_xpath(
                    "//*[@id='work_container']/div/div/div[2]/div[2]/div/div/div/div/div[3]/table/tbody/tr[{}]/td[5]/p[1]/a".format(
                        i))
                item_name = str(item.text)
                item_url = str(item.get_attribute("href"))
                item_id = item_url.replace("https://item.taobao.com/item.htm?id=", "")
                relation[offer_id] = item_id
                # print(relation)

                # 点击修改规格
                alter = driver.find_element_by_xpath(
                    "//*[@id='work_container']/div/div/div[2]/div[2]/div/div/div/div/div[3]/table/tbody/tr[{}]/td[8]/a[1]".format(
                        i))
                # href=“javascript:;” 无法直接点击
                driver.execute_script("arguments[0].click();", alter)
                sleep(3)

                sku_count = len(driver.find_elements_by_class_name("sku-value-tr"))
                for s in range(1, sku_count + 1):
                    item_sku_name = driver.find_element_by_xpath(
                        "/html/body/div[3]/div/div[2]/div/div/div[2]/div[2]/div[3]/table/tr[{}]/td[1]/table/tr/td".format(
                            s)).text
                    offer_sku_name = driver.find_element_by_xpath(
                        "/html/body/div[3]/div/div[2]/div/div/div[2]/div[2]/div[3]/table/tr[{}]/td[2]/table/tr/td/span".format(
                            s)).get_attribute("value")
                    print("item_sku_name:" + str(item_sku_name))
                    print("offer_sku_name:" + str(offer_sku_name))

                    update_time = taobao.getCuurenttime()
                    sql = 'insert into relation(item_name,item_id,item_sku_name,offer_id,offer_sku_name,update_time) values (\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\")' % (
                        item_name, item_id, item_sku_name, offer_id, offer_sku_name, update_time)
                    taobao.controldb(mysql_obj, sql)

                # 取消按钮
                sleep(1)
                driver.find_element_by_xpath("/html/body/div[3]/div/div[2]/div/div/div[3]/button[2]").click()
        else:
            pass


# 判断下一页
def nextAble():
    global nextpage
    nextpage = driver.find_element_by_xpath(
        "//*[@id='work_container']/div/div/div[2]/div[2]/div/div/div/div/div[4]/div/div/button[2]")
    driver.execute_script("arguments[0].scrollIntoView();", nextpage)
    next_able = nextpage.is_enabled()
    print("是否有下一页：" + str(next_able) + "\n")
    return next_able
    sleep(1)


# 销售状态的分类处理
def getOnsale():
    onsale = []
    ready = []
    onoff = []
    other = []
    for t in product.keys():
        if product[t] == '在售':
            onsale.append(t)
        elif product[t] == '未上架':
            ready.append(t)
        elif product[t] == '已下架':
            onoff.append(t)
        else:
            other.append(t)

    print("\n淘宝在售商品列表：")
    print(onsale)
    print("\n淘宝未上架商品列表：")
    print(ready)
    print("\n淘宝已下架商品列表：")
    print(onoff)
    print("\n其他：")
    print(other)


if __name__ == '__main__':
    option = ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    option.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(options=option)

    # 数据库初始化
    mysql_obj = connect(host='localhost', user='root', password='', db='taobao_data', port=3306,
                        charset='utf8mb4')
    print("数据库连接成功")
    sql_truncate = 'truncate table relation'
    taobao.controldb(mysql_obj, sql_truncate)

    # 数据初始化
    url = "https://guanjia.1688.com/page/consignoffer.htm?menuCode=consignoffer"
    product = {}
    product_mach = []
    relation = {}
    n = 1
    un = "15521080769"
    pw = "Lky965823-"

    driver.get(url)
    # 跳转到登录页面
    login()
    # 进入淘管家-已铺货商品
    driver.get(url)

    # 获取页面商品id、规格匹配的id
    getPageItem()
    # 判断翻页
    while nextAble() == True:
        nextpage.click()
        n += 1
        getPageItem()

    print(product)
    getOnsale()
    driver.quit()
