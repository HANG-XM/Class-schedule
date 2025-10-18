import ttkbootstrap as tb
from ttkbootstrap.constants import *
from main import logger
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

        # 添加学期选择器
        semester_frame = tb.Frame(top_frame)
        semester_frame.pack(side=RIGHT, padx=10)
        
        tb.Label(semester_frame, text="学期:").pack(side=LEFT)
        self.semester_var = tb.StringVar()
        semester_combo = tb.Combobox(semester_frame, textvariable=self.semester_var,
                                values=[s[1] for s in self.app.semesters],
                                state="readonly", width=15)
        semester_combo.pack(side=LEFT, padx=5)
        semester_combo.set(self.app.current_semester[1])
        semester_combo.bind('<<ComboboxSelected>>', self.on_semester_change)
        
        # 添加新建学期按钮
        tb.Button(semester_frame, text="新建学期",
                command=self.show_add_semester_dialog,
                bootstyle=(PRIMARY, OUTLINE)).pack(side=LEFT, padx=5)

    def on_semester_change(self, event):
        """学期切换事件"""
        selected_name = event.widget.get()
        for semester in self.app.semesters:
            if semester[1] == selected_name:
                self.app.course_manager.set_current_semester(semester[0])
                self.app.current_semester = semester
                self.app.load_courses()  # 重新加载课程
                self.app.update_display()  # 更新显示
                break

    def show_add_semester_dialog(self):
        """显示新建学期对话框"""
        from dialogs import AddSemesterDialog
        AddSemesterDialog(self.parent, self.app)
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
        # 清空现有统计信息
        for widget in self.stats_frame.winfo_children():
            widget.destroy()

        # 计算统计信息
        total_courses = len(courses)
        current_week_courses = len(course_manager.get_courses_by_week(current_week))

        # 按类型统计
        normal_courses = len([c for c in courses if c[10] == 0])
        special_courses = len([c for c in courses if c[10] == 1])

        # 显示统计信息
        stats_data = [
            ("总课程数", total_courses, "primary"),
            ("本周课程", current_week_courses, "success"),
            ("正常课程", normal_courses, "info"),
            ("调休课程", special_courses, "warning")
        ]

        for text, value, style in stats_data:
            frame = tb.Frame(self.stats_frame)
            frame.pack(fill=X, pady=5)

            tb.Label(frame, text=text, font=("Helvetica", 10)).pack(side=LEFT)
            tb.Label(frame, text=str(value), bootstyle=style,
                    font=("Helvetica", 12, "bold")).pack(side=RIGHT)
