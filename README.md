##### **albb_item.py：**
~~~~
1.webdriver模拟登录，从淘管家-已铺货商品列表中导出商品id，并在控制台输出
2.导出淘宝和1688的匹配关系（只包含在售、已下架），存入relation表
~~~~
##### **alibaba.py：**
~~~~
访问1688商品详情页，抓取一件代发的价格库存数据，存入price_stock_1688表
~~~~
##### **tb_item.py：**
~~~~
访问淘宝店铺页，抓取店铺所有商品id，并在控制台输出
~~~~
##### **getcookie.py：**
~~~~
webdriver模拟登录，访问淘宝商品详情页，获取指定数量cookies，处理成字典在控制台输出
~~~~
##### **taobao.py：**
~~~~
request请求接口获取淘宝商品价格库存信息，存入price_stock表
~~~~
##### **tools.py：**
~~~~
封装response格式化、获取当前时间、数据库操作方法
~~~~
### **代码原理：**
~~~~
1.albb_item.py导出匹配关系
    _每天首次登录需密码登录和手机验证码，login()中休眠时间加大，后续运行可调至10s_
    （修改：main中mysql_obj中的数据库连接；un阿里巴巴账号；pw密码）
2.将albb_item.py控制台输出的淘宝在售商品列表复制到alibaba.py的itemids里，运行
    一开始需要滑块验证，20个商品左右需要再次滑块验证
    （修改：main中mysql_obj中的数据库连接；itemids）
3.运行tb_item.py，将控制台最后输出的数组复制到taobao.py的itemid中
4.运行getcookie.py,需要密码和手机淘宝验证，将控制台输出的结果复制到taobao.py的cookies中
（修改：username.send_keys("淘宝账号")；password.send_keys("淘宝密码")）
5.运行taobao.py
（修改：main中mysql_obj中的数据库连接；cookies（第4点输出结果）；itemid（第3点输出结果））
6.数据库查看结果，执行sql查询
~~~~


### **使用步骤：**
~~~~
1.按database.DDL在数据库建好表
variable表必填字段：
![img.png](https://github.com/lkyhahaha/tb_tools/blob/ed84d6a032664320745bdb56ef52b7db49ef80aa/img.png)
1.运行getcookie.py,复制cookieset在控制台输出的值，替换到taobao.py的cookies中
2.运行main.py
~~~~
