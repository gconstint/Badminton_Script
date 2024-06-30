import datetime
import time
import os
import sys
import ctypes
import win32api
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # 设置窗口标题
        self.setWindowTitle("Set System Time")

        # 创建标签
        self.label = QLabel("Current Time: " + str(datetime.datetime.now()), self)

        # 创建按钮
        self.button = QPushButton("Set System Time", self)
        self.button.clicked.connect(self.set_system_time)

        # 创建布局
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)

        # 设置窗口布局
        self.setLayout(layout)

    def set_system_time(self):
        # 获取当前时间
        now = datetime.datetime.now()

        # 打印当前时间
        self.label.setText("Current Time: " + str(now))

        # 设置新的时间
        new_time = now + datetime.timedelta(seconds=120)

        # 将新的时间转换为时间戳
        new_time_stamp = time.mktime(new_time.timetuple())

        # 设置系统时间
        if sys.platform == "win32":
            # Windows系统
            if ctypes.windll.shell32.IsUserAnAdmin():
                # 已经以管理员身份运行
                win32api.SetSystemTime(new_time.year, new_time.month, new_time.weekday(), new_time.day, new_time.hour, new_time.minute, new_time.second, 0)
            else:
                # 以管理员身份运行
                cmd = f"\"{sys.executable}\" \"{os.path.abspath(__file__)}\""
                ctypes.windll.shell32.ShellExecuteW(None, "runas", "cmd.exe", f"/k {cmd}", None, 1)
        else:
            # Linux系统
            os.system(f"date -s @{int(new_time_stamp)}")


if __name__ == "__main__":
    # 创建应用程序对象
    app = QApplication(sys.argv)

    # 创建主窗口对象
    window = MainWindow()

    # 显示主窗口
    window.show()

    # 运行应用程序
    sys.exit(app.exec_())