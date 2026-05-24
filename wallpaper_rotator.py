#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
壁纸自动轮换工具
功能：2027年9月1日后，每周自动更换指定目录中的壁纸
"""

import os
import sys
import ctypes
import json
import time
from datetime import datetime, date, timedelta
from pathlib import Path
from typing import List, Optional
import logging
from logging.handlers import RotatingFileHandler

# 全局变量
APP_DIR = None

def get_app_dir():
    """获取应用程序目录（支持打包后的exe）"""
    global APP_DIR
    if APP_DIR:
        return APP_DIR
    
    if getattr(sys, 'frozen', False):
        # 打包后的exe运行
        APP_DIR = Path(sys.executable).parent
    else:
        # 脚本运行
        APP_DIR = Path(__file__).parent
    
    return APP_DIR

def setup_logging():
    """设置日志系统"""
    app_dir = get_app_dir()
    log_dir = app_dir / "logs"
    log_dir.mkdir(exist_ok=True)
    
    log_file = log_dir / f"wallpaper_rotator_{datetime.now().strftime('%Y%m%d')}.log"
    
    # 创建logger
    logger = logging.getLogger('WallpaperRotator')
    logger.setLevel(logging.INFO)
    
    # 文件处理器
    file_handler = RotatingFileHandler(
        log_file, maxBytes=10*1024*1024, backupCount=5, encoding='utf-8'
    )
    file_handler.setLevel(logging.INFO)
    
    # 控制台处理器（仅在非打包模式或调试时启用）
    if not getattr(sys, 'frozen', False) or '--debug' in sys.argv:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    # 格式化器
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    
    return logger

# 初始化日志
logger = setup_logging()

class WallpaperRotator:
    """壁纸轮换器类"""
    
    def __init__(self):
        """初始化壁纸轮换器"""
        self.app_dir = get_app_dir()
        self.config_file = self.app_dir / "config.json"
        self.config = self.load_config()
        self.wallpaper_list: List[Path] = []
        self.current_index = 0
        self.start_date = date(2027, 9, 1)
        
        # 壁纸样式映射
        self.style_map = {
            'fill': 10,      # 填充
            'fit': 6,        # 适应
            'stretch': 2,    # 拉伸
            'center': 0,     # 居中
            'tile': 1,       # 平铺
            'span': 22       # 跨显示器
        }
        
        logger.info(f"应用程序目录: {self.app_dir}")
        logger.info(f"配置文件: {self.config_file}")
    
    def load_config(self) -> dict:
        """加载配置文件"""
        default_config = {
            "images_folder": "wallpapers",
            "wallpaper_style": "fill",
            "rotation_interval_days": 7,
            "enable_random": False,
            "supported_formats": [".jpg", ".jpeg", ".png", ".bmp", ".webp"],
            "start_date": "2027-09-01",
            "last_update": None,
            "current_index": 0
        }
        
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    # 合并默认配置
                    for key, value in default_config.items():
                        if key not in config:
                            config[key] = value
                    logger.info("配置文件加载成功")
                    return config
            except Exception as e:
                logger.error(f"加载配置文件失败: {e}")
                return default_config
        else:
            # 创建默认配置文件
            self.save_config(default_config)
            logger.info("已创建默认配置文件")
            return default_config
    
    def save_config(self, config: dict = None):
        """保存配置文件"""
        if config is None:
            config = self.config
        
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
            logger.info("配置文件保存成功")
        except Exception as e:
            logger.error(f"保存配置文件失败: {e}")
    
    def load_wallpapers(self) -> List[Path]:
        """加载壁纸文件夹中的所有图片"""
        images_folder = self.app_dir / self.config['images_folder']
        
        if not images_folder.exists():
            logger.warning(f"壁纸文件夹不存在: {images_folder}")
            # 创建示例文件夹
            images_folder.mkdir(exist_ok=True)
            # 创建说明文件
            readme_file = images_folder / "说明.txt"
            with open(readme_file, 'w', encoding='utf-8') as f:
                f.write("请将壁纸图片放入此文件夹\n")
                f.write("支持的格式：.jpg, .jpeg, .png, .bmp, .webp\n")
                f.write("程序将按文件名顺序每周更换一次壁纸\n")
            logger.info(f"已创建壁纸文件夹: {images_folder}")
            return []
        
        wallpapers = []
        for ext in self.config['supported_formats']:
            wallpapers.extend(images_folder.glob(f"*{ext}"))
            wallpapers.extend(images_folder.glob(f"*{ext.upper()}"))
        
        # 去重并排序
        wallpapers = list(set(wallpapers))
        wallpapers.sort()
        
        logger.info(f"找到 {len(wallpapers)} 张壁纸")
        for wp in wallpapers[:5]:  # 只显示前5张
            logger.debug(f"  - {wp.name}")
        if len(wallpapers) > 5:
            logger.debug(f"  ... 还有 {len(wallpapers)-5} 张")
        
        return wallpapers
    
    def set_wallpaper_windows(self, image_path: Path) -> bool:
        """设置Windows壁纸"""
        try:
            abs_path = str(image_path.absolute())
            
            # 设置壁纸样式
            style = self.style_map.get(
                self.config['wallpaper_style'], 
                self.style_map['fill']
            )
            
            # 修改注册表
            import winreg
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER, 
                r"Control Panel\Desktop", 
                0, 
                winreg.KEY_SET_VALUE
            )
            
            winreg.SetValueEx(key, "WallpaperStyle", 0, winreg.REG_SZ, str(style))
            winreg.SetValueEx(key, "TileWallpaper", 0, winreg.REG_SZ, "0")
            winreg.CloseKey(key)
            
            # 应用壁纸
            result = ctypes.windll.user32.SystemParametersInfoW(20, 0, abs_path, 3)
            
            if result:
                logger.info(f"✓ 壁纸设置成功: {image_path.name}")
                return True
            else:
                logger.error(f"✗ 壁纸设置失败: {image_path.name}")
                return False
                
        except Exception as e:
            logger.error(f"设置壁纸时出错: {e}")
            return False
    
    def should_start(self) -> bool:
        """检查是否到达开始日期"""
        try:
            start_date = datetime.strptime(
                self.config.get('start_date', '2027-09-01'), 
                '%Y-%m-%d'
            ).date()
        except:
            start_date = self.start_date
        
        today = datetime.now().date()
        
        if today >= start_date:
            logger.info(f"已到达开始日期: {start_date}")
            return True
        else:
            days_left = (start_date - today).days
            logger.info(f"距离开始日期还有 {days_left} 天")
            return False
    
    def needs_rotation(self) -> bool:
        """检查是否需要轮换壁纸"""
        last_update = self.config.get('last_update')
        
        if last_update is None:
            logger.info("首次运行，需要设置壁纸")
            return True
        
        try:
            last_date = datetime.fromisoformat(last_update).date()
            today = datetime.now().date()
            days_passed = (today - last_date).days
            
            interval = self.config.get('rotation_interval_days', 7)
            
            if days_passed >= interval:
                logger.info(f"距离上次更换已过 {days_passed} 天，需要更换")
                return True
            else:
                days_to_wait = interval - days_passed
                logger.info(f"距离下次更换还有 {days_to_wait} 天")
                return False
                
        except Exception as e:
            logger.error(f"检查轮换条件时出错: {e}")
            return True
    
    def rotate_wallpaper(self):
        """执行壁纸轮换"""
        logger.info("=" * 50)
        logger.info("开始执行壁纸轮换任务")
        
        # 检查是否到达开始日期
        if not self.should_start():
            logger.info("未到达开始日期，不执行轮换")
            return False
        
        # 加载壁纸列表
        self.wallpaper_list = self.load_wallpapers()
        if not self.wallpaper_list:
            logger.warning("没有找到任何壁纸图片")
            logger.info(f"请将图片放入: {self.app_dir / self.config['images_folder']}")
            return False
        
        # 获取当前索引
        self.current_index = self.config.get('current_index', 0)
        if self.current_index >= len(self.wallpaper_list):
            self.current_index = 0
        
        # 获取要设置的壁纸
        if self.config.get('enable_random', False):
            import random
            wallpaper = random.choice(self.wallpaper_list)
            self.current_index = self.wallpaper_list.index(wallpaper)
            logger.info(f"随机模式 - 选择壁纸: {wallpaper.name}")
        else:
            wallpaper = self.wallpaper_list[self.current_index]
            logger.info(f"顺序模式 - 当前索引: {self.current_index + 1}/{len(self.wallpaper_list)}")
            self.current_index = (self.current_index + 1) % len(self.wallpaper_list)
        
        # 设置壁纸
        success = self.set_wallpaper_windows(wallpaper)
        
        if success:
            # 更新配置
            self.config['last_update'] = datetime.now().isoformat()
            self.config['current_index'] = self.current_index
            self.save_config()
            
            logger.info(f"当前壁纸: {wallpaper.name}")
            logger.info(f"下次轮换: {self.get_next_rotation_time()}")
        
        logger.info("=" * 50)
        return success
    
    def get_next_rotation_time(self) -> str:
        """获取下次轮换时间"""
        last_update = self.config.get('last_update')
        if not last_update:
            return "未知"
        
        try:
            last_date = datetime.fromisoformat(last_update)
            interval = self.config.get('rotation_interval_days', 7)
            next_date = last_date + timedelta(days=interval)
            return next_date.strftime('%Y-%m-%d %H:%M:%S')
        except:
            return "未知"
    
    def run_once(self):
        """运行一次（不进入循环）"""
        logger.info("运行单次壁纸检查")
        if self.should_start() and self.needs_rotation():
            return self.rotate_wallpaper()
        return False
    
    def manual_rotate(self):
        """手动轮换壁纸"""
        logger.info("手动触发壁纸轮换")
        return self.rotate_wallpaper()

def show_message_box(title, message, style=0):
    """显示消息框（用于打包后的exe）"""
    try:
        ctypes.windll.user32.MessageBoxW(0, message, title, style)
    except:
        pass

def main():
    """主函数"""
    # 检查是否在打包环境中运行
    is_frozen = getattr(sys, 'frozen', False)
    
    # 解析命令行参数
    args = sys.argv[1:] if len(sys.argv) > 1 else []
    
    # 创建壁纸轮换器实例
    rotator = WallpaperRotator()
    
    # 如果没有命令行参数，静默运行
    if not args:
        # 静默模式：运行一次检查，不显示任何界面
        try:
            rotator.run_once()
        except Exception as e:
            logger.error(f"运行出错: {e}")
        return
    
    # 有命令行参数时的处理
    if args[0] in ["--once", "-o"]:
        # 单次检查模式
        if not is_frozen:
            print("运行单次检查...")
        rotator.run_once()
        
    elif args[0] in ["--rotate", "-r"]:
        # 强制更换模式
        if not is_frozen:
            print("强制更换壁纸...")
        success = rotator.manual_rotate()
        if not is_frozen:
            if success:
                print("壁纸更换成功！")
            else:
                print("壁纸更换失败，请查看日志")
        else:
            # 打包模式下显示消息框
            if success:
                show_message_box("壁纸轮换工具", "壁纸更换成功！", 0x40)  # 信息图标
            else:
                show_message_box("壁纸轮换工具", "壁纸更换失败！\n请查看日志文件", 0x10)  # 错误图标
                
    elif args[0] in ["--help", "-h", "/?", "-?"]:
        # 帮助模式
        help_text = """壁纸轮换工具 v1.0

使用方法:
  WallpaperRotator.exe              静默运行（后台检查）
  WallpaperRotator.exe --once       运行一次检查
  WallpaperRotator.exe --rotate     强制更换壁纸
  WallpaperRotator.exe --help       显示帮助信息

配置文件: config.json
壁纸文件夹: wallpapers
日志文件夹: logs

如需开机启动，请运行 install.bat
"""
        if not is_frozen:
            print(help_text)
        else:
            show_message_box("帮助信息", help_text, 0x40)
    
    else:
        # 未知参数
        error_msg = f"未知参数: {args[0]}\n使用 --help 查看帮助"
        if not is_frozen:
            print(error_msg)
        else:
            show_message_box("错误", error_msg, 0x10)

if __name__ == "__main__":
    # 检查操作系统
    if sys.platform != "win32":
        error_msg = "错误：此程序仅支持Windows系统"
        if getattr(sys, 'frozen', False):
            show_message_box("错误", error_msg, 0x10)
        else:
            print(error_msg)
            input("按回车键退出...")
        sys.exit(1)
    
    try:
        main()
    except Exception as e:
        logger.error(f"程序运行出错: {e}", exc_info=True)
        if not getattr(sys, 'frozen', False):
            input("按回车键退出...")