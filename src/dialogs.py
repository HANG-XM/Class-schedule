import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox
from datetime import datetime
from logger_config import logger
from course_manager import SpecialCourse  # 添加这行导入语句
class AddCourseDialog:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.create_dialog()

    def create_dialog(self):
        """创建添加课程对话框"""
        self.dialog = tb.Toplevel(self.parent)
        self.dialog.title("添加课程")
        self.dialog.geometry("590x720")  # 调整窗口大小
        self.dialog.resizable(False, False)
        self.dialog.transient(self.parent)
        self.dialog.grab_set()

        # 创建主容器
        main_frame = tb.Frame(self.dialog, padding=10)
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

    def create_basic_info_section(self, parent):
        """创建基本信息部分"""
        section_frame = tb.LabelFrame(parent, text="基本信息", padding=10)
        section_frame.pack(fill=X, pady=5)

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
        section_frame = tb.LabelFrame(parent, text="时间安排", padding=10)
        section_frame.pack(fill=X, pady=5)

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
        section_frame = tb.LabelFrame(parent, text="课程样式", padding=10)
        section_frame.pack(fill=X, pady=5)

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
            ("primary", "蓝"), ("success", "绿"), ("warning", "黄"),
            ("danger", "红"), ("info", "青"), ("secondary", "灰")
        ]
        self.color_var = tb.StringVar(value=colors[0][0])

        for color, name in colors:
            btn = tb.Button(color_btn_frame, text=name, bootstyle=color, 
                        command=lambda c=color: self.on_color_select(c),
                        width=4)  # 将宽度从6改为4
            btn.pack(side=LEFT, padx=1)  # 将间距从2改为1

    def create_day_section(self, parent):
        """创建星期选择部分"""
        section_frame = tb.LabelFrame(parent, text="上课星期", padding=10)
        section_frame.pack(fill=X, pady=5)

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
        btn_frame.pack(fill=X, pady=10)

        # 添加一些间距和分隔线
        separator = tb.Separator(btn_frame, orient=HORIZONTAL)
        separator.pack(fill=X, pady=5)

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
                self.color_var.get(),
                self.type_var.get(),
                "1" if self.type_var.get() == "调休" else "0",
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