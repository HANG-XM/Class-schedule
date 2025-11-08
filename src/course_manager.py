import sqlite3
from datetime import datetime,timedelta
from typing import List, Tuple
from logger_config import logger
import re
import time
class CourseManager:
    def __init__(self):
        self.init_database()
        self._cache = {}
        self._cache_timeout = 300
    
    def init_database(self):
        """初始化数据库"""
        try:
            with sqlite3.connect('courses.db') as conn:
                cursor = conn.cursor()
                cursor.executescript('''
                    CREATE TABLE IF NOT EXISTS semesters (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        start_date TEXT NOT NULL,
                        end_date TEXT NOT NULL,
                        current INTEGER DEFAULT 0
                    );
                    
                    CREATE TABLE IF NOT EXISTS courses (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        teacher TEXT NOT NULL,
                        location TEXT NOT NULL,
                        start_week INTEGER NOT NULL,
                        end_week INTEGER NOT NULL,
                        day_of_week INTEGER NOT NULL,
                        start_time TEXT NOT NULL,
                        end_time TEXT NOT NULL,
                        color TEXT NOT NULL,
                        course_type TEXT NOT NULL,
                        is_special INTEGER NOT NULL,
                        semester_id INTEGER NOT NULL,
                        reminder_enabled INTEGER DEFAULT 0,
                        reminder_minutes INTEGER DEFAULT 15,
                        reminder_type TEXT DEFAULT 'popup',
                        FOREIGN KEY (semester_id) REFERENCES semesters (id)
                    );
                ''')
                conn.commit()
                logger.info("数据库初始化成功")
        except sqlite3.Error as e:
            logger.error(f"数据库初始化失败: {str(e)}")
            raise
    def _get_cache_key(self, method_name, *args):
        """生成缓存键"""
        return f"{method_name}:{'_'.join(map(str, args))}"

    def _is_cache_valid(self, cache_key):
        """检查缓存是否有效"""
        if cache_key not in self._cache:
            return False
        timestamp, _ = self._cache[cache_key]
        return (time.time() - timestamp) < self._cache_timeout

    def _get_from_cache(self, cache_key):
        """从缓存获取数据"""
        if self._is_cache_valid(cache_key):
            _, data = self._cache[cache_key]
            return data
        return None

    def _set_cache(self, cache_key, data):
        """设置缓存"""
        self._cache[cache_key] = (time.time(), data)
    def add_semester(self, name, start_date, end_date):
        """添加学期"""
        conn = sqlite3.connect('courses.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO semesters (name, start_date, end_date)
            VALUES (?, ?, ?)
        ''', (name, start_date, end_date))
        conn.commit()
        conn.close()

    def get_semesters(self):
        """获取所有学期"""
        conn = sqlite3.connect('courses.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM semesters ORDER BY start_date')
        semesters = cursor.fetchall()
        conn.close()
        return semesters

    def get_current_semester(self):
        """获取当前学期"""
        conn = sqlite3.connect('courses.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM semesters WHERE current = 1')
        semester = cursor.fetchone()
        conn.close()
        return semester

    def set_current_semester(self, semester_id):
        """设置当前学期"""
        conn = sqlite3.connect('courses.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE semesters SET current = 0')
        cursor.execute('UPDATE semesters SET current = 1 WHERE id = ?', (semester_id,))
        conn.commit()
        conn.close()
    
    def add_course(self, course_data: Tuple) -> None:
        """添加课程"""
        try:
            conn = sqlite3.connect('courses.db')
            cursor = conn.cursor()
            # 将周数和星期转换为整数
            processed_data = (
                course_data[0],  # name
                course_data[1],  # teacher
                course_data[2],  # location
                int(course_data[3]),  # start_week
                int(course_data[4]),  # end_week
                int(course_data[5]),  # day_of_week
                course_data[6],  # start_time
                course_data[7],  # end_time
                course_data[8],  # color
                course_data[9],  # course_type
                course_data[10], # is_special
                course_data[11]  # semester_id
            )
            cursor.execute('''
                INSERT INTO courses (name, teacher, location, start_week, end_week, 
                                day_of_week, start_time, end_time, color, course_type, is_special, semester_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', processed_data)
            conn.commit()
            logger.info(f"成功添加课程: {course_data[0]},保存课程时使用的学期ID: {course_data[11]}")
        except Exception as e:
            logger.error(f"添加课程失败: {str(e)}")
            raise
        finally:
            conn.close()
    
    def get_courses(self) -> List[Tuple]:
        cache_key = self._get_cache_key("get_courses")
        cached_data = self._get_from_cache(cache_key)
        if cached_data is not None:
            return cached_data

        try:
            conn = sqlite3.connect('courses.db')
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM courses ORDER BY semester_id, day_of_week, start_time')
            courses = cursor.fetchall()
            
            valid_courses = []
            for c in courses:
                try:
                    processed_course = (
                        c[0], c[1], c[2], c[3], int(c[4]), int(c[5]), 
                        int(c[6]), c[7], c[8], c[9], c[10], c[11], 
                        c[12], c[13], c[14], c[15]
                    )
                    if self._is_valid_course(processed_course):
                        valid_courses.append(processed_course)
                except (ValueError, TypeError):
                    continue
            
            self._set_cache(cache_key, valid_courses)
            return valid_courses
        except Exception as e:
            logger.error(f"获取课程列表失败: {str(e)}")
            return []
        finally:
            conn.close()

    def _is_valid_course(self, course: Tuple) -> bool:
        """验证课程数据是否有效"""
        try:
            # 检查必要字段是否存在且非空
            required_fields = [
                course[1],  # name
                course[2],  # teacher
                course[3],  # location
                course[4],  # start_week
                course[5],  # end_week
                course[6],  # day_of_week
                course[7],  # start_time
                course[8],  # end_time
            ]
            
            # 验证数据类型
            int(course[4])  # start_week
            int(course[5])  # end_week
            int(course[6])  # day_of_week
            
            # 验证所有必要字段
            is_valid = all(required_fields)
            if not is_valid:
                logger.warning(f"无效课程数据: {course}")
                return is_valid
                
            return True
                
        except (ValueError, TypeError, IndexError) as e:
            logger.error(f"课程数据验证失败: {course}, 错误: {e}")
            return False

    def delete_course(self, course_id: int) -> None:
        """删除课程"""
        conn = sqlite3.connect('courses.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM courses WHERE id = ?', (course_id,))
        conn.commit()
        conn.close()
    
    def get_courses_by_week(self, week: int) -> List[Tuple]:
        """获取指定周的课程"""
        courses = self.get_courses()
        return [c for c in courses if int(c[4]) <= week <= int(c[5])]
    
    def get_courses_by_day(self, day: int, week: int) -> List[Tuple]:
        """获取指定周指定日的课程"""
        courses = self.get_courses()
        return [c for c in courses if int(c[6]) == day and int(c[4]) <= week <= int(c[5])]
    
    def update_course(self, course_id: int, course_data: Tuple) -> None:
        """更新课程信息"""
        conn = sqlite3.connect('courses.db')
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE courses SET name=?, teacher=?, location=?, start_week=?, end_week=?,
                        day_of_week=?, start_time=?, end_time=?, color=?, course_type=?,
                        is_special=?, semester_id=?
            WHERE id=?
        ''', course_data + (course_id,))
        conn.commit()
        conn.close()
    def update_semester(self, semester_id: int, name: str, start_date: str, end_date: str) -> None:
        """更新学期信息"""
        conn = sqlite3.connect('courses.db')
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE semesters 
            SET name=?, start_date=?, end_date=?
            WHERE id=?
        ''', (name, start_date, end_date, semester_id))
        conn.commit()
        conn.close()
    def search_courses(self, keyword: str, search_type: str = "name") -> List[Tuple]:
        """搜索课程
        Args:
            keyword: 搜索关键词
            search_type: 搜索类型 ("name", "teacher", "location")
        Returns:
            List[Tuple]: 匹配的课程列表
        """
        courses = self.get_courses()
        if search_type == "name":
            return [c for c in courses if keyword.lower() in c[1].lower()]
        elif search_type == "teacher":
            return [c for c in courses if keyword.lower() in c[2].lower()]
        elif search_type == "location":
            return [c for c in courses if keyword.lower() in c[3].lower()]
        return []
    def export_courses(self, courses: List[Tuple], format: str = "excel", filename: str = None, view_type: str = "week", target_date: datetime = None) -> bool:
        """导出课程数据"""
        try:
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"courses_{timestamp}"
                
            if format == "excel":
                return self._export_to_excel(courses, filename)
            elif format == "csv":
                return self._export_to_csv(courses, filename)
            elif format == "json":
                return self._export_to_json(courses, filename)
            elif format == "pdf":
                return self._export_to_pdf(courses, filename)
            elif format == "image":
                return self._export_to_image(courses, filename, view_type, target_date)
            else:
                raise ValueError(f"不支持的导出格式: {format}")
        except Exception as e:
            logger.error(f"导出课程失败: {str(e)}")
            return False

    def _export_to_excel(self, courses: List[Tuple], filename: str) -> bool:
        """导出为Excel格式"""
        try:
            import pandas as pd
            
            # 转换数据格式
            df_data = []
            for course in courses:
                df_data.append({
                    "课程名称": course[1],
                    "任课老师": course[2],
                    "上课地点": course[3],
                    "开始周数": course[4],
                    "结束周数": course[5],
                    "星期": self._get_weekday(course[6]),
                    "上课时间": f"{course[7]}-{course[8]}",
                    "课程类型": course[10],
                    "学期": course[12]
                })
            
            df = pd.DataFrame(df_data)
            df.to_excel(f"{filename}.xlsx", index=False)
            logger.info(f"成功导出Excel文件: {filename}.xlsx")
            return True
        except Exception as e:
            logger.error(f"导出Excel失败: {str(e)}")
            return False

    def _export_to_csv(self, courses: List[Tuple], filename: str) -> bool:
        """导出为CSV格式"""
        try:
            import csv
            
            with open(f"{filename}.csv", 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                writer.writerow(["课程名称", "任课老师", "上课地点", "开始周数", "结束周数", 
                            "星期", "上课时间", "课程类型", "学期"])
                for course in courses:
                    writer.writerow([
                        course[1], course[2], course[3], course[4], course[5],
                        self._get_weekday(course[6]), f"{course[7]}-{course[8]}",
                        course[10], course[12]
                    ])
            logger.info(f"成功导出CSV文件: {filename}.csv")
            return True
        except Exception as e:
            logger.error(f"导出CSV失败: {str(e)}")
            return False

    def _export_to_json(self, courses: List[Tuple], filename: str) -> bool:
        """导出为JSON格式"""
        try:
            import json
            
            data = []
            for course in courses:
                data.append({
                    "name": course[1],
                    "teacher": course[2],
                    "location": course[3],
                    "start_week": course[4],
                    "end_week": course[5],
                    "day_of_week": self._get_weekday(course[6]),
                    "time": f"{course[7]}-{course[8]}",
                    "course_type": course[10],
                    "semester": course[12]
                })
            
            with open(f"{filename}.json", 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logger.info(f"成功导出JSON文件: {filename}.json")
            return True
        except Exception as e:
            logger.error(f"导出JSON失败: {str(e)}")
            return False
    def _export_to_pdf(self, courses: List[Tuple], filename: str) -> bool:
        """导出为PDF格式"""
        try:
            from reportlab.lib import colors
            from reportlab.lib.pagesizes import letter, A4
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.pdfbase import pdfmetrics
            from reportlab.pdfbase.ttfonts import TTFont
            import os
            
            # 注册中文字体
            font_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'fonts', 'simsun.ttc')
            try:
                pdfmetrics.registerFont(TTFont('SimSun', font_path))
                font_name = 'SimSun'
            except:
                try:
                    # 尝试使用系统字体
                    pdfmetrics.registerFont(TTFont('SimSun', 'C:/Windows/Fonts/simsun.ttc'))
                    font_name = 'SimSun'
                except:
                    logger.warning("未找到中文字体，使用默认字体")
                    font_name = 'Helvetica'
            
            doc = SimpleDocTemplate(f"{filename}.pdf", pagesize=A4)
            styles = getSampleStyleSheet()
            
            # 创建中文字体样式
            styles.add(ParagraphStyle(name='ChineseTitle',
                                    parent=styles['Title'],
                                    fontName=font_name,
                                    fontSize=16))
            styles.add(ParagraphStyle(name='ChineseNormal',
                                    parent=styles['Normal'],
                                    fontName=font_name,
                                    fontSize=10))
            
            story = []
            
            # 添加标题
            title = Paragraph("课程表", styles['ChineseTitle'])
            story.append(title)
            
            # 准备表格数据
            data = [["课程名称", "任课老师", "上课地点", "开始周数", "结束周数", 
                    "星期", "上课时间", "课程类型"]]
            for course in courses:
                data.append([
                    course[1], course[2], course[3], course[4], course[5],
                    self._get_weekday(course[6]), f"{course[7]}-{course[8]}",
                    course[10]
                ])
            
            # 创建表格
            table = Table(data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), font_name),
                ('FONTSIZE', (0, 0), (-1, 0), 14),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('FONTNAME', (0, 1), (-1, -1), font_name),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(table)
            doc.build(story)
            
            logger.info(f"成功导出PDF文件: {filename}.pdf")
            return True
        except Exception as e:
            logger.error(f"导出PDF失败: {str(e)}")
            return False
    def _export_to_image(self, courses: List[Tuple], filename: str, view_type: str = "week", target_date: datetime = None) -> bool:
        """导出为图片格式"""
        try:
            from PIL import Image, ImageDraw, ImageFont
            import os
            
            # 创建图片
            width, height = 1200, 800
            image = Image.new('RGB', (width, height), color='white')
            draw = ImageDraw.Draw(image)
            
            # 尝试使用中文字体
            try:
                font_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'fonts', 'simsun.ttc')
                font_title = ImageFont.truetype(font_path, 24)
                font_content = ImageFont.truetype(font_path, 16)
            except:
                try:
                    # 尝试使用系统字体
                    font_title = ImageFont.truetype("C:/Windows/Fonts/simsun.ttc", 24)
                    font_content = ImageFont.truetype("C:/Windows/Fonts/simsun.ttc", 16)
                except:
                    logger.warning("未找到中文字体，使用默认字体")
                    font_title = ImageFont.load_default()
                    font_content = ImageFont.load_default()
            
            # 绘制标题
            title = "课程表" if view_type == "week" else f"{target_date.strftime('%Y年%m月%d日')}课程安排"
            draw.text((width//2 - 100, 20), title, fill='black', font=font_title)
            
            # 绘制表格
            if view_type == "week":
                # 周视图布局
                start_y = 80
                cell_height = 100
                cell_width = 150
                
                # 绘制表头
                headers = ["时间"] + ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
                for i, header in enumerate(headers):
                    x = i * cell_width
                    draw.rectangle([x, start_y, x + cell_width, start_y + 40], outline='black')
                    draw.text((x + 10, start_y + 10), header, fill='black', font=font_content)
                
                # 绘制时间行和课程
                time_slots = [
                    ("07:35", "07:45"), ("08:00", "09:40"), ("10:00", "11:40"),
                    ("14:00", "15:40"), ("16:00", "17:40"), ("19:00", "20:40")
                ]
                
                for i, (start, end) in enumerate(time_slots):
                    y = start_y + 40 + i * cell_height
                    # 绘制时间列
                    draw.rectangle([0, y, cell_width, y + cell_height], outline='black')
                    draw.text((10, y + 40), f"{start}\n{end}", fill='black', font=font_content)
                    
                    # 绘制课程
                    for j in range(7):
                        x = (j + 1) * cell_width
                        draw.rectangle([x, y, x + cell_width, y + cell_height], outline='black')
                        
                        # 查找对应课程
                        for course in courses:
                            if (course[6] == j + 1 and  # 星期几
                                course[7] == start and course[8] == end):  # 时间匹配
                                # 绘制课程信息
                                text = f"{course[1]}\n{course[3]}\n{course[2]}"
                                draw.text((x + 10, y + 10), text, fill='black', font=font_content)
                                break
            else:
                # 日视图布局
                start_y = 80
                cell_height = 80
                current_day = target_date.weekday() + 1
                
                # 筛选当天课程
                day_courses = [c for c in courses if int(c[6]) == current_day]
                
                # 绘制课程列表
                for i, course in enumerate(day_courses):
                    y = start_y + i * cell_height
                    draw.rectangle([50, y, width - 50, y + cell_height], outline='black')
                    text = f"{course[1]} - {course[2]}\n地点：{course[3]}\n时间：{course[7]}-{course[8]}"
                    draw.text((60, y + 10), text, fill='black', font=font_content)
            
            # 保存图片
            image.save(f"{filename}.png")
            logger.info(f"成功导出图片文件: {filename}.png")
            return True
        except Exception as e:
            logger.error(f"导出图片失败: {str(e)}")
            return False
    def _get_weekday(self, day: int) -> str:
        """将数字星期转换为文字"""
        weekdays = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
        return weekdays[day - 1] if 1 <= day <= 7 else "未知"
    
    def get_free_time_slots(self, day: int, week: int) -> List[Tuple]:
        """获取指定日期的空闲时间段"""
        try:
            # 获取当天的课程
            day_courses = self.get_courses_by_day(day, week)
            
            # 获取所有时间段
            time_slots = [
                ("07:35", "07:45"), ("08:00", "09:40"), ("10:00", "11:40"),
                ("14:00", "15:40"), ("16:00", "17:40"), ("19:00", "20:40")
            ]
            
            # 找出已被占用的时间段
            occupied_slots = []
            for course in day_courses:
                start_time = course[7]
                end_time = course[8]
                occupied_slots.append((start_time, end_time))
            
            # 找出空闲时间段
            free_slots = []
            for slot in time_slots:
                if slot not in occupied_slots:
                    free_slots.append(slot)
            
            return free_slots
        except Exception as e:
            logger.error(f"获取空闲时间失败: {str(e)}")
            return []
    def get_week_free_time_slots(self, week: int) -> dict:
        """获取一周的空闲时间段"""
        try:
            week_free_slots = {}
            for day in range(1, 8):  # 1-7 代表周一到周日
                day_free_slots = self.get_free_time_slots(day, week)
                week_free_slots[day] = day_free_slots
            return week_free_slots
        except Exception as e:
            logger.error(f"获取周空闲时间失败: {str(e)}")
            return {}

    def get_month_free_time_slots(self, year: int, month: int) -> dict:
        """获取月份的空闲时间段统计"""
        try:
            month_free_stats = {
                'total_free_time': 0.0,
                'total_occupied_time': 0.0,
                'days': {}
            }
            
            # 获取当前学期
            current_semester = self.get_current_semester()
            if not current_semester:
                return month_free_stats
                
            # 获取月份的第一天和最后一天
            first_day = datetime(year, month, 1)
            last_day = datetime(year, month + 1, 1) - timedelta(days=1) if month < 12 else datetime(year, 12, 31)
            
            # 计算月份的第一天和最后一天对应的周数
            start_week = ((first_day - datetime.strptime(current_semester[2], "%Y-%m-%d")).days // 7) + 1
            end_week = ((last_day - datetime.strptime(current_semester[2], "%Y-%m-%d")).days // 7) + 1
            
            # 定义所有时间段
            all_time_slots = [
                ("07:35", "07:45"), ("08:00", "09:40"), ("10:00", "11:40"),
                ("14:00", "15:40"), ("16:00", "17:40"), ("19:00", "20:40")
            ]
            
            # 计算每天的总时间
            daily_total_time = sum(self._calculate_duration(start, end) for start, end in all_time_slots)
            
            # 遍历月份中的每一天
            current_day = first_day
            while current_day <= last_day:
                day_of_week = current_day.weekday() + 1
                week_num = ((current_day - datetime.strptime(current_semester[2], "%Y-%m-%d")).days // 7) + 1
                
                # 获取当天的空闲时间
                free_slots = self.get_free_time_slots(day_of_week, week_num)
                # 使用 _calculate_duration 方法计算每个时间段的时长
                day_free_time = sum(self._calculate_duration(start, end) for start, end in free_slots)
                
                # 更新统计信息
                month_free_stats['total_free_time'] += day_free_time
                month_free_stats['total_occupied_time'] += (daily_total_time - day_free_time)
                month_free_stats['days'][current_day.day] = {
                    'free_time': day_free_time,
                    'free_slots': free_slots
                }
                
                current_day += timedelta(days=1)
            
            # 最后对总时间进行一次舍入
            month_free_stats['total_free_time'] = round(month_free_stats['total_free_time'], 1)
            month_free_stats['total_occupied_time'] = round(month_free_stats['total_occupied_time'], 1)
                
            return month_free_stats
        except Exception as e:
            logger.error(f"获取月空闲时间失败: {str(e)}")
            return {
                'total_free_time': 0.0,
                'total_occupied_time': 0.0,
                'days': {}
            }
    def _calculate_duration(self, start_time: str, end_time: str) -> float:
        """计算时间段长度（小时）"""
        try:
            start = datetime.strptime(start_time, "%H:%M")
            end = datetime.strptime(end_time, "%H:%M")
            # 先计算分钟数，再转换为小时，避免浮点数精度问题
            minutes = int((end - start).total_seconds() / 60)
            hours = minutes / 60
            return round(hours, 1)  # 转换为小时并保留一位小数
        except Exception as e:
            logger.error(f"计算时间段长度失败: {str(e)}")
            return 0.0
    def get_study_statistics(self, semester_id: int) -> dict:
        """获取学期学习统计数据"""
        try:
            stats = {
                'total_courses': 0,
                'total_hours': 0.0,
                'course_types': {},
                'weekly_hours': {},
                'daily_hours': {},
                'time_distribution': {}
            }
            
            # 获取学期所有课程
            courses = [c for c in self.get_courses() if str(c[12]) == str(semester_id)]
            stats['total_courses'] = len(courses)
            
            # 计算总学习时长
            for course in courses:
                # 计算单次课程时长
                duration = self._calculate_duration(course[7], course[8])
                # 计算总周数
                weeks = int(course[5]) - int(course[4]) + 1
                # 计算该课程总时长
                total_hours = duration * weeks
                stats['total_hours'] += total_hours
                
                # 统计课程类型分布
                course_type = course[10]
                if course_type not in stats['course_types']:
                    stats['course_types'][course_type] = {'count': 0, 'hours': 0.0}
                stats['course_types'][course_type]['count'] += 1
                stats['course_types'][course_type]['hours'] += total_hours
                
                # 统计每周学习时长
                for week in range(int(course[4]), int(course[5]) + 1):
                    if week not in stats['weekly_hours']:
                        stats['weekly_hours'][week] = 0.0
                    stats['weekly_hours'][week] += duration
                
                # 统计每日学习时长
                day = int(course[6])
                if day not in stats['daily_hours']:
                    stats['daily_hours'][day] = 0.0
                stats['daily_hours'][day] += total_hours
                
                # 统计时间段分布
                time_slot = f"{course[7]}-{course[8]}"
                if time_slot not in stats['time_distribution']:
                    stats['time_distribution'][time_slot] = 0.0
                stats['time_distribution'][time_slot] += total_hours
            
            return stats
        except Exception as e:
            logger.error(f"获取学习统计数据失败: {str(e)}")
            return {}
class SpecialCourse:
    TYPES = {
        "早签": {"color": "#ffc107", "duration": 30},
        "自习课": {"color": "#17a2b8", "duration": 45},
        "班会": {"color": "#28a745", "duration": 60},
        "实验课": {"color": "#dc3545", "duration": 90},
        "考试": {"color": "#007bff", "duration": 120},
        "讲座": {"color": "#6c757d", "duration": 90},
        "社团活动": {"color": "#17a2b8", "duration": 120},
        "运动会": {"color": "#ffc107", "duration": 240}
    }
    
    @classmethod
    def get_course_type(cls, course_name: str) -> str:
        """根据课程名称获取课程类型"""
        for course_type, info in cls.TYPES.items():
            if course_type in course_name:
                return course_type
        return "普通课程"
    
    @classmethod
    def get_course_color(cls, course_name: str) -> str:
        """根据课程名称获取课程颜色"""
        course_type = cls.get_course_type(course_name)
        return cls.TYPES.get(course_type, {}).get("color", "primary")
