from PyQt6.QtWidgets import QApplication, QWidget

from ui_source.time_is_website import Ui_Form


class TimeWindow(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Time.is")
        self.resize(640, 455)
        self.pushButton.clicked.connect(self.refresh_page)
        # 点击pushButton_2按钮，关闭窗口
        self.pushButton_2.clicked.connect(self.close)

    def refresh_page(self):
        self.webEngineView.reload()

    def closeEvent(self, event):
        # 停止加载网页
        self.webEngineView.stop()
        event.accept()


if __name__ == "__main__":
    app = QApplication([])
    window = TimeWindow()
    window.show()
    app.exec_()
