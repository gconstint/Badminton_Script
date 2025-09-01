#!/usr/bin/env python
# -*- coding:utf-8 -*-
import warnings
# 抑制PyQt6的sipPyTypeDict deprecation warning
warnings.filterwarnings("ignore", message="sipPyTypeDict.*deprecated", category=DeprecationWarning)

import logging
# from pprint import pprint
import os
import shutil
import sys
import zipfile
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

import requests
from PyQt6.QtCore import QCoreApplication, QDate, QSettings, QTimer, QTime, Qt, pyqtSlot
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from modules.Appointment_thread import AppointmentPage
from modules.open_checkboxs import CheckBoxWindow
from modules.open_version_log import LogWindow
from modules.version_manager import get_app_version
# from modules.time_sync import sync_windows_time
from ui_source.badminton_window import Ui_MainWindow
import version_config


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(
            self,
    ):  # 标准的__init__方法，parent=None表示没有父类，args=None表示没有参数，macros=None表示没有宏
        super().__init__()  # 调用父类的__init__方法，super(MyDisplay, self)表示调用父类的__init__方法，parent=parent, args=args, macros=macros表示传入参数
        self.setupUi(self)

        # 动态获取版本号并设置窗口标题
        app_version = get_app_version(
            repo_owner=version_config.GITHUB_REPO_OWNER,
            repo_name=version_config.GITHUB_REPO_NAME
        )
        self.setWindowTitle(f"{version_config.APP_NAME} V{app_version}")
        self.init_size()
        self.log_init()

        self.dateEdit.dateChanged.connect(
            self.set_combobox_options
        )  # 信号与槽，当dateEdit的日期改变时，执行set_combobox_options方法，该方法用于设置combobox的选项
        self.pushButton_1.clicked.connect(
            self.set_target_time
        )  # 信号与槽，pushButton的点击与set_target_time方法绑定，通过执行该方法来设置目标时间
        self.pushButton_2.clicked.connect(
            self.check
        )  # 信号与槽，pushButton_2的点击与check方法绑定，通过执行该方法来校准时间，当前日期+2
        # 上面的信号与槽机制，很好的实现了QT的事件机制，当某个事件发生时，执行某个方法，这里的事件就是点击按钮，日期改变等。

        self.pushButton_3.clicked.connect(
            self.open_webpage
        )  # 信号与槽，pushButton_3的点击与open_webpage方法绑定,通过执行该方法来打开网页
        self.appointment_threads = []
        self.timer = QTimer(
            self
        )  # 初始化定时器对象。这里我们将定时器对象作为MyDisplay类的成员变量，这样定时器对象就不会被垃圾回收了
        self.type = self.comboBox_6.currentText()
        self.brower_flag = self.checkBox_1.isChecked()

        self.msg = QMessageBox()

        self.setting1 = QSettings("MyCompany", "MyApp")
        self.setting2 = QSettings("MyCompany", "MyApp")
        self.apply_default_settings_1()
        # 保存默认设置按钮1
        self.pushButton_5.clicked.connect(self.save_default_settings)
        self.pushButton_5.clicked.connect(self.show_saved_message)

        self.time_window = None
        # self.pushButton_4.clicked.connect(self.update_webdriver)
        self.pushButton_4.clicked.connect(self.update_webdriver)

        # self.pushButton_4.clicked.connect(self.apply_default_settings)
        self.comboBox.currentIndexChanged.connect(self.on_combobox_changed)

        self.bug_windows = CheckBoxWindow()
        self.pushButton_6.clicked.connect(self.open_bug_windows)

        self.log_window = LogWindow()
        self.pushButton_7.clicked.connect(self.open_version_log)

        self.webdriver_version = "129.0.6668.70"

    def init_size(self):
        # 方案2: 固定合适的尺寸 (可选择使用)
        width = 420
        height = 740
        # 设置窗口大小
        self.resize(width, height)

    # def show_time(self):
    #     if self.time_window is not None:
    #         self.time_window.close()
    #     self.time_window = TimeWindow()
    #     self.time_window.show()

    def open_bug_windows(self):
        if self.bug_windows is not None:
            self.bug_windows.close()
            # return

        self.bug_windows.show()

    def open_version_log(self):
        if self.log_window is not None:
            self.log_window.close()

        self.log_window.show()

    def on_combobox_changed(self, index):
        if index == 0:
            # 加载默认设置1
            self.apply_default_settings_1()
        elif index == 1:
            # 加载默认设置2
            self.apply_default_settings_2()

    def save_default_settings_1(self):
        # 将默认值保存到设置中
        # settings1 = QSettings('MyCompany', 'MyApp')

        self.setting1.setValue("default_account", self.lineEdit.text())
        self.setting1.setValue("default_password", self.lineEdit_2.text())
        self.setting1.setValue("default_phone_number", self.lineEdit_4.text())
        self.setting1.setValue("default_people", self.lineEdit_3.text())

        self.setting1.setValue(
            "default_start_time", self.timeEdit_1.time().toString("hh:mm:ss")
        )
        self.setting1.setValue(
            "default_end_time", self.timeEdit_3.time().toString("hh:mm:ss")
        )
        # self.setting1.setValue('default_error_time', self.timeEdit_3.time().toString('hh:mm:ss'))

        self.setting1.setValue("default_type", self.comboBox_6.currentText())

        self.setting1.setValue("default_num1", self.comboBox_5.currentText())
        self.setting1.setValue("default_num2", self.comboBox_7.currentText())
        self.setting1.setValue("default_num3", self.comboBox_10.currentText())

        self.setting1.setValue("default_time1", self.comboBox_9.currentText())
        self.setting1.setValue("default_time2", self.comboBox_2.currentText())
        self.setting1.setValue("default_time3", self.comboBox_8.currentText())

        self.setting1.setValue("webdriver_version", self.webdriver_version)

        self.setting1.setValue('hide_web1', self.checkBox_1.isChecked())

        self.setting1.setValue('court_type1',self.comboBox_3.currentText())

    def save_default_settings_2(self):
        # 将默认值保存到设置中
        # settings2 = QSettings('MyCompany', 'MyApp')
        self.setting2.setValue("default_account2", self.lineEdit.text())
        self.setting2.setValue("default_password2", self.lineEdit_2.text())
        self.setting2.setValue("default_phone_number2", self.lineEdit_4.text())
        self.setting2.setValue("default_people2", self.lineEdit_3.text())
        self.setting2.setValue(
            "default_start_time2", self.timeEdit_1.time().toString("hh:mm:ss")
        )
        self.setting2.setValue(
            "default_end_time2", self.timeEdit_3.time().toString("hh:mm:ss")
        )
        # self.setting2.setValue('default_error_time2', self.timeEdit_3.time().toString('hh:mm:ss'))

        self.setting2.setValue("default_type2", self.comboBox_6.currentText())

        self.setting2.setValue("default_num12", self.comboBox_5.currentText())
        self.setting2.setValue("default_num22", self.comboBox_7.currentText())
        self.setting2.setValue("default_num32", self.comboBox_10.currentText())

        self.setting2.setValue("default_time12", self.comboBox_9.currentText())
        self.setting2.setValue("default_time22", self.comboBox_2.currentText())
        self.setting2.setValue("default_time32", self.comboBox_8.currentText())

        self.setting2.setValue("webdriver_version", self.webdriver_version)
        self.setting2.setValue('hide_web12', self.checkBox_1.isChecked())

        self.setting2.setValue('court_type2',self.comboBox_3.currentText())

    def save_default_settings(self):
        if self.comboBox.currentText() == "1":
            self.save_default_settings_1()
        if self.comboBox.currentText() == "2":
            self.save_default_settings_2()

    def apply_default_settings_1(self):
        # 加载默认设置1
        # settings1 = QSettings('MyCompany', 'MyApp')

        default_account1 = self.setting1.value("default_account", "")
        default_password1 = self.setting1.value("default_password", "")
        default_phone_number1 = self.setting1.value("default_phone_number", "")
        default_people1 = self.setting1.value("default_people", "")

        default_start_time1 = self.setting1.value("default_start_time", "")
        default_end_time1 = self.setting1.value("default_end_time", "")
        # default_error_time1= self.setting1.value('default_error_time','')

        default_type1 = self.setting1.value("default_type", "")
        default_num1 = self.setting1.value("default_num1", "")
        default_num2 = self.setting1.value("default_num2", "")
        default_num3 = self.setting1.value("default_num3", "")
        default_time11 = self.setting1.value("default_time1", "")
        default_time21 = self.setting1.value("default_time2", "")
        default_time31 = self.setting1.value("default_time3", "")

        self.webdriver_version = self.setting1.value("webdriver_version", "")
        self.checkBox_1.setChecked(self.setting1.value('hide_web1', "", type=bool))
        # default_check = self.setting1.value('default_check', False, type=bool)

        self.lineEdit.setText(default_account1)
        self.lineEdit_2.setText(default_password1)
        self.lineEdit_4.setText(default_phone_number1)
        self.lineEdit_3.setText(default_people1)
        # 给timeEdit组件赋值
        self.timeEdit_1.setTime(QTime.fromString(default_start_time1, "hh:mm:ss"))
        self.timeEdit_3.setTime(QTime.fromString(default_end_time1, "hh:mm:ss"))
        # self.timeEdit_3.setTime(QTime.fromString(default_error_time1,'hh:mm:ss'))

        self.comboBox_6.setCurrentText(default_type1)

        self.comboBox_5.setCurrentText(default_num1)
        self.comboBox_7.setCurrentText(default_num2)
        self.comboBox_10.setCurrentText(default_num3)

        self.comboBox_9.setCurrentText(default_time11)
        self.comboBox_2.setCurrentText(default_time21)
        self.comboBox_8.setCurrentText(default_time31)

        # self.checkBox_2.setChecked(default_check)

        self.comboBox_3.setCurrentText(self.setting1.value('court_type1', ""))

    def apply_default_settings_2(self):
        # 加载默认设置2
        # settings2 = QSettings('MyCompany', 'MyApp')
        default_account2 = self.setting2.value("default_account2", "")
        default_password2 = self.setting2.value("default_password2", "")
        default_phone_number2 = self.setting2.value("default_phone_number2", "")
        default_people2 = self.setting2.value("default_people2", "")
        default_start_time2 = self.setting2.value("default_start_time2", "")
        default_end_time2 = self.setting2.value("default_end_time2", "")
        # default_error_time2= self.setting2.value('default_error_time2','')

        default_type2 = self.setting2.value("default_type2", "")

        default_num12 = self.setting2.value("default_num12", "")
        default_num22 = self.setting2.value("default_num22", "")
        default_num32 = self.setting2.value("default_num32", "")

        default_time12 = self.setting2.value("default_time12", "")
        default_time22 = self.setting2.value("default_time22", "")
        default_time32 = self.setting2.value("default_time32", "")

        self.webdriver_version = self.setting2.value("webdriver_version", "")
        self.checkBox_1.setChecked(self.setting2.value('hide_web12', "", type=bool))
        # default_check2 = self.setting2.value('default_check2', False, type=bool)

        self.lineEdit.setText(default_account2)
        self.lineEdit_2.setText(default_password2)
        self.lineEdit_4.setText(default_phone_number2)
        self.lineEdit_3.setText(default_people2)
        # 给timeEdit组件赋值
        self.timeEdit_1.setTime(QTime.fromString(default_start_time2, "hh:mm:ss"))
        self.timeEdit_3.setTime(QTime.fromString(default_end_time2, "hh:mm:ss"))
        # self.timeEdit_3.setTime(QTime.fromString(default_error_time2,'hh:mm:ss'))

        self.comboBox_6.setCurrentText(default_type2)

        self.comboBox_5.setCurrentText(default_num12)
        self.comboBox_7.setCurrentText(default_num22)
        self.comboBox_10.setCurrentText(default_num32)

        self.comboBox_9.setCurrentText(default_time12)
        self.comboBox_2.setCurrentText(default_time22)
        self.comboBox_8.setCurrentText(default_time32)

        # self.checkBox_2.setChecked(default_check2)

        self.comboBox_3.setCurrentText(self.setting2.value('court_type2', ""))

    def show_saved_message(self):
        # 显示保存成功的消息
        self.msg.setIcon(QMessageBox.Information)
        self.msg.setWindowTitle("information")
        self.msg.setText("默认设置已保存")
        self.msg.exec()

    # 判断浏览器类型
    def judge_brower(self):
        driver = None
        self.type = self.comboBox_6.currentText()
        if self.type == "Google":
            if self.brower_flag:
                # 设置浏览器选项，参数--headless表示隐藏浏览器模式
                options = webdriver.ChromeOptions()
                options.add_argument("--headless")
                try:
                    # 尝试使用webdriver.Chrome打开chrome浏览器，如果失败，则说明webdriver版本不对，需要更新
                    driver = webdriver.Chrome(
                        service=Service("chromedriver.exe"), options=options
                    )
                    error_message = "the version of webdriver is right!"
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    message = current_time + ":" + error_message
                    self.textBrowser.append(message)
                except Exception as e:
                    error_tmp = str(e)
                    error_message = "the version of webdriver is wrong!\nPlease visit the website: https://sites.google.com/chromium.org/driver/downloads \n Maybe you need to use VPN to visit this website!"
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    message = current_time + ":" + error_message
                    self.textBrowser.append(message)

            else:
                try:
                    driver = webdriver.Chrome(service=Service("chromedriver.exe"))

                    error_message = "the version of webdriver is right!"
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    message = current_time + ":" + error_message
                    self.textBrowser.append(message)
                except Exception as e:
                    error_tmp = str(e)
                    error_message = "the version of webdriver is wrong!\nPlease visit the website: https://sites.google.com/chromium.org/driver/downloads \n Maybe you need to use VPN to visit this website!"
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    message = current_time + ":" + error_message
                    self.textBrowser.append(message)

        else:
            if self.brower_flag:
                options = webdriver.EdgeOptions()
                options.add_argument("--headless")
                try:
                    # 尝试使用webdriver.Edge打开microsoft edge浏览器，如果失败，则说明webdriver版本不对，需要更新
                    driver = webdriver.Edge(
                        service=Service("msedgedriver.exe"), options=options
                    )
                    error_message = "the version of webdriver is right!"
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    message = current_time + ":" + error_message
                    self.textBrowser.append(message)
                except Exception as e:
                    error_tmp = str(e)
                    error_message = "the version of webdriver is wrong!\nPlease visit the website: https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/"
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    message = current_time + ":" + error_message
                    self.textBrowser.append(message)
            else:
                try:
                    driver = webdriver.Edge(service=Service("msedgedriver.exe"))
                    error_message = "the version of webdriver is right!"
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    message = current_time + ":" + error_message
                    self.textBrowser.append(message)
                except Exception as e:
                    error_tmp = str(e)
                    error_message = "the version of webdriver is wrong!\nPlease visit the website: https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/"
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    message = current_time + ":" + error_message
                    self.textBrowser.append(message)

        return driver

    def open_webpage(self):
        self.driver_extend = self.judge_brower()
        if self.driver_extend == None:
            return
        url = "https://oa.shanghaitech.edu.cn/formmode/search/CustomSearchBySimple.jsp?customid=16201"  #
        self.driver_extend.get(url)

        # auto login
        # 使用driver的find_element去找元素,By.NAME表示通过name属性去找，By.ID表示通过id属性去找
        # 使用click()方法去点击元素
        account = self.lineEdit.text()
        password = self.lineEdit_2.text()
        self.driver_extend.find_element(By.NAME, "username").send_keys(account)
        self.driver_extend.find_element(By.ID, "password").send_keys(password)
        self.driver_extend.find_element(By.ID, "login_submit").click()

        # 等待页面加载完成，使用方法implicity_wait(),参数为等待时间，单位为秒
        self.driver_extend.implicitly_wait(5)
        if self.bug_windows.checkBox_2.isChecked():
            self.driver_extend.get(url)
            self.driver_extend.implicitly_wait(5)

        # # 切换窗口，将窗口聚焦到最新打开的窗口上，使用方法switch_to.window(),参数为窗口的句柄,driver.window_handles[-1]表示最新打开的窗口
        # self.driver.switch_to.window(self.driver.window_handles[-1])
        # self.driver.switch_to.frame('bodyiframe')    # 切换frame，

        # self.driver.find_element(By.XPATH, '//*[@id="advancedSearch"]/span').click()

    def update_webdriver(self):

        # JSON文件的URL，通常是直接的下载链接
        json_url = 'https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json'

        # 发送GET请求获取JSON文件内容
        response = requests.get(json_url, allow_redirects=True)

        # 检查请求是否成功
        if response.status_code == 200:
            url = response.json()["channels"]["Stable"]["downloads"]["chromedriver"][-1]["url"]  # -1 表示win64平台
            version_num = url.split("/")[-3]
            # pprint(url)
            # pprint("version: " + version_num)

            self.webdriver_version = self.setting1.value("webdriver_version", "")
            # 弹出消息框
            self.msg.setIcon(QMessageBox.Information)
            self.msg.setWindowTitle("information")
            self.msg.setText(
                "当前浏览器driver版本为:{}\n最新浏览器driver版本为:{}".format(self.webdriver_version, version_num))

            self.msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

            # 如果点击ok
            if self.msg.exec() == QMessageBox.Ok:

                # 设置自定义请求头（可选）
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
                }
                # 发送请求
                response = requests.get(url, headers=headers)
                # 检查请求是否成功
                if response.status_code == 200:
                    # 保存文件
                    with open('chromedriver.zip', 'wb') as f:
                        f.write(response.content)
                    # print("download success")

                    # 对zip文件进行解压操作

                    with zipfile.ZipFile('chromedriver.zip', 'r') as zip_ref:
                        zip_ref.extractall('.')
                    # print("extract success")

                    # 将解压后的chromedriver.exe文件移动到上一级目录
                    os.chdir('chromedriver-win64')
                    shutil.move('chromedriver.exe', '..\\chromedriver.exe')
                    # print("move success")

                    os.chdir('..')
                    os.remove('chromedriver.zip')
                    shutil.rmtree('chromedriver-win64')
                    # print("delete success")
                    self.webdriver_version = version_num
                    self.setting1.setValue("webdriver_version", self.webdriver_version)
                    # 弹出消息框
                    self.msg.setIcon(QMessageBox.Information)
                    self.msg.setWindowTitle("information")
                    self.msg.setText("webdriver更新成功！\n当前浏览器driver版本为: " + self.webdriver_version)
                    self.msg.setStandardButtons(QMessageBox.Ok)
                    self.msg.exec()
                else:
                    # print("下载chromedriver.zip 失败")
                    self.msg.setIcon(QMessageBox.Information)
                    self.msg.setWindowTitle("information")
                    self.msg.setText(f"下载失败，状态码: {response.status_code}")
                    self.msg.setStandardButtons(QMessageBox.Ok)
                    self.msg.exec()
        else:
            self.msg.setIcon(QMessageBox.Information)
            self.msg.setWindowTitle("information")
            self.msg.setText(f"下载失败，状态码: {response.status_code}")
            self.msg.setStandardButtons(QMessageBox.Ok)

    def set_combobox_options(self, date):
        day_of_week = (
            date.dayOfWeek()
        )  # 判断时间格式date所处的星期几，dayOfWeek(),返回值为1-7，1表示星期一，7表示星期日

        if day_of_week == Qt.Thursday:  # Qt.Thursday表示星期四
            # self.comboBox_5.clear() # 使用方法clear(),清空comboBox中的选项
            # self.comboBox_5.addItems(["1", "3", "5","2","4","6"])   #设置comboBox的选项，使用方法addItems(),以列表的形式给出值
            # self.comboBox_7.clear()
            # self.comboBox_7.addItems(["1", "3", "5","2","4","6"])
            # self.comboBox_10.clear()
            # self.comboBox_10.addItems(["1", "3", "5","2","4","6"])
            # 弹出弹窗

            self.msg.setIcon(QMessageBox.Information)
            self.msg.setWindowTitle("information")
            self.msg.setText("当前是星期四，六点到九点的2、4、6号场地可能被占用，请注意！")
            self.msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

            # 创建定时器
            self.timer = QTimer(self)
            self.timer.setSingleShot(True)
            self.timer.timeout.connect(self.msg.close)
            self.msg.show()
            self.timer.start(1000)

        # # 星期三
        # elif day_of_week == Qt.Wednesday:   # Qt.Wednesday表示星期三
        #     self.comboBox_5.clear()
        #     self.comboBox_5.addItems(["2", "4", "6","1","3","5"])
        #     # 设置['1','3','5']为comboBox的选项,字体颜色为红色
        #     #
        #     self.comboBox_7.clear()
        #     self.comboBox_7.addItems(["2", "4", "6","1","3","5"])
        #     self.comboBox_10.clear()
        #     self.comboBox_10.addItems(["2", "4", "6","1","3","5"])

        # else:
        #     self.comboBox_5.clear()
        #     self.comboBox_5.addItems(["1", "2", "3", "4", "5", "6"])
        #     self.comboBox_7.clear()
        #     self.comboBox_7.addItems(["1", "2", "3", "4", "5", "6"])
        #     self.comboBox_10.clear()
        #     self.comboBox_10.addItems(["1", "2", "3", "4", "5", "6"])

    def msg_close(self):
        self.msg.close()

    def check(self):
        # 获取当前日期并加上2天
        current_date = (
            QDate.currentDate()
        )  # QDate.currentDate()获取当前日期，与之对应的，QTime.currentTime()获取当前时间
        target_date = current_date.addDays(2)  # 将时间元组增加指定天数，使用方法addDays()

        # 将结果设置为 dateEdit 的值
        self.dateEdit.setDate(target_date)  # 设置dateEdit控件的内容，使用方法setDate(),参数是时间元组

    @pyqtSlot()  # 使用修饰符pyqtSlot(),将该方法注册为槽
    def start_thread(self):
        # 如果线程列表为空，则退出函数
        # 这里应该优化一下，开始线程前，终止前面的线程
        if self.appointment_threads:
            return
        combobox_list_time = [
            self.comboBox_9,
            self.comboBox_2,
            self.comboBox_8,
        ]  # 每个线程对应的comboBox，用于选择时间
        combobox_list_num = [
            self.comboBox_5,
            self.comboBox_7,
            self.comboBox_10,
        ]  # 每个线程对应的comboBox，用于选择场地号
        keys = [
            Keys.SPACE,
            Keys.ESCAPE,
            Keys.ENTER,
        ]  # 模拟的按键，Keys.SPACE表示空格键，Keys.ENTER表示回车键，Keys.ESCAPE表示ESC键

        with ThreadPoolExecutor(max_workers=4) as executor:  # 使用线程池，最大线程数为3
            for index, (combo_box, combobox2, key) in enumerate(
                    zip(combobox_list_time, combobox_list_num, keys)
            ):  # 这里方法非常巧妙，使用了zip()方法，将多个列表的元素一一对应起来，然后使用enumerate()方法，将列表的索引和元素一一对应起来
                value = combo_box.currentText()  # 获取comboBox的当前选项，使用方法currentText()
                num = combobox2.currentText()  # 获取comboBox的当前选项，使用方法currentText()
                if value != "None":  # combo_box的内容设置为None，表示不选中当前进程，不加入线程池
                    value = int(value)  # 将字符串转换为整数。comboBox的内容是字符串形式，需要转换为整数
                    num = int(num)  # 同上
                    # 经典来了

                    appointment_thread = AppointmentPage(
                        self,
                        time_temp=value,
                        num_temp=num,
                        index=index + 1,
                        key_tmp=key,
                    )  # 创建线程对象。我们在类MyDisplay中声明了一个AppointmentThread类的对象，我们传入参数self，表示该线程对象的父对象是MyDisplay类的对象，然后设置了四个单独的参数用以区别不同的线程，参数time_tmp,num_temp,index,key_tmp

                    appointment_thread.errorOccurredWithInfo.connect(
                        self.displayErrorMessageWithInfo
                    )  # 连接 errorOccurredWithInfo 信号。这里便是我们在AppointmentThread声明的信号errorOccurredWithInfo，我们将其连接到displayErrorMessageWithInfo函数，我们之前声明了该信号会接受三个参数，(str,int,str)，对应的方法displayErrorMessageWithInfo也应接受三个参数
                    appointment_thread.finished.connect(
                        self.appointment_finished
                    )  # 将线程自带的finished信号，连接到appointment_finished方法上。在finished.emit()方法中会将需要的参数传递过来。
                    self.appointment_threads.append(appointment_thread)  # 将线程加入线程队列中
                    executor.submit(
                        appointment_thread.run
                    )  # 将线程加入线程池中，使用方法submit()，参数是线程对象的run方法

    def set_target_time(self):
        # 获取 timeEdit_1 的时间对象
        time_tmp = (
            self.timeEdit_1.time()
        )  # 获取timeEdit控件的内容，使用方法time()。返回值是时间对象。之前，dateEdit控件的内容也与之类似，也可以通过方法time()获取时间对象
        # 获取小时、分钟和秒
        hour = time_tmp.hour()  # 获取时间对象的小时，使用方法hour()
        minute = time_tmp.minute()  # 获取时间对象的分钟，使用方法minute()
        second = time_tmp.second()  # 获取时间对象的秒，使用方法second()

        # 设置 target_time
        target_time = QTime(hour, minute, second)  # 使用QTime类的构造函数，创建时间对象，参数是小时、分钟和秒

        # 打印目标时间
        # print(target_time.toString('hh:mm:ss.zzz'))  # 使用toString()方法，将时间对象转换为字符串，参数是时间格式，'hh:mm:ss.zzz'表示时、分、秒、毫秒
        current_time = QTime.currentTime()  # 使用QTime.currentTime()获取当前时间
        if target_time > current_time:
            time_to_target = current_time.msecsTo(
                target_time
            )  # 计算当前时间到目标时间的毫秒数，使用方法msecsTo()

            # 创建 QTimer 定时器对象
            # timer = QTimer()    # 使用QTimer类的构造函数，创建定时器对象
            self.timer.timeout.connect(
                self.start_thread
            )  # 将定时器的timeout信号，连接到start_thread方法上。表示到达目标时间时，执行start_thread方法

            # 启动定时器，在到达目标时间时触发 timeout 信号
            self.timer.setSingleShot(True)  # 设置定时器只运行一次
            self.timer.start(
                time_to_target
            )  # 启动定时器，使用方法start()，参数是时间。当时间到达时，会触发timeout信号
            msg = "定时器已启动，将在{}时{}分{}秒时开始预约".format(
                hour, minute, second
            )  # 使用format()方法，格式化字符串
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            msg = current_time + ":" + msg
            self.textBrowser.append(msg)

        else:
            self.start_thread()  # 如果目标时间已经过去，则直接执行start_thread方法

    @pyqtSlot(
        str, int, str
    )  # 使用修饰符pyqtSlot(),将该方法注册为槽。其参数类型与信号errorOccurredWithInfo的参数类型一致
    def displayErrorMessageWithInfo(self, current_time, index, error_info):
        error_message = f"[Time: {current_time}] [Thread: {index}] {error_info}"  # 使用f-string,格式化字符串
        self.textBrowser.append(error_message)

    def appointment_finished(self):  # 该方法是槽，用于处理信号finished
        sender = self.sender()  # 获取信号的发送者，使用方法sender()。返回值是发送者的对象
        self.appointment_threads.remove(sender)  # 将发送者从线程队列中移除，使用方法remove()
        sender.reset()  # 重置发送者，使用方法reset()
        # 获取当前时间
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        msg = current_time + ":" + "定时器已结束，请手动点击查询按钮进行查看"  # 使用format()方法，格式化字符串
        self.textBrowser.append(msg)

    # def resizeEvent(self, event):
    #     # 获取屏幕的几何信息
    #     screen_geometry = QCoreApplication.instance().desktop().availableGeometry()

    #     # 设置窗口的大小为屏幕的80%
    #     width = int(screen_geometry.width() * 0.23)
    #     height = int(screen_geometry.height() * 0.6)
    #     self.resize(width, height)

    #     # 将窗口移动到屏幕的中央
    #     window_geometry = self.geometry()
    #     x = int((screen_geometry.width() - window_geometry.width()) / 2)
    #     y = int((screen_geometry.height() - window_geometry.height()) / 2)
    #     self.setGeometry(QRect(x, y, window_geometry.width(), window_geometry.height()))
    def log_init(self):
        os.path.join(os.getcwd(), "error.log")
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.ERROR)
        handler = logging.FileHandler("error.log")
        handler.setLevel(logging.ERROR)

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def handle_exception(self, exc_type, exc_value, exc_traceback):
        self.logger.error(
            "Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback)
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.excepthook = window.handle_exception
    window.show()
    sys.exit(app.exec())
