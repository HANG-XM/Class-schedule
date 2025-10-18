import sqlite3
from datetime import datetime
from typing import List, Tuple

class CourseManager:
    def __init__(self):
        self.init_database()
    
    def init_database(self):
        """初始化数据库"""
        conn = sqlite3.connect('courses.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS courses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                teacher TEXT,
                location TEXT,
                start_week INTEGER,
                end_week INTEGER,
                day_of_week INTEGER,
                start_time TEXT,
                end_time TEXT,
                color TEXT,
                course_type TEXT,
                is_special INTEGER DEFAULT 0
            )
        ''')
        conn.commit()
        conn.close()
    
    def add_course(self, course_data: Tuple) -> None:
        """添加课程
        
        Args:
            course_data: 包含课程信息的元组
        """
        conn = sqlite3.connect('courses.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO courses (name, teacher, location, start_week, end_week, 
                               day_of_week, start_time, end_time, color, course_type, is_special)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', course_data)
        conn.commit()
        conn.close()
    
    def get_courses(self) -> List[Tuple]:
        """获取所有课程
        
        Returns:
            List[Tuple]: 所有课程的列表
        """
        conn = sqlite3.connect('courses.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM courses ORDER BY day_of_week, start_time')
        courses = cursor.fetchall()
        conn.close()
        return courses
    
    def delete_course(self, course_id: int) -> None:
        """删除课程
        
        Args:
            course_id: 课程ID
        """
        conn = sqlite3.connect('courses.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM courses WHERE id = ?', (course_id,))
        conn.commit()
        conn.close()
    
    def get_courses_by_week(self, week: int) -> List[Tuple]:
        """获取指定周的课程
        
        Args:
            week: 周数
            
        Returns:
            List[Tuple]: 指定周的课程列表
        """
        courses = self.get_courses()
        return [c for c in courses if c[3] <= week <= c[4]]
    
    def get_courses_by_day(self, day: int, week: int) -> List[Tuple]:
        """获取指定周指定日的课程
        
        Args:
            day: 星期几 (1-7)
            week: 周数
            
        Returns:
            List[Tuple]: 指定周指定日的课程列表
        """
        courses = self.get_courses()
        return [c for c in courses if c[5] == day and c[3] <= week <= c[4]]
    
    def update_course(self, course_id: int, course_data: Tuple) -> None:
        """更新课程信息
        
        Args:
            course_id: 课程ID
            course_data: 新的课程信息
        """
        conn = sqlite3.connect('courses.db')
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE courses SET name=?, teacher=?, location=?, start_week=?, end_week=?,
                           day_of_week=?, start_time=?, end_time=?, color=?, course_type=?,
                           is_special=?
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
        """根据课程名称获取课程类型
        
        Args:
            course_name: 课程名称
            
        Returns:
            str: 课程类型
        """
        for course_type, info in cls.TYPES.items():
            if course_type in course_name:
                return course_type
        return "普通课程"
    
    @classmethod
    def get_course_color(cls, course_name: str) -> str:
        """根据课程名称获取课程颜色
        
        Args:
            course_name: 课程名称
            
        Returns:
            str: 颜色标识
        """
        course_type = cls.get_course_type(course_name)
        return cls.TYPES.get(course_type, {}).get("color", "primary")
