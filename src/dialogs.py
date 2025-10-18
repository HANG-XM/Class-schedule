import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox
from datetime import datetime

class AddCourseDialog:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.create_dialog()

    def create_dialog(self):
        """创建添加课程对话框"""
        self.dialog = tb.Toplevel(self.parent)
        self.dialog.title("添加课程")
        self.dialog.geometry("400x500")
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
                             font=("Helvetica", 14, "bold"),
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
        # 创建主容器
        main_container = tb.Frame(parent)
        main_container.pack(fill=BOTH, expand=True)

        # 使用网格布局创建表单
        grid_frame = tb.Frame(main_container)
        grid_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # 左侧字段
        # 课程名称
        tb.Label(grid_frame, text="课程名称:", width=12).grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.name_entry = tb.Entry(grid_frame)
        self.name_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        tb.Label(grid_frame, text="例：高等数学", font=("Helvetica", 9), 
                foreground="gray").grid(row=0, column=2, sticky="w", padx=5)

        # 任课老师
        tb.Label(grid_frame, text="任课老师:", width=12).grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.teacher_entry = tb.Entry(grid_frame)
        self.teacher_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        tb.Label(grid_frame, text="例：张老师", font=("Helvetica", 9), 
                foreground="gray").grid(row=1, column=2, sticky="w", padx=5)

        # 上课地点
        tb.Label(grid_frame, text="上课地点:", width=12).grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.location_entry = tb.Entry(grid_frame)
        self.location_entry.grid(row=2, column=1, sticky="ew", padx=5, pady=5)
        tb.Label(grid_frame, text="例：教学楼A101", font=("Helvetica", 9), 
                foreground="gray").grid(row=2, column=2, sticky="w", padx=5)

        # 时间选择部分修改
        time_frame = tb.Frame(grid_frame)
        time_frame.grid(row=3, column=0, columnspan=3, sticky="ew", padx=5, pady=5)

        tb.Label(time_frame, text="上课时间", font=("Helvetica", 10, "bold")).pack(anchor="w", pady=(0, 5))
        time_inner = tb.Frame(time_frame)
        time_inner.pack(fill="x")

        self.start_time = tb.Combobox(time_inner, 
                                    values=[f"{start}-{end}" for start, end in self.app.time_slots],
                                    state="readonly")
        self.start_time.pack(side=LEFT, padx=2)
        self.start_time.current(0)

        # 课程类型和颜色部分修改
        type_color_frame = tb.Frame(grid_frame)
        type_color_frame.grid(row=4, column=0, columnspan=3, sticky="ew", padx=5, pady=5)

        # 课程类型
        type_frame = tb.Frame(type_color_frame)
        type_frame.pack(side=LEFT, fill="x", expand=True)

        tb.Label(type_frame, text="课程类型", font=("Helvetica", 10, "bold")).pack(anchor="w", pady=(0, 5))
        type_inner = tb.Frame(type_frame)
        type_inner.pack(fill="x")

        self.type_var = tb.StringVar(value="正常")
        tb.Radiobutton(type_inner, text="正常", variable=self.type_var, value="正常").pack(side=LEFT, padx=5)
        tb.Radiobutton(type_inner, text="调休", variable=self.type_var, value="调休").pack(side=LEFT, padx=5)

        # 颜色选择
        color_frame = tb.Frame(type_color_frame)
        color_frame.pack(side=LEFT, fill="x", expand=True)

        tb.Label(color_frame, text="颜色标记", font=("Helvetica", 10, "bold")).pack(anchor="w", pady=(0, 5))
        color_inner = tb.Frame(color_frame)
        color_inner.pack(fill="x")

        colors = ["primary", "secondary", "success", "danger", "warning", "info", "light", "dark"]
        self.color_var = tb.StringVar(value=colors[0])
        for color in colors:
            btn = tb.Button(color_inner, text="●", bootstyle=color, width=3)
            btn.pack(side=LEFT, padx=2)
            btn.bind("<Button-1>", lambda e, c=color: self.color_var.set(c))

        # 周数范围部分修改
        week_frame = tb.Frame(grid_frame)
        week_frame.grid(row=5, column=0, columnspan=3, sticky="ew", padx=5, pady=5)

        tb.Label(week_frame, text="周数范围", font=("Helvetica", 10, "bold")).pack(anchor="w", pady=(0, 5))
        week_inner = tb.Frame(week_frame)
        week_inner.pack(fill="x")

        tb.Label(week_inner, text="第").pack(side=LEFT)
        self.start_week = tb.Spinbox(week_inner, from_=1, to=20, width=5)
        self.start_week.pack(side=LEFT, padx=2)
        tb.Label(week_inner, text="至").pack(side=LEFT, padx=2)
        self.end_week = tb.Spinbox(week_inner, from_=1, to=20, width=5)
        self.end_week.pack(side=LEFT, padx=2)
        tb.Label(week_inner, text="周").pack(side=LEFT)

        # 星期几选择部分修改
        day_frame = tb.Frame(grid_frame)
        day_frame.grid(row=6, column=0, columnspan=3, sticky="ew", padx=5, pady=5)

        tb.Label(day_frame, text="上课星期", font=("Helvetica", 10, "bold")).pack(anchor="w", pady=(0, 5))
        day_inner = tb.Frame(day_frame)
        day_inner.pack(fill="x")

        self.day_var = tb.IntVar(value=1)
        for i in range(7):
            day_btn = tb.Radiobutton(day_inner, 
                                 text=self.app.days_of_week[i],
                                 variable=self.day_var, 
                                 value=i + 1)
            day_btn.pack(side=LEFT, padx=5)

        # 配置网格权重
        grid_frame.columnconfigure(1, weight=1)
        grid_frame.columnconfigure(2, weight=1)
        grid_frame.columnconfigure(3, weight=1)

    def save_course(self):
        """保存课程"""
        try:
            # 验证必填字段
            if not self.name_entry.get().strip():
                raise ValueError("请输入课程名称")
            if not self.teacher_entry.get().strip():
                raise ValueError("请输入任课老师")
            if not self.location_entry.get().strip():
                raise ValueError("请输入上课地点")

            # 验证周数范围
            start_week = int(self.start_week.get())
            end_week = int(self.end_week.get())
            if start_week > end_week:
                raise ValueError("起始周不能大于结束周")

            # 获取时间选择
            time_index = self.start_time.current()
            if time_index < 0:
                raise ValueError("请选择上课时间")
            start_time, end_time = self.app.time_slots[time_index]

            course_data = (
                self.name_entry.get().strip(),
                self.teacher_entry.get().strip(),
                self.location_entry.get().strip(),
                start_week,
                end_week,
                self.day_var.get(),
                start_time,
                end_time,
                self.color_var.get(),
                self.type_var.get(),
                1 if self.type_var.get() == "调休" else 0,
                self.app.current_semester[0]  # 添加学期ID
            )

            self.app.course_manager.add_course(course_data)
            self.app.load_courses()
            self.app.update_display()
            self.dialog.destroy()
            messagebox.showinfo("成功", "课程添加成功！")

        except ValueError as ve:
            messagebox.showerror("输入错误", str(ve))
        except Exception as e:
            messagebox.showerror("错误", f"添加课程失败: {str(e)}")

class AddSemesterDialog:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.create_dialog()

    def create_dialog(self):
        """创建新建学期对话框"""
        self.dialog = tb.Toplevel(self.parent)
        self.dialog.title("新建学期")
        self.dialog.geometry("500x430")  # 增加窗口尺寸
        self.dialog.transient(self.parent)
        self.dialog.grab_set()

        main_frame = tb.Frame(self.dialog, padding=20)  # 增加内边距
        main_frame.pack(fill=BOTH, expand=True)

        # 学期类型选择
        tb.Label(main_frame, text="学期类型:", font=("Helvetica", 12)).pack(anchor="w", pady=(10, 5))
        self.semester_type = tb.Combobox(main_frame, 
                                   values=["秋季", "春季"],
                                   state="readonly",
                                   font=("Helvetica", 11))  # 增大字体
        self.semester_type.pack(fill="x", pady=(0, 15))
        self.semester_type.set("秋季")
        self.semester_type.bind('<<ComboboxSelected>>', lambda e: self.update_semester_name())

        # 学期名称
        tb.Label(main_frame, text="学期名称:", font=("Helvetica", 12)).pack(anchor="w", pady=(10, 5))
        self.name_entry = tb.Entry(main_frame, font=("Helvetica", 11))  # 增大字体
        self.name_entry.pack(fill="x", pady=(0, 15))
        self.name_entry.insert(0, self.generate_semester_name())
        self.name_entry.config(state="readonly")

        # 日期选择框架
        date_frame = tb.Frame(main_frame)
        date_frame.pack(fill="x", pady=20)  # 增加上下间距

        # 开始日期
        start_frame = tb.Frame(date_frame)
        start_frame.pack(fill="x", pady=(0, 15))
        tb.Label(start_frame, text="开始日期:", font=("Helvetica", 12)).pack(side=LEFT)
        self.start_date = tb.DateEntry(start_frame, bootstyle="primary", 
                                    dateformat="%Y-%m-%d")  # 移除font参数
        self.start_date.pack(side=LEFT, padx=10)

        # 结束日期
        end_frame = tb.Frame(date_frame)
        end_frame.pack(fill="x", pady=(0, 15))
        tb.Label(end_frame, text="结束日期:", font=("Helvetica", 12)).pack(side=LEFT)
        self.end_date = tb.DateEntry(end_frame, bootstyle="primary",
                                dateformat="%Y-%m-%d")  # 移除font参数
        self.end_date.pack(side=LEFT, padx=10)

        # 按钮
        btn_frame = tb.Frame(main_frame)
        btn_frame.pack(fill="x", pady=0)  # 增加上下间距
        
        tb.Button(btn_frame, text="取消", command=self.dialog.destroy,
                bootstyle=(SECONDARY, OUTLINE), width=10).pack(side="right", padx=5)
        tb.Button(btn_frame, text="保存", command=self.save_semester,
                bootstyle=(SUCCESS, OUTLINE), width=10).pack(side="right", padx=5)

    def update_semester_name(self):
        """更新学期名称"""
        self.name_entry.config(state="normal")
        self.name_entry.delete(0, tb.END)
        self.name_entry.insert(0, self.generate_semester_name())
        self.name_entry.config(state="readonly")

    def generate_semester_name(self):
        """根据当前年份和选择的学期类型生成学期名称"""
        current_year = datetime.now().year
        semester_type = self.semester_type.get()
        
        if semester_type == "秋季":
            return f"{current_year}年秋季学期"
        else:
            return f"{current_year + 1}年春季学期"

    def save_semester(self):
        """保存学期"""
        try:
            name = self.name_entry.get().strip()
            start = self.start_date.entry.get()
            end = self.end_date.entry.get()
            
            if not all([name, start, end]):
                raise ValueError("请填写完整信息")
                
            # 验证日期格式
            try:
                start_date = datetime.strptime(start, "%Y-%m-%d")
                end_date = datetime.strptime(end, "%Y-%m-%d")
            except ValueError:
                raise ValueError("日期格式不正确，请使用YYYY-MM-DD格式")
                
            # 验证日期范围
            if start_date >= end_date:
                raise ValueError("结束日期必须晚于开始日期")
                    
            self.app.course_manager.add_semester(name, start, end)
            self.app.semesters = self.app.course_manager.get_semesters()
            self.dialog.destroy()
            messagebox.showinfo("成功", "学期创建成功！")
            
        except ValueError as ve:
            messagebox.showerror("错误", str(ve))
