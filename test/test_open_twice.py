from selenium.webdriver.chrome.service import Service
from selenium.webdriver import Chrome

driver = Chrome(service=Service('chromedriver.exe'))

# 打开一个网页
driver.get('https://www.baidu.com')

# 在这里进行一些操作...

# 打开一个新的标签，显示 www.baidu.com
driver.get('https://www.baidu.com')

# 切换到新的标签
driver.switch_to.window(driver.window_handles[-1])

# 关闭原来的网页标签
# driver.close()

# 切换回新的标签
driver.switch_to.window(driver.window_handles[0])