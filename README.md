# 壁纸自动轮换工具

[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue.svg)](https://www.python.org/downloads/)
[![Windows](https://img.shields.io/badge/platform-Windows-brightgreen.svg)](https://www.microsoft.com/windows)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## 📋 项目简介

壁纸自动轮换工具是一款专为 Windows 系统设计的桌面壁纸自动更换软件。它可以在指定日期（默认 2027 年 9 月 1 日）后，按照设定的时间间隔（默认每周）自动更换电脑壁纸，支持顺序轮换和随机轮换两种模式。

程序可以打包为独立的 `.exe` 文件，无需 Python 环境即可运行，并支持开机自启动。

## ✨ 主要功能

- 🎯 **定时启动**：可设置开始日期，在此之前不会更换壁纸（默认 2027‑09‑01）
- 🔄 **自动轮换**：支持自定义轮换间隔（默认 7 天）
- 🎲 **两种模式**：顺序轮换 / 随机轮换
- 🖼️ **多格式支持**：JPG, JPEG, PNG, BMP, WEBP
- 🎨 **壁纸样式**：填充、适应、拉伸、居中、平铺、跨屏
- 🚀 **开机自启**：一键安装为开机启动项
- 📝 **日志记录**：完整的日志系统，便于排查问题
- 💼 **可打包 EXE**：提供打包脚本，生成独立可执行文件

## 📦 系统要求

- **操作系统**：Windows 7 / 8 / 10 / 11
- **Python 版本**：3.6+（仅运行源码时需要）
- **磁盘空间**：约 10 MB（程序） + 壁纸文件空间
- **权限要求**：安装/卸载需要管理员权限，日常运行普通权限即可

## 🚀 快速开始

### 方式一：使用预编译的 EXE（推荐）

1. 下载 ‘dist’文件夹。
2. 运行 `install.py`。(很抱歉因为技术原因暂时无法打包成exe，如未安装python或出现问题请看2.5）
	-2.5其他安装方法：
	-简单模式：win+r打开运行窗口，输入shell:startup回车在文件夹中创建的‘WallpaperRotator.exe’的快捷方式
	-高级模式：执行schtasks /create /tn "WallpaperRotator" /tr "**替换为WallpaperRotator.exe的路径**" /sc daily /st 09:00
3. 将壁纸图片放入程序目录下的 `wallpapers` 文件夹。
4. 程序会自动添加到开机启动并开始运行。

### 方式二：从源码运行

```bash
# 克隆仓库
git clone https://github.com/yourusername/wallpaper-rotator.git
cd wallpaper-rotator

# 安装依赖
pip install -r requirements.txt

# 运行程序（单次检查）
python wallpaper_rotator.py --once

# 强制更换壁纸
python wallpaper_rotator.py --rotate
```

## ⚙️ 配置说明

程序首次运行时会自动生成 `config.json` 配置文件，内容如下：

```json
{
  "images_folder": "wallpapers",        // 壁纸文件夹名称
  "wallpaper_style": "fill",            // 壁纸显示样式
  "rotation_interval_days": 7,          // 轮换间隔（天）
  "enable_random": false,               // 是否随机顺序（false=顺序）
  "supported_formats": [                // 支持的图片扩展名
    ".jpg", ".jpeg", ".png", ".bmp", ".webp"
  ],
  "start_date": "2027-09-01",           // 开始更换日期
  "last_update": null,                  // 上次更换时间（自动记录）
  "current_index": 0                    // 当前壁纸索引（自动记录）
}
```

### 壁纸样式对照表

| 样式值   | 说明       | 效果                     |
|----------|------------|--------------------------|
| `fill`   | 填充       | 保持宽高比，完全覆盖屏幕 |
| `fit`    | 适应       | 保持宽高比，完整显示图片 |
| `stretch`| 拉伸       | 拉伸图片填满屏幕         |
| `center` | 居中       | 原始尺寸居中显示         |
| `tile`   | 平铺       | 重复平铺图片             |
| `span`   | 跨屏       | 跨越多显示器显示         |

## 📖 使用方法

### 命令行参数

| 参数                 | 说明                           |
|----------------------|--------------------------------|
| 无参数               | 静默运行，执行一次自动检查     |
| `--once` / `-o`      | 运行一次检查（根据规则决定）   |
| `--rotate` / `-r`    | 强制更换壁纸（忽略时间规则）   |
| `--help` / `-h`      | 显示帮助信息                   |

示例：

```batch
# 强制更换壁纸（会弹出提示框）
WallpaperRotator.exe --rotate

# 仅检查是否需要更换
WallpaperRotator.exe --once

# 静默后台运行（适合任务计划或开机启动）
WallpaperRotator.exe
```

## 🛠️ 打包为 EXE

如果你修改了源码，可以重新打包：

1. 确保已安装 PyInstaller：
   ```bash
   pip install pyinstaller
   ```

2. 运行打包脚本：
   ```bash
   python build.py
   ```

3. 打包后的 `WallpaperRotator.exe` 位于 `dist` 文件夹内。

## 📂 目录结构

```
壁纸轮换工具/
├── WallpaperRotator.exe      # 主程序
├── config.json                # 配置文件
├── install.bat                # 安装脚本
├── uninstall.bat              # 卸载脚本
├── wallpapers/                # 壁纸文件夹（需手动放入图片）
│   └── 说明.txt
└── logs/                      # 日志文件夹
    └── wallpaper_rotator_日期.log
```

## ❓ 常见问题

### 1. 程序没有自动更换壁纸？

- 检查当前日期是否已达到 `start_date`（默认 2027‑09‑01）。
- 检查 `wallpapers` 文件夹中是否有支持的图片。
- 查看 `logs` 文件夹中的日志文件，定位错误原因。
- 以管理员身份运行一次 `WallpaperRotator.exe --rotate` 测试。

### 2. 如何立即测试？

- 临时修改 `config.json` 中的 `start_date` 为今天的日期，然后运行 `WallpaperRotator.exe --rotate`。
- 或者直接运行 `WallpaperRotator.exe --rotate` 强制更换。

### 3. 壁纸更换后没有立即生效？

- 系统可能需要几秒钟刷新，按 `F5` 刷新桌面。
- 或者重启资源管理器：`taskkill /f /im explorer.exe && start explorer.exe`

### 4. 支持哪些图片格式？

- 默认支持 `.jpg`, `.jpeg`, `.png`, `.bmp`, `.webp`。可以在 `config.json` 的 `supported_formats` 中添加其他格式。

### 5. 如何卸载？

-如使用简单模式win+r打开运行窗口，输入shell:startup回车删除文件夹中的WallpaperRotator快捷方式
-如使用高级模式执行schtasks /delete /tn "WallpaperRotator" /f

### 6. 程序占用资源多吗？

- 非常轻量，平时不占用 CPU 和内存（仅后台等待），只有在实际更换壁纸时才会短暂运行（约 1‑2 秒）。

## 📝 更新日志

### v1.0 (2024-01-15)
- 初始版本发布
- 支持定时更换壁纸（2027‑09‑01 后生效）
- 支持顺序 / 随机轮换
- 支持多种壁纸样式
- 支持开机自启动
- 完整的日志系统
- 可打包为独立 EXE

## 🤝 贡献

欢迎提交 Issue 或 Pull Request。

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

## 🙏 致谢

感谢所有使用和反馈问题的用户，以及开源社区提供的优秀工具。

## ⚠️ 免责声明

本工具仅供学习和个人使用。使用本工具所产生的任何问题，开发者不承担任何责任。请确保您拥有壁纸图片的合法使用权。

---

**Enjoy automatic wallpaper rotation!** 🎉
