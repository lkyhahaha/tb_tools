from time import sleep
from selenium import webdriver
import unittest
import HTMLTestRunner

from zhkuTest import login


class TestMenu(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()
        cls.base_url = "http://jw.zhku.edu.cn/home.aspx"
        cls.driver.refresh()
        login.login(cls)

    # 学生学籍-学籍档案-基本信息
    def test_0_BasicInfo(self):
        u'''基本信息'''
        self.driver.switch_to.frame("frmbody")
        # 学生学籍
        self.driver.find_element_by_id('memuBarText1').click()
        # 学籍档案
        self.driver.find_element_by_xpath("//td[@id='memuLinkDiv1']/table/tbody/tr[2]/td[2]").click()
        # 基本信息
        self.driver.find_element_by_xpath("//td[@value='../xsxj/Stu_MyInfo.aspx']").click()
        sleep(3)
        # 断言
        self.driver.switch_to.frame("frmMain")
        text = self.driver.find_element_by_xpath("//body/table[1]/tbody/tr[1]/td[1]").text
        self.assertEqual(text, '基本信息')
        # 返回左侧目录栏iframe(frmbody)
        self.driver.switch_to.parent_frame()
        # 点击收起学籍档案
        self.driver.find_element_by_xpath("//td[@id='memuLinkDiv1']/table/tbody/tr[2]/td[2]").click()
        # 返回主iframe
        self.driver.switch_to.default_content()

    # 学生学籍-学籍档案-辅修报名
    def test_10_MinorRegistration(self):
        u'''辅修报名'''
        self.driver.switch_to.frame("frmbody")
        # 学生学籍
        self.driver.find_element_by_id('memuBarText1').click()
        # 学籍档案
        self.driver.find_element_by_xpath("//td[@id='memuLinkDiv1']/table/tbody/tr[2]/td[2]").click()
        # 辅修报名
        self.driver.find_element_by_xpath("//td[@value='../xsxj/Stu_fxzy_bm.aspx']").click()
        sleep(3)
        # 断言
        self.driver.switch_to.frame("frmMain")
        text = self.driver.find_element_by_xpath("//body/table[1]/tbody/tr[1]/td[1]").text
        self.assertEqual(text, '辅修报名')
        # 返回左侧目录栏iframe(frmbody)
        self.driver.switch_to.parent_frame()
        # 点击收起学籍档案
        self.driver.find_element_by_xpath("//td[@id='memuLinkDiv1']/table/tbody/tr[2]/td[2]").click()
        # 返回主iframe
        self.driver.switch_to.default_content()

    # 学生学籍-学籍档案-奖惩信息
    def test_11_RewardsPunishments(self):
        u'''奖惩信息'''
        self.driver.switch_to.frame("frmbody")
        # 学生学籍
        self.driver.find_element_by_id('memuBarText1').click()
        # 学籍档案
        self.driver.find_element_by_xpath("//td[@id='memuLinkDiv1']/table/tbody/tr[2]/td[2]").click()
        # 奖惩信息
        self.driver.find_element_by_xpath("//td[@value='../xsxj/Stu_xscjxx.aspx']").click()
        sleep(3)
        # 断言
        self.driver.switch_to.frame("frmMain")
        text = self.driver.find_element_by_xpath("//body/table[1]/tbody/tr[1]/td[1]").text
        self.assertEqual(text, '奖惩信息')
        # 返回左侧目录栏iframe(frmbody)
        self.driver.switch_to.parent_frame()
        # 点击收起学籍档案
        self.driver.find_element_by_xpath("//td[@id='memuLinkDiv1']/table/tbody/tr[2]/td[2]").click()
        # 返回主iframe
        self.driver.switch_to.default_content()

    # 学生学籍-学籍异动-学业预警
    def test_12_AcademicWarning(self):
        u'''学业预警'''
        self.driver.switch_to.frame("frmbody")
        # 学生学籍
        self.driver.find_element_by_id('memuBarText1').click()
        # 学籍异动
        self.driver.find_element_by_xpath("//td[@id='memuLinkDiv1']/table/tbody/tr[5]/td[2]").click()
        # 学业预警
        self.driver.find_element_by_xpath("//td[@value='../xsxj/Stu_xyyj.aspx']").click()
        sleep(3)
        # 断言
        self.driver.switch_to.frame("frmMain")
        text = self.driver.find_element_by_xpath("//body/table[1]/tbody/tr[1]/td[1]").text
        self.assertEqual(text, '学业预警')
        # 返回左侧目录栏iframe(frmbody)
        self.driver.switch_to.parent_frame()
        # 点击收起学籍异动
        self.driver.find_element_by_xpath("//td[@id='memuLinkDiv1']/table/tbody/tr[5]/td[2]").click()
        # 返回主iframe
        self.driver.switch_to.default_content()

    # 学生学籍-学籍异动-申请异动
    def test_13_ApplyMove(self):
        u'''申请异动'''
        self.driver.switch_to.frame("frmbody")
        # 学生学籍
        self.driver.find_element_by_id('memuBarText1').click()
        # 学籍异动
        self.driver.find_element_by_xpath("//td[@id='memuLinkDiv1']/table/tbody/tr[5]/td[2]").click()
        # 申请异动
        self.driver.find_element_by_xpath("//td[@value='../xsxj/Stu_ydsq.aspx']").click()
        sleep(3)
        # 断言
        self.driver.switch_to.frame("frmMain")
        text = self.driver.find_element_by_xpath("//body/table[1]/tbody/tr[1]/td[1]").text
        self.assertEqual(text, '申请异动')
        # 返回左侧目录栏iframe(frmbody)
        self.driver.switch_to.parent_frame()
        # 点击收起学籍异动
        self.driver.find_element_by_xpath("//td[@id='memuLinkDiv1']/table/tbody/tr[5]/td[2]").click()
        # 返回主iframe
        self.driver.switch_to.default_content()

    # 学生学籍-学籍异动-预计异动信息
    def test_14_PredictMove(self):
        u'''预计异动信息'''
        self.driver.switch_to.frame("frmbody")
        # 学生学籍
        self.driver.find_element_by_id('memuBarText1').click()
        # 学籍异动
        self.driver.find_element_by_xpath("//td[@id='memuLinkDiv1']/table/tbody/tr[5]/td[2]").click()
        # 预计异动信息
        self.driver.find_element_by_xpath("//td[@value='../xsxj/Stu_yjqdxx.aspx']").click()
        sleep(3)
        # 断言
        self.driver.switch_to.frame("frmMain")
        text = self.driver.find_element_by_xpath("//body/table[1]/tbody/tr[1]/td[1]").text
        self.assertEqual(text, '预计异动信息')
        # 返回左侧目录栏iframe(frmbody)
        self.driver.switch_to.parent_frame()
        # 点击收起学籍异动
        self.driver.find_element_by_xpath("//td[@id='memuLinkDiv1']/table/tbody/tr[5]/td[2]").click()
        # 返回主iframe
        self.driver.switch_to.default_content()

    # 学生学籍-学籍异动-异动信息
    def test_15_MoveInfo(self):
        u'''预计异动信息'''
        self.driver.switch_to.frame("frmbody")
        # 学生学籍
        self.driver.find_element_by_id('memuBarText1').click()
        # 学籍异动
        self.driver.find_element_by_xpath("//td[@id='memuLinkDiv1']/table/tbody/tr[5]/td[2]").click()
        # 异动信息
        self.driver.find_element_by_xpath("//td[@value='../xsxj/Stu_xsydxs.aspx']").click()
        sleep(3)
        # 断言
        self.driver.switch_to.frame("frmMain")
        text = self.driver.find_element_by_xpath("//body/table[1]/tbody/tr[1]/td[1]").text
        self.assertEqual(text, '异动信息')
        # 返回左侧目录栏iframe(frmbody)
        self.driver.switch_to.parent_frame()
        # 点击收起学籍异动
        self.driver.find_element_by_xpath("//td[@id='memuLinkDiv1']/table/tbody/tr[5]/td[2]").click()
        # 返回主iframe
        self.driver.switch_to.default_content()

    # 学生学籍-毕业事宜-学业进展
    def test_16_AcademicProgress(self):
        u'''学业进展'''
        self.driver.switch_to.frame("frmbody")
        # 学生学籍
        self.driver.find_element_by_id('memuBarText1').click()
        # 毕业事宜
        self.driver.find_element_by_xpath("//td[@id='memuLinkDiv1']/table/tbody/tr[7]/td[2]").click()
        # 学业进展
        self.driver.find_element_by_xpath("//td[@value='../xsxj/Stu_xyjzqk.aspx']").click()
        sleep(2)
        # 断言
        self.driver.switch_to.frame("frmMain")
        text = self.driver.find_element_by_xpath("//form[@id='form1']/table[1]/tbody/tr[1]/td[1]").text
        self.assertEqual(text, '学业进展')
        # 返回左侧目录栏iframe(frmbody)
        self.driver.switch_to.parent_frame()
        # 点击收起毕业事宜
        self.driver.find_element_by_xpath("//td[@id='memuLinkDiv1']/table/tbody/tr[7]/td[2]").click()
        # 返回主iframe
        self.driver.switch_to.default_content()

    # 学生学籍-毕业事宜-申请提前/推迟毕业
    def test_17_ApplyGraduation(self):
        u'''申请提前/推迟毕业'''
        self.driver.switch_to.frame("frmbody")
        # 学生学籍
        self.driver.find_element_by_id('memuBarText1').click()
        # 毕业事宜
        self.driver.find_element_by_xpath("//td[@id='memuLinkDiv1']/table/tbody/tr[7]/td[2]").click()
        # 申请提前/推迟毕业
        self.driver.find_element_by_xpath("//td[@value='../xsxj/Stu_tqtcby.aspx']").click()
        sleep(2)
        # 断言
        self.driver.switch_to.frame("frmMain")
        text = self.driver.find_element_by_xpath("//body/table[1]/tbody/tr[1]/td[1]").text
        self.assertEqual(text, '申请提前/推迟毕业')
        # 返回左侧目录栏iframe(frmbody)
        self.driver.switch_to.parent_frame()
        # 点击收起毕业事宜
        self.driver.find_element_by_xpath("//td[@id='memuLinkDiv1']/table/tbody/tr[7]/td[2]").click()
        # 返回主iframe
        self.driver.switch_to.default_content()

    # 学生学籍-毕业事宜-毕业审核结论
    def test_18_GraduationConclusion(self):
        u'''毕业审核结论'''
        self.driver.switch_to.frame("frmbody")
        # 学生学籍
        self.driver.find_element_by_id('memuBarText1').click()
        # 毕业事宜
        self.driver.find_element_by_xpath("//td[@id='memuLinkDiv1']/table/tbody/tr[7]/td[2]").click()
        # 毕业审核结论
        self.driver.find_element_by_xpath("//td[@value='../xsxj/Stu_byshjl.aspx']").click()
        sleep(2)
        # 断言
        self.driver.switch_to.frame("frmMain")
        text = self.driver.find_element_by_xpath("//body/table[1]/tbody/tr[1]/td[1]").text
        self.assertEqual(text, '毕业审核结论')
        # 返回左侧目录栏iframe(frmbody)
        self.driver.switch_to.parent_frame()
        # 点击收起毕业事宜
        self.driver.find_element_by_xpath("//td[@id='memuLinkDiv1']/table/tbody/tr[7]/td[2]").click()
        # 返回主iframe
        self.driver.switch_to.default_content()

    # 培养方案-理论课程
    def test_19_TheoryCourse(self):
        u'''理论课程'''
        self.driver.switch_to.frame("frmbody")
        # 培养方案
        self.driver.find_element_by_id('memuBarText2').click()
        # 理论课程
        self.driver.find_element_by_xpath("//span[@value='../jxjh/Stu_byfakc.aspx']").click()
        sleep(2)
        # 断言
        self.driver.switch_to.frame("frmMain")
        text = self.driver.find_element_by_xpath("//form[@id='form1']/table[1]/tbody/tr[1]/td[1]").text
        self.assertEqual(text, '理论课程')
        # 返回主iframe
        self.driver.switch_to.default_content()

    # 培养方案-实践环节
    def test_20_PracticeSection(self):
        u'''实践环节'''
        self.driver.switch_to.frame("frmbody")
        # 培养方案
        self.driver.find_element_by_id('memuBarText2').click()
        # 实践环节
        self.driver.find_element_by_xpath("//span[@value='../jxjh/Stu_byfahj.aspx']").click()
        sleep(2)
        # 断言
        self.driver.switch_to.frame("frmMain")
        text = self.driver.find_element_by_xpath("//body/table[1]/tbody/tr[1]/td[1]").text
        self.assertEqual(text, '实践环节')
        # 返回主iframe
        self.driver.switch_to.default_content()

    # 培养方案-毕业学分要求
    def test_21_CreditRequirements(self):
        u'''毕业学分要求'''
        self.driver.switch_to.frame("frmbody")
        # 培养方案
        self.driver.find_element_by_id('memuBarText2').click()
        # 毕业学分要求
        self.driver.find_element_by_xpath("//span[@value='../jxjh/Stu_byxfyq.aspx']").click()
        sleep(2)
        # 断言
        self.driver.switch_to.frame("frmMain")
        text = self.driver.find_element_by_xpath("//body/table[1]/tbody/tr[1]/td[1]").text
        self.assertEqual(text, '毕业学分要求')
        # 返回主iframe
        self.driver.switch_to.default_content()

    # 网上选课-预选
    def test_22_Primary(self):
        u'''预选'''
        self.driver.switch_to.frame("frmbody")
        # 网上选课
        self.driver.find_element_by_id('memuBarText3').click()
        # 预选
        self.driver.find_element_by_xpath("//span[@value='../wsxk/stu_xsyx.aspx']").click()
        sleep(2)
        # 断言
        self.driver.switch_to.frame("frmMain")
        text = self.driver.find_element_by_xpath("//form[@name='form1']/table[1]/tbody/tr[1]/td[1]").text
        self.assertEqual(text, '预选')
        # 返回主iframe
        self.driver.switch_to.default_content()

    # 网上选课-预选结果
    def test_23_PrimaryResult(self):
        u'''预选结果'''
        self.driver.switch_to.frame("frmbody")
        # 网上选课
        self.driver.find_element_by_id('memuBarText3').click()
        # 预选结果
        self.driver.find_element_by_xpath("//span[@value='../wsxk/stu_yxjg.aspx']").click()
        sleep(2)
        # 断言
        self.driver.switch_to.frame("frmMain")
        text = self.driver.find_element_by_xpath("//body/table[1]/tbody/tr[1]/td[1]").text
        self.assertEqual(text, '预选结果')
        # 返回主iframe
        self.driver.switch_to.default_content()

    # 网上选课-正选
    def test_24_Gregory(self):
        u'''正选'''
        self.driver.switch_to.frame("frmbody")
        # 网上选课
        self.driver.find_element_by_id('memuBarText3').click()
        # 正选
        self.driver.find_element_by_xpath("//span[@value='../wsxk/stu_xszx.aspx']").click()
        sleep(2)
        # 断言
        self.driver.switch_to.frame("frmMain")
        text = self.driver.find_element_by_xpath("//form[@name='form1']/table[1]/tbody/tr[1]/td[1]").text
        self.assertEqual(text, '正选')
        # 返回主iframe
        self.driver.switch_to.default_content()

    # 网上选课-正选结果
    def test_25_GregoryResult(self):
        u'''正选结果'''
        self.driver.switch_to.frame("frmbody")
        # 网上选课
        self.driver.find_element_by_id('memuBarText3').click()
        # 正选结果
        self.driver.find_element_by_xpath("//span[@value='../wsxk/stu_zxjg.aspx']").click()
        sleep(2)
        # 断言
        self.driver.switch_to.frame("frmMain")
        text = self.driver.find_element_by_xpath("//body/table[1]/tbody/tr[1]/td[1]").text
        self.assertEqual(text, '正选结果')
        # 返回主iframe
        self.driver.switch_to.default_content()

    # 网上选课-补选
    def test_26_ByElection(self):
        u'''补选'''
        self.driver.switch_to.frame("frmbody")
        # 网上选课
        self.driver.find_element_by_id('memuBarText3').click()
        # 补选
        self.driver.find_element_by_xpath("//span[@value='../wsxk/stu_btx.aspx']").click()
        sleep(2)
        # 断言
        self.driver.switch_to.frame("frmMain")
        text = self.driver.find_element_by_xpath("//form[@name='form1']/table[1]/tbody/tr[1]/td[1]").text
        self.assertEqual(text, '补选')
        # 返回主iframe
        self.driver.switch_to.default_content()

    # 网上选课-退选
    def test_27_DropChoose(self):
        u'''退选'''
        self.driver.switch_to.frame("frmbody")
        # 网上选课
        self.driver.find_element_by_id('memuBarText3').click()
        # 退选
        self.driver.find_element_by_xpath("//span[@value='../wsxk/stu_txjg.aspx']").click()
        sleep(2)
        # 断言
        self.driver.switch_to.frame("frmMain")
        text = self.driver.find_element_by_xpath("//body/table[1]/tbody/tr[1]/td[1]").text
        self.assertEqual(text, '退选')
        # 返回主iframe
        self.driver.switch_to.default_content()

    # 网上选课-被取消课程
    def test_28_CancelledCourse(self):
        u'''被取消课程'''
        self.driver.switch_to.frame("frmbody")
        # 网上选课
        self.driver.find_element_by_id('memuBarText3').click()
        # 被取消课程
        self.driver.find_element_by_xpath("//span[@value='../wsxk/stu_bqxkc.aspx']").click()
        sleep(2)
        # 断言
        self.driver.switch_to.frame("frmMain")
        text = self.driver.find_element_by_xpath("//body/table[1]/tbody/tr[1]/td[1]").text
        self.assertEqual(text, '被取消课程')
        # 返回主iframe
        self.driver.switch_to.default_content()

    # 教学安排-教学安排表
    def test_29_TeachingSchedule(self):
        u'''教学安排表'''
        self.driver.switch_to.frame("frmbody")
        # 教学安排
        self.driver.find_element_by_id('memuBarText4').click()
        # 教学安排表
        self.driver.find_element_by_xpath("//span[@value='../znpk/Pri_StuSel.aspx']").click()
        sleep(2)
        # 断言
        self.driver.switch_to.frame("frmMain")
        text = self.driver.find_element_by_xpath("//form[@name='form']/table[1]/tbody/tr[1]/td[1]").text
        self.assertEqual(text, '教学安排表')
        # 返回主iframe
        self.driver.switch_to.default_content()

    # 教学安排-调/停课信息
    def test_30_CourseChangeInfo(self):
        u'''调/停课信息'''
        self.driver.switch_to.frame("frmbody")
        # 教学安排
        self.driver.find_element_by_id('memuBarText4').click()
        # 调/停课信息
        self.driver.find_element_by_xpath("//span[@value='../znpk/Pri_StuJXAPTZXX.aspx']").click()
        sleep(2)
        # 断言
        self.driver.switch_to.frame("frmMain")
        text = self.driver.find_element_by_xpath("//body/table[1]/tbody/tr[1]/td[1]").text
        self.assertEqual(text, '调/停课信息')
        # 返回主iframe
        self.driver.switch_to.default_content()

    # 考试安排-考试安排表
    def test_31_ExaminationSchedule(self):
        u'''考试安排表'''
        self.driver.switch_to.frame("frmbody")
        # 考试安排
        self.driver.find_element_by_id('memuBarText5').click()
        # 考试安排表
        self.driver.find_element_by_xpath("//span[@value='../KSSW/stu_ksap.aspx']").click()
        sleep(2)
        # 断言
        self.driver.switch_to.frame("frmMain")
        text = self.driver.find_element_by_xpath("//form[@name='form1']/table[1]/tbody/tr[1]/td[1]").text
        self.assertEqual(text, '考试安排表')
        # 返回主iframe
        self.driver.switch_to.default_content()

    # 考试安排-考试通报信息
    def test_32_TestReportInfo(self):
        u'''考试通报信息'''
        self.driver.switch_to.frame("frmbody")
        # 考试安排
        self.driver.find_element_by_id('memuBarText5').click()
        # 考试通报信息
        self.driver.find_element_by_xpath("//span[@value='../KSSW/stu_kstb.aspx']").click()
        sleep(2)
        # 断言
        self.driver.switch_to.frame("frmMain")
        text = self.driver.find_element_by_xpath("//body/table[1]/tbody/tr[1]/td[1]").text
        self.assertEqual(text, '考试通报信息')
        # 返回主iframe
        self.driver.switch_to.default_content()

    # 学生成绩-重修报名
    def test_33_RetakeRegistration(self):
        u'''重修报名'''
        self.driver.switch_to.frame("frmbody")
        # 学生成绩
        self.driver.find_element_by_id('memuBarText6').click()
        # 重修报名
        self.driver.find_element_by_xpath("//span[@value='../xscj/Stu_xscxsq.aspx']").click()
        sleep(2)
        # 断言
        self.driver.switch_to.frame("frmMain")
        text = self.driver.find_element_by_xpath("//form[@name='form1']/table[1]/tbody/tr[1]/td[1]").text
        self.assertEqual(text, '重修报名')
        # 返回主iframe
        self.driver.switch_to.default_content()

    # 学生成绩-获准重修课程/环节
    def test_34_RetakePermission(self):
        u'''获准重修课程/环节'''
        self.driver.switch_to.frame("frmbody")
        # 学生成绩
        self.driver.find_element_by_id('memuBarText6').click()
        # 获准重修课程/环节
        self.driver.find_element_by_xpath("//span[@value='../xscj/Stu_cxkc.aspx']").click()
        sleep(2)
        # 断言
        self.driver.switch_to.frame("frmMain")
        text = self.driver.find_element_by_xpath("//body/table[1]/tbody/tr[1]/td[1]").text
        self.assertEqual(text, '获准重修课程/环节')
        # 返回主iframe
        self.driver.switch_to.default_content()

    # 学生成绩-查看成绩认定记录
    def test_35_AchievementRecord(self):
        u'''查看成绩认定记录'''
        self.driver.switch_to.frame("frmbody")
        # 学生成绩
        self.driver.find_element_by_id('memuBarText6').click()
        # 查看成绩认定记录
        self.driver.find_element_by_xpath("//span[@value='../xscj/c_ydcjrdjl.aspx']").click()
        sleep(2)
        # 断言
        self.driver.switch_to.frame("frmMain")
        text = self.driver.find_element_by_xpath("//form[@name='form1']/table[1]/tbody/tr[1]/td[1]").text
        self.assertEqual(text, '查看成绩认定记录')
        # 返回主iframe
        self.driver.switch_to.default_content()

    # 学生成绩-查看成绩
    def test_36_CheckScores(self):
        u'''查看成绩'''
        self.driver.switch_to.frame("frmbody")
        # 学生成绩
        self.driver.find_element_by_id('memuBarText6').click()
        # 查看成绩
        self.driver.find_element_by_xpath("//span[@value='../xscj/Stu_MyScore.aspx']").click()
        sleep(2)
        # 断言
        self.driver.switch_to.frame("frmMain")
        text = self.driver.find_element_by_xpath("//form[@name='form1']/table[1]/tbody/tr[1]/td[1]").text
        self.assertEqual(text, '查看成绩')
        # 返回主iframe
        self.driver.switch_to.default_content()

    # 学生成绩-成绩分布
    def test_37_GradeDistribution(self):
        u'''成绩分布'''
        self.driver.switch_to.frame("frmbody")
        # 学生成绩
        self.driver.find_element_by_id('memuBarText6').click()
        # 成绩分布
        self.driver.find_element_by_xpath("//span[@value='../xscj/Stu_cjfb.aspx']").click()
        sleep(2)
        # 断言
        self.driver.switch_to.frame("frmMain")
        text = self.driver.find_element_by_xpath("//body/table[1]/tbody/tr[1]/td[1]").text
        self.assertEqual(text, '成绩分布')
        # 返回主iframe
        self.driver.switch_to.default_content()

    # 学生成绩-等级考试报名
    def test_38_LevelExamRegistration(self):
        u'''等级考试报名'''
        self.driver.switch_to.frame("frmbody")
        # 学生成绩
        self.driver.find_element_by_id('memuBarText6').click()
        # 等级考试报名
        self.driver.find_element_by_xpath("//span[@value='../xscj/Stu_djksbm.aspx']").click()
        sleep(2)
        # 断言
        self.driver.switch_to.frame("frmMain")
        text = self.driver.find_element_by_xpath("//body/table[1]/tbody/tr[1]/td[1]").text
        self.assertEqual(text, '等级考试报名')
        # 返回主iframe
        self.driver.switch_to.default_content()

    # 学生成绩-查看等级考试成绩
    def test_39_LevelExamScores(self):
        u'''查看等级考试成绩'''
        self.driver.switch_to.frame("frmbody")
        # 学生成绩
        self.driver.find_element_by_id('memuBarText6').click()
        # 查看等级考试成绩
        self.driver.find_element_by_xpath("//span[@value='../xscj/Stu_djkscj.aspx']").click()
        sleep(2)
        # 断言
        self.driver.switch_to.frame("frmMain")
        text = self.driver.find_element_by_xpath("//body/table[1]/tbody/tr[1]/td[1]").text
        self.assertEqual(text, '查看等级考试成绩')
        # 返回主iframe
        self.driver.switch_to.default_content()

    # 教材信息-领取教材信息
    def test_40_ReceiveTextBookInfo(self):
        u'''领取教材信息'''
        self.driver.switch_to.frame("frmbody")
        # 教材信息
        self.driver.find_element_by_id('memuBarText7').click()
        # 领取教材信息
        self.driver.find_element_by_xpath("//span[@value='../jcgl/Stu_CKLQJCXX.aspx']").click()
        sleep(2)
        # 断言
        self.driver.switch_to.frame("frmMain")
        text = self.driver.find_element_by_xpath("//body/table[1]/tbody/tr[1]/td[1]").text
        self.assertEqual(text, '领取教材信息')
        # 返回主iframe
        self.driver.switch_to.default_content()

    # 教材信息-领取教材对帐
    def test_41_TextbookReconciliation(self):
        u'''领取教材对帐'''
        self.driver.switch_to.frame("frmbody")
        # 教材信息
        self.driver.find_element_by_id('memuBarText7').click()
        # 领取教材对帐
        self.driver.find_element_by_xpath("//span[@value='../jcgl/R_SK_FXSDZMX.aspx']").click()
        sleep(2)
        # 断言
        self.driver.switch_to.frame("frmMain")
        text = self.driver.find_element_by_xpath("//body/table[1]/tbody/tr[1]/td[1]").text
        self.assertEqual(text, '领取教材对帐')
        # 返回主iframe
        self.driver.switch_to.default_content()

    # 教材信息-有售教材信息
    def test_42_TextbookSale(self):
        u'''有售教材信息'''
        self.driver.switch_to.frame("frmbody")
        # 教材信息
        self.driver.find_element_by_id('memuBarText7').click()
        # 有售教材信息
        self.driver.find_element_by_xpath("//span[@value='../JCGL/R_JCGL_KCJC_A3.aspx']").click()
        sleep(2)
        # 断言
        self.driver.switch_to.frame("frmMain")
        text = self.driver.find_element_by_xpath("//form[@name='form1']/table[1]/tbody/tr[1]/td[1]").text
        self.assertEqual(text, '有售教材信息')
        # 返回主iframe
        self.driver.switch_to.default_content()

    # 网上评教-提交问卷调查表
    def test_43_SubmitQuestionnaire(self):
        u'''提交问卷调查表'''
        self.driver.switch_to.frame("frmbody")
        # 网上评教
        self.driver.find_element_by_id('memuBarText8').click()
        # 提交问卷调查表
        self.driver.find_element_by_xpath("//span[@value='../jxkp/Stu_yjjy.aspx']").click()
        sleep(2)
        # 断言
        self.driver.switch_to.frame("frmMain")
        text = self.driver.find_element_by_xpath("//form[@name='form1']/table[1]/tbody/tr[1]/td[1]").text
        self.assertEqual(text, '提交问卷调查表')
        # 返回主iframe
        self.driver.switch_to.default_content()

    # 网上评教-提交教学评价表
    def test_44_EvaluationForm(self):
        u'''提交教学评价表'''
        self.driver.switch_to.frame("frmbody")
        # 网上评教
        self.driver.find_element_by_id('memuBarText8').click()
        # 提交教学评价表
        self.driver.find_element_by_xpath("//span[@value='../jxkp/Stu_wskp.aspx']").click()
        sleep(2)
        # 断言
        self.driver.switch_to.frame("frmMain")
        text = self.driver.find_element_by_xpath("//form[@name='form1']/table[1]/tbody/tr[1]/td[1]").text
        self.assertEqual(text, '提交教学评价表')
        # 返回主iframe
        self.driver.switch_to.default_content()

    # 其他-修改个人密码
    def test_45_ChangePassword(self):
        u'''修改个人密码'''
        self.driver.switch_to.frame("frmbody")
        # 其他
        self.driver.find_element_by_id('memuBarText9').click()
        # 修改个人密码
        self.driver.find_element_by_xpath("//span[@value='../MyWeb/User_ModPWD.aspx']").click()
        sleep(2)
        # 断言
        self.driver.switch_to.frame("frmMain")
        text = self.driver.find_element_by_xpath(
            "//form[@name='Form1']/table[1]/tbody/tr[1]/td[1]/table[1]/tbody/tr[1]/td[1]/table/tbody/tr[1]/td[1]").text
        self.assertEqual(text, '修改个人密码')
        # 返回主iframe
        self.driver.switch_to.default_content()

    # 其他-查看个人登录日志
    def test_46_RegistrationLog(self):
        u'''查看个人登录日志'''
        self.driver.switch_to.frame("frmbody")
        # 其他
        self.driver.find_element_by_id('memuBarText9').click()
        # 查看个人登录日志
        self.driver.find_element_by_xpath("//span[@value='../MyWeb/M_Log.aspx']").click()
        sleep(2)
        # 断言
        self.driver.switch_to.frame("frmMain")
        text = self.driver.find_element_by_xpath("//form[@name='form1']/table[1]/tbody/tr[1]/td[1]").text
        self.assertEqual(text, '查看个人登录日志')
        # 返回主iframe
        self.driver.switch_to.default_content()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


# 定义一个测试套
def suite():
    suiteTest = unittest.TestSuite()
    suiteTest.addTest(TestMenu('test_0_BasicInfo'))
    suiteTest.addTest(TestMenu('test_10_MinorRegistration'))
    suiteTest.addTest(TestMenu('test_11_RewardsPunishments'))
    suiteTest.addTest(TestMenu('test_12_AcademicWarning'))
    suiteTest.addTest(TestMenu('test_13_ApplyMove'))
    suiteTest.addTest(TestMenu('test_14_PredictMove'))
    suiteTest.addTest(TestMenu('test_15_MoveInfo'))
    suiteTest.addTest(TestMenu('test_16_AcademicProgress'))
    suiteTest.addTest(TestMenu('test_17_ApplyGraduation'))
    suiteTest.addTest(TestMenu('test_18_GraduationConclusion'))
    suiteTest.addTest(TestMenu('test_19_TheoryCourse'))
    suiteTest.addTest(TestMenu('test_20_PracticeSection'))
    suiteTest.addTest(TestMenu('test_21_CreditRequirements'))
    suiteTest.addTest(TestMenu('test_22_Primary'))
    suiteTest.addTest(TestMenu('test_23_PrimaryResult'))
    suiteTest.addTest(TestMenu('test_24_Gregory'))
    suiteTest.addTest(TestMenu('test_25_GregoryResult'))
    suiteTest.addTest(TestMenu('test_26_ByElection'))
    suiteTest.addTest(TestMenu('test_27_DropChoose'))
    suiteTest.addTest(TestMenu('test_28_CancelledCourse'))
    suiteTest.addTest(TestMenu('test_29_TeachingSchedule'))
    suiteTest.addTest(TestMenu('test_30_CourseChangeInfo'))
    suiteTest.addTest(TestMenu('test_31_ExaminationSchedule'))
    suiteTest.addTest(TestMenu('test_32_TestReportInfo'))
    suiteTest.addTest(TestMenu('test_33_RetakeRegistration'))
    suiteTest.addTest(TestMenu('test_34_RetakePermission'))
    suiteTest.addTest(TestMenu('test_35_AchievementRecord'))
    suiteTest.addTest(TestMenu('test_36_CheckScores'))
    suiteTest.addTest(TestMenu('test_37_GradeDistribution'))
    suiteTest.addTest(TestMenu('test_38_LevelExamRegistration'))
    suiteTest.addTest(TestMenu('test_39_LevelExamScores'))
    suiteTest.addTest(TestMenu('test_40_ReceiveTextBookInfo'))
    suiteTest.addTest(TestMenu('test_41_TextbookReconciliation'))
    suiteTest.addTest(TestMenu('test_42_TextbookSale'))
    suiteTest.addTest(TestMenu('test_43_SubmitQuestionnaire'))
    suiteTest.addTest(TestMenu('test_44_EvaluationForm'))
    suiteTest.addTest(TestMenu('test_45_ChangePassword'))
    suiteTest.addTest(TestMenu('test_46_RegistrationLog'))
    return suiteTest


if __name__ == '__main__':
    # 存放路径
    filepath = "E:/PyProject/zhkuTest/TestReport/report_menu.html"
    fp = open(filepath, 'wb')
    # 定义测试报告的标题和描述
    runner = HTMLTestRunner.HTMLTestRunner(
        stream=fp,
        title=u'目录',
        description=u'用例测试情况'
    )
    runner.run(suite())
    fp.close()
