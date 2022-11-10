# 抓取淘宝数据入库

# 问题1：可能是cookie失效导致item()获取title和name为空
# 解决方法：多个cookie存放在数组里，检测title为空用下一个
# ！！！问题：多个cookie也不稳定，一般第5个以后的cookie都会直接失败

# 问题2：成功的日志不知道加在哪
# 解决办法：while判断条件改为判断数组的个数，而不是判断是否抓取成功

# 问题3：detail()部分itemid有时会报错，原因大概率是防爬，换cookie也没用
# 报错：raise JSONDecodeError("Expecting value", s, err.value) from None
# json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
# 解决办法：记录失败的itemid失败重试

# 问题4：异常重试itemid一直跑，程序执行不完
# 解决办法：重试成功的itemid，在需要重试的数组里移除掉

# 优化1：获取当前时间，updatetime入库（已处理）
# 优化2：导出cookie（getcookie.py）

from lxml import html
from time import sleep

import requests
from pymysql import *
from qianniu1688 import tools


def detail(url, cookies, headers):
    # print(cookies)
    response = requests.get(url, cookies=cookies, headers=headers)
    # print(response.text)
    response_json = tools.getJson(response.text)
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

        update_time = tools.getCuurenttime()

        # 把数据写入数据库

        sql = 'insert into price_stock(itemid,itemurl,sku,price,stock,update_time) values (\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\")' % (
            itemid, itemurl, newsku, price, stock, update_time)

        tools.controldb(mysql_obj, sql)
    if itemid in fail_item:
        fail_item.remove(itemid)
    else:
        pass


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
            tools.controldb(mysql_obj, sql)
        n = result.xpath("//li [@data-value='{}']/a/span".format(newsku))
        for skuname in n:
            name = skuname.text
            print(newsku + name)
            sql = 'update price_stock set sku_title=\"%s\" where itemid=\"%s\" and sku=\"%s\"' % (name, itemid, newsku)
            tools.controldb(mysql_obj, sql)
        update_time = tools.getCuurenttime()
        sql = 'update price_stock set update_time=\"%s\" where itemid=\"%s\" and sku=\"%s\"' % (
            update_time, itemid, newsku)
        tools.controldb(mysql_obj, sql)

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
    tools.controldb(mysql_obj, sql)
    # 枚举itemid
    itemid = ['682628841629', '682628893840', '682629885060', '683308540897', '683309088097', '683659301242', '683772068974', '683774244669', '683951894890', '683951954010', '683952234437', '683998782707', '684123453537', '684220105836', '684260735021', '684870251584', '685563720325', '685990624333', '686190966897', '686337101767', '686337805638', '686487223945', '686618602595', '686620474835', '686909999020', '686910479826', '686911823407', '686912367321', '689420852239', '689928673523', '691412744949', '691415428909', '691738205618', '691738333242', '692010342132', '692279347473']

    cookies = [
        {
            'Cookies': 'tfstk=ch3OBgcdhpvGlX908PK3gp0-yS3AZafTn1wAk4EoTDNlfRbAi6goyMFBfSyzBBC..;l=eBTSDdkRTHdqWxAoKOfwourza77OSIRAguPzaNbMiOCP9Z1e5DlGW6ri8v8wC3GVh67JR3r0glSeBeYBqSvwsWRKe5DDwQHmn;v=0;uc1=cookie15=WqG3DMC9VAQiUQ%3D%3D&existShop=true&cookie21=V32FPkk%2Fgi8IDE%2FSq3xx&pas=0&cookie14=UoeyCUjnTRZKgQ%3D%3D&cookie16=W5iHLLyFPlMGbLDwA%2BdvAGZqLg%3D%3D;dnk=lky559329;cancelledSubSites=empty;cookie1=BxSiYm0C5xPzAFVtUBOVTsU2XZ2Il%2F3qsYzo7iONJrQ%3D;_l_g_=Ug%3D%3D;cookie2=14a8a451956b608845bf1ac06b367f48;uc4=nk4=0%40Desk%2FC3VypAQUzkCG9e23ZR9MFs%3D&id4=0%40U2%2F8mBU1rpluU%2FXQ4al1yhaKWyK0;_nk_=lky559329;existShop=MTY2Nzk3ODU5MA%3D%3D;csg=99455e07;tracknick=lky559329;thw=cn;cna=U0PyG3pueCMCAXFtzndoGYkw;uc3=id2=UU27LusEqE%2FVmA%3D%3D&nk2=D8jtMcFdMhmF&lg2=WqG3DMC9VAQiUQ%3D%3D&vt3=F8dCvjXiHGXxJNHV5Xw%3D;unb=2591219604;mt=ci=9_1;sg=948;lgc=lky559329;isg=BBgYsxSrz5DbxuMUV61UQpt16UaqAXyLwEQZglIJZNMG7bjX-hFMGy5PISVdfTRj;skt=8f9f7476e1d27525;_tb_token_=e55386eb3458f;sgcookie=E100a4zE%2BKdyU8NDv47OEKVjDUHR%2BuVZNdZggAJGFgqtvWImYdzLQ%2BVGUn5%2Bt9bi%2BmoEHSRQV4BlZ45RycwvvsOArc2gY%2BqhgobO1j3UPkop%2Fcc%3D;_cc_=V32FPkk%2Fhw%3D%3D;cookie17=UU27LusEqE%2FVmA%3D%3D;xlly_s=1;t=744e54e438fa15eabcc43fad71e36f22;_samesite_flag_=true'},
        {
            'Cookies': 'tfstk=cU9CBVfsey4Bo6HuKwiZzyVi_LBAZOu1jX_pA2G31sxEKaKCix2VlKc9ZPXP2G1..;l=eBTSDdkRTHdqWxqEKOfwourza77OSIRAguPzaNbMiOCPO8fe5XA1W6ri8YTwC3GVh67JR3r0glSeBeYBqSvwsWRKe5DDwQHmn;v=0;uc1=cookie15=WqG3DMC9VAQiUQ%3D%3D&existShop=true&cookie21=V32FPkk%2Fgi8IDE%2FSq3xx&pas=0&cookie14=UoeyCUjnTRZKgQ%3D%3D&cookie16=W5iHLLyFPlMGbLDwA%2BdvAGZqLg%3D%3D;dnk=lky559329;cancelledSubSites=empty;cookie1=BxSiYm0C5xPzAFVtUBOVTsU2XZ2Il%2F3qsYzo7iONJrQ%3D;_l_g_=Ug%3D%3D;cookie2=14a8a451956b608845bf1ac06b367f48;uc4=nk4=0%40Desk%2FC3VypAQUzkCG9e23ZR9MFs%3D&id4=0%40U2%2F8mBU1rpluU%2FXQ4al1yhaKWyK0;_nk_=lky559329;existShop=MTY2Nzk3ODU5MA%3D%3D;csg=99455e07;tracknick=lky559329;thw=cn;cna=U0PyG3pueCMCAXFtzndoGYkw;uc3=id2=UU27LusEqE%2FVmA%3D%3D&nk2=D8jtMcFdMhmF&lg2=WqG3DMC9VAQiUQ%3D%3D&vt3=F8dCvjXiHGXxJNHV5Xw%3D;unb=2591219604;mt=ci=9_1;sg=948;lgc=lky559329;isg=BCkpAFzBbjOiAlKHbppVwZLqONWD9h0omcsIMcsepZBPkkmkE0Yt-BcAUDakCrVg;skt=8f9f7476e1d27525;_tb_token_=e55386eb3458f;sgcookie=E100a4zE%2BKdyU8NDv47OEKVjDUHR%2BuVZNdZggAJGFgqtvWImYdzLQ%2BVGUn5%2Bt9bi%2BmoEHSRQV4BlZ45RycwvvsOArc2gY%2BqhgobO1j3UPkop%2Fcc%3D;_cc_=V32FPkk%2Fhw%3D%3D;cookie17=UU27LusEqE%2FVmA%3D%3D;xlly_s=1;t=744e54e438fa15eabcc43fad71e36f22;_samesite_flag_=true'},
        {
            'Cookies': 'l=eBTSDdkRTHdqWpnyKOfwourza77OSIRAguPzaNbMiOCP9C1e5BZdW6ri8xLwC3GVh67JR3r0glSeBeYBqSvwsWRKe5DDwQHmn;tfstk=cfqRBAwvOsfkA-1n00QmLsqTM6qdZs9-tLGpvl3g3R11WbKdiOZgXEHfPvlZwtC..;v=0;uc1=cookie15=WqG3DMC9VAQiUQ%3D%3D&existShop=true&cookie21=V32FPkk%2Fgi8IDE%2FSq3xx&pas=0&cookie14=UoeyCUjnTRZKgQ%3D%3D&cookie16=W5iHLLyFPlMGbLDwA%2BdvAGZqLg%3D%3D;dnk=lky559329;cancelledSubSites=empty;cookie1=BxSiYm0C5xPzAFVtUBOVTsU2XZ2Il%2F3qsYzo7iONJrQ%3D;_l_g_=Ug%3D%3D;cookie2=14a8a451956b608845bf1ac06b367f48;uc4=nk4=0%40Desk%2FC3VypAQUzkCG9e23ZR9MFs%3D&id4=0%40U2%2F8mBU1rpluU%2FXQ4al1yhaKWyK0;_nk_=lky559329;existShop=MTY2Nzk3ODU5MA%3D%3D;csg=99455e07;tracknick=lky559329;thw=cn;cna=U0PyG3pueCMCAXFtzndoGYkw;uc3=id2=UU27LusEqE%2FVmA%3D%3D&nk2=D8jtMcFdMhmF&lg2=WqG3DMC9VAQiUQ%3D%3D&vt3=F8dCvjXiHGXxJNHV5Xw%3D;unb=2591219604;mt=ci=9_1;sg=948;lgc=lky559329;isg=BNbWeXU6qcrJtp1uJfuyqKnbJ4zYdxqxcpoHmEA_wrlUA3adqAdqwTxxn5_vqxLJ;skt=8f9f7476e1d27525;_tb_token_=e55386eb3458f;sgcookie=E100a4zE%2BKdyU8NDv47OEKVjDUHR%2BuVZNdZggAJGFgqtvWImYdzLQ%2BVGUn5%2Bt9bi%2BmoEHSRQV4BlZ45RycwvvsOArc2gY%2BqhgobO1j3UPkop%2Fcc%3D;_cc_=V32FPkk%2Fhw%3D%3D;cookie17=UU27LusEqE%2FVmA%3D%3D;xlly_s=1;t=744e54e438fa15eabcc43fad71e36f22;_samesite_flag_=true'},
        {
            'Cookies': 'tfstk=czlRBAgAAnxlGix3g7p08nc9OWGdZCQ8xaZd9feiuLFWeuCdiNGi6tUXFyra2EC..;l=eBTSDdkRTHdqWp0kKOfwourza77OSIRAguPzaNbMiOCP9U5e5quCW6ri8DYwC3GVhsGpR3r0glSeBeYBqSAo0kGSe5DDwQHmn;v=0;uc1=cookie15=WqG3DMC9VAQiUQ%3D%3D&existShop=true&cookie21=V32FPkk%2Fgi8IDE%2FSq3xx&pas=0&cookie14=UoeyCUjnTRZKgQ%3D%3D&cookie16=W5iHLLyFPlMGbLDwA%2BdvAGZqLg%3D%3D;dnk=lky559329;cancelledSubSites=empty;cookie1=BxSiYm0C5xPzAFVtUBOVTsU2XZ2Il%2F3qsYzo7iONJrQ%3D;_l_g_=Ug%3D%3D;cookie2=14a8a451956b608845bf1ac06b367f48;uc4=nk4=0%40Desk%2FC3VypAQUzkCG9e23ZR9MFs%3D&id4=0%40U2%2F8mBU1rpluU%2FXQ4al1yhaKWyK0;_nk_=lky559329;existShop=MTY2Nzk3ODU5MA%3D%3D;csg=99455e07;tracknick=lky559329;thw=cn;cna=U0PyG3pueCMCAXFtzndoGYkw;uc3=id2=UU27LusEqE%2FVmA%3D%3D&nk2=D8jtMcFdMhmF&lg2=WqG3DMC9VAQiUQ%3D%3D&vt3=F8dCvjXiHGXxJNHV5Xw%3D;unb=2591219604;mt=ci=9_1;sg=948;lgc=lky559329;isg=BHh4kzPXb7C7l4M0N400IjsVSSYK4dxrIGT5YrLpxLNmzRi3WvGs-45vgcX9nZRD;skt=8f9f7476e1d27525;_tb_token_=e55386eb3458f;sgcookie=E100a4zE%2BKdyU8NDv47OEKVjDUHR%2BuVZNdZggAJGFgqtvWImYdzLQ%2BVGUn5%2Bt9bi%2BmoEHSRQV4BlZ45RycwvvsOArc2gY%2BqhgobO1j3UPkop%2Fcc%3D;_cc_=V32FPkk%2Fhw%3D%3D;cookie17=UU27LusEqE%2FVmA%3D%3D;xlly_s=1;t=744e54e438fa15eabcc43fad71e36f22;_samesite_flag_=true'},
        {
            'Cookies': 'tfstk=c2uGBjgXTcr_dWLxdAa6Pcif-yJRZ-xaCquE8B0xHOTxzq3FiUsF4tBytRpWQi1..;l=eBTSDdkRTHdqWLOkKOfwourza77OSIRAguPzaNbMiOCP9fCe5z-NW6ri8c8wC3GVh67JR3r0glSeBeYBqSvwsWRKe5DDwQHmn;v=0;uc1=cookie15=WqG3DMC9VAQiUQ%3D%3D&existShop=true&cookie21=V32FPkk%2Fgi8IDE%2FSq3xx&pas=0&cookie14=UoeyCUjnTRZKgQ%3D%3D&cookie16=W5iHLLyFPlMGbLDwA%2BdvAGZqLg%3D%3D;dnk=lky559329;cancelledSubSites=empty;cookie1=BxSiYm0C5xPzAFVtUBOVTsU2XZ2Il%2F3qsYzo7iONJrQ%3D;_l_g_=Ug%3D%3D;cookie2=14a8a451956b608845bf1ac06b367f48;uc4=nk4=0%40Desk%2FC3VypAQUzkCG9e23ZR9MFs%3D&id4=0%40U2%2F8mBU1rpluU%2FXQ4al1yhaKWyK0;_nk_=lky559329;existShop=MTY2Nzk3ODU5MA%3D%3D;csg=99455e07;tracknick=lky559329;thw=cn;cna=U0PyG3pueCMCAXFtzndoGYkw;uc3=id2=UU27LusEqE%2FVmA%3D%3D&nk2=D8jtMcFdMhmF&lg2=WqG3DMC9VAQiUQ%3D%3D&vt3=F8dCvjXiHGXxJNHV5Xw%3D;unb=2591219604;mt=ci=9_1;sg=948;lgc=lky559329;isg=BMnJIF4QzhPCHbJnjrr14XLK2PUjFr1IOSuoUWs-RbDvsunEs2bNGLdg8BYE6lWA;skt=8f9f7476e1d27525;_tb_token_=e55386eb3458f;sgcookie=E100a4zE%2BKdyU8NDv47OEKVjDUHR%2BuVZNdZggAJGFgqtvWImYdzLQ%2BVGUn5%2Bt9bi%2BmoEHSRQV4BlZ45RycwvvsOArc2gY%2BqhgobO1j3UPkop%2Fcc%3D;_cc_=V32FPkk%2Fhw%3D%3D;cookie17=UU27LusEqE%2FVmA%3D%3D;xlly_s=1;t=744e54e438fa15eabcc43fad71e36f22;_samesite_flag_=true'},
        {
            'Cookies': 'tfstk=cY_GBBbbTG-1RrUAdOT_PGsf4weRZcEwCZ7F8WbAHD395e_FiziE4xHztde7Qm1..;l=eBTSDdkRTHdqWgCoKOfwourza77OSIRAguPzaNbMiOCPOkfe5ti1W6ri8mTwC3GVh67JR3r0glSeBeYBqSvwsWRKe5DDwQHmn;v=0;uc1=cookie15=WqG3DMC9VAQiUQ%3D%3D&existShop=true&cookie21=V32FPkk%2Fgi8IDE%2FSq3xx&pas=0&cookie14=UoeyCUjnTRZKgQ%3D%3D&cookie16=W5iHLLyFPlMGbLDwA%2BdvAGZqLg%3D%3D;dnk=lky559329;cancelledSubSites=empty;cookie1=BxSiYm0C5xPzAFVtUBOVTsU2XZ2Il%2F3qsYzo7iONJrQ%3D;_l_g_=Ug%3D%3D;cookie2=14a8a451956b608845bf1ac06b367f48;uc4=nk4=0%40Desk%2FC3VypAQUzkCG9e23ZR9MFs%3D&id4=0%40U2%2F8mBU1rpluU%2FXQ4al1yhaKWyK0;_nk_=lky559329;existShop=MTY2Nzk3ODU5MA%3D%3D;csg=99455e07;tracknick=lky559329;thw=cn;cna=U0PyG3pueCMCAXFtzndoGYkw;uc3=id2=UU27LusEqE%2FVmA%3D%3D&nk2=D8jtMcFdMhmF&lg2=WqG3DMC9VAQiUQ%3D%3D&vt3=F8dCvjXiHGXxJNHV5Xw%3D;unb=2591219604;mt=ci=9_1;sg=948;lgc=lky559329;isg=BIyMXzvpA7S39RfIw2kIpqfJXeq-xTBvLEgNvuZNmDfacSx7DtUA_4JDFXnJOWjH;skt=8f9f7476e1d27525;_tb_token_=e55386eb3458f;sgcookie=E100a4zE%2BKdyU8NDv47OEKVjDUHR%2BuVZNdZggAJGFgqtvWImYdzLQ%2BVGUn5%2Bt9bi%2BmoEHSRQV4BlZ45RycwvvsOArc2gY%2BqhgobO1j3UPkop%2Fcc%3D;_cc_=V32FPkk%2Fhw%3D%3D;cookie17=UU27LusEqE%2FVmA%3D%3D;xlly_s=1;t=744e54e438fa15eabcc43fad71e36f22;_samesite_flag_=true'},
        {
            'Cookies': 'l=eBTSDdkRTHdqW2-sKOfwourza77OSIRAguPzaNbMiOCP951e5WyAW6ri8VTwC3GVh67JR3r0glSeBeYBqSvwsWRKe5DDwQHmn;tfstk=cJ0ABgcRCLvc5b9gzrKu_L0dJWgOZg5YIswOW2Enagth1-QOi_gnJgFWc5yUHQC..;v=0;uc1=cookie15=WqG3DMC9VAQiUQ%3D%3D&existShop=true&cookie21=V32FPkk%2Fgi8IDE%2FSq3xx&pas=0&cookie14=UoeyCUjnTRZKgQ%3D%3D&cookie16=W5iHLLyFPlMGbLDwA%2BdvAGZqLg%3D%3D;dnk=lky559329;cancelledSubSites=empty;cookie1=BxSiYm0C5xPzAFVtUBOVTsU2XZ2Il%2F3qsYzo7iONJrQ%3D;_l_g_=Ug%3D%3D;cookie2=14a8a451956b608845bf1ac06b367f48;uc4=nk4=0%40Desk%2FC3VypAQUzkCG9e23ZR9MFs%3D&id4=0%40U2%2F8mBU1rpluU%2FXQ4al1yhaKWyK0;_nk_=lky559329;existShop=MTY2Nzk3ODU5MA%3D%3D;csg=99455e07;tracknick=lky559329;thw=cn;cna=U0PyG3pueCMCAXFtzndoGYkw;uc3=id2=UU27LusEqE%2FVmA%3D%3D&nk2=D8jtMcFdMhmF&lg2=WqG3DMC9VAQiUQ%3D%3D&vt3=F8dCvjXiHGXxJNHV5Xw%3D;unb=2591219604;mt=ci=9_1;sg=948;lgc=lky559329;isg=BExMH_LOQ_T3rVcIA6lIZmeJHap-hfAv7AhNfqYNWPeaMew7zpXAv0ID1TkJeSiH;skt=8f9f7476e1d27525;_tb_token_=e55386eb3458f;sgcookie=E100a4zE%2BKdyU8NDv47OEKVjDUHR%2BuVZNdZggAJGFgqtvWImYdzLQ%2BVGUn5%2Bt9bi%2BmoEHSRQV4BlZ45RycwvvsOArc2gY%2BqhgobO1j3UPkop%2Fcc%3D;_cc_=V32FPkk%2Fhw%3D%3D;cookie17=UU27LusEqE%2FVmA%3D%3D;xlly_s=1;t=744e54e438fa15eabcc43fad71e36f22;_samesite_flag_=true'}]

    fail_item = []
    m = 1

    # 失败重试
    while itemid != []:
        total = len(itemid)
        for item in itemid:
            itemurl = "https://item.taobao.com/item.htm?spm=a1z10.3-c.w4002-24537816225.9.6bfd6f73yJ9Wts&id=" + item
            print("\n" + str(m) + "/" + str(total) + "正在抓取 " + item + " 数据")
            print(itemurl)
            headers = {
                # "Host": "item.taobao.com",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
                "referer": itemurl
            }
            detailurl = 'https://detailskip.taobao.com/service/getData/1/p1/item/detail/sib.htm?itemId=' + item + '&sellerId=2591219604&modules=dynStock,qrcode,viewer,price,duty,xmpPromotion,delivery,activity,fqg,zjys,couponActivity,soldQuantity,page,originalPrice,tradeContract&callback=onSibRequestSuccess'

            # detail(detailurl, cookies[0], headers)
            try:
                # @retry(stop_max_attempt_number=5)
                detail(detailurl, cookies[0], headers)
            except:
                fail_item.append(item)
                print(fail_item)
                print(item + "detail抓取失败")
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
            m += 1
            sleep(10)
        # print(fail_item)
        itemid = fail_item
        print("失败列表：" + str(itemid))

    # 断开连接
    mysql_obj.close()
