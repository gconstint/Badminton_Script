from datetime import datetime
import time
import sys
from PyQt5.QtCore import QThread, pyqtSignal, QTime
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait


class AppointmentPage(QThread):
    loc_username = (By.NAME, "username")
    loc_password = (By.ID, "password")
    loc_login_btn = (By.ID, "login_submit")

    loc_date = (By.ID, "field31901")
    loc_time = (By.ID, "field31902_browserbtn")
    loc_field_type = (By.ID, "field31883_browserbtn")
    loc_field_num = (By.CSS_SELECTOR, "#CustomTree_3_span")
    loc_join_num = (By.ID, "field31884")
    loc_person_id = (By.ID, "field31885")
    loc_person_response = (By.ID, "field31888")
    loc_person_tel = (By.ID, "field31889")
    loc_submit_btn = (By.XPATH, '//*[@id="topTitleNew"]/tbody/tr/td/input[1]')

    finished = pyqtSignal()
    errorOccurredWithInfo = pyqtSignal(str, int, str)  # 自定义的信号，带有时间、线程号和错误信息作为参数

    # qt的信号和槽机制，用于线程间的通信,信号可以带参数，也可以不带参数
    # (str,int,str)说明含有三个参数，分别是str、int、str类型

    def __init__(
            self, parent=None, time_temp=None, num_temp=None, key_tmp=None, index=None
    ):
        # 对于这里的超类的初始化，需要把parent带上
        super().__init__(parent)
        self.type = parent.comboBox_6.currentText()

        self.account = parent.lineEdit.text()
        self.password = parent.lineEdit_2.text()

        self.field_type = 1

        self.date = parent.dateEdit.text()

        self.time_temp = time_temp

        self.num = num_temp

        self.join_num = "4"
        self.person_id = 1

        self.person_response = parent.lineEdit_3.text()
        self.person_tel = parent.lineEdit_4.text()

        self.commit = True if parent.comboBox_4.currentText() == "提交" else False

        # 判断checkBox控件是否被选择，使用方法isChecked()，如被选中，返回True，否则返回False
        self.brower_flag = parent.checkBox_1.isChecked()

        self.message_edit = parent.textBrowser
        self.index = index
        self.key_tmp = key_tmp
        self.timeEdit_3 = parent.timeEdit_3

        self.timeerror = parent.bug_windows.checkBox.isChecked()
        if self.timeerror:
            self.timeEdit_3 = parent.bug_windows.timeEdit_3
        self.twice_clicked = parent.bug_windows.checkBox_2.isChecked()
        self.old_clicked = parent.bug_windows.checkBox_3.isChecked()
        self.quit_flag = parent.bug_windows.checkBox_4.isChecked()

        self.driver = None
        self.url = "https://oa.shanghaitech.edu.cn/workflow/request/AddRequest.jsp?workflowid=14862&t_s=1648003625917&amp_sec_version_=1&gid_=dHArWDUwc2pjeWJMRlk3RlhKaEJoaG1vbmI3VE9PeE03Z1dGSlFVazIxWDVwcE9Zcnk5a2pIazdtTGM2eHFIVFRPS3NFNmVMYmIrRWNWUG1TZlg5RFE9PQ&EMAP_LANG=zh&THEME=cherry"
        # self.fail_flag = parent.checkBox_2.isChecked()

    def find_element(self, locator):
        return self.driver.find_element(*locator)

    def click(self, locator):
        self.find_element(locator).click()

    def input_text(self, locator, text):
        self.find_element(locator).send_keys(text)

    def start_driver(self):
        driver = None
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
                except Exception as e:
                    error_tmp = str(e)
                    error_message = "the version of webdriver is wrong!\nPlease visit the website: https://sites.google.com/chromium.org/driver/downloads \n Maybe you need to use VPN to visit this website!"
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    # 信号槽机制，将时间、手动输入的线程号、错误信息传递给主线程
                    self.errorOccurredWithInfo.emit(
                        current_time, self.index, error_message
                    )
                    # 退出线程
                    self.quit()
            else:
                try:
                    driver = webdriver.Chrome(service=Service("chromedriver.exe"))
                except Exception as e:
                    error_tmp = str(e)
                    error_message = "the version of webdriver is wrong!\nPlease visit the website: https://sites.google.com/chromium.org/driver/downloads \n Maybe you need to use VPN to visit this website!"
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    # 信号槽机制，将时间、手动输入的线程号、错误信息传递给主线程
                    self.errorOccurredWithInfo.emit(
                        current_time, self.index, error_message
                    )
                    # 退出线程
                    self.quit()
        else:
            if self.brower_flag:
                options = webdriver.EdgeOptions()
                options.add_argument("--headless")
                try:
                    # 尝试使用webdriver.Edge打开microsoft edge浏览器，如果失败，则说明webdriver版本不对，需要更新
                    driver = webdriver.Edge(
                        service=Service("msedgedriver.exe"), options=options
                    )
                except Exception as e:
                    error_tmp = str(e)
                    # print('the version of webdriver is wrong!')
                    # self.message_edit.append('the version of webdriver is wrong!\nPlease visit the website:https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/')
                    error_message = "the version of webdriver is wrong!\nPlease visit the website: https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/"
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    # 信号槽机制，将时间、手动输入的线程号、错误信息传递给主线程
                    self.errorOccurredWithInfo.emit(
                        current_time, self.index, error_message
                    )
                    # 退出线程
                    self.quit()
            else:
                try:
                    driver = webdriver.Edge(service=Service("msedgedriver.exe"))
                except Exception as e:
                    error_tmp = str(e)
                    # print('the version of webdriver is wrong!')
                    # self.message_edit.append('the version of webdriver is wrong!\nPlease visit the website:https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/')
                    error_message = "the version of webdriver is wrong!\nPlease visit the website: https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/"
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    self.errorOccurredWithInfo.emit(
                        current_time, self.index, error_message
                    )
                    self.quit()
        return driver

    def login(self, username, password):
        self.input_text(self.loc_username, username)
        self.input_text(self.loc_password, password)
        self.click(self.loc_login_btn)
        self.driver.implicitly_wait(5)
        if self.twice_clicked:
            self.driver.get(
                r"https://oa.shanghaitech.edu.cn/workflow/request/AddRequest.jsp?workflowid=14862&t_s=1648003625917&amp_sec_version_=1&gid_=dHArWDUwc2pjeWJMRlk3RlhKaEJoaG1vbmI3VE9PeE03Z1dGSlFVazIxWDVwcE9Zcnk5a2pIazdtTGM2eHFIVFRPS3NFNmVMYmIrRWNWUG1TZlg5RFE9PQ&EMAP_LANG=zh&THEME=cherry"
            )
        self.click_login_frame()

    def click_login_frame(self):
        self.driver.implicitly_wait(5)
        # 切换窗口，将窗口聚焦到最新打开的窗口上，使用方法switch_to.window(),参数为窗口的句柄,driver.window_handles[-1]表示最新打开的窗口
        self.driver.switch_to.window(self.driver.window_handles[-1])
        self.driver.switch_to.frame("bodyiframe")  # 切换frame，

    def choose_type(self, field_type):
        # Choose field type
        Select(self.driver.find_element(By.ID, "field32340")).select_by_index(
            field_type
        )  # 选择下拉框的第几个选项，从0开始。其中我们需要通过find_element找到下拉框的元素，然后使用Select()方法将其转换为下拉框的形式，然后使用select_by_index()方法选择第几个选项。

    def choose_date(self, date, key_tmp):
        try:
            date_temp = self.driver.find_element(By.ID, "field31901")  # 日期输入框
            self.driver.execute_script(
                "arguments[0].setAttribute(arguments[1], arguments[2])",
                date_temp,
                "value",
                date,
            )
            time.sleep(1)
            self.click((By.ID, "field31901browser"))

            # time.sleep(3)
            # actions = ActionChains(self.driver)
            # actions.send_keys(key_tmp)

            # # 执行动作3次
            # for i in range(3):
            #     actions.perform()
            self.driver.swtich_to.alert.dimiss()

            # # 等待弹窗消失
            # WebDriverWait(self.driver, 5).until(EC.invisibility_of_element_located((By.XPATH, '//*[@id="layui-layer1"]')))

        except:
            # 如果没有弹窗，就什么都不做
            pass

    def choose_time(self, time_temp):
        self.click(self.loc_time)

        self.driver.switch_to.default_content()  # 切换到默认frame。Switch focus to the default frame.
        self.driver.switch_to.frame(4)  # 切换到第4个frame
        self.driver.switch_to.frame(0)  # 切换到第0个frame
        time.sleep(2)
        self.click_time_in_iframe(time_temp)

    def click_time_in_iframe(self, time_temp):
        # 在iframe中点击时间
        times = (time_temp - 11) * 2 + 1
        if time_temp >= 21:
            # 当选择的时间大于21点时，需要点击下一页
            self.click(
                (
                    By.XPATH,
                    '//*[@id="_xTable"]/div[1]/div[3]/div/table/tbody/tr/td[2]/div/span/span[3]',
                )
            )
            time.sleep(1)
            self.click(
                (By.XPATH, '//*[@id="_xTable"]/div[1]/div[2]/table/tbody/tr[1]/td[3]/a')
            )
        else:
            self.click(
                (
                    By.XPATH,
                    '//*[@id="_xTable"]/div[1]/div[2]/table/tbody/tr[{}]/td[3]/a'.format(
                        times
                    ),
                )
            )

        self.driver.switch_to.default_content()  # 切换到默认frame。Switch focus to the default frame.
        self.driver.switch_to.frame("bodyiframe")  # 切换到bodyiframe

    def choose_field(self, field):
        self.click(self.loc_field_type)
        self.driver.switch_to.default_content()
        self.driver.switch_to.frame(4)
        self.driver.switch_to.frame(0)
        self.driver.switch_to.frame(0)

        self.click((By.CSS_SELECTOR, "#CustomTree_2_switch"))
        self.driver.implicitly_wait(5)
        self.click((By.CSS_SELECTOR, "#CustomTree_3_switch"))
        time.sleep(1)
        # 处理iframe切换
        self.click_field_in_iframe(field)

    def click_field_in_iframe(self, field):
        WebDriverWait(self.driver, 3).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#CustomTree_3_span"))
        )  # 设置等待时间，driver等待找到元素定位，通过css_selector去找元素，设置默认等待时间为3s
        elements = self.driver.find_elements(
            By.CSS_SELECTOR, '[id^="CustomTree_"][id$="_a"]'
        )  # 定位元素，以'CustomTree_'开头，'_span'结尾的css_selector的元素。

        # 选择场地号
        time.sleep(3)
        found_element = None
        # 选择场地号
        element_name = "羽毛球场地{}号".format(field)
        for element in elements[3:9]:
            # print(element.get_attribute("title"))
            if element.get_attribute("title") == element_name:
                found_element = element
                break
        if found_element is None:
            found_element = elements[3]  # 默认选择第一个场地

        found_element.click()

        self.click((By.XPATH, '//*[@id="btnok"]'))
        self.driver.switch_to.default_content()  # 切换到默认的frame
        self.driver.switch_to.frame("bodyiframe")  # 切换到bodyiframe

    def fill_form(self, join_num, person_id, person_response, person_tel):
        self.input_text(self.loc_join_num, join_num)
        # person identity
        Select(self.find_element(self.loc_person_id)).select_by_index(person_id)

        self.input_text(self.loc_person_response, person_response)
        self.input_text(self.loc_person_tel, person_tel)

        # third party service
        Select(self.driver.find_element(By.ID, "field31892")).select_by_index(2)

        time.sleep(2)

    def reset(self):
        self.quit()
        self.wait()

    def run(self):
        time.sleep(1 * int(self.index))
        try:
            self.appoint()
        except Exception as e:
            # 将错误信息转换为str格式，便于打印
            error_message = str(e)

            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # 给信号槽传递信息，该信号槽有三个变量分别对应不同的含义(str,int,str)
            self.errorOccurredWithInfo.emit(current_time, self.index, error_message)

            # 线程的退出，使用方法quit()
            self.quit()
        finally:
            self.finished.emit()

    def appoint(self):
        self.driver = self.start_driver()
        self.driver.get(
            r"https://oa.shanghaitech.edu.cn/workflow/request/AddRequest.jsp?workflowid=14862&t_s=1648003625917&amp_sec_version_=1&gid_=dHArWDUwc2pjeWJMRlk3RlhKaEJoaG1vbmI3VE9PeE03Z1dGSlFVazIxWDVwcE9Zcnk5a2pIazdtTGM2eHFIVFRPS3NFNmVMYmIrRWNWUG1TZlg5RFE9PQ&EMAP_LANG=zh&THEME=cherry"
        )

        self.login(self.account, self.password)

        self.choose_type(self.field_type)
        self.choose_date(self.date, self.key_tmp)
        self.choose_time(self.time_temp)
        self.choose_field(self.num)
        self.fill_form(
            self.join_num, self.person_id, self.person_response, self.person_tel
        )

        current_time = (
            QTime.currentTime()
        )  # 使用QTIme获取时间，我推荐在QT中使用QTime而不是datetime.now()
        # 获取 timeEdit_3 的时间对象
        time_tmp = self.timeEdit_3.time()

        hour = time_tmp.hour()  # 时间格式，获取小时数，hour()
        minute = time_tmp.minute()  # 时间格式，获取分钟数，minute()
        second = time_tmp.second()  # 时间格式，获取秒钟数，second()
        # 设置 target_time
        target_time = QTime(
            hour, minute, second
        )  # 将时间格式转换为QTime格式，QTime(hour, minute, second)，对应时、分、秒

        # 获取当前时间
        # current_time = QTime.currentTime()
        actions = ActionChains(self.driver)
        # 模拟按下某个键，空格对应Keys.SPACE、回车对应Keys.ENTER、Esc对应Keys.ESCAPE
        actions.send_keys(self.key_tmp)

        if self.timeerror:
            start_time = self.timeEdit_3.time()
            hour_start = start_time.hour()
            minute_start = start_time.minute()
            second_start = start_time.second()

            start_time_tmp = QTime(hour_start, minute_start, second_start)
            current_time = QTime.currentTime()
            # 如果当前时间未到达start_time_tmp，则等待
            while current_time < start_time_tmp:
                current_time = QTime.currentTime()
                time.sleep(0.2)

        if self.commit:
            if not self.old_clicked:
                # 新的点击方法
                while True:
                    try:
                        # 等待元素可见
                        self.driver.implicitly_wait(0.1)
                        self.driver.find_element(
                            By.XPATH, '//*[@id="topTitleNew"]/tbody/tr/td/input[1]'
                        ).click()
                        actions.perform()  # 执行点击动作

                    except:
                        pass
                    finally:
                        if self.driver.current_url != self.url:
                            break
            else:
                # 旧的点击方法
                while True:
                    try:
                        # 等待元素可见
                        self.driver.implicitly_wait(1)
                        self.driver.find_element(
                            By.XPATH, '//*[@id="topTitleNew"]/tbody/tr/td/input[1]'
                        ).click()
                        # actions.perform()   # 执行点击动作
                        self.driver.execute_script("window.alert = function() {};")

                    except:
                        # 如果没有弹窗，就什么都不做
                        pass
                    finally:
                        if self.driver.current_url != self.url:
                            break
        else:
            # driver.find_element(By.XPATH, '//*[@id="topTitleNew"]/tbody/tr/td/input[2]').click()
            while True:
                # print('保存test')
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # 给信号槽传递信息，该信号槽有三个变量分别对应不同的含义(str,int,str)
                self.errorOccurredWithInfo.emit(current_time, self.index, "Testing")
                current_time = QTime.currentTime()
                if current_time >= target_time:
                    break

        if self.timeerror:
            self.driver.implicitly_wait(1)
            # 切换窗口，将窗口聚焦到最新打开的窗口上，使用方法switch_to.window(),参数为窗口的句柄,driver.window_handles[-1]表示最新打开的窗口
            self.driver.switch_to.window(self.driver.window_handles[-1])
            self.driver.switch_to.frame("bodyiframe")  # 切换frame，
            try:
                self.driver.implicitly_wait(1)
                self.driver.find_element(
                    By.XPATH, '//*[@id="topTitleNew"]/tbody/tr/td/input[1]'
                ).click()
            except:
                pass

        if self.quit_flag:
            self.driver.quit()
