import sqlite3
from datetime import datetime
from typing import List, Tuple
from logger_config import logger
class CourseManager:
    def __init__(self):
        self.init_database()
    
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
                        FOREIGN KEY (semester_id) REFERENCES semesters (id)
                    );
                ''')
                conn.commit()
                logger.info("数据库初始化成功")
        except sqlite3.Error as e:
            logger.error(f"数据库初始化失败: {str(e)}")
            raise

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
        try:
            conn = sqlite3.connect('courses.db')
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM courses ORDER BY semester_id, day_of_week, start_time')
            courses = cursor.fetchall()
            # 转换数据类型
            valid_courses = []
            for c in courses:
                try:
                    processed_course = (
                        c[0],  # id
                        c[1],  # name
                        c[2],  # teacher
                        c[3],  # location
                        int(c[4]),  # start_week
                        int(c[5]),  # end_week
                        int(c[6]),  # day_of_week
                        c[7],  # start_time
                        c[8],  # end_time
                        c[9],  # color
                        c[10], # course_type
                        c[11], # is_special
                        c[12]  # semester_id
                    )
                    if self._is_valid_course(processed_course):
                        valid_courses.append(processed_course)
                except (ValueError, TypeError):
                    logger.warning(f"跳过无效课程数据: {c}")
                    continue
            logger.info(f"获取到 {len(valid_courses)} 门有效课程")
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
    def export_courses(self, courses: List[Tuple], format: str = "excel", filename: str = None) -> bool:
        """导出课程数据
        Args:
            courses: 要导出的课程列表
            format: 导出格式 (excel, csv, json, pdf)
            filename: 导出文件名（可选）
        Returns:
            bool: 导出是否成功
        """
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
            from reportlab.lib.styles import getSampleStyleSheet
            from reportlab.pdfbase import pdfmetrics
            from reportlab.pdfbase.ttfonts import TTFont
            
            # 注册中文字体
            try:
                pdfmetrics.registerFont(TTFont('SimSun', 'SimSun.ttf'))
            except:
                logger.warning("未找到SimSun字体，使用默认字体")
            
            doc = SimpleDocTemplate(f"{filename}.pdf", pagesize=A4)
            styles = getSampleStyleSheet()
            story = []
            
            # 添加标题
            title = Paragraph("课程表", styles['Title'])
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
                ('FONTNAME', (0, 0), (-1, 0), 'SimSun-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 14),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('FONTNAME', (0, 1), (-1, -1), 'SimSun'),
                ('FONTSIZE', (0, 1), (-1, -1), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(table)
            doc.build(story)
            
            logger.info(f"成功导出PDF文件: {filename}.pdf")
            return True
        except Exception as e:
            logger.error(f"导出PDF失败: {str(e)}")
            return False
    def _get_weekday(self, day: int) -> str:
        """将数字星期转换为文字"""
        weekdays = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
        return weekdays[day - 1] if 1 <= day <= 7 else "未知"
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
