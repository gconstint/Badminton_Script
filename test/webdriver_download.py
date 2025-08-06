from pprint import pprint

import requests

# JSON文件的URL，通常是直接的下载链接
json_url = 'https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json'

# 发送GET请求获取JSON文件内容
response = requests.get(json_url, allow_redirects=True)

# 检查请求是否成功
if response.status_code == 200:
    url = response.json()["channels"]["Stable"]["downloads"]["chromedriver"][-1]["url"]  # -1 表示win64平台
    version_num = url.split("/")[-3]
    pprint(url)
    pprint("version: " + version_num)
    # TODO: 下载文件
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
        print("download success")

        # 对zip文件进行解压操作
        import zipfile

        with zipfile.ZipFile('chromedriver.zip', 'r') as zip_ref:
            zip_ref.extractall('.')
        print("extract success")

        # 将解压后的chromedriver.exe文件移动到上一级目录
        import os
        import shutil

        # TODO: 移动文件
        os.chdir('chromedriver-win64')
        os.rename('chromedriver.exe', '../chromedriver.exe')
        print("move success")
        # TODO: 删除zip及其解压文件
        os.chdir('..')
        os.remove('chromedriver.zip')
        shutil.rmtree('chromedriver-win64')
        print("delete success")


    else:
        print("下载chromedriver.zip 失败")

else:
    print(f"下载失败，状态码: {response.status_code}")
