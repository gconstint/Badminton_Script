import argparse
import time
from datetime import datetime

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

class AppointmentCLI:
    # Locator constants
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

    def __init__(self, args):
        self.account = args.username
        self.password = args.password
        self.date = args.date
        self.time_temp = args.time
        self.num = args.court
        self.field_type = args.field_type  # 新增
        self.join_num = "4"
        self.person_id = 1
        self.person_response = args.contact_name
        self.person_tel = args.contact_phone
        self.headless = args.headless
        self.browser_type = args.browser
        self.commit = args.commit
        self.submit_time = getattr(args, 'submit_time', None)  # 新增
        self.submit_key = int(getattr(args, 'submit_key', 1))  # 1=空格，2=回车，3=ESC

        self.driver = None
        self.url = "https://oa.shanghaitech.edu.cn/workflow/request/AddRequest.jsp?workflowid=14862&t_s=1648003625917&amp_sec_version_=1&gid_=dHArWDUwc2pjeWJMRlk3RlhKaEJoaG1vbmI3VE9PeE03Z1dGSlFVazIxWDVwcE9Zcnk5a2pIazdtTGM2eHFIVFRPS3NFNmVMYmIrRWNWUG1TZlg5RFE9PQ&EMAP_LANG=zh&THEME=cherry"

    def find_element(self, locator):
        return self.driver.find_element(*locator)

    def click(self, locator):
        self.find_element(locator).click()

    def input_text(self, locator, text):
        self.find_element(locator).send_keys(text)

    def start_driver(self):
        if self.browser_type == "chrome":
            options = webdriver.ChromeOptions()
            if self.headless:
                options.add_argument("--headless")
            try:
                return webdriver.Chrome(service=Service("chromedriver.exe"), options=options)
            except Exception as e:
                print(f"Chrome driver启动失败: {e}")
                raise
        else:
            options = webdriver.EdgeOptions()
            if self.headless:
                options.add_argument("--headless")
            try:
                return webdriver.Edge(service=Service("msedgedriver.exe"), options=options)
            except Exception as e:
                print(f"Edge driver启动失败: {e}")
                raise

    def login(self, username, password):
        self.input_text(self.loc_username, username)
        self.input_text(self.loc_password, password)
        self.click(self.loc_login_btn)
        self.driver.implicitly_wait(5)
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

            # 修正拼写错误
            try:
                self.driver.switch_to.alert.dismiss()
            except Exception:
                pass  # 没有弹窗时忽略

            # # 等待弹窗消失
            # WebDriverWait(self.driver, 5).until(EC.invisibility_of_element_located((By.XPATH, '//*[@id="layui-layer1"]')))

        except Exception as e:
            print(f"choose_date error: {e}")
            pass

    def choose_time(self, time_temp):
        self.click(self.loc_time)

        # 切换到默认frame。Switch focus to the default frame.
        self.driver.switch_to.default_content()
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
                (By.XPATH,
                 '//*[@id="_xTable"]/div[1]/div[2]/table/tbody/tr[1]/td[3]/a')
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

        # 切换到默认frame。Switch focus to the default frame.
        self.driver.switch_to.default_content()
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
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "#CustomTree_3_span"))
        )  # 设置等待时间，driver等待找到元素定位，通过css_selector去找元素，设置默认等待时间为3s
        elements = self.driver.find_elements(
            By.CSS_SELECTOR, '[id^="CustomTree_"][id$="_a"]'
        )  # 定位元素，以'CustomTree_'开头，'_span'结尾的css_selector的元素。

        # 通配符匹配场地类型
        time.sleep(3)
        found_element = None
        for element in elements[3:9]:
            title = element.get_attribute("title")
            if title and "场" in title and str(field) in title:
                found_element = element
                break
        if found_element is None:
            # 兜底：只要有“场”字的都可以
            for element in elements[3:9]:
                title = element.get_attribute("title")
                if title and "场" in title:
                    found_element = element
                    break
        if found_element is None:
            found_element = elements[3]  # 还找不到就默认第一个

        found_element.click()

        self.click((By.XPATH, '//*[@id="btnok"]'))
        self.driver.switch_to.default_content()  # 切换到默认的frame
        self.driver.switch_to.frame("bodyiframe")  # 切换到bodyiframe

    def fill_form(self, join_num, person_id, person_response, person_tel):
        self.input_text(self.loc_join_num, join_num)
        # person identity
        Select(self.find_element(self.loc_person_id)
               ).select_by_index(person_id)

        self.input_text(self.loc_person_response, person_response)
        self.input_text(self.loc_person_tel, person_tel)

        # third party service
        Select(self.driver.find_element(By.ID, "field31892")).select_by_index(2)

        time.sleep(2)

    def run(self):
        try:
            self.driver = self.start_driver()
            print("Starting appointment process...")
            self.appoint()
            print("Appointment completed successfully!")
        except Exception as e:
            print(f"Error occurred: {str(e)}")
        finally:
            if self.driver:
                self.driver.quit()

    def appoint(self):
        self.driver.get(
            r"https://oa.shanghaitech.edu.cn/workflow/request/AddRequest.jsp?workflowid=14862&t_s=1648003625917&amp_sec_version_=1&gid_=dHArWDUwc2pjeWJMRlk3RlhKaEJoaG1vbmI3VE9PeE03Z1dGSlFVazIxWDVwcE9Zcnk5a2pIazdtTGM2eHFIVFRPS3NFNmVMYmIrRWNWUG1TZlg5RFE9PQ&EMAP_LANG=zh&THEME=cherry"
        )

        self.login(self.account, self.password)

        self.choose_type(self.field_type)  # 传递场地类型
        self.choose_date(self.date, "")
        self.choose_time(self.time_temp)
        self.choose_field(self.num)
        self.fill_form(
            self.join_num, self.person_id, self.person_response, self.person_tel
        )


        key_map = {1: Keys.SPACE, 2: Keys.ENTER, 3: Keys.ESCAPE}
        key_to_press = key_map.get(self.submit_key, Keys.SPACE)
        actions = ActionChains(self.driver)
        if key_to_press:
            actions.send_keys(key_to_press)

        # 新增：等待到提交时间
        if self.submit_time:
            now = datetime.now()
            try:
                submit_today = datetime.strptime(now.strftime("%Y-%m-%d ") + self.submit_time, "%Y-%m-%d %H:%M:%S")
            except Exception:
                print(f"提交时间格式错误，应为 HH:MM:SS，实际为: {self.submit_time}")
                submit_today = now
            wait_seconds = (submit_today - now).total_seconds()
            if wait_seconds > 0:
                print(f"距离提交时间还有 {wait_seconds:.3f} 秒，等待中...")
                time.sleep(wait_seconds)
                
        if self.commit ==0:
            print("Test finished!")
        else:
            while True:
                try:
                    # 等待元素可见
                    self.driver.implicitly_wait(0.1)
                    self.driver.find_element(
                        By.XPATH, '//*[@id="topTitleNew"]/tbody/tr/td/input[1]'
                    ).click()
                    actions.perform()  # 执行点击动作
                except Exception as e:
                    pass
                finally:
                    if self.driver.current_url != self.url:
                        break
                    # if time.time() - start_time > timeout:
                    #     print("提交超时，未检测到页面跳转。")
                    #     break


def main():
    parser = argparse.ArgumentParser(
        description='Badminton Court Appointment CLI')
    parser.add_argument('--config', type=str, help='Path to config file (key=value per line)')
    parser.add_argument('--username', required=False,
                        help='Login username')
    parser.add_argument('--password', required=False,
                        help='Login password')
    parser.add_argument('--date', required=False,
                        help='Appointment date (YYYY-MM-DD)')
    parser.add_argument('--time', required=False, type=int,
                        help='Appointment time (hour, e.g. 21 for 21:00)')
    parser.add_argument('--court', required=False, type=int,
                        help='Court number (e.g. 4)')
    parser.add_argument('--field-type', required=False, type=int, choices=[1,2,3,4,5,6],
                        help='Field type: 1=羽毛球场, 2=乒乓球场, 3=网球场, 4=匹克球场')
    parser.add_argument('--contact-name', required=False,
                        help='Contact person name')
    parser.add_argument('--contact-phone', required=False,
                        help='Contact person phone')
    parser.add_argument(
        '--browser', choices=['chrome', 'edge'], help='Browser type')
    parser.add_argument('--headless', required=False, type=bool,
                        help='Run in headless mode')
    parser.add_argument('--commit', required=False, type=int,
                        help='Actually submit the appointment')
    parser.add_argument('--submit-time', required=False, help='Earliest time to submit (format: HH:MM:SS)')
    parser.add_argument('--submit-key', required=False, type=int, choices=[1,2,3],
                        help='Key to press on submit: 1=空格, 2=回车, 3=ESC (default: 1)')
    parser.add_argument('--start-time', required=False, help='Earliest time to start the program (format: HH:MM:SS)')
    parser.add_argument('--check-date', required=False, type=int, choices=[0,1],
                        help='If 1, use current date + 2 days as appointment date (default: 0)')

    args = parser.parse_args()

    # 处理 config 文件
    config_dict = {}
    if args.config:
        with open(args.config, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if '=' in line:
                    k, v = line.split('=', 1)
                    config_dict[k.strip()] = v.strip()

    # 用 config_dict 填充缺失参数
    def get_arg(name, default=None, is_bool=False, is_int=False):
        val = getattr(args, name.replace('-', '_'))
        if val is not None:
            return val
        if name in config_dict:
            v = config_dict[name]
            if is_bool:
                return str(v).strip().lower() in ('1', 'true', 'yes', 'on')
            if is_int:
                try:
                    return int(v)
                except Exception:
                    return default
            return v
        return default

    # 新增：启动时间等待
    start_time_str = get_arg('start-time')
    if start_time_str:
        now = datetime.now()
        try:
            start_today = datetime.strptime(now.strftime("%Y-%m-%d ") + start_time_str, "%Y-%m-%d %H:%M:%S")
        except Exception:
            print(f"启动时间格式错误，应为 HH:MM:SS，实际为: {start_time_str}")
            start_today = now
        wait_seconds = (start_today - now).total_seconds()
        if wait_seconds > 0:
            print(f"距离启动时间还有 {wait_seconds:.3f} 秒，等待中...")
            time.sleep(wait_seconds)

    # 检查必需参数
    required_args = ['username', 'password', 'date', 'time', 'court', 'field-type', 'contact-name', 'contact-phone']
    missing = [a for a in required_args if get_arg(a) is None]
    if missing:
        parser.error(f'Missing required arguments: {", ".join(missing)}')

    # check-date 逻辑：如果为1，则date为当前日期+2天
    check_date_flag = get_arg('check-date', is_int=True)
    if check_date_flag == 1:
        from datetime import timedelta
        date_val = (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d")
    else:
        date_val = get_arg('date')
    # 构造 args 对象
    class Args:
        pass
    merged_args = Args()
    merged_args.username = get_arg('username')
    merged_args.password = get_arg('password')
    merged_args.date = date_val
    merged_args.time = get_arg('time', is_int=True)
    merged_args.court = get_arg('court', is_int=True)
    merged_args.field_type = get_arg('field-type', is_int=True)
    merged_args.contact_name = get_arg('contact-name')
    merged_args.contact_phone = get_arg('contact-phone')
    merged_args.browser = get_arg('browser', default='chrome')
    merged_args.headless = get_arg('headless', is_bool=True)
    merged_args.commit = get_arg('commit', is_int=True)
    merged_args.submit_time = get_arg('submit-time')
    merged_args.submit_key = get_arg('submit-key', default=1, is_int=True)

    appointment = AppointmentCLI(merged_args)
    appointment.run()


if __name__ == "__main__":
    main()
