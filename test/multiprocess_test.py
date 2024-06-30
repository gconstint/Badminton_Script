import sys
import multiprocessing
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget

# 创建一个Worker类
class Worker:
    def __init__(self, start_button):
        self.start_button = start_button

    def work(self):
        # 在这里编写工作任务
        self.start_button.setText("Working...")

# 创建工作任务类
class WorkerProcess(multiprocessing.Process):
    def __init__(self, start_button):
        super().__init__()
        self.start_button = start_button

    def run(self):
        app = QApplication([])  # 创建独立的Qt应用程序
        worker = Worker(self.start_button)
        worker.work()
        app.exec_()  # 启动Qt应用程序事件循环

# 创建主窗口类
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PyQt Multi-Process Example")
        self.setGeometry(100, 100, 400, 200)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        self.start_button = QPushButton("Start Processes", self)
        layout.addWidget(self.start_button)

        self.start_button.clicked.connect(self.start_processes)

    def start_processes(self):
        # 启动三个进程，每个进程中都运行一个Worker对象的work方法
        processes = []
        for _ in range(3):
            process = WorkerProcess(self.start_button)
            processes.append(process)
            process.start()

        # 等待所有进程完成
        for process in processes:
            process.join()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())