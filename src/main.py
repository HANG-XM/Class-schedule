import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from course_manager import CourseManager, SpecialCourse
from ui_components import TopBar, StatsPanel
from views import WeekView, DayView, MonthView
from dialogs import AddCourseDialog
from logger_config import logger

class ModernCourseScheduleApp:
    def __init__(self):
        self.root = tb.Window(themename="flatly")
        self.style = tb.Style(theme="flatly")
        self.root.title("小梦课程表")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 800)

        self._init_variables()
        self.init_semesters()
        self.setup_ui()
        self._post_init()
    def _init_variables(self):
        """初始化变量"""
        self.course_manager = CourseManager()
        self.current_view = "week"
        self.current_theme = "flatly"
        self.themes = ["flatly", "darkly", "solar", "superhero", "cyborg"]
        self.time_slots = [
            ("07:35", "07:45"), ("08:00", "09:40"), ("10:00", "11:40"),
            ("14:00", "15:40"), ("16:00", "17:40"), ("19:00", "20:40")
        ]
        self.days_of_week = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
        self.courses = []
        self.current_week = self.get_current_week()

    def _post_init(self):
        """UI初始化后的设置"""
        self.top_bar.week_var.set(self.current_week)
        self.load_courses()
        self.update_display()
    def init_semesters(self):
        """初始化学期"""
        self.semesters = self.course_manager.get_semesters()
        if not self.semesters:
            # 如果没有学期，创建默认学期
            self.course_manager.add_semester("2023-2024学年", "2023-09-01", "2024-01-20")
            self.semesters = self.course_manager.get_semesters()
        
        # 设置当前学期
        current_semester = self.course_manager.get_current_semester()
        if current_semester:
            self.current_semester = current_semester
        else:
            self.current_semester = self.semesters[0]
            self.course_manager.set_current_semester(self.current_semester[0])
    def setup_ui(self):
        """设置用户界面"""
        # 主容器
        main_frame = tb.Frame(self.root)
        main_frame.pack(fill=BOTH, expand=True, padx=15, pady=15)

        # 顶部控制栏
        self.top_bar = TopBar(main_frame, self)

        # 内容区域
        content_frame = tb.Frame(main_frame)
        content_frame.pack(fill=BOTH, expand=True, pady=(10, 0))

        # 左侧统计面板
        self.stats_panel = StatsPanel(content_frame)

        # 右侧显示区域
        self.display_frame = tb.Frame(content_frame)
        self.display_frame.pack(side=LEFT, fill=BOTH, expand=True)

        # 初始化视图
        self.week_view = WeekView(self.display_frame, self)
        self.day_view = DayView(self.display_frame, self)
        self.month_view = MonthView(self.display_frame, self)

    def show_add_course_dialog(self):
        """显示添加课程对话框"""
        AddCourseDialog(self.root, self)

    def load_courses(self):
        """加载课程数据"""
        self.courses = self.course_manager.get_courses()
        # 过滤当前学期的课程
        self.courses = [c for c in self.courses if c[11] == self.current_semester[0]]
        logger.info(f"已加载当前学期课程，共 {len(self.courses)} 门")
        logger.info(f"当前学期ID: {self.current_semester[0]}")

    def update_display(self):
        """更新显示"""
        self.stats_panel.update_stats(self.courses, self.current_week, self.course_manager)

        # 隐藏所有视图
        self.week_view.frame.pack_forget()
        self.day_view.frame.pack_forget()
        self.month_view.frame.pack_forget()

        # 显示当前视图
        if self.current_view == "week":
            self.week_view.show()
            self.week_view.frame.pack(fill=BOTH, expand=True)
        elif self.current_view == "day":
            self.day_view.show()
            self.day_view.frame.pack(fill=BOTH, expand=True)
        else:
            self.month_view.show()
            self.month_view.frame.pack(fill=BOTH, expand=True)

    def on_week_change(self):
        """周数改变事件"""
        self.current_week = self.top_bar.week_var.get()
        self.load_courses()
        self.update_display()

    def switch_view(self, view):
        """切换视图"""
        self.current_view = view
        self.update_display()
        logger.info(f"视图已切换到: {view}")

    def on_theme_change(self, event):
        """主题切换事件"""
        new_theme = event.widget.get()
        self.style.theme_use(new_theme)
        self.current_theme = new_theme
        logger.info(f"主题已切换到: {new_theme}")
        # 重置表格样式
        style = ttk.Style()
        style.configure("Treeview", rowheight=100)
        style.configure("Treeview.Heading", font=("Helvetica", 11, "bold"))

        # 如果当前是周视图，刷新显示
        if self.current_view == "week":
            self.week_view.show()
    def get_current_week(self):
        """获取当前周数"""
        # 获取当前日期
        today = datetime.now()
        
        # 假设学期开始日期为9月1日
        start_date = datetime(today.year, 9, 1)
        
        # 计算周数差
        week_diff = (today - start_date).days // 7 + 1
        
        # 确保周数在合理范围内
        return max(1, min(week_diff, 20))
    def run(self):
        """运行应用"""
        self.root.mainloop()

if __name__ == "__main__":
    app = ModernCourseScheduleApp()
    app.run()
