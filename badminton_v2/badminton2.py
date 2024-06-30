from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import UnexpectedAlertPresentException, NoAlertPresentException
from selenium.webdriver.support import expected_conditions as EC
from datetime import *
import time
# from threading import Thread
import multiprocessing
from datetime import datetime, timedelta
import ntplib
import pytz


def handle_alert(driver):
    try:
        wait = WebDriverWait(driver, timeout=2)
        alert = wait.until(lambda d: d.switch_to.alert)
        alert.accept()

    except (UnexpectedAlertPresentException, NoAlertPresentException):
        pass


def get_network_time():
    ntp_client = ntplib.NTPClient()
    # 使用国内NTP服务器IP地址
    ntp_servers = ['210.72.145.44', '203.107.6.88', '182.254.116.116', '166.111.8.28']

    for server in ntp_servers:
        try:
            response = ntp_client.request(server)
            return datetime.utcfromtimestamp(response.tx_time)
        except:
            pass
    raise Exception("All NTP servers failed.")


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
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--incognito")
        options.add_argument("--disable-extensions")
        # options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)
        driver.get(
            r'https://oa.shanghaitech.edu.cn/workflow/request/AddRequest.jsp?workflowid=14862&t_s=1648003625917&amp_sec_version_=1&gid_=dHArWDUwc2pjeWJMRlk3RlhKaEJoaG1vbmI3VE9PeE03Z1dGSlFVazIxWDVwcE9Zcnk5a2pIazdtTGM2eHFIVFRPS3NFNmVMYmIrRWNWUG1TZlg5RFE9PQ&EMAP_LANG=zh&THEME=cherry')

        # 登录
        driver.find_element(By.NAME, 'username').send_keys(self.username)
        driver.find_element(By.ID, 'password').send_keys(self.password)
        driver.find_element(By.ID, 'login_submit').click()

        time.sleep(3)
        driver.implicitly_wait(5)
        driver.switch_to.window(driver.window_handles[-1])
        driver.switch_to.frame('bodyiframe')

        # 设置场地类型
        Select(driver.find_element(By.ID, 'field32340')).select_by_index(self.field_type)
        time.sleep(3)

        # 设置日期
        today = date.today()
        choose_date = today + timedelta(days=3)
        choose_date = choose_date.strftime("%Y-%m-%d")

        date_input = driver.find_element(By.ID, 'field31901')
        driver.execute_script("arguments[0].setAttribute(arguments[1], arguments[2])", date_input, 'value',
                              choose_date)
        driver.find_element(By.ID, 'field31901browser').click()
        time.sleep(2)
        handle_alert(driver)

        # 设置时间
        driver.find_element(By.ID, 'field31902_browserbtn').click()
        driver.switch_to.default_content()
        driver.switch_to.frame(4)
        driver.switch_to.frame(0)
        if self.choose_time >= 21:
            driver.find_element(By.XPATH,
                                '//*[@id="_xTable"]/div[1]/div[3]/div/table/tbody/tr/td[2]/div/span/span[3]').click()
            time.sleep(1)
            driver.find_element(By.XPATH,
                                '//*[@id="_xTable"]/div[1]/div[2]/table/tbody/tr[1]/td[3]/a').click()
        else:
            time.sleep(1)
            time_temp = (self.choose_time - 11) * 2 + 1
            driver.find_element(By.XPATH,
                                '//*[@id="_xTable"]/div[1]/div[2]/table/tbody/tr[{}]/td[3]/a'.format(
                                    time_temp)).click()

        driver.switch_to.default_content()
        driver.switch_to.frame('bodyiframe')

        # 设置场地号
        # 1
        driver.find_element(By.ID, 'field31883_browserbtn').click()
        driver.switch_to.default_content()
        driver.switch_to.frame(4)
        driver.switch_to.frame(0)
        driver.switch_to.frame(0)
        driver.find_element(By.XPATH, '//*[@id="CustomTree_2_switch"]').click()
        driver.find_element(By.XPATH, '//*[@id="CustomTree_3_switch"]').click()
        # 2
        WebDriverWait(driver, 3).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#CustomTree_3_span"))
        )  # 设置等待时间，driver等待找到元素定位，通过css_selector去找元素，设置默认等待时间为3s
        elements = driver.find_elements(By.CSS_SELECTOR, '[id^="CustomTree_"][id$="_a"]')
        element_name = "羽毛球场地{}号".format(self.course_number)
        # 选择场地号
        time.sleep(3)
        found_element = None
        for i in elements[3:]:
            # print(i.get_attribute("title"))
            if i.get_attribute('title') == element_name:
                found_element = i
                break
        if found_element is None:
            found_element = elements[3]  # 默认选择第一个场地
        found_element.click()

        driver.find_element(By.XPATH, '//*[@id="btnok"]').click()
        driver.switch_to.default_content()
        driver.switch_to.frame('bodyiframe')

        # 设置参与人数
        driver.find_element(By.ID, 'field31884').send_keys(self.join_number)

        # 设置人员类型
        Select(driver.find_element(By.ID, 'field31885')).select_by_index(self.person_id)

        # 设置负责人及其电话
        driver.find_element(By.ID, 'field31888').send_keys(self.responsible_person)
        driver.find_element(By.ID, 'field31889').send_keys(self.responsible_person_tel)
        time.sleep(3)
        # 设置第三方服务
        Select(driver.find_element(By.ID, 'field31892')).select_by_index(2)

        # 提交
        ele = driver.find_element(By.XPATH, '//*[@id="topTitleNew"]/tbody/tr/td/input[1]')
        ele.click()
        # 精确计时
        # 获取网络时间
        ntp_time = get_network_time()
        # 设置北京时间时区
        beijing_tz = pytz.timezone('Asia/Shanghai')
        # 将NTP时间转换为北京时间
        beijing_time = ntp_time.replace(tzinfo=pytz.utc).astimezone(beijing_tz)
        # 设置开始时间
        start_time = datetime.strptime('11:59:59', '%H:%M:%S')
        current_time = datetime.strptime(beijing_time.strftime('%H:%M:%S'), '%H:%M:%S')
        # 打印北京时间
        print('Beijing Time:', beijing_time.strftime('%H:%M:%S'))

        # 本机需要17s才能运行到此
        if start_time.time() > current_time.time():
            t_diff = start_time - current_time
            t_diff_s = t_diff.total_seconds()
            print(t_diff_s)
            time.sleep(t_diff_s)

        # while True:
        #     try:
        #         if not ele.is_displayed():
        #             break
        #         ele.click()
        #         handle_alert(driver)
        #     except UnexpectedAlertPresentException:
        #         continue
        try:
            ele.click()
            handle_alert(driver)
        except UnexpectedAlertPresentException:
            pass
        try:
            ele.click()
            handle_alert(driver)
        except UnexpectedAlertPresentException:
            pass
        try:
            ele.click()
            handle_alert(driver)
        except UnexpectedAlertPresentException:
            pass
        try:
            ele.click()
            handle_alert(driver)
        except UnexpectedAlertPresentException:
            pass
        try:
            ele.click()
            handle_alert(driver)
        except UnexpectedAlertPresentException:
            pass
        try:
            ele.click()
            handle_alert(driver)
        except UnexpectedAlertPresentException:
            pass
        try:
            ele.click()
            handle_alert(driver)
        except UnexpectedAlertPresentException:
            pass

        if self.wrong_flag:
            driver.implicitly_wait(1)
            driver.switch_to.window(driver.window_handles[-1])
            driver.switch_to.frame("bodyiframe")  # 切换frame，
            driver.implicitly_wait(1)
            driver.find_element(
                By.XPATH, '//*[@id="topTitleNew"]/tbody/tr/td/input[1]').click()


def run_badminton_instance(c: BadmintonPage):
    c.work()


if __name__ == "__main__":
    # 设置粗计时
    # 设置开始时间
    current_time = datetime.now().strftime('%H:%M:%S')
    start_time = datetime.strptime('11:59:00', '%H:%M:%S')
    # 获取当前时间的datetime对象
    current_time = datetime.strptime(current_time, '%H:%M:%S')
    # 本机时间大概慢了2s，不过没关系，通过精确计时可以弥补
    if start_time.time() > current_time.time():
        # t = start_time - current_time
        t_diff = start_time - current_time
        t_diff_s = t_diff.total_seconds()
        print(t_diff_s)
        time.sleep(t_diff_s)

    badminton1 = BadmintonPage(username='2021213203', password='guanzhihao@0912', field_type=1,
                               choose_date='',
                               choose_time=21, course_number=6, join_number='4', person_id=3,
                               responsible_person='关治豪', responsible_person_tel='13016406828')
    badminton2 = BadmintonPage(username='2021213203', password='guanzhihao@0912', field_type=1,
                               choose_date='',
                               choose_time=21, course_number=4, join_number='4', person_id=3,
                               responsible_person='关治豪', responsible_person_tel='13016406828')

    # Thread(target=run_badminton_instance, args=(badminton1,)).start()
    # Thread(target=run_badminton_instance, args=(badminton2,)).start()
    with multiprocessing.Pool(2) as p:
        p.map(run_badminton_instance, [badminton1, badminton2])
