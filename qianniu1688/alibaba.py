# 抓取1688价格库存数据
import os
# 问题1：有商品有规格选项和颜色选项，执行会报错，要加个判断（举例：抓娃娃机）

# 问题2：除了前3个颜色的名称能抓取到，后面的颜色名称抓取成功率低
# 原因：可能是页面上没加载出来？加了向下滚动至按钮可见试试

# 问题3：中途会出现滑块验证

# 问题4：库存含有中文

# 优化1：一开始的滑块验证
# 优化2：获取当前时间，updatetime入库(已解决)
# 优化3：淘宝和1688的关联关系(已解决：albb_item.py)
# 优化4：1688商品id目前只能枚举，看看有没有地方看到已铺货商品导出（已解决：albb_item.py）
import re

from selenium import webdriver
from time import sleep

from selenium.webdriver import ChromeOptions
from pymysql import *
from qianniu1688 import tools
import albb_item


def getsku():
    for i in range(1, sku_count + 1):
        skuid = itemid + "-" + str(i)
        print(skuid)
        # 失败标记，每失败一次fail_status+1，fail_status==0则该商品所有sku抓取成功
        global fail_status
        fail_status = 0
        try:
            name = driver.find_element_by_xpath(
                "//div [@id='sku-count-widget-wrapper']/div[{}]/div[2]/div[1]".format(i))
            # sku2 = driver.find_element_by_xpath("//div [@id='sku-count-widget-wrapper']/div[6]/div[2]/div[1]")
            skuname = name.text
            if skuname == "":
                fail_status += 1
                print("抓取第" + str(i) + "个sku名称为空")
            else:
                print("第" + str(i) + "个sku数据：")
                print(skuname)
        except:
            fail_status += 1
            print("抓取第" + str(i) + "个sku名称失败")

        try:
            price = driver.find_element_by_xpath(
                "//div [@id='sku-count-widget-wrapper']/div[{}]/div[2]/div[2]".format(i))
            skuprice = price.text.strip("元")
            if skuprice == "":
                fail_status += 1
                print("抓取第" + str(i) + "个sku价格为空")
            else:
                print(skuprice)
        except:
            fail_status += 1
            print("抓取第" + str(i) + "个sku价格失败")

        try:
            stock = driver.find_element_by_xpath(
                "//div [@id='sku-count-widget-wrapper']/div[{}]/div[2]/div[3]".format(i))
            # skustock = stock.text.strip("可售")
            skustock = re.sub("\D", "", stock.text)
            # number(skustock)
            if skustock == "":
                fail_status += 1
                print("抓取第" + str(i) + "个sku库存为空")
            else:
                print(skustock)
        except:
            fail_status += 1
            print("抓取第" + str(i) + "个sku库存失败")
            continue

        update_time = tools.getCuurenttime()

        sql_product = 'insert into price_stock_1688(productId,product_name,logistics,sku,sku_name,sku_price,sku_stock,product_url,update_time) values (\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\")' % (
            itemid, product_name, logistics, skuid, skuname, skuprice, skustock, url, update_time)
        tools.controldb(mysql_obj, sql_product)


if __name__ == '__main__':
    mysql_obj = connect(host='localhost', user='root', password='', db='taobao_data', port=3306,
                        charset='utf8mb4')
    print("数据库连接成功")
    sql_truncate = 'truncate table price_stock_1688'
    tools.controldb(mysql_obj, sql_truncate)

    option = ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    option.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(options=option)
    # driver.maximize_window()

    # driver = webdriver.Chrome()

    # itemids = ['677766044544', '683104580152', '669052169822', '681688786854', '674588187519', '645763747545',
    #            '678480221196', '649999853265', '688807014913', '672728166015', '676527350382', '680615136541',
    #            '674753097881', '623392165199', '649654527723', '663686382031', '655990749842', '678373222207',
    #            '684922867792', '655241160564', '610364573858', '676158252515', '593672520597', '638750254497',
    #            '657930105302', '679844062811', '682871222899', '621844269195', '652469954533', '643914409183',
    #            '626946615414', '661937814500', '662729457093', '597303088611', '676526444193', '682304010365',
    #            '668983174869', '676891149817', '681392374055', '670188883840']
    sql_read = "select v_value from variable where v_key='albb_item'"
    results = tools.readdb(mysql_obj, sql_read)
    result = str(results).replace("((\"['", "").replace("']\",),)", "")
    # print(result)
    res = result.split('\', \'')
    # print(type(re))
    itemids = res
    # print(type(itemids))
    fail_item = []
    item_404 = []
    total_item = len(itemids)
    m = 1
    product = {}

    for itemid in itemids:
        url = "https://detail.1688.com/offer/" + itemid + ".html?spm=a261y.7663282.10811813088311.3.5d6b2802L7sleG&sk=consign"
        driver.get(url)
        sleep(6)
        # try:
        #     huakuai=driver.find_element_by_id("nc_1_n1z")
        #     action = ActionChains(driver)
        #     action.drag_and_drop_by_offset(huakuai,xoffset=300,yoffset=0).perform()
        # except:
        try:
            product_name = driver.find_element_by_class_name("title-text").text
            product[itemid] = product_name
            # 抓取到北京的运费
            try:
                select = driver.find_element_by_class_name("next-select-inner")
                select.click()
                province = driver.find_element_by_xpath("//span[text()='北京']")
                province.click()
                city = driver.find_element_by_xpath("//span[text()='北京市']")
                city.click()
                district = driver.find_element_by_xpath("//span[text()='东城区']")
                district.click()
                # sleep(1)
                submit = driver.find_element_by_xpath(
                    "//div[@class='next-loading-wrap']/div/div[2]/div[3]/div/button[1]")
                submit.click()
                sleep(1)
                logistics = driver.find_element_by_class_name("logistics-express").text
                if logistics == "包邮":
                    logistics = 0

            except:
                logistics = driver.find_element_by_xpath("//div[@class='logistics-wrapper']/div[1]/span[2]").text
                if logistics == "卖家承担运费":
                    logistics = 0

            sku_name = driver.find_elements_by_class_name("sku-item-name")
            sku_count = len(sku_name)
            print(
                "\n" + str(m) + "/" + str(total_item) + "\t开始抓取" + itemid + "\t共" + str(
                    sku_count) + "个sku：" + product_name + "\n运费：" + str(logistics))

            try:
                morebutton = driver.find_element_by_class_name("sku-wrapper-expend-button")
                # 向下滚动至按钮可见
                driver.execute_script("arguments[0].scrollIntoView();", morebutton)
                morebutton.click()
                sleep(2)
                getsku()
            except:
                getsku()
            m += 1

            # print(fail_status)
            if fail_status > 0:
                fail_item.append(itemid)
            else:
                pass
        except:
            item_404.append(itemid)
    # print(product)
    print("404商品列表：" + str(item_404))
    print("失败商品列表：" + str(fail_item))
    for f in fail_item:
        print(str(f) + ":" + str(product[f]))

    driver.quit()
    # 断开连接
    mysql_obj.close()
