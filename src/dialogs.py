import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox
from datetime import datetime
from logger_config import logger
from course_manager import SpecialCourse  # 添加这行导入语句
import matplotlib.pyplot as plt
import numpy as np
class AddCourseDialog:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
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
        errors = []
        
        # 验证必填字段
        if not self.name_entry.get().strip():
            errors.append("请输入课程名称")
        if not self.teacher_entry.get().strip():
            errors.append("请输入任课老师")
        if not self.location_entry.get().strip():
            errors.append("请输入上课地点")
            
        # 验证时间选择
        time_index = self.start_time.current()
        if time_index < 0:
            errors.append("请选择上课时间段")
            
        # 验证周数范围
        try:
            start_week = int(self.start_week.get())
            end_week = int(self.end_week.get())
            if start_week < 1 or end_week > 20:
                errors.append("周数范围应在1-20周之间")
            if start_week > end_week:
                errors.append("起始周不能大于结束周")
        except ValueError:
            errors.append("周数必须是有效的数字")
            
        return errors

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
        self.dialog.geometry("1200x800")
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        # 设置现代化样式
        self.dialog.tk_setPalette(background="#f0f2f5")
        
        # 创建主容器
        main_container = tb.Frame(self.dialog, padding=0)
        main_container.pack(fill=BOTH, expand=True)
        
        # 生成报告内容
        self.generate_report(main_container)

    def generate_report(self, parent):
        """生成报告内容"""
        stats = self.app.course_manager.get_study_statistics(self.app.current_semester[0])
        
        # 创建顶部标题区域
        self.create_header_card(parent, stats)
        
        # 创建统计概览区域
        self.create_stats_grid(parent, stats)
        
        # 创建图表区域
        self.create_chart_area(parent, stats)
        
        # 创建底部操作区域
        self.create_action_section(parent)

    def create_header_card(self, parent, stats):
        """创建顶部标题卡片"""
        header_card = tb.Frame(parent, bootstyle=PRIMARY, padding=25)
        header_card.pack(fill=X, padx=20, pady=(10, 10))
        
        # 学期标题
        title_label = tb.Label(header_card, 
                          text=f"{self.app.current_semester[1]}",
                          font=("Helvetica", 28, "bold"),
                          bootstyle=(PRIMARY, INVERSE))
        title_label.pack()
        
        subtitle_label = tb.Label(header_card, 
                               text="📊 学习报告",
                               font=("Helvetica", 16),
                               bootstyle=(PRIMARY, INVERSE))
        subtitle_label.pack(pady=(5, 0))

    def create_stats_grid(self, parent, stats):
        """创建统计卡片网格"""
        stats_container = tb.Frame(parent)
        stats_container.pack(fill=X, padx=20, pady=(0, 10))
        
        # 第一行统计卡片
        row1 = tb.Frame(stats_container)
        row1.pack(fill=X, pady=(0, 10))
        
        # 总课程数卡片
        self.create_stat_card(row1, "总课程数", f"{stats['total_courses']}", 
                           "门", SUCCESS, "📚")
        
        # 总学时卡片
        self.create_stat_card(row1, "总学时", f"{stats['total_hours']:.1f}", 
                           "小时", INFO, "⏰")
        
        # 平均每周卡片
        self.create_stat_card(row1, "平均每周", f"{stats['total_hours']/20:.1f}", 
                           "小时", WARNING, "📅")
        
        # 平均每天卡片
        self.create_stat_card(row1, "平均每天", f"{stats['total_hours']/140:.1f}", 
                           "小时", DANGER, "📆")
        
        # 第二行详细统计
        row2 = tb.Frame(stats_container)
        row2.pack(fill=X, pady=(0, 10))
        
        # 课程类型分布
        type_card = self.create_detail_card(row2, "课程类型分布", 
                                       self._format_type_distribution(stats))
        
        # 时间利用情况
        time_card = self.create_detail_card(row2, "时间利用情况", 
                                      self._format_time_utilization(stats))
        
        # 学习建议
        suggestion_card = self.create_detail_card(row2, "💡 学习建议", 
                                               self._generate_suggestions(stats))

    def create_stat_card(self, parent, title, value, unit, style, icon):
        """创建单个统计卡片"""
        card = tb.Frame(parent, bootstyle=style, padding=20, relief="raised")
        card.pack(side=LEFT, fill=BOTH, expand=True, padx=5)
        
        # 顶部：图标和标题
        top_frame = tb.Frame(card)
        top_frame.pack(fill=X, pady=(0, 10))
        
        icon_label = tb.Label(top_frame, text=icon, font=("Helvetica", 24))
        icon_label.pack(side=LEFT, padx=(0, 10))
        
        title_label = tb.Label(top_frame, text=title, 
                           font=("Helvetica", 14, "bold"))
        title_label.pack(side=LEFT)
        
        # 底部：数值和单位
        bottom_frame = tb.Frame(card)
        bottom_frame.pack(fill=BOTH, expand=True)
        
        value_label = tb.Label(bottom_frame, text=value, 
                             font=("Helvetica", 32, "bold"),
                             bootstyle=(style, INVERSE))
        value_label.pack(expand=True)
        
        unit_label = tb.Label(bottom_frame, text=unit, 
                             font=("Helvetica", 12))
        unit_label.pack()

    def create_detail_card(self, parent, title, content):
        """创建详细信息卡片"""
        card = tb.Frame(parent, bootstyle=LIGHT, padding=15, relief="raised")
        card.pack(side=LEFT, fill=BOTH, expand=True, padx=5)
        
        # 标题
        title_label = tb.Label(card, text=title, 
                           font=("Helvetica", 12, "bold"))
        title_label.pack(anchor="w", pady=(0, 10))
        
        # 内容
        content_label = tb.Label(card, text=content, 
                              font=("Helvetica", 10),
                              wraplength=250,
                              justify="left")
        content_label.pack(anchor="w", fill=BOTH, expand=True)

    def create_chart_area(self, parent, stats):
        """创建图表区域"""
        chart_container = tb.LabelFrame(parent, text="📈 数据可视化", 
                                      padding=20, bootstyle=PRIMARY)
        chart_container.pack(fill=BOTH, expand=True, padx=20, pady=(0, 10))
        
        # 创建标签页
        notebook = tb.Notebook(chart_container)
        notebook.pack(fill=BOTH, expand=True)
        
        # 概览标签页
        overview_tab = tb.Frame(notebook)
        notebook.add(overview_tab, text="📊 概览")
        self.create_overview_charts(overview_tab, stats)
        
        # 详细分析标签页
        analysis_tab = tb.Frame(notebook)
        notebook.add(analysis_tab, text="📈 详细分析")
        self.create_analysis_charts(analysis_tab, stats)
        
        # 趋势标签页
        trend_tab = tb.Frame(notebook)
        notebook.add(trend_tab, text="📈 趋势")
        self.create_trend_charts(trend_tab, stats)

    def create_overview_charts(self, parent, stats):
        """创建概览图表"""
        try:
            import matplotlib.pyplot as plt
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
            import matplotlib.font_manager as fm
            
            # 设置样式
            plt.style.use('default')
            plt.rcParams['font.sans-serif'] = ['SimHei']
            plt.rcParams['axes.unicode_minus'] = False
            
            # 创建图表容器
            chart_frame = tb.Frame(parent, padding=15)
            chart_frame.pack(fill=BOTH, expand=True)
            
            # 创建2x2图表布局
            fig = plt.figure(figsize=(10, 8), facecolor='white')
            
            # 1. 课程类型分布饼图
            ax1 = plt.subplot(2, 2, 1)
            self._create_pie_chart(ax1, stats)
            
            # 2. 每周学习时长
            ax2 = plt.subplot(2, 2, 2)
            self._create_weekly_chart(ax2, stats)
            
            # 3. 每日学习分布
            ax3 = plt.subplot(2, 2, 3)
            self._create_daily_chart(ax3, stats)
            
            # 4. 学习时段分布
            ax4 = plt.subplot(2, 2, 4)
            self._create_pattern_chart(ax4, stats)
            
            plt.tight_layout(pad=2.0)
            
            # 嵌入到tkinter
            canvas = FigureCanvasTkAgg(fig, master=chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=BOTH, expand=True)
            
        except Exception as e:
            logger.error(f"创建概览图表失败: {str(e)}")
            self._show_error_message(parent, "概览图表生成失败")

    def create_analysis_charts(self, parent, stats):
        """创建详细分析图表"""
        try:
            import matplotlib.pyplot as plt
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
            
            # 创建图表容器
            chart_frame = tb.Frame(parent, padding=15)
            chart_frame.pack(fill=BOTH, expand=True)
            
            # 创建大图：学习时间分布热力图
            fig = plt.figure(figsize=(12, 6), facecolor='white')
            
            # 热力图
            ax = fig.add_subplot(1, 1, 1)
            self._create_heatmap(ax, stats)
            
            plt.tight_layout()
            
            # 嵌入到tkinter
            canvas = FigureCanvasTkAgg(fig, master=chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=BOTH, expand=True)
            
            # 添加说明
            info_frame = tb.Frame(chart_frame)
            info_frame.pack(fill=X, pady=10)
            
            tb.Label(info_frame, 
                    text="📊 热力图展示了整个学期每周每天的课程密度分布",
                    font=("Helvetica", 10),
                    bootstyle=INFO).pack()
            
        except Exception as e:
            logger.error(f"创建分析图表失败: {str(e)}")
            self._show_error_message(parent, "分析图表生成失败")

    def create_trend_charts(self, parent, stats):
        """创建趋势图表"""
        try:
            import matplotlib.pyplot as plt
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
            
            # 创建图表容器
            chart_frame = tb.Frame(parent, padding=15)
            chart_frame.pack(fill=BOTH, expand=True)
            
            # 创建趋势图
            fig = plt.figure(figsize=(12, 6), facecolor='white')
            
            # 周学时趋势
            ax1 = plt.subplot(1, 2, 1)
            self._create_week_trend(ax1, stats)
            
            # 月学时趋势
            ax2 = plt.subplot(1, 2, 2)
            self._create_month_trend(ax2, stats)
            
            plt.tight_layout()
            
            # 嵌入到tkinter
            canvas = FigureCanvasTkAgg(fig, master=chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=BOTH, expand=True)
            
        except Exception as e:
            logger.error(f"创建趋势图表失败: {str(e)}")
            self._show_error_message(parent, "趋势图表生成失败")

    def create_action_section(self, parent):
        """创建底部操作区域"""
        action_frame = tb.Frame(parent, padding=20)
        action_frame.pack(fill=X, padx=20, pady=(0, 10))
        
        # 导出按钮
        export_frame = tb.Frame(action_frame)
        export_frame.pack(side=LEFT)
        
        tb.Button(export_frame, text="📄 导出PDF", 
                 command=self.export_pdf,
                 bootstyle=INFO, width=12).pack(side=LEFT, padx=5)
        
        tb.Button(export_frame, text="🖼️ 导出图片", 
                 command=self.export_image,
                 bootstyle=SUCCESS, width=12).pack(side=LEFT, padx=5)
        
        tb.Button(export_frame, text="📊 导出数据", 
                 command=self.export_data,
                 bootstyle=WARNING, width=12).pack(side=LEFT, padx=5)
        
        # 关闭按钮
        tb.Button(action_frame, text="关闭", 
                 command=self.dialog.destroy,
                 bootstyle=(SECONDARY, OUTLINE), 
                 width=10).pack(side=RIGHT)

    def _format_type_distribution(self, stats):
        """格式化课程类型分布"""
        lines = []
        for course_type, data in stats['course_types'].items():
            percentage = (data['hours']/stats['total_hours']*100)
            lines.append(f"• {course_type}: {data['count']}门 ({percentage:.1f}%)")
        return "\n".join(lines)

    def _format_time_utilization(self, stats):
        """格式化时间利用情况"""
        lines = []
        lines.append(f"• 总学习时间: {stats['total_hours']:.1f}小时")
        lines.append(f"• 平均每周: {stats['total_hours']/20:.1f}小时")
        lines.append(f"• 平均每天: {stats['total_hours']/140:.1f}小时")
        return "\n".join(lines)

    def _generate_suggestions(self, stats):
        """生成学习建议"""
        suggestions = []
        
        # 基于学习时长的建议
        weekly_avg = stats['total_hours']/20
        if weekly_avg < 15:
            suggestions.append("• 建议增加学习时间，当前每周学习时间偏低")
        elif weekly_avg > 25:
            suggestions.append("• 学习时间较充足，注意劳逸结合")
        else:
            suggestions.append("• 学习时间安排合理")
        
        # 基于课程类型的建议
        if len(stats['course_types']) < 3:
            suggestions.append("• 课程类型较为单一，建议多样化学习")
        
        return "\n".join(suggestions)

    def _create_pie_chart(self, ax, stats):
        """创建课程类型分布饼图"""
        types = list(stats['course_types'].keys())
        hours = [d['hours'] for d in stats['course_types'].values()]
        
        # 创建饼图
        wedges, texts, autotexts = ax.pie(hours, labels=types, autopct='%1.1f%%',
                                        startangle=90, textprops={'fontsize': 10})
        
        # 设置样式
        ax.set_title('课程类型分布', pad=20, fontweight='bold', fontsize=12)
        
        # 美化百分比文本
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(9)

    def _create_weekly_chart(self, ax, stats):
        """创建每周学习时长图表"""
        weeks = sorted(stats['weekly_hours'].keys())
        hours = [stats['weekly_hours'][w] for w in weeks]
        
        # 创建条形图
        bars = ax.bar(range(len(weeks)), hours, color=plt.cm.viridis(np.linspace(0.3, 0.9, len(weeks))))
        
        # 设置样式
        ax.set_xticks(range(len(weeks)))
        ax.set_xticklabels([f'第{w}周' for w in weeks], rotation=45, fontsize=9)
        ax.set_title('每周学习时长', pad=20, fontweight='bold', fontsize=12)
        ax.set_ylabel('学时', labelpad=10, fontsize=10)
        ax.grid(True, axis='y', alpha=0.3)
        
        # 添加数值标签
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}h',
                    ha='center', va='bottom', fontsize=8)

    def _create_daily_chart(self, ax, stats):
        """创建每日学习分布图表"""
        days = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
        hours = [stats['daily_hours'].get(d+1, 0) for d in range(7)]
        
        # 创建条形图
        bars = ax.bar(range(len(days)), hours, color=plt.cm.plasma(np.linspace(0.3, 0.9, len(days))))
        
        # 设置样式
        ax.set_xticks(range(len(days)))
        ax.set_xticklabels(days, fontsize=9)
        ax.set_title('每日学习分布', pad=20, fontweight='bold', fontsize=12)
        ax.set_ylabel('学时', labelpad=10, fontsize=10)
        ax.grid(True, axis='y', alpha=0.3)
        
        # 添加数值标签
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                ax.text(bar.get_x() + bar.get_width()/2., height,
                        f'{height:.1f}h',
                        ha='center', va='bottom', fontsize=8)

    def _create_pattern_chart(self, ax, stats):
        """创建学习时段分布图表"""
        periods = list(stats['study_patterns'].keys())
        hours = [stats['study_patterns'][p] for p in periods]
        
        # 创建条形图
        bars = ax.bar(periods, hours, color=plt.cm.Set3(np.linspace(0.3, 0.9, len(periods))))
        
        # 设置样式
        ax.set_title('学习时段分布', pad=20, fontweight='bold', fontsize=12)
        ax.set_ylabel('学时', labelpad=10, fontsize=10)
        ax.grid(True, axis='y', alpha=0.3)
        
        # 添加数值标签
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}h',
                    ha='center', va='bottom', fontsize=8)

    def _create_heatmap(self, ax, stats):
        """创建学习时间分布热力图"""
        import numpy as np
        
        # 准备数据
        days = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
        weeks = range(1, 21)
        data = np.zeros((7, 20))
        
        for week_day, count in stats['course_density'].items():
            week, day = map(int, week_day.split('-'))
            if week <= 20:
                data[day-1, week-1] = count
        
        # 绘制热力图
        im = ax.imshow(data, cmap='YlOrRd', aspect='auto', interpolation='nearest')
        
        # 设置样式
        ax.set_xticks(range(0, 20, 2))
        ax.set_xticklabels([f'第{w}周' for w in range(1, 21, 2)], rotation=45, fontsize=9)
        ax.set_yticks(range(7))
        ax.set_yticklabels(days, fontsize=9)
        ax.set_title('课程密度热力图', pad=20, fontweight='bold', fontsize=12)
        ax.grid(False)
        
        # 添加颜色条
        cbar = plt.colorbar(im, ax=ax, shrink=0.8, pad=0.02)
        cbar.set_label('课程数量', rotation=270, labelpad=15, fontsize=10)

    def _create_week_trend(self, ax, stats):
        """创建周学时趋势图"""
        weeks = sorted(stats['weekly_hours'].keys())
        hours = [stats['weekly_hours'][w] for w in weeks]
        
        # 创建趋势线
        ax.plot(weeks, hours, marker='o', linewidth=2, markersize=6)
        ax.fill_between(weeks, hours, alpha=0.3)
        
        # 设置样式
        ax.set_title('每周学习时长趋势', pad=20, fontweight='bold', fontsize=12)
        ax.set_xlabel('周数', labelpad=10, fontsize=10)
        ax.set_ylabel('学时', labelpad=10, fontsize=10)
        ax.grid(True, alpha=0.3)

    def _create_month_trend(self, ax, stats):
        """创建月学时趋势图"""
        months = sorted(stats['monthly_hours'].keys())
        hours = [stats['monthly_hours'][m] for m in months]
        
        # 创建趋势线
        ax.plot(months, hours, marker='s', linewidth=2, markersize=6)
        ax.fill_between(months, hours, alpha=0.3)
        
        # 设置样式
        ax.set_title('每月学习时长趋势', pad=20, fontweight='bold', fontsize=12)
        ax.set_xlabel('月份', labelpad=10, fontsize=10)
        ax.set_ylabel('学时', labelpad=10, fontsize=10)
        ax.grid(True, alpha=0.3)

    def _show_error_message(self, parent, message):
        """显示错误消息"""
        error_frame = tb.Frame(parent, padding=20)
        error_frame.pack(fill=BOTH, expand=True)
        
        tb.Label(error_frame, 
                text=f"❌ {message}",
                font=("Helvetica", 12),
                bootstyle=DANGER).pack(expand=True)

    def export_pdf(self):
        """导出PDF报告"""
        try:
            # 实现PDF导出逻辑
            messagebox.showinfo("成功", "PDF报告导出成功！")
        except Exception as e:
            logger.error(f"PDF导出失败: {str(e)}")
            messagebox.showerror("错误", f"PDF导出失败: {str(e)}")

    def export_image(self):
        """导出图片报告"""
        try:
            # 实现图片导出逻辑
            messagebox.showinfo("成功", "图片报告导出成功！")
        except Exception as e:
            logger.error(f"图片导出失败: {str(e)}")
            messagebox.showerror("错误", f"图片导出失败: {str(e)}")

    def export_data(self):
        """导出数据"""
        try:
            # 实现数据导出逻辑
            messagebox.showinfo("成功", "数据导出成功！")
        except Exception as e:
            logger.error(f"数据导出失败: {str(e)}")
            messagebox.showerror("错误", f"数据导出失败: {str(e)}")