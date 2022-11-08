# 抓取1688价格库存数据

# 问题1：有商品有规格选项和颜色选项，执行会报错，要加个判断（举例：抓娃娃机）

# 问题2：除了前3个颜色的名称能抓取到，后面的颜色名称抓取成功率低
# 原因：可能是页面上没加载出来？加了向下滚动至按钮可见试试

# 优化1：一开始的滑块验证
# 优化2：获取当前时间，updatetime入库
# 优化3：淘宝和1688的关联关系（研究千牛）
# 优化4：1688商品id目前只能枚举，看看有没有地方看到已铺货商品导出


from selenium import webdriver
from time import sleep

from selenium.webdriver import ChromeOptions
from pymysql import *
import taobao


def getsku():
    for i in range(1, sku_count + 1):
        skuid = itemid + "-" + str(i)
        print(skuid)
        try:
            name = driver.find_element_by_xpath(
                "//div [@id='sku-count-widget-wrapper']/div[{}]/div[2]/div[1]".format(i))
            # sku2 = driver.find_element_by_xpath("//div [@id='sku-count-widget-wrapper']/div[6]/div[2]/div[1]")
            skuname = name.text
            if skuname == "":
                print("抓取第" + str(i) + "个sku名称为空")
            else:
                print("第" + str(i) + "个sku数据：")
                print(skuname)
        except:
            print("抓取第" + str(i) + "个sku名称失败")

        try:
            price = driver.find_element_by_xpath(
                "//div [@id='sku-count-widget-wrapper']/div[{}]/div[2]/div[2]".format(i))
            skuprice = price.text.strip("元")
            if skuprice == "":
                print("抓取第" + str(i) + "个sku价格为空")
            else:
                print(skuprice)
        except:
            print("抓取第" + str(i) + "个sku价格失败")

        try:
            stock = driver.find_element_by_xpath(
                "//div [@id='sku-count-widget-wrapper']/div[{}]/div[2]/div[3]".format(i))
            skustock = stock.text.strip("个可售")
            if skustock == "":
                print("抓取第" + str(i) + "个sku库存为空")
            else:
                print(skustock)
        except:
            print("抓取第" + str(i) + "个sku库存失败")

        update_time=taobao.getCuurenttime()

        sql_product = 'insert into price_stock_1688(productId,product_name,sku,sku_name,sku_price,sku_stock,product_url,update_time) values (\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\")' % (
            itemid, product_name, skuid, skuname, skuprice, skustock, url,update_time)
        taobao.controldb(mysql_obj, sql_product)


if __name__ == '__main__':
    mysql_obj = connect(host='localhost', user='root', password='', db='taobao_data', port=3306,
                        charset='utf8mb4')
    print("数据库连接成功")
    sql_truncate = 'truncate table price_stock_1688'
    taobao.controldb(mysql_obj, sql_truncate)

    option = ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    option.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(options=option)

    # driver = webdriver.Chrome()

    itemids = ["662729457093","676527350382","657930105302"]

    for itemid in itemids:
        url = "https://detail.1688.com/offer/" + itemid + ".html?spm=a261y.7663282.10811813088311.3.5d6b2802L7sleG&sk=consign"
        driver.get(url)
        sleep(5)
        # try:
        #     huakuai=driver.find_element_by_id("nc_1_n1z")
        #     action = ActionChains(driver)
        #     action.drag_and_drop_by_offset(huakuai,xoffset=300,yoffset=0).perform()
        # except:
        product_name = driver.find_element_by_class_name("title-text").text
        sku_name = driver.find_elements_by_class_name("sku-item-name")
        sku_count = len(sku_name)
        print("\n开始抓取" + itemid + "一共" + str(sku_count) + "个sku：" + product_name)

        try:
            morebutton = driver.find_element_by_class_name("sku-wrapper-expend-button")
            # 向下滚动至按钮可见
            driver.execute_script("arguments[0].scrollIntoView();", morebutton)
            morebutton.click()
            sleep(2)
            getsku()
        except:
            getsku()

    driver.quit()
    # 断开连接
    mysql_obj.close()
