from datetime import datetime

import LoadTxt
import tkinter as tk
from tkinter import *
import time
paralist = {
    'type': '',
    'name': '',
    'password': '',
    'borrower_name1': '',
    'borrower_name2': '',
    'borrower1contact_info': '',
    'borrower2contact_info': '',
    'field_type': 1,
    'date': '',
    'start_time': '',
    'how_long': 2,
    'join_num': 2,
    'person_id': 1,
    'person_response': '',
    'person_tel': '',
    'user_list': '',
}


def windows_display(para):
    windows_temp = tk.Tk()
    tmp1 = tk.Label(windows_temp, text="预约成功")
    tmp1.pack(side=TOP)
    time_tmp = str(para['start_time']) if para['how_long'] == 1 else str(para['start_time'] - 1)
    tmp2 = tk.Label(windows_temp, text="预约时间：" + str(para['date']) + ' ' + time_tmp + "点")
    tmp2.pack(side=BOTTOM)
    sw = windows_temp.winfo_screenwidth()
    sh = windows_temp.winfo_screenheight()
    ww, wh = 160, 50
    x, y = (sw - ww) / 2, (sh - wh) / 2
    windows_temp.geometry("%dx%d+%d+%d" % (ww, wh, x, y))
    windows_temp.mainloop(0)


if __name__ == '__main__':
    filename = 'auto_info.txt'
    LoadTxt.load_txt(paralist, filename)
    while True:
        # time.sleep(1)
        current_date_and_time = datetime.now()
        current_time = current_date_and_time.strftime("%H:%M:%S")
        if '11:59:59' <= current_time <= '12:00:05':

            robot1 = Auto(paralist)
            robot1.FieldBook()
            if int(paralist['how_long']) == 2:
                paralist['start_time'] += 1
                robot2 = Auto(paralist)
                robot2.FieldBook()

            windows_display(paralist)
            time.sleep(1)
