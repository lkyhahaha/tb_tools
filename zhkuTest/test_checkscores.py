from time import sleep
from selenium import webdriver
import unittest
import HTMLTestRunner

from zhkuTest import login


class TestCheckScores(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()
        cls.base_url = "http://jw.zhku.edu.cn/home.aspx"
        login.login(cls)
        cls.driver.switch_to.frame("frmbody")
        # 学生成绩
        cls.driver.find_element_by_id('memuBarText6').click()
        # 查看成绩
        cls.driver.find_element_by_xpath("//span[@value='../xscj/Stu_MyScore.aspx']").click()
        sleep(2)
        cls.driver.switch_to.frame("frmMain")

    def test_0_OriginalScores1(self):
        u'''点击原始成绩，原始成绩选中'''
        self.driver.find_element_by_id('ys_sj').click()
        sleep(1)
        selected = self.driver.find_element_by_id('ys_sj').is_selected()
        # print(selected)
        self.assertTrue(selected)

    def test_10_OriginalScores2(self):
        u'''点击原始成绩，有效成绩不选中'''
        self.driver.find_element_by_id('ys_sj').click()
        sleep(1)
        selected = self.driver.find_element_by_id('yx_sj').is_selected()
        self.assertFalse(selected)

    def test_11_EffectiveScores1(self):
        u'''点击有效成绩，有效成绩选中'''
        self.driver.find_element_by_id('yx_sj').click()
        sleep(1)
        selected = self.driver.find_element_by_id('yx_sj').is_selected()
        self.assertTrue(selected)

    def test_12_EffectiveScores2(self):
        u'''点击有效成绩，原始成绩不选中'''
        self.driver.find_element_by_id('yx_sj').click()
        sleep(1)
        selected = self.driver.find_element_by_id('ys_sj').is_selected()
        self.assertFalse(selected)

    def test_13_SinceEntrance1(self):
        u'''点击入学以来，学年下拉框禁用'''
        self.driver.find_element_by_xpath("//label[@for='SelXNXQ_0']").click()
        sleep(1)
        state = self.driver.find_element_by_id('sel_xn').is_enabled()
        self.assertFalse(state)

    def test_14_SinceEntrance2(self):
        u'''点击入学以来，学期下拉框禁用'''
        self.driver.find_element_by_id('SelXNXQ_0').click()
        sleep(1)
        state = self.driver.find_element_by_id('sel_xq').is_enabled()
        self.assertFalse(state)

    def test_15_SinceEntrance3(self):
        u'''点击入学以来，入学以来选项选中'''
        self.driver.find_element_by_id('SelXNXQ_0').click()
        sleep(1)
        selected = self.driver.find_element_by_id('SelXNXQ_0').is_selected()
        self.assertTrue(selected)

    def test_16_SinceEntrance4(self):
        u'''点击入学以来，学年选项不选中'''
        self.driver.find_element_by_id('SelXNXQ_0').click()
        sleep(1)
        selected = self.driver.find_element_by_id('SelXNXQ_1').is_selected()
        self.assertFalse(selected)

    def test_17_SinceEntrance5(self):
        u'''点击入学以来，学期选项不选中'''
        self.driver.find_element_by_id('SelXNXQ_0').click()
        sleep(1)
        selected = self.driver.find_element_by_id('SelXNXQ_2').is_selected()
        self.assertFalse(selected)

    def test_18_AcademicYear1(self):
        u'''点击学年，学年下拉框可用'''
        self.driver.find_element_by_id('SelXNXQ_1').click()
        sleep(1)
        state = self.driver.find_element_by_id('sel_xn').is_enabled()
        self.assertTrue(state)

    def test_19_AcademicYear2(self):
        u'''点击学年，学期下拉框禁用'''
        self.driver.find_element_by_id('SelXNXQ_1').click()
        sleep(1)
        state = self.driver.find_element_by_id('sel_xq').is_enabled()
        self.assertFalse(state)

    def test_20_AcademicYear3(self):
        u'''点击学年，学年选项选中'''
        self.driver.find_element_by_id('SelXNXQ_1').click()
        sleep(1)
        selected = self.driver.find_element_by_id('SelXNXQ_1').is_selected()
        self.assertTrue(selected)

    def test_21_AcademicYear4(self):
        u'''点击学年，入学以来选项不选中'''
        self.driver.find_element_by_id('SelXNXQ_1').click()
        sleep(1)
        selected = self.driver.find_element_by_id('SelXNXQ_0').is_selected()
        self.assertFalse(selected)

    def test_22_AcademicYear5(self):
        u'''点击学年，学期选项不选中'''
        self.driver.find_element_by_id('SelXNXQ_1').click()
        sleep(1)
        selected = self.driver.find_element_by_id('SelXNXQ_2').is_selected()
        self.assertFalse(selected)

    def test_23_Semester1(self):
        u'''点击学期，学年下拉框可用'''
        self.driver.find_element_by_id('SelXNXQ_2').click()
        sleep(1)
        state = self.driver.find_element_by_id('sel_xn').is_enabled()
        self.assertTrue(state)

    def test_24_Semester2(self):
        u'''点击学期，学期下拉框可用'''
        self.driver.find_element_by_id('SelXNXQ_2').click()
        sleep(1)
        state = self.driver.find_element_by_id('sel_xq').is_enabled()
        self.assertTrue(state)

    def test_25_Semester3(self):
        u'''点击学期，学期选项选中'''
        self.driver.find_element_by_id('SelXNXQ_2').click()
        sleep(1)
        selected = self.driver.find_element_by_id('SelXNXQ_2').is_selected()
        self.assertTrue(selected)

    def test_26_Semester4(self):
        u'''点击学期，入学以来不选中'''
        self.driver.find_element_by_id('SelXNXQ_2').click()
        sleep(1)
        selected = self.driver.find_element_by_id('SelXNXQ_0').is_selected()
        self.assertFalse(selected)

    def test_27_Semester5(self):
        u'''点击学期，学年不选中'''
        self.driver.find_element_by_id('SelXNXQ_2').click()
        sleep(1)
        selected = self.driver.find_element_by_id('SelXNXQ_1').is_selected()
        self.assertFalse(selected)

    def test_28_Major1(self):
        u'''点击主修，主修选中'''
        self.driver.find_element_by_id('zfx_flag_0').click()
        sleep(1)
        selected = self.driver.find_element_by_id('zfx_flag_0').is_selected()
        self.assertTrue(selected)

    def test_29_Major2(self):
        u'''点击主修，辅修不选中'''
        self.driver.find_element_by_id('zfx_flag_0').click()
        sleep(1)
        selected = self.driver.find_element_by_id('zfx_flag_1').is_selected()
        self.assertFalse(selected)

    def test_30_Minor1(self):
        u'''点击辅修，辅修选中'''
        self.driver.find_element_by_id('zfx_flag_1').click()
        sleep(1)
        selected = self.driver.find_element_by_id('zfx_flag_1').is_selected()
        self.assertTrue(selected)

    def test_31_Minor2(self):
        u'''点击辅修，主修不选中'''
        self.driver.find_element_by_id('zfx_flag_1').click()
        sleep(1)
        selected = self.driver.find_element_by_id('zfx_flag_0').is_selected()
        self.assertFalse(selected)

    def test_32_SearchAble(self):
        u'''检索按钮可用'''
        search = self.driver.find_element_by_name('btn_search')
        state = search.is_enabled()
        self.assertTrue(state)

    def test_33_PrintAble(self):
        u'''打印按钮可用'''
        button = self.driver.find_element_by_id('print')
        state = button.is_enabled()
        self.assertTrue(state)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


# 定义一个测试套
def suite():
    suiteTest = unittest.TestSuite()
    suiteTest.addTest(TestCheckScores('test_0_OriginalScores1'))
    suiteTest.addTest(TestCheckScores('test_10_OriginalScores2'))
    suiteTest.addTest(TestCheckScores('test_11_EffectiveScores1'))
    suiteTest.addTest(TestCheckScores('test_12_EffectiveScores2'))
    suiteTest.addTest(TestCheckScores('test_13_SinceEntrance1'))
    suiteTest.addTest(TestCheckScores('test_14_SinceEntrance2'))
    suiteTest.addTest(TestCheckScores('test_15_SinceEntrance3'))
    suiteTest.addTest(TestCheckScores('test_16_SinceEntrance4'))
    suiteTest.addTest(TestCheckScores('test_17_SinceEntrance5'))
    suiteTest.addTest(TestCheckScores('test_18_AcademicYear1'))
    suiteTest.addTest(TestCheckScores('test_19_AcademicYear2'))
    suiteTest.addTest(TestCheckScores('test_20_AcademicYear3'))
    suiteTest.addTest(TestCheckScores('test_21_AcademicYear4'))
    suiteTest.addTest(TestCheckScores('test_22_AcademicYear5'))
    suiteTest.addTest(TestCheckScores('test_23_Semester1'))
    suiteTest.addTest(TestCheckScores('test_24_Semester2'))
    suiteTest.addTest(TestCheckScores('test_25_Semester3'))
    suiteTest.addTest(TestCheckScores('test_26_Semester4'))
    suiteTest.addTest(TestCheckScores('test_27_Semester5'))
    suiteTest.addTest(TestCheckScores('test_28_Major1'))
    suiteTest.addTest(TestCheckScores('test_29_Major2'))
    suiteTest.addTest(TestCheckScores('test_30_Minor1'))
    suiteTest.addTest(TestCheckScores('test_31_Minor2'))
    suiteTest.addTest(TestCheckScores('test_32_SearchAble'))
    suiteTest.addTest(TestCheckScores('test_33_PrintAble'))
    return suiteTest


if __name__ == '__main__':
    # 存放路径
    filepath = "E:/PyProject/zhkuTest/TestReport/report_checkscores.html"
    fp = open(filepath, 'wb')
    # 定义测试报告的标题和描述
    runner = HTMLTestRunner.HTMLTestRunner(
        stream=fp,
        title=u'查看成绩',
        description=u'用例测试情况'
    )
    runner.run(suite())
    fp.close()
