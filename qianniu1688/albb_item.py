from selenium import webdriver
from time import sleep

from selenium.webdriver import ChromeOptions


def getPageItem():
    # 单页的商品个数
    sleep(5)
    pagecount = len(driver.find_elements_by_class_name("item-title"))
    print("\n正在抓取第" + str(n) + "页 " + str(pagecount) + "个商品")
    for i in range(1, pagecount + 1):
        # print(i)
        item = driver.find_element_by_xpath(
            "//*[@id='work_container']/div/div/div[2]/div[2]/div/div/div/div/div[3]/table/tbody/tr[{}]/td[2]/div[2]/p/a".format(
                i))
        item_url = str(item.get_attribute("href"))
        item_id = item_url.replace("https://detail.1688.com/offer/", "").replace(".html?sk=consignPrivate", "")
        # print(item_id)
        # total_item.append(item_id)
        sleep(1)
        status = driver.find_element_by_xpath(
            "//*[@id='work_container']/div/div/div[2]/div[2]/div/div/div/div/div[3]/table/tbody/tr[{}]/td[6]".format(
                i)).text
        print(item_id + ":" + status)
        product[item_id] = status


def nextAble():
    global nextpage
    nextpage = driver.find_element_by_xpath(
        "//*[@id='work_container']/div/div/div[2]/div[2]/div/div/div/div/div[4]/div/div/button[2]")
    driver.execute_script("arguments[0].scrollIntoView();", nextpage)
    next_able = nextpage.is_enabled()
    print("是否有下一页：" + str(next_able))
    return next_able


if __name__ == '__main__':
    option = ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    option.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(options=option)

    url = "https://guanjia.1688.com/page/consignoffer.htm?menuCode=consignoffer"
    driver.get(url)
    # 跳转到登录页面
    driver.switch_to.frame(0)
    username = driver.find_element_by_id("fm-login-id")
    username.click()
    username.send_keys("15521080769")
    password = driver.find_element_by_id("fm-login-password")
    password.click()
    password.send_keys("Lky965823-")
    submit = driver.find_element_by_class_name("fm-submit")
    submit.click()
    # 休眠手动输入验证码
    sleep(5)
    # 进入淘管家-已铺货商品
    driver.get(url)
    total_item = []
    product = {}
    n = 1

    getPageItem()
    while nextAble() == True:
        nextpage.click()
        n += 1
        getPageItem()
        sleep(2)

    # print(total_item)
    print(product)
    driver.quit()
