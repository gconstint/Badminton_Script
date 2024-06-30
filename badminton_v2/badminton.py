#!/user/bin/env python
# -*- coding=utf-8 -*-
"""
@project : Badminton_Script
@author  : guanzhihao guanzhh1@outlook.com
@file   : badminton.py
@ide    : PyCharm
@time   : 2024-06-27 19:53:34
"""
from DrissionPage import ChromiumPage, ChromiumOptions
from DrissionPage.common import Keys
from datetime import *
import multiprocessing
from threading import Thread
import time


class BadmintonPage:
    def __init__(self, username: str, password: str, field_type: int, choose_date: str, choose_time: int,
                 course_number: int, join_number: str, person_id: int, responsible_person: str,
                 responsible_person_tel: str):
        self.username = username
        self.password = password
        self.field_type = field_type
        self.choose_date = choose_date
        self.choose_time = choose_time
        self.course_number = course_number
        self.join_number = join_number
        self.person_id = person_id
        self.responsible_person = responsible_person
        self.responsible_person_tel = responsible_person_tel
        # self.page = None
        self.wrong_flag = False

    def work(self):
        co = ChromiumOptions().auto_port()
        co.incognito()  # 匿名模式
        # co.headless()  # 无头模式
        co.set_argument('--no-sandbox')  # 无沙盒模式
        # 使用来宾模式打开浏览器
        co.set_argument('--guest')
        co.remove_extensions()
        page = ChromiumPage(co)
        page.set.auto_handle_alert()
        page.get(
            r'https://oa.shanghaitech.edu.cn/workflow/request/AddRequest.jsp?workflowid=14862&t_s=1648003625917&amp_sec_version_=1&gid_=dHArWDUwc2pjeWJMRlk3RlhKaEJoaG1vbmI3VE9PeE03Z1dGSlFVazIxWDVwcE9Zcnk5a2pIazdtTGM2eHFIVFRPS3NFNmVMYmIrRWNWUG1TZlg5RFE9PQ&EMAP_LANG=zh&THEME=cherry')

        # 登录
        page.ele("#username").input(self.username)
        page.ele("#password").input(self.password)
        page.wait(2)
        page.ele("#login_submit").click()

        # 等待页面跳转
        page.wait.load_start()

        # 设置场地类型，1为空白，2为羽毛球
        page.ele('#field32340').select(text_or_index="羽毛球场")

        # 设置选择日期
        today = date.today()
        choose_date = today + timedelta(days=2)
        choose_date = choose_date.strftime("%Y-%m-%d")
        date_input = page.ele('#field31901')
        date_input.run_js('this.value="{}"'.format(choose_date))
        page.wait(1)
        # 消除弹窗
        # page.handle_alert(accept=True)

        # 选择时间
        page.ele("#field31902_browserbtn").click()
        if self.choose_time >= 21:
            page.ele('xpath://*[@id="_xTable"]/div[1]/div[3]/div/table/tbody/tr/td[2]/div/span/span[3]').click()
            page.wait(1)
            page.ele('xpath://*[@id="_xTable"]/div[1]/div[2]/table/tbody/tr[1]/td[3]/a').click()
        else:
            page.ele('//*[@id="_xTable"]/div[1]/div[2]/table/tbody/tr[{}]/td[3]/a'.format(
                self.choose_time)).click()

        # 设置场地号
        page.ele('#field31883_browserbtn').click()
        page.ele('xpath://*[@id="CustomTree_2_switch"]').click()
        page.ele('xpath://*[@id="CustomTree_3_switch"]').click()
        ele = page.ele('xpath://*[@id="CustomTree_4_span"]')
        ele.wait.displayed()
        ele = page.eles('css:[id^="CustomTree_"][id$="_a"]')
        element_name = "羽毛球场地{}号".format(self.course_number)

        for i in ele[3:]:
            if i.attr('title') == element_name:
                i.click()
                break
        page.ele("#btnok").click()

        # 设置参与人数
        page.ele("#field31884").input(self.join_number)

        # 设置人员id，1为空白，2为学生
        page.ele("#field31885").select(text_or_index="学生")

        # 设置负责人
        page.ele("#field31888").input(self.responsible_person)

        # 设置负责人电话
        page.ele("#field31889").input(self.responsible_person_tel)

        # 设置第三方服务
        page.ele("#field31892").select(text_or_index="无")

        # 提交
        ele = page.ele('xpath://*[@id="topTitleNew"]/tbody/tr/td/input[1]')
        ele.click()
        while True:
            page.actions.key_down(Keys.ENTER)
            # 消除弹窗
            # page.handle_alert(accept=True)
            if not ele.states.is_alive:
                break

        if self.wrong_flag:
            page.actions.key_down(Keys.ENTER)


def run_badminton_instance(b: BadmintonPage):
    b.work()


if __name__ == '__main__':
    # 设置开始时间
    current_time = datetime.now().strftime('%H:%M:%S')
    start_time = datetime.strptime('11:59:45', '%H:%M:%S')
    # 获取当前时间的datetime对象
    current_time = datetime.strptime(current_time, '%H:%M:%S')

    if start_time.time() > current_time.time():
        # t = start_time - current_time
        t_diff = start_time - current_time
        t_diff_s = t_diff.total_seconds()
        print(t_diff_s)
        time.sleep(t_diff_s)

    badminton1 = BadmintonPage(username='2021213203', password='guanzhihao@0912', field_type=1,
                               choose_date='',
                               choose_time=21, course_number=6, join_number='4', person_id=4,
                               responsible_person='关治豪', responsible_person_tel='13016406828')
    badminton2 = BadmintonPage(username='2021213203', password='guanzhihao@0912', field_type=1,
                               choose_date='',
                               choose_time=21, course_number=4, join_number='4', person_id=4,
                               responsible_person='关治豪', responsible_person_tel='13016406828')
    # with multiprocessing.Pool(2) as p:
    #     p.map(run_badminton_instance, [badminton1, badminton2])
    Thread(target=run_badminton_instance, args=(badminton1,)).start()
    Thread(target=run_badminton_instance, args=(badminton2,)).start()
