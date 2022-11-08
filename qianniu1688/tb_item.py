# 获取店铺所有商品id

# 问题1：通过url实现翻页(打印n=2，但url的n还是等于1？)
# 解决方法：
# 1.url和n的拼装在上面，拼装n+1后的结果要在重新给url赋值
# 2.通过获取并访问下一页的超链接实现翻页

# 问题2：想要在taobao.py运行这个问题，并引用最后productId的值

from selenium import webdriver
from time import sleep

from selenium.webdriver import ChromeOptions


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

    n = 1
    url = "https://shop330863453.taobao.com/search.htm?spm=a1z10.3-c.w4002-24537816225.9.6d3f6f734UhVfz&_ksTS=1667309300936_121&callback=jsonp122&input_charset=gbk&mid=w-24537816225-0&wid=24537816225&path=%2Fsearch.htm&search=y&viewType=list&pageNo=" + str(
        n)
    driver.get(url)
    sleep(3)
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

    driver.quit()
