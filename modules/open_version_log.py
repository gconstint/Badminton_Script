import os
import sys

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QWidget, QListWidgetItem

# 获取当前脚本所在的目录
current_dir = os.path.dirname(os.path.abspath(__file__))
# 获取src目录的绝对路径
src_dir = os.path.dirname(current_dir)
# 将src目录添加到Python路径中
sys.path.append(src_dir)

from ui_source.version_log import Ui_Form
from modules.version_manager import get_app_version
import version_config


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
        self.addLog("V2.8", "2024-09-26", "修复UI；增加更新WebDriver功能", "\n1.修改UI在小尺寸屏幕上的字体显示问题\n2.增加更新WebDriver功能。")
        self.addLog("V3.0", "2024-10-24","新增获取服务器时间功能","新增获取服务器时间功能")

        # 获取当前版本并添加到日志顶部
        current_version = get_app_version(
            repo_owner=version_config.GITHUB_REPO_OWNER,
            repo_name=version_config.GITHUB_REPO_NAME
        )
        self.addLog(f"V{current_version}", "当前版本", "版本号自动同步", "\n1.版本号现在自动与GitHub tag同步\n2.支持从本地Git和GitHub API获取版本信息")

        # 动态设置窗口标题，显示当前版本
        self.setWindowTitle(f"版本更新日志 - 当前版本: V{current_version}")

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
