from tkinter import *
from tkinter import messagebox as mg
import os,pathlib
import subprocess
import win32com.client

aim = os.path.join(os.path.dirname(__file__),"WallpaperRotator.exe")

def create_startup_shortcut(target_path, shortcut_name="MyApp.lnk", description=""):
    # 获取当前用户的 Startup 目录
    startup_dir = os.path.join(os.environ['APPDATA'], 
                               r'Microsoft\\Windows\\Start Menu\\Programs\\Startup')
    shortcut_path = os.path.join(startup_dir, shortcut_name)

    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortcut(shortcut_path)
    shortcut.TargetPath = target_path
    shortcut.WorkingDirectory = os.path.dirname(target_path)
    shortcut.Description = description
    shortcut.Save()
    return shortcut_path

def service():
    cmd = 'schtasks /create /tn "WallpaperRotator" /tr '+aim+' /sc daily /st 09:00 /f'
    subprocess.run(f'powershell Start-Process cmd -Verb RunAs -ArgumentList \'/c {cmd}\'', shell=True)
    mg.showinfo('info','添加成功')

def startup():
    exe_path = os.path.join(os.path.dirname(__file__),"WallpaperRotator.exe")
    if os.path.exists(exe_path):
        create_startup_shortcut(exe_path, "WallpaperRotator.lnk", "壁纸轮换工具")
    mg.showinfo('info','添加成功')

root = Tk()
root.title("installer")
title = Label(root,text='          wallpaper rotator安装工具v1.0          ',font=(24))
easy=Button(root,text='简单模式（开机自启动）',command=startup,font=18)
hard=Button(root,text='高级模式（添加服务）',command = service,font=18)
title.grid(row=0,columnspan=3,pady=15)
easy.grid(row=1,columnspan=3,pady=15)
hard.grid(row=2,columnspan=3,pady=15)
root.mainloop()