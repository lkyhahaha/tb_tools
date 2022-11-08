# 抓取淘宝数据入库

# 问题1：可能是cookie失效导致item()获取title和name为空
# 解决方法：多个cookie存放在数组里，检测title为空用下一个
# 问题2：成功的日志不知道加在哪
# 解决办法：while判断条件改为判断数组的个数，而不是判断是否抓取成功
# 问题3：detail()部分itemid有时会报错，原因大概率是防爬，换cookie也没用
# 报错：raise JSONDecodeError("Expecting value", s, err.value) from None
# json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)

# 优化1：获取当前时间，updatetime入库
import datetime

from lxml import html
import re
import json
from time import sleep

import requests
from retrying import retry
from pymysql import *


# response --> str --> json
def getJson(str):
    p1 = re.compile(r'[(](.*?)[)]', re.S)
    result_str = re.findall(p1, str)[0]
    result_json = json.loads(result_str)
    return result_json


def getCuurenttime():
    now = datetime.datetime.now()
    current_time = datetime.datetime.strftime(now, '%Y-%m-%d %H:%M:%S')
    return current_time


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


def detail(url, cookies, headers):
    # print(cookies)
    response = requests.get(url, cookies=cookies, headers=headers)
    print(response.text)
    response_json = getJson(response.text)
    # print(response_json)
    # print(type(response_json))

    global skuid
    skuid = response_json['data']['originalPrice'].keys()
    for sku in skuid:
        # 颜色分类id
        newsku = sku.replace(';', '')
        # print(newsku)
        # 每个颜色分类对应的价格

        # item(newsku, itemurl, cookies, headers)

        price = response_json['data']['originalPrice'].get(sku)['price']
        # print(price)
        try:
            stock = response_json['data']['dynStock']['sku'].get(sku)['sellableQuantity']
        except:
            stock = 0
        # print(stock)

        update_time = getCuurenttime()

        # 把数据写入数据库

        sql = 'insert into price_stock(itemid,itemurl,sku,price,stock,update_time) values (\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\")' % (
            itemid, itemurl, newsku, price, stock, update_time)

        controldb(mysql_obj, sql)


def item(url, cookies, headers):
    response = requests.get(url, cookies=cookies, headers=headers)
    # sleep(1)
    # print(cookies)
    result = html.fromstring(response.text)
    # print(type(result))
    # print("result:"+str(result))

    for sku in skuid:
        newsku = sku.replace(';', '')
        i = result.xpath("//title/text()")
        # print(i)
        for title in i:
            # print(title)
            sql = 'update price_stock set title=\"%s\" where itemid=\"%s\" and sku=\"%s\"' % (title, itemid, newsku)
            controldb(mysql_obj, sql)
        n = result.xpath("//li [@data-value='{}']/a/span".format(newsku))
        for skuname in n:
            name = skuname.text
            print(newsku + name)
            sql = 'update price_stock set sku_title=\"%s\" where itemid=\"%s\" and sku=\"%s\"' % (name, itemid, newsku)
            controldb(mysql_obj, sql)
        update_time = getCuurenttime()
        sql = 'update price_stock set update_time=\"%s\" where itemid=\"%s\" and sku=\"%s\"' % (
        update_time, itemid, newsku)
        controldb(mysql_obj, sql)

    if i == []:
        title_none = 1
    else:
        title_none = 0
    # print("title_none=" + str(title_none))
    return title_none


if __name__ == '__main__':
    # 数据库连接
    mysql_obj = connect(host='localhost', user='root', password='', db='taobao_data', port=3306,
                        charset='utf8mb4')
    print("数据库连接成功")
    sql = 'truncate table price_stock'
    controldb(mysql_obj, sql)
    # 枚举itemid
    itemid = ['682628841629', '682628893840', '682629885060', '683308540897', '683309088097', '683659301242',
              '683772068974', '683774244669', '683951894890', '683951954010', '683952234437', '683998782707',
              '684123453537', '684220105836', '684260735021', '684870251584', '685563720325', '685990624333',
              '686190966897', '686337101767', '686337805638', '686487223945', '686618602595', '686620474835',
              '686909999020', '686910479826', '686911823407', '686912367321', '689420852239', '689928673523']

    cookies = [{
        "Cookies": "t=8e521727a10093728fe1229e5b926b29; cna=7s8rGkLGih4CAXFtzwxn28TY; xlly_s=1; _m_h5_tk=b9434f009c5402959b06b043d42969a0_1667644960207; _m_h5_tk_enc=b081d75d0089dedd9873377d7823b092; _samesite_flag_=true; cookie2=1e2e109a5ad97626667533f07ca72ef3; _tb_token_=eebb7ebe1333; sgcookie=E100L3ynWGIp7WDSu%2FBkuqr3pP%2BbjrO8qZzs05mGV12ybRERMJrhUyWW4kclCrDM9IkjMzsAb9OVL9vvX7zolH0LSj4Y76hFaHuEzqzCAhRx80s%3D; unb=2211358392866; uc3=id2=UUpgR1F7JgdS4u3KKA%3D%3D&vt3=F8dCvjXlQq1u43T6cwo%3D&nk2=F5RBwKrgrLVhz5%2BN&lg2=URm48syIIVrSKA%3D%3D; csg=819565cd; lgc=tb4591965965; cancelledSubSites=empty; cookie17=UUpgR1F7JgdS4u3KKA%3D%3D; dnk=tb4591965965; skt=822fa873a1e78b0c; existShop=MTY2NzY1ODYzMg%3D%3D; uc4=id4=0%40U2gqyOyvuXMk8e0lB5UEkyqbr4JXk%2Bi%2F&nk4=0%40FY4KpXKms%2Fq39Bv945vNWOh%2FAsZ9KEo%3D; tracknick=tb4591965965; _cc_=UIHiLt3xSw%3D%3D; _l_g_=Ug%3D%3D; sg=56c; _nk_=tb4591965965; cookie1=VqpeaWELWYXKCVNa4G6ZKtTh0lGponFARJhBopJ6IqU%3D; tfstk=cXaABPNJCTXDoJBizqIo_Ql_DkUOZ_RxIIM9Wy3KoP6GPxLOi_a3J3h5cfkEH_C..; l=eBIfWso4LjFTQrv2BOfanurza77OSIRYSuPzaNbMiOCPOzC65_ElW6rrFjTBC3GVh64MR3r0glSeBeYBqIbH3CPie5DDwQHmn; isg=BMPDMnBypEzycGlXwg5ZLGfmUodtOFd6j-3SI_WgHyKZtOPWfQjnyqEmKkT6Ea9y; mt=ci=6_1; uc1=existShop=false&cookie21=VFC%2FuZ9ainBZ&pas=0&cookie15=WqG3DMC9VAQiUQ%3D%3D&cookie14=UoeyCUeiKMNpNg%3D%3D&cookie16=VFC%2FuZ9az08KUQ56dCrZDlbNdA%3D%3D; thw=cn"
    },
        {
            "Cookies": "t=8e521727a10093728fe1229e5b926b29; cna=7s8rGkLGih4CAXFtzwxn28TY; xlly_s=1; _m_h5_tk=b9434f009c5402959b06b043d42969a0_1667644960207; _m_h5_tk_enc=b081d75d0089dedd9873377d7823b092; _samesite_flag_=true; cookie2=1e2e109a5ad97626667533f07ca72ef3; _tb_token_=eebb7ebe1333; sgcookie=E100L3ynWGIp7WDSu%2FBkuqr3pP%2BbjrO8qZzs05mGV12ybRERMJrhUyWW4kclCrDM9IkjMzsAb9OVL9vvX7zolH0LSj4Y76hFaHuEzqzCAhRx80s%3D; unb=2211358392866; uc3=id2=UUpgR1F7JgdS4u3KKA%3D%3D&vt3=F8dCvjXlQq1u43T6cwo%3D&nk2=F5RBwKrgrLVhz5%2BN&lg2=URm48syIIVrSKA%3D%3D; csg=819565cd; lgc=tb4591965965; cancelledSubSites=empty; cookie17=UUpgR1F7JgdS4u3KKA%3D%3D; dnk=tb4591965965; skt=822fa873a1e78b0c; existShop=MTY2NzY1ODYzMg%3D%3D; uc4=id4=0%40U2gqyOyvuXMk8e0lB5UEkyqbr4JXk%2Bi%2F&nk4=0%40FY4KpXKms%2Fq39Bv945vNWOh%2FAsZ9KEo%3D; tracknick=tb4591965965; _cc_=UIHiLt3xSw%3D%3D; _l_g_=Ug%3D%3D; sg=56c; _nk_=tb4591965965; cookie1=VqpeaWELWYXKCVNa4G6ZKtTh0lGponFARJhBopJ6IqU%3D; mt=ci=6_1; uc1=existShop=false&cookie21=VFC%2FuZ9ainBZ&pas=0&cookie15=WqG3DMC9VAQiUQ%3D%3D&cookie14=UoeyCUeiKMNpNg%3D%3D&cookie16=VFC%2FuZ9az08KUQ56dCrZDlbNdA%3D%3D; thw=cn; tfstk=cfAABpT8f0m0iHnGasHl7z76oBAAZVaAjrsT6BCdihPsEiPOi4OH98QShNSFD4C..; l=eBIfWso4LjFTQCoSBOfanurza77OSIRYSuPzaNbMiOCPOb5e5NxlW6rrFALwC3GVh6-wR3r0glSeBeYBqBAnnxvte5DDwQHmn; isg=BJOTxdiO9NyimbnnEj6JnDf2Ihe9SCcK__0is0Ww77LpxLNmzRi3WvEe_jSq4X8C"}
        , {
            "Cookies": "t=8e521727a10093728fe1229e5b926b29; cna=7s8rGkLGih4CAXFtzwxn28TY; xlly_s=1; _m_h5_tk=b9434f009c5402959b06b043d42969a0_1667644960207; _m_h5_tk_enc=b081d75d0089dedd9873377d7823b092; _samesite_flag_=true; cookie2=1e2e109a5ad97626667533f07ca72ef3; _tb_token_=eebb7ebe1333; sgcookie=E100L3ynWGIp7WDSu%2FBkuqr3pP%2BbjrO8qZzs05mGV12ybRERMJrhUyWW4kclCrDM9IkjMzsAb9OVL9vvX7zolH0LSj4Y76hFaHuEzqzCAhRx80s%3D; unb=2211358392866; uc3=id2=UUpgR1F7JgdS4u3KKA%3D%3D&vt3=F8dCvjXlQq1u43T6cwo%3D&nk2=F5RBwKrgrLVhz5%2BN&lg2=URm48syIIVrSKA%3D%3D; csg=819565cd; lgc=tb4591965965; cancelledSubSites=empty; cookie17=UUpgR1F7JgdS4u3KKA%3D%3D; dnk=tb4591965965; skt=822fa873a1e78b0c; existShop=MTY2NzY1ODYzMg%3D%3D; uc4=id4=0%40U2gqyOyvuXMk8e0lB5UEkyqbr4JXk%2Bi%2F&nk4=0%40FY4KpXKms%2Fq39Bv945vNWOh%2FAsZ9KEo%3D; tracknick=tb4591965965; _cc_=UIHiLt3xSw%3D%3D; _l_g_=Ug%3D%3D; sg=56c; _nk_=tb4591965965; cookie1=VqpeaWELWYXKCVNa4G6ZKtTh0lGponFARJhBopJ6IqU%3D; mt=ci=6_1; uc1=existShop=false&cookie21=VFC%2FuZ9ainBZ&pas=0&cookie15=WqG3DMC9VAQiUQ%3D%3D&cookie14=UoeyCUeiKMNpNg%3D%3D&cookie16=VFC%2FuZ9az08KUQ56dCrZDlbNdA%3D%3D; thw=cn; tfstk=cGG5BA2X9gjWs6OhZuT2YX4v0DNhZexboLZ-P3OJkRkkWku5iPfaffvxKiVUJr1..; l=eBIfWso4LjFTQh5BBOfanurza77OSIRYSuPzaNbMiOCP9O1e5F8OW6rrFSYwC3GVh68wR3r0glSeBeYBqQAonxvte5DDwQHmn; isg=BIWF86lSSmKAaG9R0ETnEtXMlMG_QjnUnddUpYfqQbzLHqWQT5JJpBP0KELoW1GM"}]

    fail_item = []

    for itemid in itemid:
        itemurl = "https://item.taobao.com/item.htm?spm=a1z10.3-c.w4002-24537816225.9.6bfd6f73yJ9Wts&id=" + itemid
        print("\n正在抓取 " + itemid + " 数据")
        print(itemurl)
        headers = {
            # "Host": "item.taobao.com",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
            "referer": itemurl
        }
        detailurl = 'https://detailskip.taobao.com/service/getData/1/p1/item/detail/sib.htm?itemId=' + itemid + '&sellerId=2591219604&modules=dynStock,qrcode,viewer,price,duty,xmpPromotion,delivery,activity,fqg,zjys,couponActivity,soldQuantity,page,originalPrice,tradeContract&callback=onSibRequestSuccess'

        # detail(detailurl, cookies[0], headers)
        try:
            # @retry(stop_max_attempt_number=5)
            detail(detailurl, cookies[0], headers)
        except:
            fail_item.append(itemid)
            print(fail_item)
            print(itemid + "detail抓取失败")
            # raise Exception
            continue

        sleep(8)

        i = 0
        n = len(cookies)

        while i < n:
            if item(itemurl, cookies[i], headers) == 0:
                print("成功cookies[" + str(i) + "]")
                break
            else:
                print("失败cookies[" + str(i) + "]")
                i += 1

        sleep(10)

    # 断开连接
    mysql_obj.close()
