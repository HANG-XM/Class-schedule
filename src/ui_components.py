import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox
from logger_config import logger

class TopBar:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.create_widgets()

    def create_widgets(self):
        """创建顶部控制栏"""
        top_frame = tb.Frame(self.parent)
        top_frame.pack(fill=X, pady=(0, 10))

        # 标题
        title_label = tb.Label(top_frame, text="智能课程表", font=("Helvetica", 20, "bold"),
                              bootstyle=PRIMARY)
        title_label.pack(side=LEFT)

        # 控制按钮组
        control_frame = tb.Frame(top_frame)
        control_frame.pack(side=RIGHT)

        # 周数控制
        tb.Label(control_frame, text="第").pack(side=LEFT, padx=(0, 5))
        self.week_var = tb.IntVar(value=self.app.current_week)
        week_spinbox = tb.Spinbox(control_frame, from_=1, to=20, width=5,
                                 textvariable=self.week_var, command=self.app.on_week_change)
        week_spinbox.pack(side=LEFT, padx=5)
        tb.Label(control_frame, text="周").pack(side=LEFT, padx=(0, 10))

        # 视图切换
        view_btn_frame = tb.Frame(control_frame)
        view_btn_frame.pack(side=LEFT, padx=10)

        tb.Button(view_btn_frame, text="周视图", command=lambda: self.app.switch_view("week"),
                 bootstyle=OUTLINE).pack(side=LEFT, padx=2)
        tb.Button(view_btn_frame, text="日视图", command=lambda: self.app.switch_view("day"),
                 bootstyle=OUTLINE).pack(side=LEFT, padx=2)
        tb.Button(view_btn_frame, text="月视图", command=lambda: self.app.switch_view("month"),
                 bootstyle=OUTLINE).pack(side=LEFT, padx=2)

        # 主题切换
        theme_combo = tb.Combobox(control_frame, values=self.app.themes, width=10,
                                 state="readonly")
        theme_combo.set(self.app.current_theme)
        theme_combo.pack(side=LEFT, padx=10)
        theme_combo.bind('<<ComboboxSelected>>', self.app.on_theme_change)

        # 添加课程按钮
        tb.Button(control_frame, text="添加课程", command=self.app.show_add_course_dialog,
                 bootstyle=SUCCESS).pack(side=LEFT, padx=10)

        # 添加新建学期按钮
        tb.Button(control_frame, text="新建学期",
                command=self.show_add_semester_dialog,
                bootstyle=(PRIMARY, OUTLINE)).pack(side=LEFT, padx=5)

        # 只有存在学期时才显示学期选择器
        if self.app.current_semester:
            self._create_semester_selector(top_frame)

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
            # 获取 Combobox 组件的引用
            for widget in self.parent.winfo_children():
                for child in widget.winfo_children():
                    if isinstance(child, tb.Combobox) and child['textvariable'] == str(self.semester_var):
                        semester_combo = child
                        break
            # 更新下拉框选项
            semester_combo['values'] = [s[1] for s in self.app.semesters]
            if self.app.current_semester:
                semester_combo.set(self.app.current_semester[1])
        else:
            # 如果不存在学期选择器，创建一个
            self._create_semester_selector(self.parent.winfo_children()[0])

    def _refresh_semester_list(self):
        """刷新学期列表"""
        self.app.semesters = self.app.course_manager.get_semesters()
        if hasattr(self, 'semester_var'):
            self.semester_var.set('')
            semester_combo = self.semester_var.master
            semester_combo['values'] = [s[1] for s in self.app.semesters]
            if self.app.current_semester:
                semester_combo.set(self.app.current_semester[1])

class StatsPanel:
    def __init__(self, parent):
        self.parent = parent
        self.create_widgets()

    def create_widgets(self):
        """创建统计面板"""
        self.stats_frame = tb.Labelframe(self.parent, text="课程统计", padding=15)
        self.stats_frame.pack(side=LEFT, fill=Y, padx=(0, 15))
        self.stats_labels = {}

    def update_stats(self, courses, current_week, course_manager):
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

            # 计算统计信息
            stats = self._calculate_stats(courses, current_week, course_manager)
            
            # 创建统计信息显示
            for stat_type, stats_dict in stats.items():
                self._create_stat_widget(stat_type, stats_dict)
                
        except Exception as e:
            logger.error(f"更新统计信息失败: {str(e)}")
            raise

    def _calculate_stats(self, courses, current_week, course_manager):
        """计算统计信息"""
        return {
            "total": {
                "text": "总课程数",
                "value": len(courses),
                "style": "primary"
            },
            "weekly": {
                "text": "本周课程",
                "value": len(course_manager.get_courses_by_week(current_week)),
                "style": "success"
            },
            "normal": {
                "text": "正常课程",
                "value": len([c for c in courses if not c[10]]),
                "style": "info"
            },
            "special": {
                "text": "调休课程",
                "value": len([c for c in courses if c[10]]),
                "style": "warning"
            }
        }

    def _create_stat_widget(self, stat_type, stats_dict):
        """创建统计信息组件"""
        frame = tb.Frame(self.stats_frame)
        frame.pack(fill=X, pady=5)
        
        tb.Label(frame, text=stats_dict["text"], font=("Helvetica", 10)).pack(side=LEFT)
        tb.Label(frame, text=str(stats_dict["value"]), 
                bootstyle=stats_dict["style"],
                font=("Helvetica", 12, "bold")).pack(side=RIGHT)
