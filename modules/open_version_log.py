import os, sys
from PyQt5.QtWidgets import QApplication, QWidget, QListWidgetItem
from PyQt5.QtGui import QIcon

# 获取当前脚本所在的目录
current_dir = os.path.dirname(os.path.abspath(__file__))
# 获取src目录的绝对路径
src_dir = os.path.dirname(current_dir)
# 将src目录添加到Python路径中
sys.path.append(src_dir)

from ui_source.version_log import Ui_Form


class LogWindow(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        # 创建 QListWidget 控件并添加到布局中
        self.log = self.listWidget
        # 添加列表项

        self.addLog(
            "V2.7.1",
            "2023-11-06",
            "更新UI，修复部分BUG",
            "\n1.新增BUGLIST窗口。",
        )
        self.addLog(
            "V2.7.2",
            "2023-11-07",
            "更新UI，修复部分BUG",
            "\n1.新增了版本更新日志窗口。\
            \n2.修复了部分BUG。",
        )
        self.addLog(
            "V2.7.3",
            "2023-12-04",
            "更新UI,更改弹窗清除模式",
            "\n1.更新UI，先支持自由缩放功能以及最大化。\
            \n2.使用alert消除弹窗",
        )
        self.addLog("V2.7.4", "2024-01-09", "新增功能", "\n1.增加log日志文件，自动保存软件崩溃日志")

        self.setWindowTitle("版本更新日志")

    def addLog(self, version, update_time, main_log, all_log):
        # 在日志组件中添加一条日志
        icon = QIcon(".middle_excalmatory.png")
        item = QListWidgetItem(icon, f"{version}: {main_log}", self.log)
        item.setToolTip(f"{version}({update_time}): {main_log}{all_log}")


if __name__ == "__main__":
    app = QApplication([])
    window = LogWindow()
    window.show()
    sys.exit(app.exec_())
