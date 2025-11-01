import ttkbootstrap as tb
from ttkbootstrap.constants import *
from datetime import datetime, timedelta
from logger_config import logger
from dialogs import EditCourseDialog
from course_manager import SpecialCourse
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
        for widget in self.frame.winfo_children():
            widget.destroy()
        try:
            if not self.app.current_semester:
                logger.warning("没有选择当前学期")
                tb.Label(self.frame, text="请先创建或选择学期", 
                        font=("Helvetica", 16),
                        bootstyle=WARNING).pack(expand=True)
                return

            # 确保周数在有效范围内
            self.app.current_week = max(1, min(self.app.current_week, 20))
            
            week_courses = [c for c in self.app.course_manager.get_courses_by_week(self.app.current_week)
                        if str(c[12]) == str(self.app.current_semester[0])]
            logger.info(f"当前周数: {self.app.current_week}")
            logger.info(f"当前学期ID: {self.app.current_semester[0]}")
            logger.info(f"本周课程列表: {week_courses}")

            # 创建表格
            columns = ["时间"] + self.app.days_of_week
            tree = tb.Treeview(self.frame, columns=columns, show="tree headings", height=22)
            
            # 绑定双击事件
            tree.bind("<Double-Button-1>", self.on_course_double_click)

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
            for course in week_courses:
                day_index = course[6]  # 星期几 (1-7)
                time_index = None

                # 找到对应的时间段
                for i, (start, end) in enumerate(self.app.time_slots):
                    if course[7] == start and course[8] == end:
                        time_index = i
                        break

                if time_index is not None:
                    # 获取树中的项目ID
                    item_id = tree.get_children()[time_index]

                    # 获取当前值并更新
                    current_values = list(tree.item(item_id, "values"))
                    course_text = f"{course[1]}\n{course[3]}\n{course[2]}\n{course[4]}-{course[5]}周"
                    current_values[day_index] = course_text

                    # 更新值和样式
                    tree.item(item_id, values=current_values)
                    
                    # 设置单元格颜色
                    color = course[9]  # 直接使用十六进制颜色代码
                    if color:  # 确保颜色值存在
                        # 创建唯一的标签名称
                        tag_name = f"course_{color}_{day_index}"
                        
                        # 配置标签样式
                        tree.tag_configure(tag_name, background=color)
                        
                        # 获取当前行的所有标签
                        current_tags = list(tree.item(item_id, "tags"))
                        
                        # 移除该列之前的标签（如果存在）
                        old_tag = f"course_*_{day_index}"
                        current_tags = [tag for tag in current_tags if not tag.endswith(f"_{day_index}")]
                        
                        # 添加新标签
                        current_tags.append(tag_name)
                        
                        # 更新单元格值和标签
                        current_values[day_index] = course_text
                        tree.item(item_id, values=current_values, tags=tuple(current_tags))

            tree.pack(fill=BOTH, expand=True)

            # 更新统计信息
            self.app.stats_panel.update_stats(self.app.courses, self.app.current_week,
                                            self.app.course_manager, "week")
        except Exception as e:
            logger.error(f"显示周视图失败: {str(e)}")
            raise

    def on_course_double_click(self, event):
        """处理表格双击事件"""
        try:
            # 获取点击的位置
            region = event.widget.identify_region(event.x, event.y)
            logger.info(f"双击位置: {region}")
            if region != "cell":
                return
                
            # 获取点击的列和行
            column = event.widget.identify_column(event.x)
            item = event.widget.identify_row(event.y)
            logger.info(f"点击位置: 列={column}, 行={item}")
            
            if not item:
                return
                
            # 获取时间索引和星期索引
            values = event.widget.item(item, "values")
            if not values:
                return
                
            # 修正列索引计算
            if column == "#1":  # 第一列是时间列
                return
                
            # 获取星期几（1-7）
            # #2对应周一(1)，#3对应周二(2)，以此类推
            day_index = int(column[1:]) - 2
            
            # 获取时间
            time_parts = values[0].split('\n')
            if len(time_parts) != 2:
                return
            start_time, end_time = time_parts
            
            # 查找对应的课程
            week_courses = [c for c in self.app.course_manager.get_courses_by_week(self.app.current_week)
                        if str(c[12]) == str(self.app.current_semester[0])]
            
            # 添加调试信息
            logger.info(f"查找条件: 星期={day_index+1}, 时间={start_time}-{end_time}")
            logger.info(f"本周课程列表: {week_courses}")
            
            course = None
            for c in week_courses:
                logger.info(f"检查课程: {c[1]}, 星期={c[6]}, 时间={c[7]}-{c[8]}")
                if c[6] == day_index + 1 and c[7] == start_time and c[8] == end_time:
                    course = c
                    logger.info(f"找到匹配课程: {c[1]}")
                    break
                    
            if course:
                # 打开编辑对话框
                from dialogs import EditCourseDialog
                EditCourseDialog(self.parent, self.app, course)
                logger.info(f"打开编辑对话框: {course[1]}")
            else:
                logger.warning("未找到匹配的课程")
        except Exception as e:
            logger.error(f"处理双击事件失败: {str(e)}")

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

        if not self.app.current_semester:
            logger.warning("没有选择当前学期")
            tb.Label(self.frame, text="请先创建或选择学期", 
                    font=("Helvetica", 16),
                    bootstyle=WARNING).pack(expand=True)
            return

        try:
            # 创建日视图内容
            content = tb.Frame(self.frame)
            content.pack(fill=BOTH, expand=True, padx=20, pady=20)

            tb.Label(content, text=f"{datetime.now().strftime('%Y年%m月%d日')} 日视图",
                    font=("Helvetica", 24, "bold"),
                    bootstyle=PRIMARY).pack(pady=20)

            # 创建当天的课程列表
            current_day = datetime.now().weekday() + 1
            day_courses = [c for c in self.app.course_manager.get_courses_by_day(current_day, self.app.current_week)
                        if str(c[12]) == str(self.app.current_semester[0])]
            
            logger.info(f"显示当天课程，共 {len(day_courses)} 门")

            if day_courses:
                for course in day_courses:
                    frame = tb.Frame(content, padding=10)
                    frame.pack(fill=X, pady=5)

                    # 左侧显示课程名称和地点
                    left_frame = tb.Frame(frame)
                    left_frame.pack(side=LEFT, fill=X, expand=True)
                    
                    tb.Label(left_frame, text=f"{course[1]}",
                            font=("Helvetica", 14)).pack(anchor="w")
                    tb.Label(left_frame, text=f"📍 {course[3]}",
                            font=("Helvetica", 10),
                            bootstyle=SECONDARY).pack(anchor="w")
                    
                    # 右侧显示时间
                    tb.Label(frame, text=f"{course[7]}-{course[8]}",
                            bootstyle=INFO).pack(side=RIGHT)
            else:
                tb.Label(content, text="当天暂无课程",
                        font=("Helvetica", 14),
                        bootstyle=SECONDARY).pack(expand=True)

            # 更新统计信息
            self.app.stats_panel.update_stats(self.app.courses, self.app.current_week, 
                                            self.app.course_manager, "day", datetime.now())
        except Exception as e:
            logger.error(f"显示日视图失败: {str(e)}")
            raise

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

        if not self.app.current_semester:
            logger.warning("没有选择当前学期")
            tb.Label(self.frame, text="请先创建或选择学期", 
                    font=("Helvetica", 16),
                    bootstyle=WARNING).pack(expand=True)
            return

        try:
            # 创建主容器
            main_container = tb.Frame(self.frame)
            main_container.pack(fill=BOTH, expand=True, padx=20, pady=20)

            # 月份导航
            nav_frame = tb.Frame(main_container)
            nav_frame.pack(fill=X, pady=(0, 10))

            tb.Button(nav_frame, text="◀", width=3,
                    command=self.previous_month).pack(side=LEFT, padx=5)

            self.month_label = tb.Label(nav_frame, text="",
                                    font=("Helvetica", 16, "bold"))
            self.month_label.pack(side=LEFT, expand=True)

            tb.Button(nav_frame, text="▶", width=3,
                    command=self.next_month).pack(side=LEFT, padx=5)

            # 日历容器
            calendar_container = tb.Frame(main_container)
            calendar_container.pack(fill=BOTH, expand=True)

            # 创建日历网格
            self.calendar_frame = tb.Frame(calendar_container)
            self.calendar_frame.pack(fill=BOTH, expand=True)

            # 初始化当前日期
            self.current_date = datetime.now()
            self.update_month_view()
        except Exception as e:
            logger.error(f"显示月视图失败: {str(e)}")
            raise

    def update_month_view(self):
        """更新月份视图"""
        try:
            self._clear_calendar()
            self._update_month_label()
            self._create_calendar_grid()  # 创建日历网格

            # 更新统计信息
            self.app.stats_panel.update_stats(self.app.courses, self.app.current_week,
                                            self.app.course_manager, "month", self.current_date)
            
            logger.info(f"月视图更新完成，{self.current_date.year}年{self.current_date.month}月")
        except Exception as e:
            logger.error(f"更新月视图失败: {str(e)}")
            raise
    def _clear_calendar(self):
        """清空日历"""
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

    def _update_month_label(self):
        """更新月份标签"""
        self.month_label.config(text=f"{self.current_date.year}年{self.current_date.month}月")

    def _create_calendar_grid(self):
        """创建日历网格"""
        # 添加星期标题
        week_days = ["一", "二", "三", "四", "五", "六", "日"]
        for day in week_days:
            tb.Label(self.calendar_frame, text=day, 
                    font=("Helvetica", 9, "bold"),  # 减小字体
                    padding=5).grid(row=0, column=week_days.index(day),
                                    sticky="nsew", padx=1, pady=1)  # 减小内边距

        # 获取月份第一天和最后一天
        year = self.current_date.year
        month = self.current_date.month
        first_day = datetime(year, month, 1)
        last_day = datetime(year, month + 1, 1) - timedelta(days=1) if month < 12 else datetime(year, 12, 31)

        # 添加空白格子
        first_weekday = first_day.weekday()
        for i in range(first_weekday):
            tb.Frame(self.calendar_frame, relief="ridge", borderwidth=1).grid(
                row=1, column=i, sticky="nsew", padx=1, pady=1)

        # 添加日期格子
        current_date = first_day
        week_num = 1
        month_courses = []

        while current_date <= last_day:
            # 创建固定大小的日期格子
            day_frame = tb.Frame(self.calendar_frame, relief="ridge", borderwidth=1)
            day_frame.grid(row=week_num, column=current_date.weekday(),
                        sticky="nsew", padx=1, pady=1)
            
            # 创建固定大小的内部容器
            inner_frame = tb.Frame(day_frame, width=150, height=120)
            inner_frame.pack(fill=BOTH, expand=True)
            inner_frame.pack_propagate(False)  # 防止内部容器随内容缩放

            # 日期标签
            date_label = tb.Label(inner_frame, text=str(current_date.day),
                                font=("Helvetica", 12, "bold"),
                                padding=5)
            date_label.pack(anchor="nw")

            # 获取当前月份的周数范围
            month_start = datetime(year, month, 1)
            month_end = datetime(year, month + 1, 1) - timedelta(days=1) if month < 12 else datetime(year, 12, 31)
            start_week = ((month_start - datetime.strptime(self.app.current_semester[2], "%Y-%m-%d")).days // 7) + 1
            end_week = ((month_end - datetime.strptime(self.app.current_semester[2], "%Y-%m-%d")).days // 7) + 1

            # 计算当前日期对应的周数
            current_week = ((current_date - datetime.strptime(self.app.current_semester[2], "%Y-%m-%d")).days // 7) + 1
            day_courses = [c for c in self.app.courses
                        if int(c[6]) == current_date.weekday() + 1 and 
                        int(c[4]) <= current_week <= int(c[5]) and
                        str(c[12]) == str(self.app.current_semester[0])]
            
            month_courses.extend(day_courses)

            # 显示课程
            if day_courses:
                # 创建固定大小的课程容器
                course_frame = tb.Frame(inner_frame)
                course_frame.pack(fill=BOTH, expand=True, padx=2, pady=2)
                
                # 最多显示3门课程，统一显示格式
                for i, course in enumerate(day_courses[:3]):
                    # 限制课程名称长度为6个字符，使用固定宽度字体
                    course_name = course[1][:6] + ".." if len(course[1]) > 6 else course[1]
                    course_label = tb.Label(course_frame, 
                                        text=course_name,
                                        font=("Courier", 8),  # 使用固定宽度字体
                                        background=SpecialCourse.TYPES.get(course[10], {}).get("color", course[9]),
                                        width=12)  # 固定标签宽度
                    course_label.pack(fill=X, pady=1, ipady=2)  # 使用 ipady 控制内部垂直边距
                
                # 如果课程数超过3，显示"+N"
                if len(day_courses) > 3:
                    more_label = tb.Label(course_frame,
                                        text=f"+{len(day_courses)-3}",
                                        font=("Courier", 8),  # 使用固定宽度字体
                                        bootstyle="info",
                                        width=12)  # 固定标签宽度
                    more_label.pack(fill=X, pady=1, ipady=2)  # 使用 ipady 控制内部垂直边距

            # 移动到下一天
            current_date += timedelta(days=1)
            if current_date.weekday() == 0:
                week_num += 1

        # 配置网格权重，确保所有列等宽
        for i in range(7):
            self.calendar_frame.columnconfigure(i, weight=1, minsize=120)  # 设置最小宽度
        for i in range(week_num + 1):
            self.calendar_frame.rowconfigure(i, weight=1, minsize=100)  # 设置最小高度

        # 返回月份课程列表
        return month_courses

    def _update_month_stats(self, month_courses):
        try:
            special_count = len([c for c in month_courses if c[11]])  # 修正索引
            self.total_courses.config(text=f"总课程数: {len(month_courses)}")
            self.special_courses.config(text=f"特殊课程: {special_count}")
        except Exception as e:
            logger.error(f"更新统计信息失败: {str(e)}")

    def previous_month(self):
        """切换到上个月"""
        try:
            if self.current_date.month == 1:
                self.current_date = datetime(self.current_date.year - 1, 12, 1)
            else:
                self.current_date = datetime(self.current_date.year, self.current_date.month - 1, 1)
            self.update_month_view()
        except Exception as e:
            logger.error(f"切换上个月失败: {str(e)}")

    def next_month(self):
        """切换到下个月"""
        try:
            if self.current_date.month == 12:
                self.current_date = datetime(self.current_date.year + 1, 1, 1)
            else:
                self.current_date = datetime(self.current_date.year, self.current_date.month + 1, 1)
            self.update_month_view()
        except Exception as e:
            logger.error(f"切换下个月失败: {str(e)}")
