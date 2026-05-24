"""
简单的打包脚本 - 修正版
"""

import os
import sys
import subprocess

def main():
    print("=" * 50)
    print("壁纸轮换工具 - 打包脚本")
    print("=" * 50)
    
    # 1. 安装依赖
    print("\n1. 安装依赖...")
    subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 2. 打包（移除 --noconsole 以便查看调试信息，或保留但程序已适配）
    print("\n2. 打包程序...")
    
    # 选项1：带控制台版本（便于调试）
    # cmd = ["pyinstaller", "--onefile", "--name", "WallpaperRotator", "wallpaper_rotator.py"]
    
    # 选项2：无控制台版本（静默运行，推荐）
    cmd = [
        "pyinstaller",
        "--onefile",           # 单文件
        "--noconsole",         # 无控制台（后台运行）
        "--name", "WallpaperRotator",
        "wallpaper_rotator.py"
    ]
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print("\n✓ 打包成功！")
        print("可执行文件: dist/WallpaperRotator.exe")
        
        # 3. 创建启动脚本
        print("\n3. 创建启动脚本...")
        create_startup_scripts()
    else:
        print("\n✗ 打包失败！")

def create_startup_scripts():
    """创建启动和安装脚本"""
    
    # 简化的安装脚本
    install_script = '''@echo off
chcp 65001 >nul
title 安装壁纸轮换工具

echo 正在安装壁纸轮换工具...
echo.

set "INSTALL_DIR=%CD%"

:: 创建开机启动项
set "STARTUP=%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"
copy "%INSTALL_DIR%\\WallpaperRotator.exe" "%STARTUP%\\" >nul
echo ✓ 已添加到开机启动

:: 创建配置文件（如果不存在）
if not exist "%INSTALL_DIR%\\config.json" (
    echo {> "%INSTALL_DIR%\\config.json"
    echo   "images_folder": "wallpapers",>> "%INSTALL_DIR%\\config.json"
    echo   "wallpaper_style": "fill",>> "%INSTALL_DIR%\\config.json"
    echo   "rotation_interval_days": 7,>> "%INSTALL_DIR%\\config.json"
    echo   "enable_random": false,>> "%INSTALL_DIR%\\config.json"
    echo   "supported_formats": [".jpg", ".jpeg", ".png", ".bmp", ".webp"],>> "%INSTALL_DIR%\\config.json"
    echo   "start_date": "2027-09-01",>> "%INSTALL_DIR%\\config.json"
    echo   "last_update": null,>> "%INSTALL_DIR%\\config.json"
    echo   "current_index": 0>> "%INSTALL_DIR%\\config.json"
    echo }>> "%INSTALL_DIR%\\config.json"
    echo ✓ 已创建配置文件
)

:: 创建壁纸文件夹
if not exist "%INSTALL_DIR%\\wallpapers" (
    mkdir "%INSTALL_DIR%\\wallpapers"
    echo ✓ 已创建壁纸文件夹
)

:: 创建日志文件夹
if not exist "%INSTALL_DIR%\\logs" (
    mkdir "%INSTALL_DIR%\\logs"
    echo ✓ 已创建日志文件夹
)

echo.
echo 安装完成！
echo.
echo 请将壁纸图片放入: %INSTALL_DIR%\\wallpapers
echo.
echo 程序将在后台自动运行
echo 如需立即测试，请运行: WallpaperRotator.exe --rotate
echo.
pause
'''
    
    with open("install.bat", "w", encoding="gbk") as f:
        f.write(install_script)
    
    # 卸载脚本
    uninstall_script = '''@echo off
chcp 65001 >nul
title 卸载壁纸轮换工具

echo 正在卸载壁纸轮换工具...
echo.

:: 停止进程
taskkill /f /im WallpaperRotator.exe >nul 2>&1
echo ✓ 已停止程序

:: 删除开机启动
set "STARTUP=%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"
if exist "%STARTUP%\\WallpaperRotator.exe" (
    del "%STARTUP%\\WallpaperRotator.exe"
    echo ✓ 已删除开机启动
)

:: 删除桌面快捷方式
if exist "%USERPROFILE%\\Desktop\\WallpaperRotator.lnk" (
    del "%USERPROFILE%\\Desktop\\WallpaperRotator.lnk"
    echo ✓ 已删除桌面快捷方式
)

echo.
echo 是否删除配置文件、壁纸和日志？(y/n)
set /p choice=""
if /i "%choice%"=="y" (
    if exist "config.json" del "config.json"
    if exist "wallpapers" rmdir /s /q "wallpapers"
    if exist "logs" rmdir /s /q "logs"
    echo ✓ 已删除用户数据
)

echo.
echo 卸载完成！
pause
'''
    
    with open("uninstall.bat", "w", encoding="gbk") as f:
        f.write(uninstall_script)
    
    # 使用说明
    readme = """壁纸轮换工具 使用说明
================================

功能：
- 2027年9月1日后自动开始工作
- 每周自动更换壁纸
- 支持顺序或随机轮换

安装：
1. 双击运行 install.bat（以管理员身份）
2. 将壁纸图片放入 wallpapers 文件夹
3. 程序会自动运行并添加到开机启动

手动控制：
- 立即更换：WallpaperRotator.exe --rotate
- 运行检查：WallpaperRotator.exe --once
- 查看帮助：WallpaperRotator.exe --help

配置文件说明：
编辑 config.json 修改设置：
- start_date: 开始日期（默认2027-09-01）
- rotation_interval_days: 轮换间隔（默认7天）
- enable_random: 是否随机（默认false）
- wallpaper_style: 壁纸样式

日志查看：
logs文件夹中的日志文件记录了运行状态

卸载：
双击运行 uninstall.bat
"""
    
    with open("使用说明.txt", "w", encoding="utf-8") as f:
        f.write(readme)
    
    print("✓ 已创建 install.bat")
    print("✓ 已创建 uninstall.bat")
    print("✓ 已创建 使用说明.txt")

if __name__ == "__main__":
    main()