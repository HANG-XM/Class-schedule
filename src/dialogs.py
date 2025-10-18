import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox

class AddCourseDialog:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.create_dialog()

    def create_dialog(self):
        """创建添加课程对话框"""
        self.dialog = tb.Toplevel(self.parent)
        self.dialog.title("添加课程")
        self.dialog.geometry("400x500")  # 减小窗口尺寸
        self.dialog.transient(self.parent)
        self.dialog.grab_set()

        # 创建主容器，使用padding代替内部滚动
        main_container = tb.Frame(self.dialog)
        main_container.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # 创建表单容器
        form_frame = tb.Frame(main_container)
        form_frame.pack(fill=BOTH, expand=True)

        # 标题
        title_label = tb.Label(form_frame, text="添加新课程",
                             font=("Helvetica", 14, "bold"),  # 减小字体
                             bootstyle=PRIMARY)
        title_label.pack(pady=(0, 10))

        # 创建表单字段
        self.create_form_fields(form_frame)

        # 按钮区域
        btn_frame = tb.Frame(form_frame)
        btn_frame.pack(fill=X, pady=10)

        tb.Button(btn_frame, text="取消", command=self.dialog.destroy,
                 bootstyle=(SECONDARY, OUTLINE)).pack(side=RIGHT, padx=5)
        tb.Button(btn_frame, text="保存", command=self.save_course,
                 bootstyle=(SUCCESS, OUTLINE)).pack(side=RIGHT, padx=5)

    def create_form_fields(self, parent):
        """创建表单字段"""
        # 创建两列布局
        left_frame = tb.Frame(parent)
        left_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 5))
        right_frame = tb.Frame(parent)
        right_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=(5, 0))

        # 左侧字段
        # 课程名称
        name_frame = tb.LabelFrame(left_frame, text="课程名称", padding=5)
        name_frame.pack(fill=X, pady=5)
        self.name_entry = tb.Entry(name_frame)
        self.name_entry.pack(fill=X)

        # 任课老师
        teacher_frame = tb.LabelFrame(left_frame, text="任课老师", padding=5)
        teacher_frame.pack(fill=X, pady=5)
        self.teacher_entry = tb.Entry(teacher_frame)
        self.teacher_entry.pack(fill=X)

        # 上课地点
        location_frame = tb.LabelFrame(left_frame, text="上课地点", padding=5)
        location_frame.pack(fill=X, pady=5)
        self.location_entry = tb.Entry(location_frame)
        self.location_entry.pack(fill=X)

        # 右侧字段
        # 周数范围
        week_frame = tb.LabelFrame(right_frame, text="周数范围", padding=5)
        week_frame.pack(fill=X, pady=5)
        week_inner = tb.Frame(week_frame)
        week_inner.pack(fill=X)

        self.start_week = tb.Spinbox(week_inner, from_=1, to=20, width=8)
        self.start_week.pack(side=LEFT)
        tb.Label(week_inner, text="至").pack(side=LEFT, padx=5)
        self.end_week = tb.Spinbox(week_inner, from_=1, to=20, width=8)
        self.end_week.pack(side=LEFT)

        # 星期几
        day_frame = tb.LabelFrame(right_frame, text="星期", padding=5)
        day_frame.pack(fill=X, pady=5)
        self.day_var = tb.IntVar(value=1)
        for i in range(0, 7, 2):  # 每行两个选项
            row_frame = tb.Frame(day_frame)
            row_frame.pack(fill=X)
            for j in range(2):
                if i + j < 7:
                    tb.Radiobutton(row_frame, text=self.app.days_of_week[i + j],
                                 variable=self.day_var, value=i + j + 1).pack(side=LEFT)

        # 底部字段
        bottom_frame = tb.Frame(parent)
        bottom_frame.pack(fill=X, pady=5)

        # 上课时间
        time_frame = tb.LabelFrame(bottom_frame, text="上课时间", padding=5)
        time_frame.pack(fill=X, pady=5)
        self.time_combo = tb.Combobox(time_frame,
                                    values=[f"第{i+1}节 {start}-{end}"
                                           for i, (start, end) in enumerate(self.app.time_slots)])
        self.time_combo.current(0)
        self.time_combo.pack(fill=X)

        # 课程类型和颜色
        type_color_frame = tb.Frame(bottom_frame)
        type_color_frame.pack(fill=X, pady=5)

        # 课程类型
        type_frame = tb.LabelFrame(type_color_frame, text="课程类型", padding=5)
        type_frame.pack(side=LEFT, fill=X, expand=True, padx=(0, 5))
        self.type_var = tb.StringVar(value="正常")
        tb.Radiobutton(type_frame, text="正常", variable=self.type_var, value="正常").pack(side=LEFT)
        tb.Radiobutton(type_frame, text="调休", variable=self.type_var, value="调休").pack(side=LEFT)

        # 颜色选择
        color_frame = tb.LabelFrame(type_color_frame, text="颜色标记", padding=5)
        color_frame.pack(side=LEFT, fill=X, expand=True, padx=(5, 0))
        colors = ["primary", "secondary", "success", "danger", "warning", "info", "light", "dark"]
        self.color_var = tb.StringVar(value=colors[0])
        color_combo = tb.Combobox(color_frame, values=colors, textvariable=self.color_var)
        color_combo.pack(fill=X)

    def save_course(self):
        """保存课程"""
        try:
            time_index = self.time_combo.current()
            if time_index < 0:
                raise ValueError("请选择上课时间")
            start_time, end_time = self.app.time_slots[time_index]

            course_data = (
                self.name_entry.get(),
                self.teacher_entry.get(),
                self.location_entry.get(),
                int(self.start_week.get()),
                int(self.end_week.get()),
                self.day_var.get(),
                start_time,
                end_time,
                self.color_var.get(),
                self.type_var.get(),
                1 if self.type_var.get() == "调休" else 0
            )

            self.app.course_manager.add_course(course_data)
            self.app.load_courses()
            self.app.update_display()
            self.dialog.destroy()
            messagebox.showinfo("成功", "课程添加成功！")

        except Exception as e:
            messagebox.showerror("错误", f"添加课程失败: {str(e)}")

