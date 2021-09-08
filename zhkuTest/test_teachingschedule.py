from time import sleep
from selenium import webdriver
import unittest
import HTMLTestRunner

from zhkuTest import login


class TestTeachingSchedule(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()
        cls.base_url = "http://jw.zhku.edu.cn/home.aspx"
        cls.driver.refresh()
        login.login(cls)
        cls.driver.switch_to.frame("frmbody")
        # 教学安排
        cls.driver.find_element_by_id('memuBarText4').click()
        # 教学安排表
        cls.driver.find_element_by_xpath("//span[@value='../znpk/Pri_StuSel.aspx']").click()
        sleep(2)
        cls.driver.switch_to.frame("frmMain")

    def test_0_Format1Selected(self):
        u'''点击格式一，格式二不选中'''
        self.driver.find_element_by_id('rad_gs1').click()
        sleep(1)
        # 断言
        selected = self.driver.find_element_by_id('rad_gs2').is_selected()
        # print(selected)
        self.assertFalse(selected)

    def test_10_Format1Visible(self):
        u'''点击格式一，周次排序用户不可见'''
        self.driver.find_element_by_id('rad_gs1').click()
        sleep(1)
        # 定位到周次、排序区域
        loc = self.driver.find_element_by_id('sel_area')
        # 定位到周次、排序区域
        vis = loc.get_attribute('style')
        # print('ass2='+ass2)
        # 断言
        self.assertIn('visibility: hidden;', vis)

    def test_11_Format2Selected(self):
        u'''点击格式二，格式一不选中'''
        self.driver.find_element_by_id('rad_gs2').click()
        sleep(1)
        # 断言
        selected = self.driver.find_element_by_id('rad_gs1').is_selected()
        # print(selected)
        self.assertFalse(selected)

    def test_12_Format2Visible(self):
        u'''点击格式二，周次排序用户可见'''
        self.driver.find_element_by_id('rad_gs2').click()
        sleep(1)
        # 定位到周次、排序区域
        loc = self.driver.find_element_by_id('sel_area')
        # 定位到周次、排序区域
        vis = loc.get_attribute('style')
        # print('ass2='+ass2)
        # 断言
        self.assertNotIn('visibility: hidden;', vis)

    def test_13_WeekSelected(self):
        u'''周次前单选框是否可选中'''
        self.driver.find_element_by_id('rad_gs2').click()
        # 判断周次是否已被选中，如已被选中，恢复到取消选中状态
        selected1 = self.driver.find_element_by_id('zc_flag').is_selected()
        if selected1:
            self.driver.find_element_by_id('zc_flag').click()
            sleep(1)
        # 在取消选中状态下点击复选框
        self.driver.find_element_by_id('zc_flag').click()
        sleep(1)
        # 断言
        selected2 = self.driver.find_element_by_id('zc_flag').is_selected()
        self.assertTrue(selected2)

    def test_14_WeekInputAble(self):
        u'''选中周次复选框，周次可编辑'''
        self.driver.find_element_by_id('rad_gs2').click()
        # 判断周次是否已被选中
        selected = self.driver.find_element_by_id('zc_flag').is_selected()
        # print(selected)
        if not selected:
            self.driver.find_element_by_id('zc_flag').click()
            sleep(1)
        # 断言
        state = self.driver.find_element_by_name('zc_input').is_enabled()
        # print(state)
        self.assertTrue(state)

    def test_15_WeekInputDisable(self):
        u'''取消选中周次复选框，周次禁用编辑'''
        self.driver.find_element_by_id('rad_gs2').click()
        # 判断周次是否已被选中
        selected = self.driver.find_element_by_id('zc_flag').is_selected()
        if selected:
            self.driver.find_element_by_id('zc_flag').click()
            sleep(1)
        # 断言
        state = self.driver.find_element_by_name('zc_input').is_enabled()
        self.assertFalse(state)

    def test_16_RankValue0(self):
        u'''排序下拉框中存在“按课程/环节”候选值'''
        self.driver.find_element_by_id('rad_gs2').click()
        # 断言
        value0 = self.driver.find_element_by_xpath("//select[@name='px']/option[@value='0']").text
        # print(value0)
        self.assertIn('按课程/环节', value0)

    def test_17_RankValue1(self):
        u'''排序下拉框中存在“按时间”候选值'''
        self.driver.find_element_by_id('rad_gs2').click()
        # 断言
        value1 = self.driver.find_element_by_xpath("//select[@name='px']/option[@value='1']").text
        # print(value1)
        self.assertIn('按时间', value1)

    def test_18_RankAble(self):
        u'''排序下拉框可用'''
        self.driver.find_element_by_id('rad_gs2').click()
        rank = self.driver.find_element_by_name('px')
        state = rank.is_enabled()
        self.assertTrue(state)

    def test_19_TermAble(self):
        u'''学年学期下拉框可用'''
        term = self.driver.find_element_by_name('Sel_XNXQ')
        state = term.is_enabled()
        self.assertTrue(state)

    def test_20_SearchAble(self):
        u'''检索按钮可用'''
        search = self.driver.find_element_by_name('btnSearch')
        state = search.is_enabled()
        self.assertTrue(state)

    def test_21_PrintAble(self):
        u'''打印按钮可用'''
        button = self.driver.find_element_by_name('btn_print')
        state = button.is_enabled()
        self.assertTrue(state)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


# 定义一个测试套
def suite():
    suiteTest = unittest.TestSuite()
    suiteTest.addTest(TestTeachingSchedule('test_0_Format1Selected'))
    suiteTest.addTest(TestTeachingSchedule('test_10_Format1Visible'))
    suiteTest.addTest(TestTeachingSchedule('test_11_Format2Selected'))
    suiteTest.addTest(TestTeachingSchedule('test_12_Format2Visible'))
    suiteTest.addTest(TestTeachingSchedule('test_13_WeekSelected'))
    suiteTest.addTest(TestTeachingSchedule('test_14_WeekInputAble'))
    suiteTest.addTest(TestTeachingSchedule('test_15_WeekInputDisable'))
    suiteTest.addTest(TestTeachingSchedule('test_16_RankValue0'))
    suiteTest.addTest(TestTeachingSchedule('test_17_RankValue1'))
    suiteTest.addTest(TestTeachingSchedule('test_18_RankAble'))
    suiteTest.addTest(TestTeachingSchedule('test_19_TermAble'))
    suiteTest.addTest(TestTeachingSchedule('test_20_SearchAble'))
    suiteTest.addTest(TestTeachingSchedule('test_21_PrintAble'))
    return suiteTest


if __name__ == '__main__':
    # 存放路径
    filepath = "E:/PyProject/zhkuTest/TestReport/report_teachingschedule.html"
    fp = open(filepath, 'wb')
    # 定义测试报告的标题和描述
    runner = HTMLTestRunner.HTMLTestRunner(
        stream=fp,
        title=u'教学安排表',
        description=u'用例测试情况'
    )
    runner.run(suite())
    fp.close()
