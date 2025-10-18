import sqlite3
from datetime import datetime
from typing import List, Tuple

class CourseManager:
    def __init__(self):
        self.init_database()
        self.migrate_database()
    
    def init_database(self):
        """初始化数据库"""
        conn = sqlite3.connect('courses.db')
        cursor = conn.cursor()
        
        # 创建学期表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS semesters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                start_date TEXT NOT NULL,
                end_date TEXT NOT NULL,
                current INTEGER DEFAULT 0
            )
        ''')
        
        # 创建课程表
        cursor.execute('''
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
            )
        ''')
        
        conn.commit()
        conn.close()

    def migrate_database(self):
        """数据库迁移"""
        conn = sqlite3.connect('courses.db')
        cursor = conn.cursor()
        
        # 检查courses表是否有semester_id列
        cursor.execute("PRAGMA table_info(courses)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'semester_id' not in columns:
            # 添加semester_id列
            cursor.execute('ALTER TABLE courses ADD COLUMN semester_id INTEGER')
            
            # 如果没有当前学期，创建默认学期
            if not self.get_current_semester():
                self.add_semester("默认学期", "2023-09-01", "2024-01-20")
                current_semester = self.get_current_semester()
                # 更新所有现有课程的semester_id
                cursor.execute('UPDATE courses SET semester_id = ?', (current_semester[0],))
        
        conn.commit()
        conn.close()

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
        conn = sqlite3.connect('courses.db')
        cursor = conn.cursor()
        # 将周数转换为整数
        processed_data = (
            course_data[0],  # name
            course_data[1],  # teacher
            course_data[2],  # location
            int(course_data[3]),  # start_week
            int(course_data[4]),  # end_week
            course_data[5],  # day_of_week
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
        conn.close()
    
    def get_courses(self) -> List[Tuple]:
        """获取所有课程"""
        conn = sqlite3.connect('courses.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM courses ORDER BY semester_id, day_of_week, start_time')
        courses = cursor.fetchall()
        conn.close()
        # 过滤掉无效数据
        return [c for c in courses if self._is_valid_course(c)]

    def _is_valid_course(self, course: Tuple) -> bool:
        """验证课程数据是否有效"""
        try:
            # 检查周数是否为有效数字
            int(course[3])  # start_week
            int(course[4])  # end_week
            # 检查其他必要字段
            return all([
                course[1],  # name
                course[2],  # teacher
                course[5],  # day_of_week
                course[6],  # start_time
                course[7],  # end_time
            ])
        except (ValueError, TypeError, IndexError):
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
        return [c for c in courses if c[5] == day and int(c[3]) <= week <= int(c[4])]
    
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
    def migrate_database(self):
        """数据库迁移"""
        conn = sqlite3.connect('courses.db')
        cursor = conn.cursor()
        
        # 检查courses表是否有semester_id列
        cursor.execute("PRAGMA table_info(courses)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'semester_id' not in columns:
            # 添加semester_id列
            cursor.execute('ALTER TABLE courses ADD COLUMN semester_id INTEGER')
            
            # 如果没有当前学期，创建默认学期
            if not self.get_current_semester():
                self.add_semester("默认学期", "2023-09-01", "2024-01-20")
                current_semester = self.get_current_semester()
                # 更新所有现有课程的semester_id
                cursor.execute('UPDATE courses SET semester_id = ?', (current_semester[0],))
        
        # 修复周数数据类型
        cursor.execute("SELECT id, start_week, end_week FROM courses")
        courses = cursor.fetchall()
        for course in courses:
            try:
                start_week = int(course[1])
                end_week = int(course[2])
                cursor.execute("UPDATE courses SET start_week = ?, end_week = ? WHERE id = ?",
                            (start_week, end_week, course[0]))
            except (ValueError, TypeError):
                # 如果转换失败，删除这条记录
                cursor.execute("DELETE FROM courses WHERE id = ?", (course[0],))
        
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
