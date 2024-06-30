import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox
import subprocess

class DisableChromeAutoUpdateApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setGeometry(100, 100, 300, 100)
        self.setWindowTitle('Disable Chrome Auto Update')

        self.button = QPushButton('Disable Auto Update', self)
        self.button.setGeometry(100, 30, 150, 40)
        self.button.clicked.connect(self.disable_auto_update)

    def disable_auto_update(self):
        try:
            
            # 如果是Windows系统，则使用runas命令以管理员身份运行Python解释器
            command = f'runas /user:guanzhihao "python {os.path.abspath(__file__)}"'
            subprocess.run(command, check=True, shell=True)
            
            subprocess.run('sc stop "gupdate"', check=True, shell=True)
            subprocess.run('sc stop "gupdatem"', check=True, shell=True)

            commands = [
              
                r'reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Google\Update" /v "AutoUpdateCheckPeriodMinutes" /t REG_DWORD /d 0 /f',
                r'reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Google\Update" /v "DisableAutoUpdateChecksCheckboxValue" /t REG_DWORD /d 1 /f',
                r'reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Google\Update" /v "UpdateDefault" /t REG_DWORD /d 0 /f'
            ]

            for command in commands:
                subprocess.run(command, check=True, shell=True)

            QMessageBox.information(self, 'Success', 'Google Chrome auto update has been disabled.')
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, 'Error', f"An error occurred while executing the command: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DisableChromeAutoUpdateApp()
    window.show()
    sys.exit(app.exec_())