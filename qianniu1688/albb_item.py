# 从淘管家-已铺货商品列表中导出商品id
# 实现方式：
# 1.访问淘管家自动跳转至登录界面，利用webdriver登录后，再次访问淘管家url
# 遇到的问题：直接用add_cookie()注入cookie方法程序报错，最后利用selenium完成登录操作（安全性低）
# 2.利用xpath和classname等方法定位元素，获取商品id和销售状态，处理成字典（product={itemid:status}）
# 3.通过判断“下一页”按钮是否可点击，while循环进入下一页，获取下一页的信息，继续存入product字典
# 4.利用for循环和if...else...对不同销售状态的商品id进行处理，存入不同的数组

from selenium import webdriver
from time import sleep

from selenium.webdriver import ChromeOptions


# 登录
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
    sleep(5)


# 获取单页的商品id和销售状态，存入product字典
def getPageItem():
    # 单页的商品个数
    sleep(3)
    pagecount = len(driver.find_elements_by_class_name("item-title"))
    print("正在抓取第" + str(n) + "页 " + str(pagecount) + "个商品")
    for i in range(1, pagecount + 1):
        # print(i)
        item = driver.find_element_by_xpath(
            "//*[@id='work_container']/div/div/div[2]/div[2]/div/div/div/div/div[3]/table/tbody/tr[{}]/td[2]/div[2]/p/a".format(
                i))
        item_url = str(item.get_attribute("href"))
        item_id = item_url.replace("https://detail.1688.com/offer/", "").replace(".html?sk=consignPrivate", "")
        # print(item_id)
        # total_item.append(item_id)
        # sleep(1)
        status = driver.find_element_by_xpath(
            "//*[@id='work_container']/div/div/div[2]/div[2]/div/div/div/div/div[3]/table/tbody/tr[{}]/td[6]".format(
                i)).text
        print(item_id + ":" + status)
        product[item_id] = status


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

    # 数据初始化
    url = "https://guanjia.1688.com/page/consignoffer.htm?menuCode=consignoffer"
    product = {}
    n = 1
    un = "15521080769"
    pw = "Lky965823-"

    driver.get(url)
    # 跳转到登录页面
    login()
    # 进入淘管家-已铺货商品
    driver.get(url)

    getPageItem()
    while nextAble() == True:
        nextpage.click()
        n += 1
        getPageItem()

    print(product)
    getOnsale()
    driver.quit()
