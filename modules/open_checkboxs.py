import os
import sys

from PyQt6.QtCore import QTime
from PyQt6.QtWidgets import QApplication, QWidget, QCheckBox, QTimeEdit
from PyQt6.QtCore import QSettings
# 获取当前脚本所在的目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 获取src目录的绝对路径
src_dir = os.path.dirname(current_dir)

# 将src目录添加到Python路径中
sys.path.append(src_dir)


try:
    from ui_source.bug_list import Ui_Form
except ModuleNotFoundError:
    from ..ui_source.bug_list import Ui_Form


class CheckBoxWindow(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Bug Window")
        self.resize(280, 250)
        self.dialogButtonBox.rejected.connect(self.close)
        self.dialogButtonBox.accepted.connect(self.close)
        self.settings = QSettings("MyCompany", "MyApp")
        self.restoreState()

    def closeEvent(self, event):
        self.saveState()
        event.accept()

    def saveState(self):
        for checkbox in self.findChildren(QCheckBox):
            self.settings.setValue(checkbox.objectName(), checkbox.isChecked())
        for timeedit in self.findChildren(QTimeEdit):
            self.settings.setValue(timeedit.objectName(), timeedit.time().toString())

    def restoreState(self):
        for checkbox in self.findChildren(QCheckBox):
            checked = self.settings.value(checkbox.objectName(), type=bool)
            checkbox.setChecked(checked)
        for timeedit in self.findChildren(QTimeEdit):
            time = self.settings.value(timeedit.objectName(), type=str)
            timeedit.setTime(QTime.fromString(time))


if __name__ == "__main__":
    app = QApplication([])
    window = CheckBoxWindow()
    window.show()
    app.exec_()
