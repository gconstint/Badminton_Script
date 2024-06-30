import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from example_ui import Ui_MainWindow  # 导入通过pyuic5生成的Python文件

class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # 设置UI

        # Connect the button click event to a function
        self.pushButton.clicked.connect(self.button_clicked)

    def button_clicked(self):
        # Handle the button click event
        text = self.lineEdit.text()
        print(f"Button clicked! Text in the line edit: {text}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec_())
