from time import sleep

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC

import unittest
import HTMLTestRunner


class TestLogin(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()
        cls.base_url = "http://jw.zhku.edu.cn/home.aspx"
        cls.title = '仲恺农业工程学院教务网络管理系统'

    # 定义登录方法
    def login(self, username, password):
        self.driver.get(self.base_url)
        self.driver.switch_to.frame("frm_login")
        # 用户名
        self.driver.find_element_by_id('txt_asmcdefsddsd').clear()
        self.driver.find_element_by_id('txt_asmcdefsddsd').send_keys(username)
        # 密码
        self.driver.find_element_by_id('txt_psasas').click()
        self.driver.find_element_by_id('txt_pewerwedsdfsdff').clear()
        self.driver.find_element_by_id('txt_pewerwedsdfsdff').send_keys(password)
        # # 验证码
        code = self.driver.find_element_by_id('txt_sdertfgsadscxcadsads')
        code.click()
        code.clear()

    # 用户名密码正确
    def test_login_g_success(self):
        u'''用户名密码正确'''
        username = '201710234117'
        password = '329001'
        self.login(username, password)
        sleep(8)
        # 登录
        confirm = self.driver.find_element_by_id('btn_login')
        confirm.click()
        sleep(2)
        # 判断+关闭未注销情况下alert弹框
        result = EC.alert_is_present()(self.driver)
        if result:
            result.accept()
        sleep(3)
        # 断言
        self.driver.switch_to.frame("frmFoot")
        userinfo = self.driver.find_element_by_id('lbl_userinfo').text
        self.assertIn(username, userinfo)

    # 用户名为空，密码不为空
    def test_login_a_UnNull(self):
        u'''用户名为空，密码不为空'''
        username = ''
        password = '329001'
        self.login(username, password)
        sleep(8)
        # 登录
        confirm = self.driver.find_element_by_id('btn_login')
        confirm.click()
        sleep(3)
        # 断言
        text = self.driver.switch_to.alert.text
        self.assertEqual(text, '须录入帐号！')
        self.driver.switch_to.alert.accept()

    # 用户名不为空，密码为空
    def test_login_b_PwdNULL(self):
        u'''用户名不为空，密码为空'''
        username = '201710234117'
        password = ''
        self.login(username, password)
        sleep(8)
        # 登录
        confirm = self.driver.find_element_by_id('btn_login')
        confirm.click()
        sleep(3)
        # 断言
        text = self.driver.switch_to.alert.text
        self.assertEqual(text, '须录入密码！')
        self.driver.switch_to.alert.accept()

    # 用户名、密码都为空
    def test_login_c_Null(self):
        u'''用户名、密码都为空'''
        username = ''
        password = ''
        self.login(username, password)
        sleep(8)
        # 登录
        confirm = self.driver.find_element_by_id('btn_login')
        confirm.click()
        sleep(3)
        # 断言
        text = self.driver.switch_to.alert.text
        self.assertEqual(text, '须录入帐号！')
        self.driver.switch_to.alert.accept()

    # 用户名不存在
    def test_login_d_UnWrong(self):
        u'''用户名不存在'''
        username = '12345'
        password = '111111'
        self.login(username, password)
        sleep(8)
        # 登录
        confirm = self.driver.find_element_by_id('btn_login')
        confirm.click()
        sleep(3)
        # 断言
        message = self.driver.find_element_by_id('divLogNote').text
        self.assertEqual(message, '帐号或密码不正确！请重新输入。')

    # 用户名正确，密码错误
    def test_login_e_PwdWrong(self):
        u'''用户名正确，密码错误'''
        username = '201710234117'
        password = '111111'
        self.login(username, password)
        sleep(8)
        # 登录
        confirm = self.driver.find_element_by_id('btn_login')
        confirm.click()
        sleep(3)
        # 断言
        message = self.driver.find_element_by_id('divLogNote').text
        self.assertEqual(message, '帐号或密码不正确！请重新输入。')

    # 验证码错误
    def test_login_f_CodeWrong(self):
        u'''验证码错误'''
        username = '201710234117'
        password = '329001'
        self.login(username, password)
        self.driver.find_element_by_id('txt_sdertfgsadscxcadsads').send_keys('abcd')
        # 登录
        confirm = self.driver.find_element_by_id('btn_login')
        confirm.click()
        sleep(3)
        # 断言
        message = self.driver.find_element_by_id('divLogNote').text
        self.assertEqual(message, '验证码错误！\n登录失败！')

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


# 定义一个测试套
def suite():
    suiteTest = unittest.TestSuite()
    suiteTest.addTest(TestLogin('test_login_a_UnNull'))
    suiteTest.addTest(TestLogin('test_login_b_PwdNULL'))
    suiteTest.addTest(TestLogin('test_login_c_Null'))
    suiteTest.addTest(TestLogin('test_login_d_UnWrong'))
    suiteTest.addTest(TestLogin('test_login_e_PwdWrong'))
    suiteTest.addTest(TestLogin('test_login_a_UnNull'))
    suiteTest.addTest(TestLogin('test_login_f_CodeWrong'))
    suiteTest.addTest(TestLogin('test_login_g_success'))
    return suiteTest


if __name__ == '__main__':
    # 存放路径
    filepath = "E:\\PyProject\\zhkuTest\\TestReport\\report_login.html"
    fp = open(filepath, 'wb')
    # 定义测试报告的标题和描述
    runner = HTMLTestRunner.HTMLTestRunner(
        stream=fp,
        title=u'登录模块',
        description=u'用例测试情况'
    )
    runner.run(suite())
    fp.close()
