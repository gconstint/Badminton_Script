from DrissionPage import ChromiumPage, ChromiumOptions
from DrissionPage.common import Keys
from datetime import date, timedelta

co = ChromiumOptions()
co.incognito()  # 匿名模式
# co.headless()  # 无头模式
co.set_argument('--no-sandbox')  # 无沙盒模式
username: str = "2021213203"
password: str = 'guanzhihao@0912'
field_type: int = 1
choose_date: str = "2024-06-27"
choose_time: int = 21
course_number: int = 6
join_number: str = "4"
person_id: int = 4
responsible_person: str = "关治豪"
responsible_person_tel: str = "13016406828"

page = ChromiumPage(co)
page.get(
    r'https://oa.shanghaitech.edu.cn/workflow/request/AddRequest.jsp?workflowid=14862&t_s=1648003625917&amp_sec_version_=1&gid_=dHArWDUwc2pjeWJMRlk3RlhKaEJoaG1vbmI3VE9PeE03Z1dGSlFVazIxWDVwcE9Zcnk5a2pIazdtTGM2eHFIVFRPS3NFNmVMYmIrRWNWUG1TZlg5RFE9PQ&EMAP_LANG=zh&THEME=cherry')

# 登录
page.ele("#username").input(username)
page.ele("#password").input(password)
page.ele("#login_submit").click()

# 等待页面跳转
page.wait.load_start()


# 设置场地类型，1为空白，2为羽毛球
page.ele('#field32340').select(text_or_index="羽毛球场")

# 设置选择日期
today = date.today()
choose_date = today + timedelta(days=3)
choose_date = choose_date.strftime("%Y-%m-%d")
date_input = page.ele('#field31901')
date_input.run_js('this.value="{}"'.format(choose_date))
page.wait(1)
# 消除弹窗
page.handle_alert(accept=True)

# 选择时间
page.ele("#field31902_browserbtn").click()
if choose_time >= 21:
    page.ele('xpath://*[@id="_xTable"]/div[1]/div[3]/div/table/tbody/tr/td[2]/div/span/span[3]').click()
    page.wait(1)
    page.ele('xpath://*[@id="_xTable"]/div[1]/div[2]/table/tbody/tr[1]/td[3]/a').click()
else:
    page.ele('//*[@id="_xTable"]/div[1]/div[2]/table/tbody/tr[{}]/td[3]/a'.format(
        choose_time)).click()

# 设置场地号
page.ele('#field31883_browserbtn').click()
page.ele('xpath://*[@id="CustomTree_2_switch"]').click()
page.ele('xpath://*[@id="CustomTree_3_switch"]').click()
ele = page.ele('xpath://*[@id="CustomTree_4_span"]')
ele.wait.displayed()
ele = page.eles('css:[id^="CustomTree_"][id$="_a"]')
element_name = "羽毛球场地{}号".format(course_number)

for i in ele[3:]:
    print(i.attr('title'))
    if i.attr('title') == element_name:
        i.click()
        break
page.ele("#btnok").click()

# 设置参与人数
page.ele("#field31884").input(join_number)

# 设置人员id，1为空白，2为学生
page.ele("#field31885").select(text_or_index="学生")

# 设置负责人
page.ele("#field31888").input(responsible_person)

# 设置负责人电话
page.ele("#field31889").input(responsible_person_tel)

# 设置第三方服务
page.ele("#field31892").select(text_or_index="无")


# 提交
page.ele('xpath://*[@id="topTitleNew"]/tbody/tr/td/input[1]').click()
while True:
    page.actions.key_down(Keys.ENTER)
    # 消除弹窗
    page.handle_alert(accept=True)
