from time import sleep
from selenium.webdriver.support import expected_conditions as EC


def login(self):
    # 登录
    self.driver.get(self.base_url)
    self.driver.switch_to.frame("frm_login")
    self.driver.find_element_by_id('txt_asmcdefsddsd').clear()
    self.driver.find_element_by_id('txt_asmcdefsddsd').send_keys('201710234117')
    self.driver.find_element_by_id('txt_psasas').click()
    self.driver.find_element_by_id('txt_pewerwedsdfsdff').clear()
    self.driver.find_element_by_id('txt_pewerwedsdfsdff').send_keys('329001')
    code = self.driver.find_element_by_id('txt_sdertfgsadscxcadsads')
    code.click()
    code.clear()
    sleep(8)
    confirm = self.driver.find_element_by_id('btn_login')
    confirm.click()
    sleep(2)
    # 判断+关闭未注销情况下alert弹框
    result = EC.alert_is_present()(self.driver)
    if result:
        result.accept()
    sleep(3)
