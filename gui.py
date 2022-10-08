import datetime
import tkinter.messagebox
from threading import Thread
from tkinter import *
from tkinter import ttk
from multiprocessing.pool import ThreadPool as Pool
import scraper


def update_data():
    if lot_entry.get() != '':
        if lot_entry.get() in lots_arr:
            lots_arr.remove(lot_entry.get())
        else:
            lots_arr.append(lot_entry.get())
    login_lbl.config(text=f"Логин: {login_entry.get()}")
    password_lbl.config(text=f"Пароль: {password_entry.get()}")
    lot_lbl.config(text=f"Список лотов: {lots_arr}\n")


def update_time():  # 9670826565, # 853434
    now = datetime.datetime.now(offset)
    now_delta = (now + datetime.timedelta(seconds=int(time_to_load) + 2)).strftime('%H:%M:%S')
    if now_delta == start_time:
        results = [0] * len(lots_arr)
        threads = []
        for i, lot in enumerate(lots_arr):
            th = Thread(target=scraper.main, args=([login_entry.get(), password_entry.get(), lot, ''], results, i))
            threads.append(th)
            th.start()
        for th in threads:
            th.join()
        result_str = ''
        for i in results:
            result_str += f"[{round(i['time'], 2)} сек.] Лот №{i['lot']}: {'+' if i['res'] else '-'}\n"
        tkinter.messagebox.showinfo(title='Результат обработки', message=f"{result_str}")
    current_time_lbl.config(text=f"\nТекущее время: {now.strftime('%H:%M:%S')}\n", font="Helvetica 20 bold")
    root.after(1000, update_time)


def load_time():
    global time_to_load
    if thread.is_alive():
        root.after(1000, load_time)
    else:
        time_to_load = round(res[0]['time'], 2)
        time_to_load_lbl.config(text=f"\nВремя необходимое для загрузки: {time_to_load} сек.")



time_to_load = 0
start_time = '16:32:00'
res = [0]
thread = Thread(target=scraper.main, args=(['9670826565', '853434', '6324', 'test-time'], res, 0))
thread.start()
root = Tk()
root.geometry("550x550")
root.title("Аукцион Бот")
lots_arr = []
login_entry = Entry()
password_entry = Entry()
lot_entry = Entry()
offset = datetime.timezone(datetime.timedelta(hours=3))
now = datetime.datetime.now(offset).strftime("%H:%M:%S")
current_time_lbl = Label(root, text=f"\nТекущее время: {now}\n", font="Helvetica 20 bold")
current_data_lbl = Label(root, text="\nДанные для запроса:", font="Helvetica 14 bold")
login_lbl = Label(root, text=f"Логин:")
password_lbl = Label(root, text=f"Пароль:")
lot_lbl = Label(root, text=f"Список лотов:\n")
btn = Button(root, text="Зафиксировать данные", command=update_data)
login_set_lbl = Label(root, text="\nЛогин")
password_set_lbl = Label(root, text="Пароль")
lot_set_lbl = Label(root, text="Лот")
ttk.Separator(root, orient='horizontal').pack(fill='x')
current_time_lbl.pack()
ttk.Separator(root, orient='horizontal').pack(fill='x')
current_data_lbl.pack()
login_lbl.pack()
password_lbl.pack()
lot_lbl.pack()
ttk.Separator(root, orient='horizontal').pack(fill='x')
login_set_lbl.pack()
login_entry.pack()
password_set_lbl.pack()
password_entry.pack()
lot_set_lbl.pack()
lot_entry.pack()
Label(root, text='\nНе забудьте нажать на кнопку, данные должны обновиться сверху.\nДля удвления лота из списка просто введите его номер и нажмите кнопку.\n').pack()
ttk.Separator(root, orient='horizontal').pack(fill='x')
btn.pack()
ttk.Separator(root, orient='horizontal').pack(fill='x')
Label(root, text=f"\nСкрипт работает в {start_time} часов дня по Мск").pack()
time_to_load_lbl = Label(root, text='')
time_to_load_lbl.pack()
root.after(1000, update_time)
root.after(1000, load_time)
root.mainloop()