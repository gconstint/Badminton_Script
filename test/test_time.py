import re
import sys
import requests
from PyQt5.QtCore import QTimer, QDateTime, Qt, QTimeZone
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget
from showtime  import Ui_Form
class MainWindow(QWidget,Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  
        
        self.setWindowTitle("Time calibration")  
        self.setGeometry(100, 100, 400, 200)


        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(500)

        self.update_time()

    def update_time(self):
        system_time = QDateTime.currentDateTime().toString(Qt.ISODate)
        # Set the system_time in the QDateTimeEdit widget
        self.dateTimeEdit.setDisplayFormat("yyyy-MM-dd HH:mm:ss.zzz")
        self.dateTimeEdit.setDateTime(QDateTime.fromString(system_time, Qt.ISODate))

        shanghai_time = self.get_shanghai_time()
        # Set the shanghai_time in the QDateTimeEdit widget
        self.dateTimeEdit_2.setDisplayFormat("yyyy-MM-dd HH:mm:ss.zzz")
        self.dateTimeEdit_2.setTimeSpec(Qt.UTC)
        self.dateTimeEdit_2.setDateTime(QDateTime.fromString(shanghai_time, Qt.ISODate))

        # self.shanghai_time_label.setText(f"Shanghai Time: {shanghai_time}")

    def get_shanghai_time(self):
        try:
            response = requests.get("http://worldtimeapi.org/api/timezone/Asia/Shanghai")
            response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
            data = response.json()
            shanghai_time = data["datetime"]
            return shanghai_time
        except (requests.exceptions.RequestException, ValueError, KeyError):
            # Handle network errors, JSON decoding errors, and missing keys in the response
            return "N/A"



if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()

    main_window.show()
    sys.exit(app.exec_())