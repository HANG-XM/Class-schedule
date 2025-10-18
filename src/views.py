import ttkbootstrap as tb
from ttkbootstrap.constants import *
from datetime import datetime

class WeekView:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.create_widgets()

    def create_widgets(self):
        """创建周视图"""
        self.frame = tb.Frame(self.parent)
        self.show()

    def show(self):
        """显示周视图"""
        # 清空现有内容
        for widget in self.frame.winfo_children():
            widget.destroy()

        # 创建表格
        columns = ["时间"] + self.app.days_of_week
        tree = tb.Treeview(self.frame, columns=columns, show="tree headings", height=22)

        # 设置列宽和样式
        style = tb.Style()
        style.configure("Treeview", rowheight=100)
        tree.configure(style="Treeview")

        tree.column("#0", width=0, stretch=NO)
        tree.column("时间", width=90, anchor=CENTER)
        for day in self.app.days_of_week:
            tree.column(day, width=180, anchor=CENTER)

        # 设置表头样式
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, minwidth=100)

        # 添加时间行
        for i, (start, end) in enumerate(self.app.time_slots):
            values = [f"{start}\n{end}"] + [""] * 7
            tree.insert("", "end", values=values)

        # 添加课程到表格
        week_courses = self.app.course_manager.get_courses_by_week(self.app.current_week)
        for course in week_courses:
            day_index = course[5]  # 星期几 (1-7)
            time_index = None

            # 找到对应的时间段
            for i, (start, end) in enumerate(self.app.time_slots):
                if course[6] == start and course[7] == end:
                    time_index = i
                    break

            if time_index is not None:
                # 获取树中的项目ID
                item_id = tree.get_children()[time_index]

                # 获取当前值并更新
                current_values = list(tree.item(item_id, "values"))
                course_text = f"{course[1]}\n{course[2]}\n{course[3]}-{course[4]}周"
                current_values[day_index] = course_text

                # 更新值
                tree.item(item_id, values=current_values)

        tree.pack(fill=BOTH, expand=True)

class DayView:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.create_widgets()

    def create_widgets(self):
        """创建日视图"""
        self.frame = tb.Frame(self.parent)
        self.show()

    def show(self):
        """显示日视图"""
        # 清空现有内容
        for widget in self.frame.winfo_children():
            widget.destroy()

        # 创建日视图内容
        content = tb.Frame(self.frame)
        content.pack(fill=BOTH, expand=True, padx=20, pady=20)

        tb.Label(content, text="日视图",
                font=("Helvetica", 24, "bold"),
                bootstyle=PRIMARY).pack(pady=20)

        # 创建当天的课程列表
        current_day = datetime.now().weekday() + 1
        day_courses = self.app.course_manager.get_courses_by_day(current_day, self.app.current_week)

        if day_courses:
            for course in day_courses:
                frame = tb.Frame(content, padding=10)
                frame.pack(fill=X, pady=5)

                tb.Label(frame, text=f"{course[1]}",
                        font=("Helvetica", 14)).pack(side=LEFT)
                tb.Label(frame, text=f"{course[6]}-{course[7]}",
                        bootstyle=INFO).pack(side=RIGHT)
        else:
            tb.Label(content, text="当天暂无课程",
                    font=("Helvetica", 14),
                    bootstyle=SECONDARY).pack(expand=True)

class MonthView:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.create_widgets()

    def create_widgets(self):
        """创建月视图"""
        self.frame = tb.Frame(self.parent)
        self.show()

    def show(self):
        """显示月视图"""
        # 清空现有内容
        for widget in self.frame.winfo_children():
            widget.destroy()

        # 创建月视图内容
        content = tb.Frame(self.frame)
        content.pack(fill=BOTH, expand=True, padx=20, pady=20)

        tb.Label(content, text="月视图",
                font=("Helvetica", 24, "bold"),
                bootstyle=PRIMARY).pack(pady=20)

        # 创建月份概览
        month_frame = tb.Frame(content)
        month_frame.pack(fill=BOTH, expand=True)

        # 添加星期标题
        week_days = ["一", "二", "三", "四", "五", "六", "日"]
        for day in week_days:
            tb.Label(month_frame, text=day, width=4).pack(side=LEFT, padx=2)

        # 添加日期格子
        for date in range(1, 31):  # 假设每月最多31天
            day_frame = tb.Frame(month_frame, relief=RIDGE, borderwidth=1)
            day_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=2, pady=2)

            day_of_week = (date - 1) % 7 + 1
            if date == 1:  # 新的一周开始
                tb.Frame(month_frame, height=20).pack(fill=X)  # 添加间隔

            tb.Label(day_frame, text=str(date)).pack()

            # 检查是否有课程
            has_course = any(c for c in self.app.courses
                           if c[5] == day_of_week and c[3] <= self.app.current_week <= c[4])
            if has_course:
                tb.Label(day_frame, text="●", bootstyle=SUCCESS).pack()
