import os
import shutil
import subprocess
import tkinter as tk
from tkinter import messagebox
import psutil

def get_disk_info():
    obj_Disk = psutil.disk_usage('C:/')
    free = float("{:.2f}".format(obj_Disk.free / (1024**3)))
    return free

def clean_system():
    before = get_disk_info()
    targets = [
        os.environ.get('TEMP'),
        r'C:\Windows\Temp',
        r'C:\Windows\Prefetch',
        r'C:\Windows\SoftwareDistribution\Download'
    ]
    
    count = 0
    for folder in targets:
        if os.path.exists(folder):
            for item in os.listdir(folder):
                path = os.path.join(folder, item)
                try:
                    if os.path.isfile(path) or os.path.islink(path):
                        os.unlink(path)
                    elif os.path.isdir(path):
                        shutil.rmtree(path)
                    count += 1
                except:
                    continue

    try:
        subprocess.run(["powercfg", "-h", "off"], check=True)
    except:
        pass
    
    after = get_disk_info()
    gain = round(after - before, 2)
    
    messagebox.showinfo("Killua Speed v2.0", 
                        f"Dọn xong {count} mục!\n"
                        f"Dung lượng trống trước: {before} GB\n"
                        f"Dung lượng trống sau: {after} GB\n"
                        f"Bạn đã tiết kiệm được: {gain} GB")
    update_label()

def update_label():
    info_label.config(text=f"Trạng thái ổ C: Còn trống {get_disk_info()} GB")


root = tk.Tk()
root.title("Killua Speed v2.0")
root.geometry("400x300")
root.configure(bg='#121212')

tk.Label(root, text="KILLUA SPEED SYSTEM", fg="#00f2ff", bg="#121212", font=("Arial", 16, "bold")).pack(pady=20)

info_label = tk.Label(root, text="", fg="white", bg="#121212", font=("Arial", 10))
info_label.pack(pady=10)
update_label()

btn = tk.Button(root, text="KÍCH HOẠT SẤM SÉT", command=clean_system, 
                bg="#00f2ff", fg="black", font=("Arial", 12, "bold"), padx=20, pady=10)
btn.pack(pady=20)

root.mainloop()