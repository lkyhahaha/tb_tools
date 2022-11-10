from selenium import webdriver
from selenium.webdriver import ChromeOptions
from time import sleep

option = ChromeOptions()
option.add_experimental_option('excludeSwitches', ['enable-automation'])
option.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(options=option)
url = 'https://item.taobao.com/item.htm?spm=a1z10.3-c.w4002-24537816225.9.6bfd6f73yJ9Wts&id=682628841629'
driver.get(url)
username = driver.find_element_by_id("fm-login-id")
username.click()
username.send_keys("15521080769")
password = driver.find_element_by_id("fm-login-password")
password.click()
password.send_keys("Lky965823-")
submit = driver.find_element_by_xpath("//*[@id='login-form']/div[4]/button")
submit.click()
sleep(60)

cookieset = []
i = 1
while i < 8:
    driver.get(url)
    cookie_list = driver.get_cookies()
    cookie = [item["name"] + "=" + item["value"] for item in cookie_list]
    cookiestr = ';'.join(item for item in cookie)
    # print(cookie_list)
    # print(cookiestr)
    cookie_dict = {}
    cookie_dict['Cookies'] = cookiestr
    cookieset.append(cookie_dict)
    # print("\n")
    # print(cookieset)
    print("第" + str(i) + "个cookie抓取成功")
    i += 1

    sleep(3)
print(cookieset)
driver.quit()
