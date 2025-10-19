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
        """获取所有课程"""
        try:
            conn = sqlite3.connect('courses.db')
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM courses ORDER BY semester_id, day_of_week, start_time')
            courses = cursor.fetchall()
            valid_courses = [c for c in courses if self._is_valid_course(c)]
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
        return [c for c in courses if int(c[3]) <= week <= int(c[4])]
    
    def get_courses_by_day(self, day: int, week: int) -> List[Tuple]:
        """获取指定周指定日的课程"""
        courses = self.get_courses()
        return [c for c in courses if int(c[5]) == day and int(c[3]) <= week <= int(c[4])]
    
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

class SpecialCourse:
    TYPES = {
        "早签": {"color": "warning", "duration": 30},
        "自习课": {"color": "info", "duration": 45},
        "班会": {"color": "success", "duration": 60},
        "实验课": {"color": "danger", "duration": 90},
        "考试": {"color": "primary", "duration": 120}
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
