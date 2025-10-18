# 小梦课程表 - 智能课程管理应用

## 项目概述

小梦课程表是一个基于 Python 和 Tkinter 开发的现代化课程管理应用，提供直观的界面来管理、查看和统计课程信息。支持周视图、日视图和月视图三种显示模式，具备课程添加、删除、编辑等完整功能，并内置多种主题切换选项。

### 核心特性

- 📅 **多视图模式**：支持周视图、日视图和月视图三种显示方式
- 🎨 **主题切换**：内置 5 种精美主题（flatly、darkly、solar、superhero、cyborg）
- 📊 **课程统计**：实时显示总课程数、本周课程、正常课程和调休课程统计
- 🗄️ **数据持久化**：使用 SQLite 数据库存储课程信息
- 🏷️ **颜色标记**：支持为不同课程设置颜色标签
- 📱 **响应式设计**：自适应窗口大小，最小分辨率 1200x800

## 前置条件

- Python 3.7 或更高版本
- 操作系统：Windows / macOS / Linux

## 依赖库

项目依赖以下 Python 库：

```bash
tkinter (通常随 Python 安装)
ttkbootstrap
sqlite3 (Python 标准库)
```

## 安装方法

1. 克隆项目到本地：
```bash
git clone https://github.com/yourusername/course-schedule-app.git
cd course-schedule-app
```

2. 安装依赖：
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

### 使用 PyInstaller 打包（可选）

1. 安装 PyInstaller：
```bash
pip install pyinstaller
```

2. 打包为可执行文件：
```bash
pyinstaller --onefile --windowed main.py
```

打包完成后，可在 `dist` 目录下找到可执行文件。

## 使用说明

1. **添加课程**：点击顶部"添加课程"按钮，填写课程信息
2. **切换视图**：使用视图切换按钮在周/日/月视图间切换
3. **调整周数**：通过周数选择器查看不同周的课程安排
4. **更换主题**：从主题下拉菜单选择喜欢的界面风格
5. **查看统计**：左侧面板实时显示课程统计信息

## 项目结构

```
course-schedule-app/
├── src/
│   ├── main.py           # 主程序入口
│   └── course_manager.py # 课程管理模块
├── courses.db            # SQLite 数据库文件（运行后自动生成）
└── README.md             # 项目说明文档
```

## 技术栈

- **前端框架**：Tkinter + ttkbootstrap
- **数据库**：SQLite
- **语言**：Python 3.7+

## 许可证

本项目采用 MIT 许可证。详情请参阅 [LICENSE](LICENSE) 文件。

## 贡献指南

欢迎提交 Issue 和 Pull Request 来改进项目！

## 更新日志

### v1.0.0 (2024-01-01)
- 初始版本发布
- 实现基础课程管理功能
- 支持三种视图模式
- 添加主题切换功能

## 联系方式

如有问题或建议，请通过以下方式联系：
- 邮箱：your.email@example.com
- GitHub Issues：https://github.com/yourusername/course-schedule-app/issues

---

**小梦课程表** - 让课程管理更简单高效！ 🎓✨