import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox

from logger_config import logger
from datetime import datetime, timedelta
from typing import Tuple

from course_manager import SpecialCourse

class BaseComponent:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.style = tb.Style()
        
    def create_labeled_frame(self, text, padding=10):
        """创建带标签的框架"""
        return tb.LabelFrame(self.parent, text=text, padding=padding)
        
    def create_labeled_entry(self, parent, label_text, width=20):
        """创建带标签的输入框"""
        frame = tb.Frame(parent)
        frame.pack(fill=X, pady=3)
        tb.Label(frame, text=label_text, width=10).pack(side=LEFT)
        entry = tb.Entry(frame, font=("Helvetica", 10), width=width)
        entry.pack(side=LEFT, fill=X, expand=True, padx=(10, 0))
        return entry
        
    def create_button(self, parent, text, command, style=SUCCESS, width=10):
        """创建按钮"""
        return tb.Button(parent, text=text, command=command,
                        bootstyle=style, width=width)

    def create_time_selector(self, parent, time_slots):
        """创建时间选择器"""
        return tb.Combobox(parent, 
                         values=[f"{start}-{end}" for start, end in time_slots],
                         state="readonly", 
                         font=("Helvetica", 10),
                         width=15)

    def create_week_selector(self, parent, start_week=1, end_week=20):
        """创建周数选择器"""
        frame = tb.Frame(parent)
        start_spin = tb.Spinbox(frame, from_=start_week, to=end_week, width=5)
        start_spin.pack(side=LEFT)
        tb.Label(frame, text=" 至 ").pack(side=LEFT)
        end_spin = tb.Spinbox(frame, from_=start_week, to=end_week, width=5)
        end_spin.pack(side=LEFT)
        return start_spin, end_spin
    def create_time_frame(self, parent, label_text: str) -> Tuple:
        """创建时间选择框架"""
        frame = tb.Frame(parent)
        tb.Label(frame, text=label_text).pack(side=LEFT)
        time_combo = tb.Combobox(frame, 
                            values=[f"{start}-{end}" for start, end in self.app.time_slots],
                            state="readonly")
        time_combo.pack(side=LEFT, padx=5)
        return frame, time_combo

    def create_week_frame(self, parent, label_text: str) -> Tuple:
        """创建周数选择框架"""
        frame = tb.Frame(parent)
        tb.Label(frame, text=label_text).pack(side=LEFT)
        start_spin = tb.Spinbox(frame, from_=1, to=20, width=5)
        start_spin.pack(side=LEFT)
        tb.Label(frame, text=" 至 ").pack(side=LEFT)
        end_spin = tb.Spinbox(frame, from_=1, to=20, width=5)
        end_spin.pack(side=LEFT)
        return frame, start_spin, end_spin    
class TopBar(BaseComponent):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        self.create_widgets()

    def create_widgets(self):
        """创建顶部控制栏"""
        # 创建主容器，添加渐变背景
        top_frame = tb.Frame(self.parent, bootstyle=PRIMARY)
        top_frame.pack(fill=X, pady=(0, 10))
        
        # 添加阴影效果
        shadow = tb.Frame(self.parent, height=2, bootstyle=SECONDARY)
        shadow.pack(fill=X, pady=(0, 5))
        
        # 创建内层容器，添加边距和圆角
        inner_frame = tb.Frame(top_frame, padding=15)
        inner_frame.pack(fill=X, expand=True)

        # 创建控制面板容器
        control_container = tb.Frame(inner_frame)
        control_container.pack(side=RIGHT, fill=X, expand=True)

        # 创建Notebook样式
        style = tb.Style()
        style.configure("Custom.TNotebook", 
            background="#f8f9fa",
            tabposition="top")  # 添加更多配置
        style.configure("Custom.TNotebook.Tab", 
            padding=[12, 8],
            background="#ffffff")  # 添加更多配置

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
            ("✏️ 修改学期", self.show_edit_semester_dialog, INFO),
            ("📤 导出课程", self.show_export_dialog, WARNING),
            ("🔗 分享课程", self.show_share_dialog, INFO),
            ("📊 学习报告", self.show_study_report, SECONDARY)
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
    def show_export_dialog(self):
        """显示导出对话框"""
        dialog = tb.Toplevel(self.parent)
        dialog.title("导出课程")
        dialog.geometry("400x420")
        dialog.transient(self.parent)
        dialog.grab_set()

        main_frame = tb.Frame(dialog, padding=20)
        main_frame.pack(fill=BOTH, expand=True)

        # 导出格式选择
        format_frame = tb.LabelFrame(main_frame, text="选择导出格式", padding=10)
        format_frame.pack(fill=X, pady=10)

        self.export_format = tb.StringVar(value="excel")
        formats = [
            ("Excel表格 (.xlsx)", "excel"),
            ("CSV文件 (.csv)", "csv"),
            ("JSON文件 (.json)", "json"),
            ("PDF文件 (.pdf)", "pdf")
        ]
        
        for text, value in formats:
            tb.Radiobutton(format_frame, text=text, variable=self.export_format,
                        value=value).pack(anchor="w", pady=2)

        # 文件名输入
        name_frame = tb.LabelFrame(main_frame, text="文件名（可选）", padding=10)
        name_frame.pack(fill=X, pady=10)
        
        self.filename_entry = tb.Entry(name_frame)
        self.filename_entry.pack(fill=X)

        # 按钮
        btn_frame = tb.Frame(main_frame)
        btn_frame.pack(fill=X, pady=20)
        
        tb.Button(btn_frame, text="取消", command=dialog.destroy,
                bootstyle=(SECONDARY, OUTLINE)).pack(side=RIGHT, padx=5)
        tb.Button(btn_frame, text="导出", command=lambda: self.do_export(dialog),
                bootstyle=SUCCESS).pack(side=RIGHT, padx=5)

    def do_export(self, dialog):
        """执行导出操作"""
        try:
            format = self.export_format.get()
            filename = self.filename_entry.get().strip()
            
            # 获取当前显示的课程
            courses = self.app.courses
            if not courses:
                messagebox.showwarning("提示", "没有可导出的课程")
                return
                
            # 执行导出
            if self.app.course_manager.export_courses(courses, format, filename):
                messagebox.showinfo("成功", "课程导出成功！")
                dialog.destroy()
            else:
                messagebox.showerror("错误", "课程导出失败")
        except Exception as e:
            logger.error(f"导出课程失败: {str(e)}")
            messagebox.showerror("错误", f"导出失败: {str(e)}")
    def show_share_dialog(self):
        """显示分享对话框"""
        from dialogs import ShareDialog
        ShareDialog(self.parent, self.app)
    def show_study_report(self):
        """显示学习报告对话框"""
        from dialogs import StudyReportDialog
        StudyReportDialog(self.parent, self.app)
class StatsPanel(BaseComponent):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        self.create_widgets()

    def create_widgets(self):
        """创建统计面板"""
        self.stats_frame = tb.Labelframe(self.parent, text="课程统计", padding=15)
        self.stats_frame.pack(side=LEFT, fill=Y, padx=(0, 15))
        self.stats_labels = {}
    def _create_stat_section(self, parent, title, stats_dict):
        """创建统计部分"""
        section = tb.LabelFrame(parent, text=title, padding=10)
        section.pack(fill=X, pady=5)
        
        for stat_type, stats in stats_dict.items():
            self._create_stat_widget(section, stat_type, stats)

    def _create_stat_widget(self, parent, stat_type, stats_dict):
        """创建统计信息组件"""
        frame = tb.Frame(parent)
        frame.pack(fill=X, pady=2)
        
        tb.Label(frame, text=stats_dict["text"], 
                font=("Helvetica", 10)).pack(side=LEFT)
        tb.Label(frame, text=str(stats_dict["value"]), 
                bootstyle=stats_dict["style"],
                font=("Helvetica", 12, "bold")).pack(side=RIGHT)
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
                # 获取当天课程时需要同时考虑星期和周数
                view_courses = [c for c in courses 
                            if int(c[6]) == current_date.weekday() + 1 and
                            int(c[4]) <= current_week <= int(c[5])]
                title = "当日信息"
            elif view_type == "month":
                year, month = current_date.year, current_date.month
                # 获取月份的第一天和最后一天
                first_day = datetime(year, month, 1)
                last_day = datetime(year, month + 1, 1) - timedelta(days=1) if month < 12 else datetime(year, 12, 31)
                
                # 计算月份的第一天和最后一天对应的周数
                start_week = ((first_day - datetime.strptime(self.app.current_semester[2], "%Y-%m-%d")).days // 7) + 1
                end_week = ((last_day - datetime.strptime(self.app.current_semester[2], "%Y-%m-%d")).days // 7) + 1
                
                # 获取该月份的所有课程
                view_courses = []
                for week in range(start_week, end_week + 1):
                    week_courses = course_manager.get_courses_by_week(week)
                    view_courses.extend([c for c in week_courses if str(c[12]) == str(self.app.current_semester[0])])
                
                title = f"{month}月信息"
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

            # 添加空闲时间统计
            free_frame = tb.LabelFrame(view_frame, text="时间统计", padding=5)
            free_frame.pack(fill=X, pady=5)

            if view_type == "day":
                # 获取当天的空闲时间
                free_slots = course_manager.get_free_time_slots(current_date.weekday() + 1, current_week)
                free_time = sum(self._calculate_duration(start, end) for start, end in free_slots)
                
                # 第一行：空闲时长标题
                time_frame = tb.Frame(free_frame)
                time_frame.pack(fill=X, pady=2)
                tb.Label(time_frame, text="空闲时长",
                        font=("Helvetica", 10)).pack()
                
                # 第二行：具体时长
                time_value_frame = tb.Frame(free_frame)
                time_value_frame.pack(fill=X, pady=2)
                tb.Label(time_value_frame, text=f"{free_time}小时",
                        font=("Helvetica", 10),
                        bootstyle=INFO).pack()
                
                # 第三行：空闲时间段
                slots_frame = tb.Frame(free_frame)
                slots_frame.pack(fill=X, pady=2)
                if free_slots:
                    slots_text = "\n".join(f"{start}-{end}" for start, end in free_slots)
                    tb.Label(slots_frame, text=f"空闲时段:\n{slots_text}",
                            font=("Helvetica", 9),
                            bootstyle=INFO,
                            wraplength=200).pack()
                else:
                    tb.Label(slots_frame, text="全天满课",
                            font=("Helvetica", 9),
                            bootstyle=WARNING).pack()
                    
            elif view_type == "week":
                # 获取一周的空闲时间统计
                week_free_slots = course_manager.get_week_free_time_slots(current_week)
                total_free_time = 0
                free_days = 0
                
                for day, slots in week_free_slots.items():
                    if slots:  # 如果当天有空闲时间
                        free_days += 1
                        total_free_time += sum(self._calculate_duration(start, end) for start, end in slots)
                
                # 第一行：空闲时长标题
                time_frame = tb.Frame(free_frame)
                time_frame.pack(fill=X, pady=2)
                tb.Label(time_frame, text="周空闲时长",
                        font=("Helvetica", 10)).pack()
                
                # 第二行：具体时长
                time_value_frame = tb.Frame(free_frame)
                time_value_frame.pack(fill=X, pady=2)
                tb.Label(time_value_frame, text=f"{total_free_time}小时",
                        font=("Helvetica", 10),
                        bootstyle=INFO).pack()
                
                # 第三行：空闲天数
                days_frame = tb.Frame(free_frame)
                days_frame.pack(fill=X, pady=2)
                tb.Label(days_frame, text=f"空闲天数: {free_days}/7",
                        font=("Helvetica", 9),
                        bootstyle=INFO).pack()
                        
            else:  # month
                # 获取月份的空闲时间统计
                month_stats = course_manager.get_month_free_time_slots(current_date.year, current_date.month)
                
                # 第一行：空闲时长标题
                time_frame = tb.Frame(free_frame)
                time_frame.pack(fill=X, pady=2)
                tb.Label(time_frame, text="月空闲时长",
                        font=("Helvetica", 10)).pack()
                
                # 第二行：具体时长
                time_value_frame = tb.Frame(free_frame)
                time_value_frame.pack(fill=X, pady=2)
                tb.Label(time_value_frame, text=f"{month_stats['total_free_time']}小时",
                        font=("Helvetica", 10),
                        bootstyle=INFO).pack()
                
                # 第三行：空闲天数
                days_frame = tb.Frame(free_frame)
                days_frame.pack(fill=X, pady=2)
                # 计算空闲天数
                free_days = len([day for day, stats in month_stats['days'].items() if stats['free_time'] > 0])
                tb.Label(days_frame, text=f"空闲天数: {free_days}/{len(month_stats['days'])}",
                        font=("Helvetica", 9),
                        bootstyle=INFO).pack()
                        
        except Exception as e:
            logger.error(f"更新统计信息失败: {str(e)}")
            raise
    def _calculate_duration(self, start_time: str, end_time: str) -> float:
        """计算时间段长度（小时）"""
        try:
            start = datetime.strptime(start_time, "%H:%M")
            end = datetime.strptime(end_time, "%H:%M")
            # 先计算分钟数，再转换为小时，避免浮点数精度问题
            minutes = int((end - start).total_seconds() / 60)
            hours = minutes / 60
            return round(hours, 1)  # 转换为小时并保留一位小数
        except Exception as e:
            logger.error(f"计算时间段长度失败: {str(e)}")
            return 0.0
    def _is_course_in_month(self, course, year, month, current_date):
        """判断课程是否在指定月份内"""
        try:
            # 获取月份第一天和最后一天
            first_day = datetime(year, month, 1)
            last_day = datetime(year, month + 1, 1) - timedelta(days=1) if month < 12 else datetime(year, 12, 31)
            
            # 计算当前日期对应的周数
            course_week = ((current_date - datetime.strptime(self.app.current_semester[2], "%Y-%m-%d")).days // 7) + 1
            
            # 检查课程是否在月份范围内
            return (int(course[4]) <= course_week <= int(course[5]) and 
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

    def create_study_stats_section(self, parent):
        """创建学习统计部分"""
        stats_frame = tb.LabelFrame(parent, text="学习统计", padding=10)
        stats_frame.pack(fill=X, pady=5)
        
        # 获取统计数据
        stats = self.app.course_manager.get_study_statistics(self.app.current_semester[0])
        
        if not stats:
            tb.Label(stats_frame, text="暂无统计数据", 
                    font=("Helvetica", 10),
                    bootstyle=SECONDARY).pack(expand=True)
            return
        
        # 显示总体统计
        total_frame = tb.Frame(stats_frame)
        total_frame.pack(fill=X, pady=5)
        
        tb.Label(total_frame, text="总课程数:",
                font=("Helvetica", 10)).pack(side=LEFT)
        tb.Label(total_frame, text=str(stats['total_courses']),
                font=("Helvetica", 12, "bold"),
                bootstyle=PRIMARY).pack(side=LEFT, padx=5)
        
        tb.Label(total_frame, text="总学时:",
                font=("Helvetica", 10)).pack(side=LEFT, padx=(20, 0))
        tb.Label(total_frame, text=f"{stats['total_hours']:.1f}小时",
                font=("Helvetica", 12, "bold"),
                bootstyle=INFO).pack(side=LEFT, padx=5)
        
        # 显示课程类型分布
        type_frame = tb.LabelFrame(stats_frame, text="课程类型分布", padding=5)
        type_frame.pack(fill=X, pady=5)
        
        for course_type, data in stats['course_types'].items():
            type_item = tb.Frame(type_frame)
            type_item.pack(fill=X, pady=2)
            
            tb.Label(type_item, text=f"{course_type}:",
                    font=("Helvetica", 10)).pack(side=LEFT)
            tb.Label(type_item, text=f"{data['count']}门 ({data['hours']:.1f}小时)",
                    font=("Helvetica", 10),
                    bootstyle=INFO).pack(side=LEFT, padx=5)
