
# 小梦课程表

一个基于 Python 和 ttkbootstrap 的现代化课程表管理应用，支持多视图切换、课程管理、提醒服务和数据导出等功能。

## 项目概述

小梦课程表是一款功能完善的课程管理工具，具有以下核心特性：

- 📅 **多视图支持**：周视图、日视图、月视图三种展示方式
- 🎨 **现代化界面**：基于 ttkbootstrap 的美观 UI 设计
- ⏰ **智能提醒**：支持课程提醒功能，避免错过课程
- 📊 **统计分析**：提供详细的学习报告和数据可视化
- 💾 **数据导出**：支持 Excel、CSV、JSON、PDF、图片等多种格式
- 🗂️ **学期管理**：支持多学期切换和管理
- 🔍 **课程搜索**：快速查找特定课程信息

## 前置条件

- Python 3.8+
- 操作系统：Windows/Linux/macOS

## 依赖库

```bash
pip install ttkbootstrap
pip install pillow
pip install matplotlib
pip install pandas
pip install reportlab
```

## 运行方法

1. 克隆或下载项目代码
2. 安装所需依赖库
3. 运行主程序：

```bash
python src/main.py
```

## 项目结构

```
src/
├── main.py              # 主程序入口
├── ui_components.py     # UI 组件
├── views.py             # 视图组件
├── dialogs.py           # 对话框组件
├── course_manager.py    # 课程管理器
├── reminder_service.py  # 提醒服务
└── logger_config.py     # 日志配置
```

## 功能特性

### 课程管理
- 添加/编辑/删除课程
- 支持特殊课程类型（早签、自习课、班会等）
- 自定义课程颜色和类型
- 课程信息搜索和筛选

### 视图展示
- **周视图**：显示一周的课程安排
- **日视图**：显示单日详细课程信息
- **月视图**：月度课程概览

### 数据分析
- 学习时长统计
- 课程类型分布
- 时间利用分析
- 可视化图表展示

### 导出功能
- Excel 表格导出
- CSV 数据导出
- JSON 格式导出
- PDF 报告导出
- 图片格式导出

## 数据库

项目使用 SQLite 数据库存储课程信息，数据库文件会自动创建在项目根目录下的 `courses.db`。

## 配置说明

- 日志配置：`logger_config.py`
- 数据库配置：自动创建 SQLite 数据库
- 主题配置：支持多种内置主题切换

## 许可证

本项目采用 MIT 许可证。

## 贡献指南

欢迎提交 Issue 和 Pull Request 来改进项目。

## 联系方式

如有问题或建议，请通过 Issue 联系我们。

---

**注意**：首次运行时会自动创建数据库和必要的配置文件。建议定期备份 `courses.db` 文件以防数据丢失。