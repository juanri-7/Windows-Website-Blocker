import tkinter as tk
from PIL import Image, ImageTk
from tkinter import font
from websiteblocker import website_blocker
import threading
import time
from datetime import datetime as dt



window = tk.Tk()
window.title("Website Blocker")
window.geometry("600x800")
window.resizable(0,0)

#website blocker canvas
canvas = tk.Canvas(window, width=600, height=800)
canvas.pack()

#background image
background_image = ImageTk.PhotoImage(Image.open("background.jpg"))
canvas.create_image(0, 0, image = background_image, anchor='nw')
canvas.create_text(300, 50, text = "Website Blocker", font="Arial 30 bold")

# delete selected sites from listbox
def delete():
    for item in reversed(site_listbox.curselection()):
        site_listbox.delete(item)

# delete all sites from listbox
def delete_all():
    site_listbox.delete(0, "end")

# resets entry box after submitting site to listbox
def add_site_listbox():
    site_listbox.insert("end", add_site_entry.get())
    add_site_entry.delete(0,"end")


# show sites / scrollbar frame
showsites_frame = tk.Frame(window, bg = "lightgray")
showsites_frame.place(relx=0.585, rely=0.125, height=250, width=225)

site_label = tk.Label(showsites_frame, text="Sites to block:", bg="lightgray", font="Arial 12 bold")
site_label.place(relx= 0.2, rely=0.028)

scrollbar_sites = tk.Scrollbar(showsites_frame)
scrollbar_sites.pack(side = "right", fill = "y")

site_listbox = tk.Listbox(showsites_frame, yscrollcommand = scrollbar_sites.set, selectmode="extended")
site_listbox.place(relx=0, rely=0.15, height=170, width=205)

delete_button = tk.Button(showsites_frame, text="DELETE", bg="lightgray", fg="black", bd=2, command=lambda:delete())
delete_button.place(relx=0.15, rely=0.870)

delete_all_button = tk.Button(showsites_frame, text="DELETE ALL", bg="lightgray", fg="black", bd=2, command=lambda:delete_all())
delete_all_button.place(relx=0.50, rely=0.870)


#add site/time frame
add_site_frame = tk.Frame(window, bg = "lightgray")
add_site_frame.place(relx=0.05, rely=0.125, height=250, width=300)

add_site_entry = tk.Entry(add_site_frame, justify = "center", font = "Courier 10", bd=4)
add_site_entry.place(relx=0.1, rely=0.175)

add_site_button = tk.Button(add_site_frame, text = "ENTER", bg = "lightgray", fg = "black", bd=2,
    command=lambda: add_site_listbox())
add_site_button.place(relx=0.75, rely=0.175)

add_site_label = tk.Label(add_site_frame, text="Add sites to block here:", bg="lightgray", font="Arial 12 bold")
add_site_label.place(relx= 0.1, rely=0.05)


#duration/time inputs

#start time
add_timestarthr_entry = tk.Entry(add_site_frame, justify = "center", font = "Courier 10", bd=4)
add_timestarthr_entry.place(relx=0.1, rely=0.475, width=60)

add_timestartmin_entry = tk.Entry(add_site_frame, justify = "center", font = "Courier 10", bd=4)
add_timestartmin_entry.place(relx=0.5, rely=0.475, width=60)

add_timestart_label = tk.Label(add_site_frame, text="Beginning time :", bg="lightgray", font="Arial 12 bold")
add_timestart_label.place(relx= 0.1, rely=0.35)

starthr_label = tk.Label(add_site_frame, text="hour", bg = "lightgray")
starthr_label.place(relx=0.35, rely=0.475)

startmin_label = tk.Label(add_site_frame, text="min", bg = "lightgray")
startmin_label.place(relx=0.75, rely=0.475)


# end time
add_timeendhr_entry = tk.Entry(add_site_frame, justify = "center", font = "Courier 10", bd=4)
add_timeendhr_entry.place(relx=0.1, rely=0.80, width=60)

add_timeendmin_entry = tk.Entry(add_site_frame, justify = "center", font = "Courier 10", bd=4)
add_timeendmin_entry.place(relx=0.5, rely=0.80, width=60)

add_timeend_label = tk.Label(add_site_frame, text="Ending time :", bg="lightgray", font="Arial 12 bold")
add_timeend_label.place(relx= 0.1, rely=0.675)

endhr_label = tk.Label(add_site_frame, text="hour", bg = "lightgray")
endhr_label.place(relx=0.35, rely=0.80)

endmin_label = tk.Label(add_site_frame, text="min", bg = "lightgray")
endmin_label.place(relx=0.75, rely=0.80)


# host id/path entry and execute frame
# may need to worry about \\ for  the host_path entry**
host_frame = tk.Frame(window, bg="lightgray")
host_frame.place(relx=0.1655, rely=0.475, height=100, width= 400)

hostid_entry = tk.Entry(host_frame, justify="center", font = "Courier 10", bd=4)
hostid_entry.place(relx=0.28, rely=0.15, width=260)
hostid_entry.insert(0, "127.0.0.1")
host_id_label = tk.Label(host_frame, text="Host ID:", bg="lightgray", font="Arial 12 bold")
host_id_label.place(relx=0.025, rely=0.15)

host_path_entry = tk.Entry(host_frame, justify="center", font = "Courier 10", bd=4)
host_path_entry.place(relx=0.28, rely=0.60, width=260)
host_path_entry.insert(0, "C:\\Windows\\System32\\drivers\\etc")
host_path_label = tk.Label(host_frame, text="Host path:", bg="lightgray", font="Arial 12 bold")
host_path_label.place(relx=0.025, rely=0.60)

hostid_entry.config(state="disabled")
host_path_entry.config(state="disabled")


# block_frame
# obtain listbox items and transform into list to feed our add_sites function
# item in listbox cursor selection returns index values of list
# access actual item by using get() command and specifying index (item)
            

def compile_list():
    blockerinstance.remove_all_sites()
    list_compiled = []
    site_listbox.select_set(0, "end")
    for item in site_listbox.curselection():
        list_compiled.append(site_listbox.get(item))
    blockerinstance.add_sites(list_compiled)
    return

def block_gui():
    blockerinstance.block_execute(int(add_timestarthr_entry.get()), int(add_timeendhr_entry.get()), int(add_timestartmin_entry.get()), int(add_timeendmin_entry.get()))
    #blockerinstance.remove_all_sites()

def block_thread():
    add_timestarthr_entry.config(state="disabled")
    add_timestartmin_entry.config(state="disabled")
    add_timeendhr_entry.config(state="disabled")
    add_timeendmin_entry.config(state="disabled")

    blockerinstance.stop_thread.clear()
    blockerinstance.thread1 = threading.Thread(target=block_gui)
    blockerinstance.thread1.start()

    timerinstance.stop_thread2.clear()
    timerinstance.thread2 = threading.Thread(target=timerinstance.timer)
    timerinstance.thread2.start()

def abort_gui():
    add_timestarthr_entry.config(state="normal")
    add_timestartmin_entry.config(state="normal")
    add_timeendhr_entry.config(state="normal")
    add_timeendmin_entry.config(state="normal")
    time_left_label.config(text = "You have " + "0" + " hr(s) " + "0" + " min(s) "+ "0" + " sec left!")

    blockerinstance.stop_thread.set()
    # blockerinstance.thread1.join()
    blockerinstance.thread1 = None
    blockerinstance.reset_host()
    #blockerinstance.remove_all_sites()

    timerinstance.stop_thread2.set()
    timerinstance.thread2 = None

class timer():
    def __init__(self):
        self.thread2 = None
        self.stop_thread2 = threading.Event()

    def timer(self):
        while not self.stop_thread2.is_set():
            hoursleft = str(int(add_timeendhr_entry.get())-dt.now().hour)
            minutesleft = str(int(add_timeendmin_entry.get())-dt.now().minute)
            secondsleft = str(int(60-dt.now().second))
            if dt.now().hour > (int(add_timeendhr_entry.get())):
                hoursleft = "0"
            if dt.now().minute > (int(add_timeendmin_entry.get())):
                minutesleft = "0"
            time_left_label.config(text = "You have " + hoursleft + " hr(s) " + minutesleft + " min(s) "+ secondsleft + " sec left!")    
            if dt.now() < dt(dt.now().year, dt.now().month, dt.now().day, int(add_timeendhr_entry.get()), int(add_timeendmin_entry.get())):
                time_left_label.after(1000, timer)
                continue
            else:
                break

        time_left_label.config(text = "You have " + "0" + " hr(s) " + "0" + " min(s) "+ "0" + " sec left!")
        add_timestarthr_entry.config(state="normal")
        add_timestartmin_entry.config(state="normal")
        add_timeendhr_entry.config(state="normal")
        add_timeendmin_entry.config(state="normal")

def on_closing():
    blockerinstance.reset_host()
    abort_gui()
    window.destroy()

blockerinstance = website_blocker(hostpath=str(host_path_entry.get()), hostid=str(hostid_entry.get()))
timerinstance = timer()


block_frame = tk.Frame(window, bg="lightgray")
block_frame.place(relx=0.0655, rely=0.65, height=200, width=525)

block_button = tk.Button(block_frame, text = "BLOCK WEBSITES", command = lambda: [compile_list(), block_thread()])
block_button.place(relx=0.225, rely=0.1, height=100, width=300)

abort_button = tk.Button(block_frame, text = "ABORT", command = lambda: abort_gui())
abort_button.place(relx=0.70, rely=0.70)

time_left_label = tk.Label(block_frame, text = "", bg="lightgray", font="Arial 10 bold")
time_left_label.place(relx=0.15, rely=0.70)


window.protocol("WM_DELETE_WINDOW", on_closing)
window.mainloop()