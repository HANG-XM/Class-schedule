import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox
from logger_config import logger
from course_manager import SpecialCourse
from datetime import datetime, timedelta

class TopBar:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.create_widgets()

    def create_widgets(self):
        """创建顶部控制栏"""
        # 创建主容器，添加渐变背景
        top_frame = tb.Frame(self.parent, bootstyle=PRIMARY)
        top_frame.pack(fill=X, pady=(0, 10))
        
        # 创建内层容器，添加边距和圆角
        inner_frame = tb.Frame(top_frame, padding=10)
        inner_frame.pack(fill=X, expand=True)

        # 创建控制面板容器
        control_container = tb.Frame(inner_frame)
        control_container.pack(side=RIGHT, fill=X, expand=True)

        # 创建Notebook，添加样式
        style = tb.Style()
        style.configure("Custom.TNotebook", background="#f8f9fa")
        style.configure("Custom.TNotebook.Tab", padding=[12, 8])
        
        control_notebook = tb.Notebook(control_container, 
                                    bootstyle=(PRIMARY, INVERSE),
                                    style="Custom.TNotebook")
        control_notebook.pack(fill=X, expand=True)

        # 基础控制标签页
        basic_frame = tb.Frame(control_notebook, padding=10)
        control_notebook.add(basic_frame, text="📊 基础控制")

        # 周数控制区域
        week_frame = tb.Frame(basic_frame)
        week_frame.pack(side=LEFT, padx=10)
        
        tb.Label(week_frame, text="当前周数", 
                font=("Helvetica", 10)).pack(side=LEFT, padx=(0, 5))
        self.week_var = tb.IntVar(value=getattr(self.app, 'current_week', 1))
        week_spinbox = tb.Spinbox(week_frame, from_=1, to=20, width=5,
                                textvariable=self.week_var, 
                                command=self.app.on_week_change)
        week_spinbox.pack(side=LEFT, padx=5)

        # 视图切换区域
        view_frame = tb.Frame(basic_frame)
        view_frame.pack(side=LEFT, padx=10)

        view_buttons = [
            ("📅 周视图", "week"),
            ("📝 日视图", "day"),
            ("📆 月视图", "month")
        ]
        
        for text, view in view_buttons:
            tb.Button(view_frame, text=text, 
                    command=lambda v=view: self.app.switch_view(v),
                    bootstyle=(INFO, OUTLINE),
                    width=12).pack(side=LEFT, padx=2)

        # 搜索标签页
        search_frame = tb.Frame(control_notebook, padding=10)
        control_notebook.add(search_frame, text="🔍 搜索")

        # 搜索控件区域
        search_container = tb.Frame(search_frame)
        search_container.pack(fill=X, expand=True)

        # 搜索类型选择
        self.search_type = tb.Combobox(search_container, 
                                    values=["课程名称", "教师姓名", "教室地点"],
                                    state="readonly", width=12)
        self.search_type.set("课程名称")
        self.search_type.pack(side=LEFT, padx=5)

        # 搜索输入框
        self.search_var = tb.StringVar()
        self.search_entry = tb.Entry(search_container, 
                                textvariable=self.search_var, 
                                width=20)
        self.search_entry.pack(side=LEFT, padx=5)
        self.search_entry.bind('<Return>', lambda e: self.app.search_courses())

        # 搜索按钮
        tb.Button(search_container, text="🔍 搜索", 
                command=self.app.search_courses,
                bootstyle=INFO).pack(side=LEFT, padx=5)

        # 高级功能标签页
        advanced_frame = tb.Frame(control_notebook, padding=10)
        control_notebook.add(advanced_frame, text="⚙️ 高级功能")

        # 主题切换区域
        theme_frame = tb.Frame(advanced_frame)
        theme_frame.pack(side=LEFT, padx=10)
        
        tb.Label(theme_frame, text="主题:", 
                font=("Helvetica", 10)).pack(side=LEFT, padx=5)
        theme_combo = tb.Combobox(theme_frame, values=self.app.themes, width=12,
                                state="readonly")
        theme_combo.set(self.app.current_theme)
        theme_combo.pack(side=LEFT, padx=5)
        theme_combo.bind('<<ComboboxSelected>>', self.app.on_theme_change)

        # 课程管理按钮区域
        manage_frame = tb.Frame(advanced_frame)
        manage_frame.pack(side=LEFT, padx=10)

        buttons = [
            ("➕ 添加课程", self.app.show_add_course_dialog, SUCCESS),
            ("📅 新建学期", self.show_add_semester_dialog, PRIMARY),
            ("✏️ 修改学期", self.show_edit_semester_dialog, INFO)
        ]
        
        for text, command, style in buttons:
            tb.Button(manage_frame, text=text, command=command,
                    bootstyle=(style, OUTLINE),
                    width=12).pack(side=LEFT, padx=5)

        # 学期选择器
        if self.app.current_semester:
            self._create_semester_selector(advanced_frame)

    def _create_semester_selector(self, parent):
        """创建学期选择器"""
        semester_frame = tb.Frame(parent)
        semester_frame.pack(side=RIGHT, padx=10)
        
        tb.Label(semester_frame, text="学期:").pack(side=LEFT)
        self.semester_var = tb.StringVar()
        semester_combo = tb.Combobox(semester_frame, textvariable=self.semester_var,
                                values=[s[1] for s in self.app.semesters],
                                state="readonly", width=15)
        semester_combo.pack(side=LEFT, padx=5)
        semester_combo.set(self.app.current_semester[1])
        semester_combo.bind('<<ComboboxSelected>>', self.on_semester_change)

    def on_semester_change(self, event):
        """学期切换事件"""
        selected_name = event.widget.get()
        try:
            for semester in self.app.semesters:
                if semester[1] == selected_name:
                    self.app.course_manager.set_current_semester(semester[0])
                    self.app.current_semester = semester
                    self.app.load_courses()
                    self.app.update_display()
                    logger.info(f"已切换到学期: {selected_name}")
                    break
        except Exception as e:
            logger.error(f"切换学期失败: {str(e)}")
            messagebox.show_error("错误", "切换学期失败")

    def show_add_semester_dialog(self):
        """显示新建学期对话框"""
        from dialogs import AddSemesterDialog
        dialog = AddSemesterDialog(self.parent, self.app)
        # 等待对话框关闭
        self.parent.wait_window(dialog.dialog)
        # 刷新学期列表
        self.app.semesters = self.app.course_manager.get_semesters()
        if hasattr(self, 'semester_var'):
            self.semester_var.set('')
            # 获取 Combobox 组件的正确方式
            for widget in self.parent.winfo_children():
                if isinstance(widget, tb.Combobox):
                    widget['values'] = [s[1] for s in self.app.semesters]
                    if self.app.current_semester:
                        widget.set(self.app.current_semester[1])
                    break
        else:
            # 如果不存在学期选择器，创建一个
            self._create_semester_selector(self.parent.winfo_children()[0])
    def _refresh_semester_list(self):
        """刷新学期列表"""
        self.app.semesters = self.app.course_manager.get_semesters()
        if hasattr(self, 'semester_var'):
            self.semester_var.set('')
            # 获取 Combobox 组件的正确方式
            for widget in self.parent.winfo_children():
                if isinstance(widget, tb.Combobox):
                    widget['values'] = [s[1] for s in self.app.semesters]
                    if self.app.current_semester:
                        widget.set(self.app.current_semester[1])
                    break
    def show_edit_semester_dialog(self):
        """显示修改学期对话框"""
        from dialogs import EditSemesterDialog
        dialog = EditSemesterDialog(self.parent, self.app)
        self.parent.wait_window(dialog.dialog)
        self._refresh_semester_list()
class StatsPanel:
    def __init__(self, parent):
        self.parent = parent
        self.create_widgets()

    def create_widgets(self):
        """创建统计面板"""
        self.stats_frame = tb.Labelframe(self.parent, text="课程统计", padding=15)
        self.stats_frame.pack(side=LEFT, fill=Y, padx=(0, 15))
        self.stats_labels = {}

    def update_stats(self, courses, current_week, course_manager, view_type="week", current_date=None):
        """更新统计信息"""
        try:
            # 清空现有统计信息
            for widget in self.stats_frame.winfo_children():
                widget.destroy()

            if not courses:
                tb.Label(self.stats_frame, text="暂无课程数据", 
                        font=("Helvetica", 12),
                        bootstyle=SECONDARY).pack(expand=True)
                return

            # 根据视图类型获取对应的课程
            if view_type == "day":
                view_courses = [c for c in courses if int(c[6]) == current_date.weekday() + 1]
                title = "当日信息"
            elif view_type == "month":
                year, month = current_date.year, current_date.month
                view_courses = [c for c in courses 
                            if self._is_course_in_month(c, year, month, current_date)]
                title = "当月信息"
            else:  # week
                view_courses = course_manager.get_courses_by_week(current_week)
                title = "本周信息"

            # 计算总体统计
            overall_frame = tb.LabelFrame(self.stats_frame, text="总体信息", padding=10)
            overall_frame.pack(fill=X, pady=5)
            
            overall_stats = {
                "total": {
                    "text": "总课程数",
                    "value": len(courses),
                    "style": "primary"
                },
                "normal": {
                    "text": "正常课程",
                    "value": len([c for c in courses if not c[11]]),
                    "style": "info"
                },
                "types": {
                    "text": "课程种类",
                    "value": len(set(c[1] for c in courses if not c[11])),
                    "style": "success"
                }
            }

            # 添加特殊课程统计
            for course_type in SpecialCourse.TYPES:
                overall_count = len([c for c in courses if c[10] == course_type])
                if overall_count > 0:
                    overall_stats[course_type] = {
                        "text": course_type,
                        "value": overall_count,
                        "style": SpecialCourse.TYPES[course_type]["color"]
                    }

            # 显示总体统计
            for stat_type, stats_dict in overall_stats.items():
                self._create_stat_widget(overall_frame, stat_type, stats_dict)

            # 创建当前视图统计部分
            view_frame = tb.LabelFrame(self.stats_frame, text=title, padding=10)
            view_frame.pack(fill=X, pady=5)
            
            # 计算当前视图统计
            view_stats = {
                "total": {
                    "text": f"{title[:-2]}课程",
                    "value": len(view_courses),
                    "style": "primary"
                },
                "normal": {
                    "text": "正常课程",
                    "value": len([c for c in view_courses if not c[11]]),
                    "style": "info"
                },
                "types": {
                    "text": "课程种类",
                    "value": len(set(c[1] for c in view_courses if not c[11])),
                    "style": "success"
                }
            }

            # 添加特殊课程统计
            for course_type in SpecialCourse.TYPES:
                view_count = len([c for c in view_courses if c[10] == course_type])
                if view_count > 0:
                    view_stats[course_type] = {
                        "text": course_type,
                        "value": view_count,
                        "style": SpecialCourse.TYPES[course_type]["color"]
                    }

            # 显示当前视图统计
            for stat_type, stats_dict in view_stats.items():
                self._create_stat_widget(view_frame, stat_type, stats_dict)
                        
        except Exception as e:
            logger.error(f"更新统计信息失败: {str(e)}")
            raise

    def _is_course_in_month(self, course, year, month, current_date):
        """判断课程是否在指定月份内"""
        try:
            # 获取月份第一天和最后一天
            first_day = datetime(year, month, 1)
            last_day = datetime(year, month + 1, 1) - timedelta(days=1) if month < 12 else datetime(year, 12, 31)
            
            # 计算当前日期对应的周数
            course_week = ((current_date - datetime.strptime(self.app.current_semester[2], "%Y-%m-%d")).days // 7) + 1
            
            # 检查课程是否在月份范围内
            return (int(c[4]) <= course_week <= int(c[5]) and 
                    first_day <= current_date <= last_day)
        except Exception as e:
            logger.error(f"判断课程月份失败: {str(e)}")
            return False

    def _calculate_stats(self, courses, current_week, course_manager):
        """计算统计信息"""
        # 获取本周课程
        week_courses = course_manager.get_courses_by_week(current_week)
        
        # 计算总体统计
        overall_stats = {
            "total": {
                "text": "总课程数",
                "value": len(courses),
                "style": "primary"
            },
            "normal": {
                "text": "正常课程",
                "value": len([c for c in courses if not c[11]]),
                "style": "info"
            },
            "types": {
                "text": "课程种类",
                "value": len(set(c[1] for c in courses if not c[11])),
                "style": "success"
            }
        }
        
        # 计算本周统计
        weekly_stats = {
            "total": {
                "text": "本周课程",
                "value": len(week_courses),
                "style": "primary"
            },
            "normal": {
                "text": "正常课程",
                "value": len([c for c in week_courses if not c[11]]),
                "style": "info"
            },
            "types": {
                "text": "课程种类",
                "value": len(set(c[1] for c in week_courses if not c[11])),
                "style": "success"
            }
        }
        
        # 添加特殊课程统计
        for course_type in SpecialCourse.TYPES:
            # 总体特殊课程统计
            overall_count = len([c for c in courses if c[10] == course_type])
            if overall_count > 0:
                overall_stats[course_type] = {
                    "text": course_type,
                    "value": overall_count,
                    "style": SpecialCourse.TYPES[course_type]["color"]
                }
            
            # 本周特殊课程统计
            week_count = len([c for c in week_courses if c[10] == course_type])
            if week_count > 0:
                weekly_stats[course_type] = {
                    "text": course_type,
                    "value": week_count,
                    "style": SpecialCourse.TYPES[course_type]["color"]
                }
        
        return {
            "overall": overall_stats,
            "weekly": weekly_stats
        }

    def _create_stat_widget(self, parent, stat_type, stats_dict):
        """创建统计信息组件"""
        frame = tb.Frame(parent)
        frame.pack(fill=X, pady=2)
        
        tb.Label(frame, text=stats_dict["text"], 
                font=("Helvetica", 10)).pack(side=LEFT)
        tb.Label(frame, text=str(stats_dict["value"]), 
                bootstyle=stats_dict["style"],
            font=("Helvetica", 12, "bold")).pack(side=RIGHT)
