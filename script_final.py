#!/user/bin/env python
# -*- coding=utf-8 -*-
"""
@project : Badmintom_Script
@author  : guanzhihao guanzhh1@outlook.com
@file   : scrip_final.py
@ide    : Vscode insider
@time   : 2023-05-31 15:39:19
"""
# 使用非pydm环境进行打包,本次使用非conda环境进行打包
from email.policy import default
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget
import os
import sys

# 获取当前脚本所在的目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 获取src目录的绝对路径
src_dir = os.path.dirname(current_dir)

# 将src目录添加到Python路径中
sys.path.append(src_dir)

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from concurrent.futures import ThreadPoolExecutor
from PyQt6.QtCore import pyqtSlot, QSettings
from datetime import datetime
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtCore import QTimer, QTime
from PyQt6.QtCore import QCoreApplication, QRect
# from PyQt6.uic import loadUi
from ui_source.ui_definition2 import Ui_Form
import time
from selenium.webdriver import ActionChains


# import logging
class AppointmentThread(QThread):
    finished = pyqtSignal()
    errorOccurredWithInfo = pyqtSignal(str, int, str)  # 自定义的信号，带有时间、线程号和错误信息作为参数

    # qt的信号和槽机制，用于线程间的通信,信号可以带参数，也可以不带参数
    # (str,int,str)说明含有三个参数，分别是str、int、str类型

    def __init__(self, parent=None, time_temp=None, num_temp=None, index=None, key_tmp=None):
        # 对于这里的超类的初始化，需要把parent带上
        super(AppointmentThread, self).__init__(parent)
        # 获取comboBox控件的当前值，使用方法currentText()
        self.type = parent.comboBox_6.currentText()
        # 获取lineEdit控件的内容，使用方法text()
        self.account = parent.lineEdit.text()
        self.password = parent.lineEdit_2.text()

        self.field_type = 1

        # date_string = parent.dateEdit.text()
        # date = QDate.fromString(date_string, "yyyy-MM-dd")
        # # 将日期对象转换为字符串，指定日期格式
        # self.date = date.toString("yyyy-MM-dd")

        # 获取dateEdit控件的内容，使用方法text()
        self.date = parent.dateEdit.text()

        self.time_temp = time_temp
        self.times = (self.time_temp - 11) * 2 + 1

        self.num = num_temp

        self.join_num = '4'
        self.person_id = 1

        self.person_response = parent.lineEdit_3.text()
        self.person_tel = parent.lineEdit_4.text()

        self.commit = True if parent.comboBox_4.currentText() == '提交' else False

        # 判断checkBox控件是否被选择，使用方法isChecked()，如被选中，返回True，否则返回False
        self.brower_flag = parent.checkBox_1.isChecked()

        self.message_edit = parent.textBrowser
        self.index = index
        self.key_tmp = key_tmp
        self.timeEdit_2 = parent.timeEdit_2

        # self.combox_time = parent.comboBox_11

    def judge_brower(self):
        driver = None
        if self.type == 'Google':
            if self.brower_flag:
                # 设置浏览器选项，参数--headless表示隐藏浏览器模式
                options = webdriver.ChromeOptions()
                options.add_argument('--headless')
                try:
                    # 尝试使用webdriver.Chrome打开chrome浏览器，如果失败，则说明webdriver版本不对，需要更新
                    driver = webdriver.Chrome(executable_path=r'chromedriver.exe', options=options)
                except Exception as e:
                    error_tmp = str(e)
                    error_message = 'the version of webdriver is wrong!\nPlease visit the website: https://sites.google.com/chromium.org/driver/downloads \n Maybe you need to use VPN to visit this website!'
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    # 信号槽机制，将时间、手动输入的线程号、错误信息传递给主线程
                    self.errorOccurredWithInfo.emit(current_time, self.index, error_message)
                    # 退出线程
                    self.quit()
            else:
                try:
                    driver = webdriver.Chrome(executable_path=r'chromedriver')
                except Exception as e:
                    error_tmp = str(e)
                    error_message = 'the version of webdriver is wrong!\nPlease visit the website: https://sites.google.com/chromium.org/driver/downloads \n Maybe you need to use VPN to visit this website!'
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    # 信号槽机制，将时间、手动输入的线程号、错误信息传递给主线程
                    self.errorOccurredWithInfo.emit(current_time, self.index, error_message)
                    # 退出线程
                    self.quit()
        else:
            if self.brower_flag:
                options = webdriver.EdgeOptions()
                options.add_argument('--headless')
                try:
                    # 尝试使用webdriver.Edge打开microsoft edge浏览器，如果失败，则说明webdriver版本不对，需要更新
                    driver = webdriver.Edge(executable_path='msedgedriver.exe', options=options)
                except Exception as e:
                    error_tmp = str(e)
                    # print('the version of webdriver is wrong!')
                    # self.message_edit.append('the version of webdriver is wrong!\nPlease visit the website:https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/')
                    error_message = 'the version of webdriver is wrong!\nPlease visit the website: https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/'
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    # 信号槽机制，将时间、手动输入的线程号、错误信息传递给主线程
                    self.errorOccurredWithInfo.emit(current_time, self.index, error_message)
                    # 退出线程
                    self.quit()
            else:
                try:
                    driver = webdriver.Edge(executable_path='msedgedriver.exe')
                except Exception as e:
                    error_tmp = str(e)
                    # print('the version of webdriver is wrong!')
                    # self.message_edit.append('the version of webdriver is wrong!\nPlease visit the website:https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/')
                    error_message = 'the version of webdriver is wrong!\nPlease visit the website: https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/'
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    self.errorOccurredWithInfo.emit(current_time, self.index, error_message)
                    self.quit()
        return driver

    def reset(self):
        self.quit()
        self.wait()

    def run(self):
        try:
            self.appoint()
        except Exception as e:
            # 将错误信息转换为str格式，便于打印
            error_message = str(e)

            # start_index = error_message.find("Alert text :") + len("Alert text :")
            # end_index = error_message.find("}", start_index)
            # error_message = error_message[start_index:end_index].strip()

            # 使用datetime.now()方法获取当前时间，并使用strftime将时间格式转换为特定的字符串格式，YY代表年，mm代表月，dd代表天，HH代表小时，MM代表分钟，SS代表秒钟
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # 给信号槽传递信息，该信号槽有三个变量分别对应不同的含义(str,int,str)
            self.errorOccurredWithInfo.emit(current_time, self.index, error_message)

            # 线程的退出，使用方法quit()
            self.quit()
        finally:
            self.finished.emit()

    def appoint(self):

        self.driver = self.judge_brower()
        if self.driver is None:
            return
        self.driver.get(
            r'https://oa.shanghaitech.edu.cn/workflow/request/AddRequest.jsp?workflowid=14862&t_s=1648003625917&amp_sec_version_=1&gid_=dHArWDUwc2pjeWJMRlk3RlhKaEJoaG1vbmI3VE9PeE03Z1dGSlFVazIxWDVwcE9Zcnk5a2pIazdtTGM2eHFIVFRPS3NFNmVMYmIrRWNWUG1TZlg5RFE9PQ&EMAP_LANG=zh&THEME=cherry')

        # auto login
        # 使用driver的find_element去找元素,By.NAME表示通过name属性去找，By.ID表示通过id属性去找
        # 使用click()方法去点击元素
        self.driver.find_element(By.NAME, 'username').send_keys(self.account)
        self.driver.find_element(By.ID, 'password').send_keys(self.password)
        self.driver.find_element(By.ID, 'login_submit').click()

        # 等待页面加载完成，使用方法implicity_wait(),参数为等待时间，单位为秒
        self.driver.implicitly_wait(5)
        # 切换窗口，将窗口聚焦到最新打开的窗口上，使用方法switch_to.window(),参数为窗口的句柄,driver.window_handles[-1]表示最新打开的窗口
        self.driver.switch_to.window(self.driver.window_handles[-1])
        self.driver.switch_to.frame('bodyiframe')  # 切换frame，

        # Choose field type
        Select(self.driver.find_element(By.ID, 'field32340')).select_by_index(
            self.field_type)  # 选择下拉框的第几个选项，从0开始。其中我们需要通过find_element找到下拉框的元素，然后使用Select()方法将其转换为下拉框的形式，然后使用select_by_index()方法选择第几个选项。

        try:
            # Choose date
            date_temp = self.driver.find_element(By.ID, 'field31901')  # 日期输入框
            self.driver.execute_script("arguments[0].setAttribute(arguments[1], arguments[2])", date_temp, 'value',
                                       self.date)
            time.sleep(1)
            self.driver.find_element(By.ID, 'field31901browser').click()

            time.sleep(5)
            # 下面模拟键盘点击动作
            # 创建 ActionChains 对象
            actions = ActionChains(self.driver)
            # 模拟按下某个键，空格对应Keys.SPACE、回车对应Keys.ENTER、Esc对应Keys.ESCAPE
            actions.send_keys(self.key_tmp)

            # 执行动作3次
            for i in range(3):
                actions.perform()
            # 等待弹窗消失
            WebDriverWait(self.driver, 5).until(
                EC.invisibility_of_element_located((By.XPATH, '//*[@id="layui-layer1"]')))
        # except TimeoutException:
        #     print('等待弹窗消失超时')
        except Exception as e:
            # 处理弹出窗口操作失败的情况
            # print('处理弹出窗口失败:', str(e))

            # 忽视异常报错

            pass

        # Choose time
        self.driver.find_element(By.ID, 'field31902_browserbtn').click()
        self.driver.switch_to.default_content()  # 切换到默认frame。Switch focus to the default frame.
        self.driver.switch_to.frame(4)  # 切换到第4个frame
        self.driver.switch_to.frame(0)  # 切换到第0个frame
        time.sleep(2)
        if self.time_temp >= 21:
            # 当选择的时间大于21点时，需要点击下一页
            self.driver.find_element(By.XPATH,
                                     '//*[@id="_xTable"]/div[1]/div[3]/div/table/tbody/tr/td[2]/div/span/span[3]').click()
            time.sleep(1)
            self.driver.find_element(By.XPATH, '//*[@id="_xTable"]/div[1]/div[2]/table/tbody/tr[1]/td[3]/a').click()
        else:
            self.driver.find_element(By.XPATH,
                                     '//*[@id="_xTable"]/div[1]/div[2]/table/tbody/tr[{}]/td[3]/a'.format(
                                         self.times)).click()

        self.driver.switch_to.default_content()  # 切换到默认frame。Switch focus to the default frame.
        self.driver.switch_to.frame('bodyiframe')  # 切换到bodyiframe

        # Choose the number of field
        # 1
        self.driver.find_element(By.ID, 'field31883_browserbtn').click()
        # WebDriverWait(driver, 5).until(EC.frame_to_be_available_and_switch_to_it((By.ID, 'layui-layer-iframe6')))
        self.driver.switch_to.default_content()
        self.driver.switch_to.frame(4)
        self.driver.switch_to.frame(0)
        self.driver.switch_to.frame(0)

        self.driver.find_element(By.CSS_SELECTOR, '#CustomTree_2_switch').click()  # By.CSS_SELECTOR表示通过selector属性来找
        self.driver.implicitly_wait(5)
        self.driver.find_element(By.CSS_SELECTOR, '#CustomTree_3_switch').click()
        time.sleep(1)
        # 2
        # Always choose tree node # 4
        WebDriverWait(self.driver, 3).until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, '#CustomTree_3_span')))  # 设置等待时间，driver等待找到元素定位，通过css_selector去找元素，设置默认等待时间为3s
        # elements = driver.find_elements(By.CSS_SELECTOR, '[id^="CustomTree_"][id$="_span"]')    # 定位元素，以'CustomTree_'开头，'_span'结尾的css_selector的元素。
        elements = self.driver.find_elements(By.CSS_SELECTOR,
                                             '[id^="CustomTree_"][id$="_a"]')  # 定位元素，以'CustomTree_'开头，'_span'结尾的css_selector的元素。

        # 选择场地号
        time.sleep(3)
        found_element = None
        # try:
        #     last_element = elements[self.num+3]
        # except Exception as e:
        #     pass
        # else:
        #     last_element = elements[self.num + 2]

        # last_element.click()

        # 选择场地号
        element_name = "羽毛球场地{}号".format(self.num)
        for element in elements[3:9]:
            # print(element.get_attribute("title"))
            if element.get_attribute("title") == element_name:
                found_element = element
                break
        if found_element is None:
            found_element = elements[3]  # 默认选择第一个场地

        found_element.click()

        # driver.find_element(By.CSS_SELECTOR, '#btnok').click()
        self.driver.find_element(By.XPATH, '//*[@id="btnok"]').click()  # 通过By.XPATH属性去定位元素，可以在网页中copy元素的XPATH属性

        self.driver.switch_to.default_content()  # 切换到默认的frame
        self.driver.switch_to.frame('bodyiframe')  # 切换到bodyiframe

        # joining number
        self.driver.find_element(By.ID, 'field31884').send_keys(self.join_num)  # 通过ID去定位元素

        # person identity
        Select(self.driver.find_element(By.ID, 'field31885')).select_by_index(self.person_id)  # 通过ID去定位元素

        # responsible person
        self.driver.find_element(By.ID, 'field31888').send_keys(self.person_response)
        self.driver.find_element(By.ID, 'field31889').send_keys(self.person_tel)

        # third party service
        Select(self.driver.find_element(By.ID, 'field31892')).select_by_index(2)
        time.sleep(5)

        # 设置自动启动时间和自动退出时间
        # 获取当前时间
        current_time = QTime.currentTime()  # 使用QTIme获取时间，我推荐在QT中使用QTime而不是datetime.now()

        # 获取 timeEdit_2 的时间对象
        time_tmp = self.timeEdit_2.time()
        # print(time_tmp)
        # 获取小时、分钟和秒
        hour = time_tmp.hour()  # 时间格式，获取小时数，hour()
        minute = time_tmp.minute()  # 时间格式，获取分钟数，minute()
        second = time_tmp.second()  # 时间格式，获取秒钟数，second()

        # 设置 target_time
        target_time = QTime(hour, minute, second)  # 将时间格式转换为QTime格式，QTime(hour, minute, second)，对应时、分、秒

        # 如果当前时间已经达到目标时间，则直接退出函数
        if current_time >= target_time:
            return
        # 循环点击直到当前时间达到目标时间
        # t = float(self.combox_time.currentText())   # 获取下拉框中的时间
        # 获取当前时间
        current_time = QTime.currentTime()
        if self.commit:

            while True:
                # 获取当前时间
                current_time = QTime.currentTime()
                if current_time >= target_time:
                    break
                try:
                    self.driver.implicitly_wait(0.1)  # 设置等待时间
                    self.driver.find_element(By.XPATH, '//*[@id="topTitleNew"]/tbody/tr/td/input[1]').click()

                except Exception as e:
                    actions.perform()  # 执行点击动作
        else:
            # driver.find_element(By.XPATH, '//*[@id="topTitleNew"]/tbody/tr/td/input[2]').click()
            print('保存test')

            # while True:

        #     # 判断当前时间是否已经达到目标时间
        #     if current_time >= target_time:
        #         break

        #         try:

        #             actions.perform()   # 执行点击动作
        #             # driver.implicitly_wait(3)   # 设置等待时间
        #             element = driver.find_element(By.XPATH, '//*[@id="topTitleNew"]/tbody/tr/td/input[1]').click()

        #             while True:   
        #                 actions.perform()   # 执行点击动作
        #             if not element:
        #                 break

        #             # driver.implicitly_wait(3)
        #             # print('提交test')
        #         except Exception as e:
        #             pass
        #     else:
        #         # driver.find_element(By.XPATH, '//*[@id="topTitleNew"]/tbody/tr/td/input[2]').click()
        #         print('保存test')
        #     # 增加适当的延时，避免过于频繁的点击
        #     time.sleep(t)
        #     # driver.implicitly_wait(1)   # 设置等待时间
        self.driver.quit()


# 使用pydm的Display类，继承Display类，重写__init__方法,添加自己的方法
class MainWindow(QMainWindow, Ui_Form):
    def __init__(self):  # 标准的__init__方法，parent=None表示没有父类，args=None表示没有参数，macros=None表示没有宏
        super(MainWindow,
              self).__init__()  # 调用父类的__init__方法，super(MyDisplay, self)表示调用父类的__init__方法，parent=parent, args=args, macros=macros表示传入参数
        # loadUi(self.ui_filepath(), self)  # Load the UI file

        self.setupUi(self)  # 调用Ui_Form类的setupUi方法，传入self参数，self表示当前的窗口

        # 创建一个窗口部件，并将布局设置为其主要布局
        # from PyQt6.QtWidgets import QWidget
        # widget = QWidget()
        # widget.setLayout(self.frame)
        # 将窗口部件设置为主窗口的中央部件
        self.setCentralWidget(self.gridWidget)

        self.dateEdit.dateChanged.connect(
            self.set_combobox_options)  # 信号与槽，当dateEdit的日期改变时，执行set_combobox_options方法，该方法用于设置combobox的选项
        self.pushButton.clicked.connect(self.set_target_time)  # 信号与槽，pushButton的点击与set_target_time方法绑定，通过执行该方法来设置目标时间
        self.pushButton_2.clicked.connect(self.check)  # 信号与槽，pushButton_2的点击与check方法绑定，通过执行该方法来校准时间，当前日期+2
        # 上面的信号与槽机制，很好的实现了QT的事件机制，当某个事件发生时，执行某个方法，这里的事件就是点击按钮，日期改变等。

        self.pushButton_3.clicked.connect(self.open_webpage)  # 信号与槽，pushButton_3的点击与open_webpage方法绑定,通过执行该方法来打开网页
        self.appointment_threads = []
        self.timer = QTimer(self)  # 初始化定时器对象。这里我们将定时器对象作为MyDisplay类的成员变量，这样定时器对象就不会被垃圾回收了
        self.type = self.comboBox_6.currentText()
        self.brower_flag = self.checkBox_1.isChecked()

        settings = QSettings('MyCompany', 'MyApp')
        default_account = settings.value('default_account', '')
        default_password = settings.value('default_password', '')
        default_phone_number = settings.value('default_phone_number', '')
        default_people = settings.value('default_people', '')
        default_start_time = settings.value('default_start_time', '')
        default_end_time = settings.value('default_end_time', '')
        default_type = settings.value('default_type', '')

        self.lineEdit.setText(default_account)
        self.lineEdit_2.setText(default_password)
        self.lineEdit_4.setText(default_phone_number)
        self.lineEdit_3.setText(default_people)
        # 给timeEdit组件赋值
        self.timeEdit.setTime(QTime.fromString(default_start_time, 'hh:mm:ss'))
        self.timeEdit_2.setTime(QTime.fromString(default_end_time, 'hh:mm:ss'))

        self.comboBox_6.setCurrentText(default_type)
        self.pushButton_4.clicked.connect(self.save_account)
        # self.account = self.lineEdit.text()
        # self.password = self.lineEdit_2.text()

    def save_account(self):
        # 将默认值保存到设置中
        settings = QSettings('MyCompany', 'MyApp')
        settings.setValue('default_account', self.lineEdit.text())
        settings.setValue('default_password', self.lineEdit_2.text())
        settings.setValue('default_phone_number', self.lineEdit_4.text())
        settings.setValue('default_people', self.lineEdit_3.text())
        settings.setValue('default_start_time', self.timeEdit.time().toString('hh:mm:ss'))
        settings.setValue('default_end_time', self.timeEdit_2.time().toString('hh:mm:ss'))
        settings.setValue('default_type', self.comboBox_6.currentText())

    # 判断浏览器类型
    def judge_brower(self):
        driver = None
        if self.type == 'Google':
            if self.brower_flag:
                # 设置浏览器选项，参数--headless表示隐藏浏览器模式
                options = webdriver.ChromeOptions()
                options.add_argument('--headless')
                try:
                    # 尝试使用webdriver.Chrome打开chrome浏览器，如果失败，则说明webdriver版本不对，需要更新
                    driver = webdriver.Chrome(executable_path=r'chromedriver.exe', options=options)
                    error_message = 'the version of webdriver is right!'
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    message = current_time + ':' + error_message
                    self.textBrowser.append(message)
                except Exception as e:
                    error_tmp = str(e)
                    error_message = 'the version of webdriver is wrong!\nPlease visit the website: https://sites.google.com/chromium.org/driver/downloads \n Maybe you need to use VPN to visit this website!'
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    message = current_time + ':' + error_message
                    self.textBrowser.append(message)

            else:
                try:
                    driver = webdriver.Chrome(executable_path=r'chromedriver')

                    error_message = 'the version of webdriver is right!'
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    message = current_time + ':' + error_message
                    self.textBrowser.append(message)
                except Exception as e:
                    error_tmp = str(e)
                    error_message = 'the version of webdriver is wrong!\nPlease visit the website: https://sites.google.com/chromium.org/driver/downloads \n Maybe you need to use VPN to visit this website!'
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    message = current_time + ':' + error_message
                    self.textBrowser.append(message)

        else:
            if self.brower_flag:
                options = webdriver.EdgeOptions()
                options.add_argument('--headless')
                try:
                    # 尝试使用webdriver.Edge打开microsoft edge浏览器，如果失败，则说明webdriver版本不对，需要更新
                    driver = webdriver.Edge(executable_path='msedgedriver.exe', options=options)
                    error_message = 'the version of webdriver is right!'
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    message = current_time + ':' + error_message
                    self.textBrowser.append(message)
                except Exception as e:
                    error_tmp = str(e)
                    error_message = 'the version of webdriver is wrong!\nPlease visit the website: https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/'
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    message = current_time + ':' + error_message
                    self.textBrowser.append(message)
            else:
                try:
                    driver = webdriver.Edge(executable_path='msedgedriver.exe')
                    error_message = 'the version of webdriver is right!'
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    message = current_time + ':' + error_message
                    self.textBrowser.append(message)
                except Exception as e:
                    error_tmp = str(e)
                    error_message = 'the version of webdriver is wrong!\nPlease visit the website: https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/'
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    message = current_time + ':' + error_message
                    self.textBrowser.append(message)

        return driver

    def open_webpage(self):
        self.driver = self.judge_brower()
        if self.driver == None:
            return
        url = 'https://oa.shanghaitech.edu.cn/formmode/search/CustomSearchBySimple.jsp?customid=16201'  # 
        self.driver.get(url)

        # auto login
        # 使用driver的find_element去找元素,By.NAME表示通过name属性去找，By.ID表示通过id属性去找
        # 使用click()方法去点击元素
        account = self.lineEdit.text()
        password = self.lineEdit_2.text()
        self.driver.find_element(By.NAME, 'username').send_keys(account)
        self.driver.find_element(By.ID, 'password').send_keys(password)
        self.driver.find_element(By.ID, 'login_submit').click()

        # 等待页面加载完成，使用方法implicity_wait(),参数为等待时间，单位为秒
        self.driver.implicitly_wait(5)
        # # 切换窗口，将窗口聚焦到最新打开的窗口上，使用方法switch_to.window(),参数为窗口的句柄,driver.window_handles[-1]表示最新打开的窗口
        # self.driver.switch_to.window(self.driver.window_handles[-1])
        # self.driver.switch_to.frame('bodyiframe')    # 切换frame，

        # self.driver.find_element(By.XPATH, '//*[@id="advancedSearch"]/span').click()

    def set_combobox_options(self, date):
        day_of_week = date.dayOfWeek()  # 判断时间格式date所处的星期几，dayOfWeek(),返回值为1-7，1表示星期一，7表示星期日

        if day_of_week == Qt.Thursday:  # Qt.Thursday表示星期四
            self.comboBox_5.clear()  # 使用方法clear(),清空comboBox中的选项
            self.comboBox_5.addItems(["1", "3", "5", "2", "4", "6"])  # 设置comboBox的选项，使用方法addItems(),以列表的形式给出值
            self.comboBox_7.clear()
            self.comboBox_7.addItems(["1", "3", "5", "2", "4", "6"])
            self.comboBox_10.clear()
            self.comboBox_10.addItems(["1", "3", "5", "2", "4", "6"])
        # 星期三
        elif day_of_week == Qt.Wednesday:  # Qt.Wednesday表示星期三
            self.comboBox_5.clear()
            self.comboBox_5.addItems(["2", "4", "6", "1", "3", "5"])
            # 设置['1','3','5']为comboBox的选项,字体颜色为红色
            # 
            self.comboBox_7.clear()
            self.comboBox_7.addItems(["2", "4", "6", "1", "3", "5"])
            self.comboBox_10.clear()
            self.comboBox_10.addItems(["2", "4", "6", "1", "3", "5"])

        else:
            self.comboBox_5.clear()
            self.comboBox_5.addItems(["1", "2", "3", "4", "5", "6"])
            self.comboBox_7.clear()
            self.comboBox_7.addItems(["1", "2", "3", "4", "5", "6"])
            self.comboBox_10.clear()
            self.comboBox_10.addItems(["1", "2", "3", "4", "5", "6"])

    def check(self):
        # 获取当前日期并加上2天
        current_date = QDate.currentDate()  # QDate.currentDate()获取当前日期，与之对应的，QTime.currentTime()获取当前时间
        target_date = current_date.addDays(2)  # 将时间元组增加指定天数，使用方法addDays()

        # 将结果设置为 dateEdit 的值
        self.dateEdit.setDate(target_date)  # 设置dateEdit控件的内容，使用方法setDate(),参数是时间元组

    @pyqtSlot()  # 使用修饰符pyqtSlot(),将该方法注册为槽
    def start_thread(self):
        # 如果线程列表为空，则退出函数
        # 这里应该优化一下，开始线程前，终止前面的线程
        if self.appointment_threads:
            return
        combobox_list_time = [self.comboBox_9, self.comboBox_2, self.comboBox_8]  # 每个线程对应的comboBox，用于选择时间
        combobox_list_num = [self.comboBox_5, self.comboBox_7, self.comboBox_10]  # 每个线程对应的comboBox，用于选择场地号
        keys = [Keys.SPACE, Keys.ENTER, Keys.ESCAPE]  # 模拟的按键，Keys.SPACE表示空格键，Keys.ENTER表示回车键，Keys.ESCAPE表示ESC键
        with ThreadPoolExecutor(max_workers=4) as executor:  # 使用线程池，最大线程数为3
            for index, (combo_box, combobox2, key) in enumerate(zip(combobox_list_time, combobox_list_num,
                                                                    keys)):  # 这里方法非常巧妙，使用了zip()方法，将多个列表的元素一一对应起来，然后使用enumerate()方法，将列表的索引和元素一一对应起来
                value = combo_box.currentText()  # 获取comboBox的当前选项，使用方法currentText()
                num = combobox2.currentText()  # 获取comboBox的当前选项，使用方法currentText()
                if value != 'None':  # combo_box的内容设置为None，表示不选中当前进程，不加入线程池
                    value = int(value)  # 将字符串转换为整数。comboBox的内容是字符串形式，需要转换为整数
                    num = int(num)  # 同上
                    # 经典来了。
                    appointment_thread = AppointmentThread(self, time_temp=value, num_temp=num, index=index + 1,
                                                           key_tmp=key)  # 创建线程对象。我们在类MyDisplay中声明了一个AppointmentThread类的对象，我们传入参数self，表示该线程对象的父对象是MyDisplay类的对象，然后设置了四个单独的参数用以区别不同的线程，参数time_tmp,num_temp,index,key_tmp

                    appointment_thread.errorOccurredWithInfo.connect(
                        self.displayErrorMessageWithInfo)  # 连接 errorOccurredWithInfo 信号。这里便是我们在AppointmentThread声明的信号errorOccurredWithInfo，我们将其连接到displayErrorMessageWithInfo函数，我们之前声明了该信号会接受三个参数，(str,int,str)，对应的方法displayErrorMessageWithInfo也应接受三个参数
                    appointment_thread.finished.connect(
                        self.appointment_finished)  # 将线程自带的finished信号，连接到appointment_finished方法上。在finished.emit()方法中会将需要的参数传递过来。
                    self.appointment_threads.append(appointment_thread)  # 将线程加入线程队列中
                    executor.submit(appointment_thread.run)  # 将线程加入线程池中，使用方法submit()，参数是线程对象的run方法

    def set_target_time(self):
        # 获取 timeEdit 的时间对象
        time_tmp = self.timeEdit.time()  # 获取timeEdit控件的内容，使用方法time()。返回值是时间对象。之前，dateEdit控件的内容也与之类似，也可以通过方法time()获取时间对象
        # 获取小时、分钟和秒
        hour = time_tmp.hour()  # 获取时间对象的小时，使用方法hour()
        minute = time_tmp.minute()  # 获取时间对象的分钟，使用方法minute()
        second = time_tmp.second()  # 获取时间对象的秒，使用方法second()
        # 设置 target_time
        target_time = QTime(hour, minute, second)  # 使用QTime类的构造函数，创建时间对象，参数是小时、分钟和秒

        current_time = QTime.currentTime()  # 使用QTime.currentTime()获取当前时间
        if target_time > current_time:
            time_to_target = current_time.msecsTo(target_time)  # 计算当前时间到目标时间的毫秒数，使用方法msecsTo()

            # 创建 QTimer 定时器对象
            # timer = QTimer()    # 使用QTimer类的构造函数，创建定时器对象
            self.timer.timeout.connect(
                self.start_thread)  # 将定时器的timeout信号，连接到start_thread方法上。表示到达目标时间时，执行start_thread方法

            # 启动定时器，在到达目标时间时触发 timeout 信号
            self.timer.setSingleShot(True)  # 设置定时器只运行一次
            self.timer.start(time_to_target)  # 启动定时器，使用方法start()，参数是时间。当时间到达时，会触发timeout信号
            msg = '定时器已启动，将在{}时{}分{}秒时开始预约'.format(hour, minute, second)  # 使用format()方法，格式化字符串
            self.textBrowser.append(msg)

        else:
            self.start_thread()  # 如果目标时间已经过去，则直接执行start_thread方法

    @pyqtSlot(str, int, str)  # 使用修饰符pyqtSlot(),将该方法注册为槽。其参数类型与信号errorOccurredWithInfo的参数类型一致
    def displayErrorMessageWithInfo(self, current_time, index, error_info):
        error_message = f"[Time: {current_time}] [Thread: {index}] {error_info}"  # 使用f-string,格式化字符串
        self.textBrowser.append(error_message)

    def appointment_finished(self):  # 该方法是槽，用于处理信号finished
        sender = self.sender()  # 获取信号的发送者，使用方法sender()。返回值是发送者的对象
        self.appointment_threads.remove(sender)  # 将发送者从线程队列中移除，使用方法remove()
        sender.reset()  # 重置发送者，使用方法reset()
        msg = '定时器已结束，请手动点击查询按钮进行查看'  # 使用format()方法，格式化字符串
        self.textBrowser.append(msg)

    def resizeEvent(self, event):
        # 获取屏幕的几何信息
        screen_geometry = QCoreApplication.instance().desktop().availableGeometry()

        # 设置窗口的大小为屏幕的80%
        width = int(screen_geometry.width() * 0.23)
        height = int(screen_geometry.height() * 0.6)
        self.resize(width, height)

        # 将窗口移动到屏幕的中央
        window_geometry = self.geometry()
        x = int((screen_geometry.width() - window_geometry.width()) / 2)
        y = int((screen_geometry.height() - window_geometry.height()) / 2)
        self.setGeometry(QRect(x, y, window_geometry.width(), window_geometry.height()))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    # window.resize(471, 551)
    window.setWindowTitle("Badminton V2.1.1")
    window.show()
    sys.exit(app.exec_())
