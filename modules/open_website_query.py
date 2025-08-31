

from PyQt6.QtWidgets import QApplication, QWidget
import os,sys
# 获取当前脚本所在的目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 获取src目录的绝对路径
src_dir = os.path.dirname(current_dir)

# 将src目录添加到Python路径中
sys.path.append(src_dir)

from ui_source.time_is_website import Ui_Form
class MainWindow(QWidget,Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  
        self.setWindowTitle("Query")
        self.setGeometry(0, 0, 640, 455)
        self.pushButton.clicked.connect(self.refresh_page)
        # 点击pushButton_2按钮，关闭窗口
        self.pushButton_2.clicked.connect(self.close)
    def refresh_page(self):
        self.webEngineView.reload()

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
