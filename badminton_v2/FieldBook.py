from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from datetime import date, timedelta

# default: after 2 days
curr_time = date.today()
delta = timedelta(days=2)
dates = (curr_time + delta).strftime("%Y-%m-%d")


class Auto:
    def __init__(self, paralist, field_type=1, join_num=2, person_id=1):
        self.type = paralist['type']
        self.account = paralist['name']
        self.password = paralist['password']
        self.borrower1 = paralist['borrower_name1']
        self.borrower2 = paralist['borrower_name2']
        self.borrower1contact_info = paralist['borrower1contact_info']
        self.borrower2contact_info = paralist['borrower2contact_info']
        self.field_type = paralist['field_type']

        self.date = dates
        if paralist['date'] >= curr_time.strftime("%Y-%m-%d"):
            self.date = paralist['date']

        self.time_temp = paralist['start_time']
        self.times = (paralist['start_time'] - 11) * 2 + 1

        self.join_num = str(paralist['join_num'])
        self.person_id = paralist['person_id']
        self.person_response = paralist['person_response']
        self.person_tel = paralist['person_tel']
        self.user_list = paralist['user_list']

    def FieldBook(self):
        if self.type == '谷歌':
            driver = webdriver.Chrome(executable_path=r'chromedriver.exe')
        else:
            driver = webdriver.Edge(executable_path='msedgedriver.exe')

        driver.maximize_window()

        driver.get(
            r'https://oa.shanghaitech.edu.cn/workflow/request/AddRequest.jsp?workflowid=14862&t_s=1648003625917&amp_sec_version_=1&gid_=dHArWDUwc2pjeWJMRlk3RlhKaEJoaG1vbmI3VE9PeE03Z1dGSlFVazIxWDVwcE9Zcnk5a2pIazdtTGM2eHFIVFRPS3NFNmVMYmIrRWNWUG1TZlg5RFE9PQ&EMAP_LANG=zh&THEME=cherry')

        # auto login
        driver.find_element(By.NAME, 'username').send_keys(self.account)
        driver.find_element(By.ID, 'password').send_keys(self.password)
        driver.find_element(By.ID, 'login_submit').click()
        # driver.find_element(By.XPATH, '//*[@id="casLoginForm"]/p[4]/button').click()

        driver.implicitly_wait(5)
        driver.switch_to.window(driver.window_handles[-1])
        driver.switch_to.frame('bodyiframe')

        # # borrower name
        # driver.find_element(By.ID, 'field31898_0').send_keys(self.borrower1)
        # driver.find_element(By.ID, 'field31898_1').send_keys(self.borrower2)
        # driver.find_element(By.ID, 'field31899_0').send_keys(self.borrower1contact_info)
        # driver.find_element(By.ID, 'field31899_1').send_keys(self.borrower2contact_info)

        # Choose field type
        Select(driver.find_element(By.ID, 'field32340')).select_by_index(self.field_type)

        # Choose date
        date_temp = driver.find_element(By.ID, 'field31901')
        driver.execute_script("arguments[0].setAttribute(arguments[1], arguments[2])", date_temp, 'value', self.date)
        driver.find_element(By.ID, 'field31901browser').click()

        # Choose time
        driver.find_element(By.ID, 'field31902_browserbtn').click()
        driver.switch_to.default_content()
        driver.switch_to.frame(4)
        driver.switch_to.frame(0)
        driver.find_element(By.XPATH,
                            '//*[@id="_xTable"]/div[1]/div[2]/table/tbody/tr[{}]/td[3]/a'.format(self.times)).click()
        driver.switch_to.default_content()
        driver.switch_to.frame('bodyiframe')

        # Choose the number of field
        # 1
        driver.find_element(By.ID, 'field31883_browserbtn').click()
        driver.switch_to.default_content()
        driver.switch_to.frame(4)
        driver.switch_to.frame(0)
        driver.switch_to.frame(0)
        driver.find_element(By.XPATH, '//*[@id="CustomTree_2_switch"]').click()
        driver.find_element(By.XPATH, '//*[@id="CustomTree_3_switch"]').click()

        # 2
        # Always choose tree node # 4
        driver.find_element(By.XPATH, '//*[@id="CustomTree_4_span"]').click()
        driver.find_element(By.XPATH, '//*[@id="btnok"]').click()
        driver.switch_to.default_content()
        driver.switch_to.frame('bodyiframe')

        # joining number
        driver.find_element(By.ID, 'field31884').send_keys(self.join_num)

        # person identity
        Select(driver.find_element(By.ID, 'field31885')).select_by_index(self.person_id)

        # responsible person
        driver.find_element(By.ID, 'field31888').send_keys(self.person_response)
        driver.find_element(By.ID, 'field31889').send_keys(self.person_tel)

        # third party service
        Select(driver.find_element(By.ID, 'field31892')).select_by_index(2)

        # user list
        driver.find_element(By.ID, 'field31896').send_keys(self.user_list)

        # save
        driver.find_element(By.XPATH, '//*[@id="topTitleNew"]/tbody/tr/td/input[1]').click()

        print('Flow chat established. Successfully！')
        print("Appointment time: {0}, {1}—{2}".format(self.date, self.time_temp, self.time_temp + 1))

        return driver.quit()
