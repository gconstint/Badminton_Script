from datetime import datetime

import requests
from pytz import timezone, utc


def get_server_time(url):
    try:
        # 发送 HEAD 请求，只获取响应头信息
        response = requests.head(url, timeout=10)
        # 从响应头中获取 'Date' 字段
        server_time = response.headers.get('Date')

        if server_time:
            print(f"Server Time: {server_time}")
        else:
            print("Date header not found in the response.")
    except requests.RequestException as e:
        print(f"Error fetching server time: {e}")


def tz_switch(time):
    time1 = datetime.strptime(time, "%a, %d %b %Y %H:%M:%S %Z")
    time1 = time1.replace(tzinfo=utc)

    local_tz = timezone('Asia/Shanghai')
    time2 = time1.astimezone(local_tz)

    print("Switched time:", time2)
    return time2




url = "https://oa.shanghaitech.edu.cn/workflow/request/AddRequest.jsp?workflowid=14862&t_s=1648003625917&amp_sec_version_=1&gid_=dHArWDUwc2pjeWJMRlk3RlhKaEJoaG1vbmI3VE9PeE03Z1dGSlFVazIxWDVwcE9Zcnk5a2pIazdtTGM2eHFIVFRPS3NFNmVMYmIrRWNWUG1TZlg5RFE9PQ&EMAP_LANG=zh&THEME=cherry"

# 示例：获取 example.com 的服务器时间
# get_server_time(url)

response = requests.get(url, timeout=10)
server_time = response.headers.get("Date")
print(server_time)
switched_time = tz_switch(server_time).time()
print(switched_time)
local_time = datetime.now().time()
print(local_time)
