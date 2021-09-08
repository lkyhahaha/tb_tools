import time
from selenium import webdriver

driver = webdriver.Chrome()
driver.get("http://jw.zhku.edu.cn/home.aspx")
time.sleep(5)

driver.find_element_by_id("txt_asmcdefsddsd").send_keys("201710234117")
driver.find_element_by_id("txt_psasas").send_keys("329001")

