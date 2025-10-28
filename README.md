
# 小梦课程表 - 智能课程管理应用

## 项目概述

小梦课程表是一个基于 Python 和 ttkbootstrap 开发的现代化课程管理应用，支持多视图模式展示、学期管理、课程统计等功能。应用采用 SQLite 数据库存储数据，提供直观的图形界面和丰富的交互体验。

### 核心特性

- 📅 **多视图模式**：支持周视图、日视图和月视图三种展示方式
- 🎨 **主题切换**：内置 5 种精美主题（flatly、darkly、solar、superhero、cyborg）
- 📊 **实时统计**：显示总课程数、本周课程、正常课程和特殊课程统计
- 🗓️ **学期管理**：支持创建、编辑和切换学期
- 🏷️ **课程分类**：支持正常课程和多种特殊课程类型（早签、自习课、班会等）
- 🎯 **双击编辑**：在周视图中双击课程可直接编辑
- 📱 **响应式布局**：自适应窗口大小，最小分辨率 1200x800

## 前置条件

- Python 3.7 或更高版本
- 操作系统：Windows / macOS / Linux

## 依赖库

```bash
pip install ttkbootstrap
```

## 运行方法

1. 进入项目目录：
```bash
cd src
```

2. 运行主程序：
```bash
python main.py
```

## 构建方法

### 使用 PyInstaller 打包

1. 安装 PyInstaller：
```bash
pip install pyinstaller
```

2. 打包为可执行文件：
```bash
pyinstaller --onefile --windowed main.py
```

打包完成后，可执行文件位于 `dist` 目录下。

## 使用说明

1. **创建学期**：首次使用需点击"新建学期"创建学期信息
2. **添加课程**：点击"添加课程"按钮，填写课程详细信息
3. **切换视图**：使用视图切换按钮在周/日/月视图间切换
4. **调整周数**：通过周数选择器查看不同周的课程安排
5. **课程编辑**：在周视图中双击课程可快速编辑
6. **更换主题**：从主题下拉菜单选择界面风格

## 项目结构

```
course-schedule-app/
├── src/
│   ├── main.py              # 主程序入口
│   ├── course_manager.py    # 课程数据管理
│   ├── ui_components.py     # UI组件
│   ├── views.py             # 视图实现
│   ├── dialogs.py           # 对话框
│   └── logger_config.py     # 日志配置
├── courses.db               # SQLite数据库（运行后自动生成）
└── README.md                # 项目说明
```

## 技术栈

- **前端框架**：tkinter + ttkbootstrap
- **数据库**：SQLite3
- **语言**：Python 3.7+

## 许可证

本项目采用 MIT 许可证。

---

**小梦课程表** - 让课程管理更简单高效！ 🎓✨