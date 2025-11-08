import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox

from datetime import datetime
from logger_config import logger

from course_manager import SpecialCourse, DataValidator
class BaseDialog:
    def __init__(self, parent, app, title, geometry):
        self.parent = parent
        self.app = app
        self.dialog = tb.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry(geometry)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
    def create_main_frame(self, padding=20):
        """创建主框架"""
        return tb.Frame(self.dialog, padding=padding)
        
    def create_button_frame(self, parent):
        """创建按钮框架"""
        btn_frame = tb.Frame(parent)
        btn_frame.pack(fill=X, pady=5)
        tb.Button(btn_frame, text="取消", command=self.dialog.destroy,
                 bootstyle=(SECONDARY, OUTLINE), width=10).pack(side=RIGHT, padx=5)
        return btn_frame

    def validate_inputs(self, *fields):
        """验证输入字段"""
        errors = []
        for field, name in fields:
            if not field or not field.strip():
                errors.append(f"请输入{name}")
        return errors

class AddCourseDialog(BaseDialog):
    def __init__(self, parent, app):
        super().__init__(parent, app, "添加课程", "580x840")
        self.create_dialog()

    def create_dialog(self):
        """创建添加课程对话框"""
        self.dialog = tb.Toplevel(self.parent)
        self.dialog.title("添加课程")
        self.dialog.geometry("580x840")
        self.dialog.resizable(False, False)
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        # 设置窗口样式
        self.dialog.tk_setPalette(background="#ffffff")
        self.dialog.configure(bg="#ffffff")

        # 创建主容器
        main_frame = tb.Frame(self.dialog, padding=8)
        main_frame.pack(fill=BOTH, expand=True)

        # 创建表单区域
        self.create_form_content(main_frame)

        # 按钮区域
        self.create_button_area(main_frame)

    def create_form_content(self, parent):
        """创建表单内容"""
        # 基本信息
        self.create_basic_info_section(parent)
        
        # 时间和周数设置
        self.create_time_week_section(parent)
        
        # 课程类型和颜色
        self.create_type_color_section(parent)
        
        # 星期设置
        self.create_day_section(parent)
        
        # 提醒设置
        self.create_reminder_section(parent)

    def create_reminder_section(self, parent):
        """创建提醒设置部分"""
        section_frame = tb.LabelFrame(parent, text="提醒设置", padding=8)
        section_frame.pack(fill=X, pady=3)

        # 启用提醒
        self.reminder_enabled = tb.BooleanVar(value=False)
        tb.Checkbutton(section_frame, text="启用上课提醒", 
                    variable=self.reminder_enabled).pack(anchor="w", pady=(0, 5))

        # 提醒时间设置
        reminder_frame = tb.Frame(section_frame)
        reminder_frame.pack(fill=X, pady=(0, 5))
        
        tb.Label(reminder_frame, text="提前提醒时间:").pack(side=LEFT)
        self.reminder_minutes = tb.Spinbox(reminder_frame, from_=5, to=60, 
                                        increment=5, width=10)
        self.reminder_minutes.set(15)
        self.reminder_minutes.pack(side=LEFT, padx=5)
        tb.Label(reminder_frame, text="分钟").pack(side=LEFT)

        # 提醒方式
        type_frame = tb.Frame(section_frame)
        type_frame.pack(fill=X)
        
        tb.Label(type_frame, text="提醒方式:").pack(side=LEFT)
        self.reminder_type = tb.StringVar(value="popup")
        types = [("弹窗提醒", "popup"), ("声音提醒", "sound"), ("两者都有", "both")]
        for text, value in types:
            tb.Radiobutton(type_frame, text=text, variable=self.reminder_type,
                        value=value).pack(side=LEFT, padx=5)

    def create_basic_info_section(self, parent):
        """创建基本信息部分"""
        section_frame = tb.LabelFrame(parent, text="基本信息", padding=8)
        section_frame.pack(fill=X, pady=3)

        # 课程名称
        name_frame = tb.Frame(section_frame)
        name_frame.pack(fill=X, pady=3)
        tb.Label(name_frame, text="课程名称:", width=10).pack(side=LEFT)
        self.name_entry = tb.Entry(name_frame, font=("Helvetica", 10))
        self.name_entry.pack(side=LEFT, fill=X, expand=True, padx=(10, 0))

        # 任课老师
        teacher_frame = tb.Frame(section_frame)
        teacher_frame.pack(fill=X, pady=3)
        tb.Label(teacher_frame, text="任课老师:", width=10).pack(side=LEFT)
        self.teacher_entry = tb.Entry(teacher_frame, font=("Helvetica", 10))
        self.teacher_entry.pack(side=LEFT, fill=X, expand=True, padx=(10, 0))

        # 上课地点
        location_frame = tb.Frame(section_frame)
        location_frame.pack(fill=X, pady=3)
        tb.Label(location_frame, text="上课地点:", width=10).pack(side=LEFT)
        self.location_entry = tb.Entry(location_frame, font=("Helvetica", 10))
        self.location_entry.pack(side=LEFT, fill=X, expand=True, padx=(10, 0))
    def create_time_week_section(self, parent):
        """创建时间和周数设置部分"""
        section_frame = tb.LabelFrame(parent, text="时间安排", padding=8)
        section_frame.pack(fill=X, pady=3)

        # 上方：时间选择
        time_frame = tb.Frame(section_frame)
        time_frame.pack(fill=X, pady=(0, 5))
        
        tb.Label(time_frame, text="上课时间:").pack(side=LEFT)
        self.start_time = tb.Combobox(time_frame, 
                                    values=[f"{start}-{end}" for start, end in self.app.time_slots],
                                    state="readonly", 
                                    font=("Helvetica", 10),
                                    width=15)
        self.start_time.pack(side=LEFT, padx=(10, 0))
        self.start_time.bind("<<ComboboxSelected>>", self.update_time_preview)

        # 添加时间预览标签
        self.time_preview = tb.Label(section_frame, text="请选择时间段", 
                                font=("Helvetica", 10), bootstyle=INFO)
        self.time_preview.pack(fill=X, pady=(0, 10))

        # 下方：周数范围
        week_frame = tb.Frame(section_frame)
        week_frame.pack(fill=X)
        
        tb.Label(week_frame, text="周数范围:").pack(side=LEFT)
        
        week_input_frame = tb.Frame(week_frame)
        week_input_frame.pack(side=LEFT, padx=(10, 0))
        
        self.start_week = tb.Spinbox(week_input_frame, from_=1, to=20, 
                                width=5, font=("Helvetica", 10))
        self.start_week.set(1)
        self.start_week.pack(side=LEFT)
        
        tb.Label(week_input_frame, text=" 至 ").pack(side=LEFT)
        
        self.end_week = tb.Spinbox(week_input_frame, from_=1, to=20, 
                                width=5, font=("Helvetica", 10))
        self.end_week.set(16)
        self.end_week.pack(side=LEFT)
        
        tb.Label(week_input_frame, text=" 周").pack(side=LEFT)
    def create_type_color_section(self, parent):
        """创建类型和颜色选择部分"""
        section_frame = tb.LabelFrame(parent, text="课程样式", padding=8)
        section_frame.pack(fill=X, pady=3)

        # 类型选择
        type_frame = tb.Frame(section_frame)
        type_frame.pack(fill=X, pady=(0, 5))
        
        tb.Label(type_frame, text="课程类型:").pack(side=LEFT)
        
        type_btn_frame = tb.Frame(type_frame)
        type_btn_frame.pack(side=LEFT, padx=(10, 0))
        
        # 修改类型选项
        self.type_var = tb.StringVar(value="正常")
        types_row1 = [
            ("正常课程", "正常"),
            ("早签", "早签"),
            ("自习课", "自习课"),
            ("班会", "班会"),
            ("实验课", "实验课")
        ]
        types_row2 = [
            ("考试", "考试"),
            ("讲座", "讲座"),
            ("社团活动", "社团活动"),
            ("运动会", "运动会")
        ]

        # 第一行
        type_btn_row1 = tb.Frame(type_btn_frame)
        type_btn_row1.pack(side=TOP, pady=(0, 5))
        for text, value in types_row1:
            tb.Radiobutton(type_btn_row1, text=text, variable=self.type_var, 
                        value=value, command=self.update_type_preview).pack(side=LEFT, padx=(0, 10))

        # 第二行
        type_btn_row2 = tb.Frame(type_btn_frame)
        type_btn_row2.pack(side=TOP)
        for text, value in types_row2:
            tb.Radiobutton(type_btn_row2, text=text, variable=self.type_var, 
                        value=value, command=self.update_type_preview).pack(side=LEFT, padx=(0, 10))

        # 类型预览
        self.type_preview = tb.Label(section_frame, text="普通课程", 
                                   font=("Helvetica", 9), bootstyle=SECONDARY)
        self.type_preview.pack(fill=X, pady=(0, 5))

        # 颜色选择
        color_frame = tb.Frame(section_frame)
        color_frame.pack(fill=X)
        
        tb.Label(color_frame, text="课程颜色:").pack(side=LEFT)
        
        color_btn_frame = tb.Frame(color_frame)
        color_btn_frame.pack(side=LEFT, padx=(10, 0))
        
        colors = [
            ("#007bff", "蓝"),  # primary
            ("#28a745", "绿"),  # success
            ("#ffc107", "黄"),  # warning
            ("#dc3545", "红"),  # danger
            ("#17a2b8", "青"),  # info
            ("#6c757d", "灰")   # secondary
        ]
        self.color_var = tb.StringVar(value=colors[0][0])

        for color, name in colors:
            btn = tb.Button(color_btn_frame, text=name, 
                        bootstyle=INFO,  # 使用统一的INFO样式
                        command=lambda c=color: self.on_color_select(c),
                        width=4)
            btn.pack(side=LEFT, padx=1)
            # 为每个按钮设置对应的背景色
            btn.configure(style=f"Color.{color}.TButton")
            # 创建并配置按钮样式
            style = tb.Style()
            style.configure(f"Color.{color}.TButton", 
                        background=color,
                        foreground='white' if color in ["#007bff", "#28a745", "#dc3545", "#17a2b8", "#6c757d"] else 'black')

    def create_day_section(self, parent):
        """创建星期选择部分"""
        section_frame = tb.LabelFrame(parent, text="上课星期", padding=8)
        section_frame.pack(fill=X, pady=3)

        day_frame = tb.Frame(section_frame)
        day_frame.pack(fill=X)
        
        self.day_var = tb.IntVar(value=1)
        
        # 创建两行按钮布局
        row1_frame = tb.Frame(day_frame)
        row1_frame.pack(fill=X, pady=2)
        row2_frame = tb.Frame(day_frame)
        row2_frame.pack(fill=X, pady=2)
        
        days_config = [
            (row1_frame, 1, "周一"), (row1_frame, 2, "周二"), (row1_frame, 3, "周三"),
            (row1_frame, 4, "周四"), (row2_frame, 5, "周五"), (row2_frame, 6, "周六"),
            (row2_frame, 7, "周日")
        ]
        
        for frame, value, text in days_config:
            tb.Radiobutton(frame, text=text, variable=self.day_var, 
                         value=value, width=6).pack(side=LEFT, padx=2)

    def create_button_area(self, parent):
        """创建按钮区域"""
        btn_frame = tb.Frame(parent)
        btn_frame.pack(fill=X, pady=5)

        # 添加一些间距和分隔线
        separator = tb.Separator(btn_frame, orient=HORIZONTAL)
        separator.pack(fill=X, pady=3)

        btn_inner_frame = tb.Frame(btn_frame)
        btn_inner_frame.pack(fill=X)

        tb.Button(btn_inner_frame, text="取消", command=self.dialog.destroy,
                 bootstyle=(SECONDARY, OUTLINE), width=10).pack(side=RIGHT, padx=5)
        tb.Button(btn_inner_frame, text="保存课程", command=self.save_course,
                 bootstyle=SUCCESS, width=10).pack(side=RIGHT, padx=5)

    def update_time_preview(self, event=None):
        """更新时间预览"""
        time_index = self.start_time.current()
        if time_index >= 0:
            start_time, end_time = self.app.time_slots[time_index]
            preview_text = f"上课时间: {start_time} - {end_time}"
            self.time_preview.config(text=preview_text, bootstyle=SUCCESS)

    def update_type_preview(self):
        """更新类型预览"""
        course_type = self.type_var.get()
        if course_type == "正常":
            preview_text = "普通课程 - 按正常课表安排"
            style = SUCCESS
        else:
            # 特殊课程类型
            if course_type in SpecialCourse.TYPES:
                duration = SpecialCourse.TYPES[course_type]["duration"]
                preview_text = f"{course_type} - 时长{duration}分钟"
                style = INFO
            else:
                preview_text = "特殊课程"
                style = INFO
        
        self.type_preview.config(text=preview_text, bootstyle=style)

    def on_color_select(self, color):
        """处理颜色选择"""
        self.color_var.set(color)

    def validate_inputs(self):
        """验证所有输入字段"""
        course_data = (
            self.name_entry.get().strip(),
            self.teacher_entry.get().strip(),
            self.location_entry.get().strip(),
            self.start_week.get(),
            self.end_week.get()
        )
        return DataValidator.validate_course_data(course_data)

    def save_course(self):
        """保存课程信息"""
        if not self.app.current_semester:
            messagebox.showerror("错误", "请先创建学期")
            return
            
        # 验证输入
        errors = self.validate_inputs()
        if errors:
            logger.warning(f"课程验证失败: {errors}")
            messagebox.showerror("输入错误", "\n".join(errors))
            return
            
        try:
            # 获取时间选择
            time_index = self.start_time.current()
            start_time, end_time = self.app.time_slots[time_index]
            
            # 获取课程类型
            course_type = self.type_var.get()
            is_special = "1" if course_type != "正常" else "0"
            
            # 根据课程类型获取颜色
            if course_type in SpecialCourse.TYPES:
                color = SpecialCourse.TYPES[course_type]["color"]
            else:
                color = self.color_var.get()
            
            # 准备课程数据
            course_data = (
                self.name_entry.get().strip(),
                self.teacher_entry.get().strip(),
                self.location_entry.get().strip(),
                self.start_week.get(),
                self.end_week.get(),
                str(self.day_var.get()),
                start_time,
                end_time,
                color,
                course_type,
                is_special,
                str(self.app.current_semester[0])
            )

            logger.info(f"准备保存课程: {course_data[0]}")
            # 保存到数据库
            self.app.course_manager.add_course(course_data)
            
            # 更新界面
            self.app.load_courses()
            self.app.update_display()
            
            # 关闭对话框并提示成功
            self.dialog.destroy()
            logger.info(f"课程保存成功: {course_data[0]}")
            messagebox.showinfo("成功", "课程添加成功！")

        except Exception as e:
            logger.error(f"添加课程失败: {str(e)}")
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
        self.dialog.geometry("500x430")
        self.dialog.transient(self.parent)
        self.dialog.grab_set()

        main_frame = tb.Frame(self.dialog, padding=20)
        main_frame.pack(fill=BOTH, expand=True)

        # 学期类型选择
        tb.Label(main_frame, text="学期类型:", font=("Helvetica", 12)).pack(anchor="w", pady=(10, 5))
        self.semester_type = tb.Combobox(main_frame, 
                                   values=["秋季", "春季"],
                                   state="readonly",
                                   font=("Helvetica", 11))
        self.semester_type.pack(fill="x", pady=(0, 15))
        self.semester_type.set("秋季")
        self.semester_type.bind('<<ComboboxSelected>>', lambda e: self.update_semester_name())

        # 学期名称
        tb.Label(main_frame, text="学期名称:", font=("Helvetica", 12)).pack(anchor="w", pady=(10, 5))
        self.name_entry = tb.Entry(main_frame, font=("Helvetica", 11))
        self.name_entry.pack(fill="x", pady=(0, 15))
        self.name_entry.insert(0, self.generate_semester_name())
        self.name_entry.config(state="readonly")

        # 日期选择框架
        date_frame = tb.Frame(main_frame)
        date_frame.pack(fill="x", pady=20)

        # 开始日期
        start_frame = tb.Frame(date_frame)
        start_frame.pack(fill="x", pady=(0, 15))
        tb.Label(start_frame, text="开始日期:", font=("Helvetica", 12)).pack(side=LEFT)
        self.start_date = tb.DateEntry(start_frame, bootstyle="primary", 
                                    dateformat="%Y-%m-%d")
        self.start_date.pack(side=LEFT, padx=10)

        # 结束日期
        end_frame = tb.Frame(date_frame)
        end_frame.pack(fill="x", pady=(0, 15))
        tb.Label(end_frame, text="结束日期:", font=("Helvetica", 12)).pack(side=LEFT)
        self.end_date = tb.DateEntry(end_frame, bootstyle="primary",
                                dateformat="%Y-%m-%d")
        self.end_date.pack(side=LEFT, padx=10)

        # 按钮
        btn_frame = tb.Frame(main_frame)
        btn_frame.pack(fill="x", pady=0)
        
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
            # 更新当前学期为新建的学期
            new_semester = self.app.semesters[-1]
            self.app.course_manager.set_current_semester(new_semester[0])
            self.app.current_semester = new_semester
            
            # 重新加载课程并更新显示
            self.app.load_courses()
            self.app.update_display()
            
            self.dialog.destroy()
            messagebox.showinfo("成功", "学期创建成功！")
            
        except ValueError as ve:
            messagebox.showerror("错误", str(ve))
class EditCourseDialog(AddCourseDialog):
    def __init__(self, parent, app, course):
        self.course = course
        super().__init__(parent, app)
        self.dialog.title("编辑课程")
        self.load_course_data()

    def load_course_data(self):
        """加载课程数据到表单"""
        try:
            # 基本信息
            self.name_entry.insert(0, self.course[1])
            self.teacher_entry.insert(0, self.course[2])
            self.location_entry.insert(0, self.course[3])
            
            # 时间设置
            time_str = f"{self.course[7]}-{self.course[8]}"
            self.start_time.set(time_str)
            self.start_week.set(self.course[4])
            self.end_week.set(self.course[5])
            
            # 星期设置
            self.day_var.set(self.course[6])
            
            # 课程类型和颜色
            self.type_var.set("调休" if self.course[11] else "正常")
            self.color_var.set(self.course[9])
            
            # 更新预览
            self.update_time_preview()
            self.update_type_preview()
        except Exception as e:
            logger.error(f"加载课程数据失败: {str(e)}")
            raise

    def save_course(self):
        """保存课程信息"""
        if not self.app.current_semester:
            messagebox.showerror("错误", "请先创建学期")
            return

        # 验证输入
        errors = self.validate_inputs()
        if errors:
            logger.warning(f"课程验证失败: {errors}")
            messagebox.showerror("输入错误", "\n".join(errors))
            return

        try:
            # 获取时间选择
            time_index = self.start_time.current()
            start_time, end_time = self.app.time_slots[time_index]
            
            # 获取课程类型
            course_type = self.type_var.get()
            is_special = "1" if course_type != "正常" else "0"
            
            # 根据课程类型获取颜色
            if course_type in SpecialCourse.TYPES:
                color = SpecialCourse.TYPES[course_type]["color"]
            else:
                color = self.color_var.get()
            
            # 准备课程数据
            course_data = (
                self.name_entry.get().strip(),
                self.teacher_entry.get().strip(),
                self.location_entry.get().strip(),
                self.start_week.get(),
                self.end_week.get(),
                str(self.day_var.get()),
                start_time,
                end_time,
                color,
                course_type,
                is_special,
                str(self.app.current_semester[0])
            )

            logger.info(f"准备更新课程: {course_data[0]}")
            # 更新数据库
            self.app.course_manager.update_course(self.course[0], course_data)
            
            # 更新界面
            self.app.load_courses()
            self.app.update_display()
            
            # 关闭对话框并提示成功
            self.dialog.destroy()
            logger.info(f"课程更新成功: {course_data[0]}")
            messagebox.showinfo("成功", "课程更新成功！")

        except Exception as e:
            logger.error(f"更新课程失败: {str(e)}")
            messagebox.showerror("错误", f"更新课程失败: {str(e)}")
class EditSemesterDialog:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.create_dialog()

    def create_dialog(self):
        """创建修改学期对话框"""
        self.dialog = tb.Toplevel(self.parent)
        self.dialog.title("修改学期")
        self.dialog.geometry("500x530")
        self.dialog.transient(self.parent)
        self.dialog.grab_set()

        main_frame = tb.Frame(self.dialog, padding=20)
        main_frame.pack(fill=BOTH, expand=True)

        # 学期选择
        tb.Label(main_frame, text="选择学期:", font=("Helvetica", 12)).pack(anchor="w", pady=(10, 5))
        self.semester_combo = tb.Combobox(main_frame, 
                                   values=[s[1] for s in self.app.semesters],
                                   state="readonly",
                                   font=("Helvetica", 11))
        self.semester_combo.pack(fill="x", pady=(0, 15))
        if self.app.current_semester:
            self.semester_combo.set(self.app.current_semester[1])
        self.semester_combo.bind('<<ComboboxSelected>>', self.on_semester_select)

        # 学期类型
        tb.Label(main_frame, text="学期类型:", font=("Helvetica", 12)).pack(anchor="w", pady=(10, 5))
        self.semester_type = tb.Combobox(main_frame, 
                                   values=["秋季", "春季"],
                                   state="readonly",
                                   font=("Helvetica", 11))
        self.semester_type.pack(fill="x", pady=(0, 15))
        self.semester_type.bind('<<ComboboxSelected>>', self.update_semester_name)

        # 学期名称
        tb.Label(main_frame, text="学期名称:", font=("Helvetica", 12)).pack(anchor="w", pady=(10, 5))
        self.name_entry = tb.Entry(main_frame, font=("Helvetica", 11))
        self.name_entry.pack(fill="x", pady=(0, 15))

        # 日期选择框架
        date_frame = tb.Frame(main_frame)
        date_frame.pack(fill="x", pady=20)

        # 开始日期
        start_frame = tb.Frame(date_frame)
        start_frame.pack(fill="x", pady=(0, 15))
        tb.Label(start_frame, text="开始日期:", font=("Helvetica", 12)).pack(side=LEFT)
        self.start_date = tb.DateEntry(start_frame, bootstyle="primary", 
                                    dateformat="%Y-%m-%d")
        self.start_date.pack(side=LEFT, padx=10)

        # 结束日期
        end_frame = tb.Frame(date_frame)
        end_frame.pack(fill="x", pady=(0, 15))
        tb.Label(end_frame, text="结束日期:", font=("Helvetica", 12)).pack(side=LEFT)
        self.end_date = tb.DateEntry(end_frame, bootstyle="primary",
                                dateformat="%Y-%m-%d")
        self.end_date.pack(side=LEFT, padx=10)

        # 按钮
        btn_frame = tb.Frame(main_frame)
        btn_frame.pack(fill="x", pady=0)
        
        tb.Button(btn_frame, text="取消", command=self.dialog.destroy,
                bootstyle=(SECONDARY, OUTLINE), width=10).pack(side="right", padx=5)
        tb.Button(btn_frame, text="保存", command=self.save_semester,
                bootstyle=(SUCCESS, OUTLINE), width=10).pack(side="right", padx=5)

        # 加载选中学期数据
        self.on_semester_select()

    def on_semester_select(self, event=None):
        """处理学期选择事件"""
        selected_name = self.semester_combo.get()
        for semester in self.app.semesters:
            if semester[1] == selected_name:
                self.current_semester = semester
                self.name_entry.delete(0, tb.END)
                self.name_entry.insert(0, semester[1])
                self.start_date.entry.delete(0, tb.END)
                self.start_date.entry.insert(0, semester[2])
                self.end_date.entry.delete(0, tb.END)
                self.end_date.entry.insert(0, semester[3])
                break

    def update_semester_name(self):
        """更新学期名称"""
        current_year = datetime.now().year
        semester_type = self.semester_type.get()
        
        if semester_type == "秋季":
            new_name = f"{current_year}年秋季学期"
        else:
            new_name = f"{current_year + 1}年春季学期"
            
        self.name_entry.delete(0, tb.END)
        self.name_entry.insert(0, new_name)

    def save_semester(self):
        """保存学期修改"""
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
                    
            # 更新数据库
            self.app.course_manager.update_semester(
                self.current_semester[0],  # semester_id
                name,  # name
                start,  # start_date
                end     # end_date
            )
            
            # 更新本地数据
            self.app.semesters = self.app.course_manager.get_semesters()
            if self.current_semester[0] == self.app.current_semester[0]:
                self.app.current_semester = (
                    self.current_semester[0],
                    name,
                    start,
                    end,
                    self.current_semester[4]
                )
            
            # 重新加载课程并更新显示
            self.app.load_courses()
            self.app.update_display()
            
            self.dialog.destroy()
            messagebox.showinfo("成功", "学期修改成功！")
            
        except ValueError as ve:
            messagebox.showerror("错误", str(ve))
        except Exception as e:
            messagebox.showerror("错误", f"修改学期失败: {str(e)}")
class ShareDialog:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.create_dialog()

    def create_dialog(self):
        """创建分享对话框"""
        self.dialog = tb.Toplevel(self.parent)
        self.dialog.title("分享课程")
        self.dialog.geometry("400x480")
        self.dialog.transient(self.parent)
        self.dialog.grab_set()

        main_frame = tb.Frame(self.dialog, padding=20)
        main_frame.pack(fill=BOTH, expand=True)

        # 分享类型选择
        type_frame = tb.LabelFrame(main_frame, text="分享类型", padding=10)
        type_frame.pack(fill=X, pady=10)

        self.share_type = tb.StringVar(value="week")
        types = [
            ("周课程表", "week"),
            ("单日课程", "day")
        ]
        
        for text, value in types:
            tb.Radiobutton(type_frame, text=text, variable=self.share_type,
                        value=value).pack(anchor="w", pady=2)

        # 导出格式选择
        format_frame = tb.LabelFrame(main_frame, text="导出格式", padding=10)
        format_frame.pack(fill=X, pady=10)

        self.export_format = tb.StringVar(value="image")
        formats = [
            ("图片 (.png)", "image"),
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
        
        tb.Button(btn_frame, text="取消", command=self.dialog.destroy,
                bootstyle=(SECONDARY, OUTLINE)).pack(side=RIGHT, padx=5)
        tb.Button(btn_frame, text="分享", command=self.do_share,
                bootstyle=SUCCESS).pack(side=RIGHT, padx=5)

    def do_share(self):
        """执行分享操作"""
        try:
            share_type = self.share_type.get()
            export_format = self.export_format.get()
            filename = self.filename_entry.get().strip()
            
            # 获取当前显示的课程
            if share_type == "week":
                courses = self.app.course_manager.get_courses_by_week(self.app.current_week)
                target_date = None
            else:
                current_date = datetime.now()
                if self.app.current_view == "month":
                    current_date = self.app.month_view.current_date
                day = current_date.weekday() + 1
                week = ((current_date - datetime.strptime(self.app.current_semester[2], "%Y-%m-%d")).days // 7) + 1
                courses = self.app.course_manager.get_courses_by_day(day, week)
                target_date = current_date
            
            if not courses:
                messagebox.showwarning("提示", "没有可分享的课程")
                return
                
            # 执行导出
            if self.app.course_manager.export_courses(courses, export_format, filename, share_type, target_date):
                messagebox.showinfo("成功", "课程分享成功！")
                self.dialog.destroy()
            else:
                messagebox.showerror("错误", "课程分享失败")
        except Exception as e:
            logger.error(f"分享课程失败: {str(e)}")
            messagebox.showerror("错误", f"分享失败: {str(e)}")
class StudyReportDialog:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.create_dialog()

    def create_dialog(self):
        """创建学习报告对话框"""
        self.dialog = tb.Toplevel(self.parent)
        self.dialog.title("学期学习报告")
        self.dialog.geometry("800x800")
        self.dialog.transient(self.parent)
        self.dialog.grab_set()

        main_frame = tb.Frame(self.dialog, padding=20)
        main_frame.pack(fill=BOTH, expand=True)

        # 创建滚动区域
        canvas = tb.Canvas(main_frame)
        scrollbar = tb.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tb.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # 生成报告内容
        self.generate_report(scrollable_frame)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def generate_report(self, parent):
        """生成报告内容"""
        stats = self.app.course_manager.get_study_statistics(self.app.current_semester[0])
        
        # 标题
        title = tb.Label(parent, text=f"{self.app.current_semester[1]} 学习报告",
                        font=("Helvetica", 16, "bold"))
        title.pack(pady=10)
        
        # 总体统计
        self.create_overview_section(parent, stats)
        
        # 课程分布
        self.create_distribution_section(parent, stats)
        
        # 时间利用
        self.create_time_utilization_section(parent, stats)

    def create_overview_section(self, parent, stats):
        """创建概览部分"""
        frame = tb.LabelFrame(parent, text="学习概览", padding=10)
        frame.pack(fill=X, padx=10, pady=5)
        
        data = [
            ("总课程数", f"{stats['total_courses']} 门"),
            ("总学时", f"{stats['total_hours']:.1f} 小时"),
            ("平均每周", f"{stats['total_hours']/20:.1f} 小时"),
            ("平均每天", f"{stats['total_hours']/140:.1f} 小时")
        ]
        
        for label, value in data:
            item = tb.Frame(frame)
            item.pack(fill=X, pady=2)
            tb.Label(item, text=f"{label}:", width=15, anchor="w").pack(side=LEFT)
            tb.Label(item, text=value, bootstyle=INFO).pack(side=LEFT)

    def create_distribution_section(self, parent, stats):
        """创建课程分布部分"""
        frame = tb.LabelFrame(parent, text="课程分布", padding=10)
        frame.pack(fill=X, padx=10, pady=5)
        
        # 按类型分布
        type_frame = tb.Frame(frame)
        type_frame.pack(fill=X, pady=5)
        tb.Label(type_frame, text="按类型分布:", font=("Helvetica", 12, "bold")).pack(anchor="w")
        
        for course_type, data in stats['course_types'].items():
            item = tb.Frame(type_frame)
            item.pack(fill=X, pady=2)
            tb.Label(item, text=f"{course_type}:", width=15, anchor="w").pack(side=LEFT)
            tb.Label(item, text=f"{data['count']}门 ({data['hours']/stats['total_hours']*100:.1f}%)",
                    bootstyle=INFO).pack(side=LEFT)

    def create_time_utilization_section(self, parent, stats):
        """创建时间利用部分"""
        frame = tb.LabelFrame(parent, text="时间利用", padding=10)
        frame.pack(fill=X, padx=10, pady=5)
        
        # 每周学时分布
        week_frame = tb.Frame(frame)
        week_frame.pack(fill=X, pady=5)
        tb.Label(week_frame, text="每周学时分布:", font=("Helvetica", 12, "bold")).pack(anchor="w")
        
        week_text = " ".join([f"第{w}周:{h:.1f}h" for w, h in sorted(stats['weekly_hours'].items())])
        tb.Label(week_frame, text=week_text, wraplength=700).pack(anchor="w")
        
        # 每日学时分布
        day_frame = tb.Frame(frame)
        day_frame.pack(fill=X, pady=5)
        tb.Label(day_frame, text="每日学时分布:", font=("Helvetica", 12, "bold")).pack(anchor="w")
        
        days = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
        day_text = " ".join([f"{days[d-1]}:{h:.1f}h" for d, h in sorted(stats['daily_hours'].items())])
        tb.Label(day_frame, text=day_text, wraplength=700).pack(anchor="w")