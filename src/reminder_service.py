import threading
import time
from datetime import datetime, timedelta
from logger_config import logger
import tkinter as tk
from tkinter import messagebox
import winsound  # 用于Windows系统声音提醒

class ReminderService:
    def __init__(self, course_manager):
        self.course_manager = course_manager
        self.running = False
        self.reminder_thread = None

    def start(self):
        """启动提醒服务"""
        if not self.running:
            self.running = True
            self.reminder_thread = threading.Thread(target=self._check_reminders)
            self.reminder_thread.daemon = True
            self.reminder_thread.start()
            logger.info("提醒服务已启动")

    def stop(self):
        """停止提醒服务"""
        self.running = False
        if self.reminder_thread:
            self.reminder_thread.join()
        logger.info("提醒服务已停止")

    def _check_reminders(self):
        """检查并触发提醒"""
        while self.running:
            try:
                now = datetime.now()
                current_week = self._get_current_week()
                current_day = now.weekday() + 1  # 转换为1-7
                
                # 获取当前周的所有课程
                courses = self.course_manager.get_courses_by_week(current_week)
                
                for course in courses:
                    if self._should_remind(course, now, current_day):
                        self._trigger_reminder(course)
                        
                time.sleep(60)  # 每分钟检查一次
            except Exception as e:
                logger.error(f"检查提醒时出错: {str(e)}")

    def _should_remind(self, course, now, current_day):
        """判断是否应该触发提醒"""
        try:
            # 检查是否是今天的课程
            if int(course[6]) != current_day:
                return False
                
            # 检查是否启用了提醒
            if not course[13]:  # reminder_enabled
                return False
                
            # 解析课程开始时间
            course_time = datetime.strptime(course[7], "%H:%M").time()
            course_datetime = datetime.combine(now.date(), course_time)
            
            # 计算提醒时间
            reminder_minutes = int(course[14])  # reminder_minutes
            reminder_time = course_datetime - timedelta(minutes=reminder_minutes)
            
            # 检查是否到了提醒时间
            time_diff = (now - reminder_time).total_seconds()
            return 0 <= time_diff < 60  # 在一分钟内的误差范围内
            
        except Exception as e:
            logger.error(f"判断提醒时出错: {str(e)}")
            return False

    def _trigger_reminder(self, course):
        """触发提醒"""
        try:
            reminder_type = course[15]  # reminder_type
            
            if reminder_type in ["popup", "both"]:
                self._show_popup_reminder(course)
                
            if reminder_type in ["sound", "both"]:
                self._play_sound_reminder()
                
        except Exception as e:
            logger.error(f"触发提醒时出错: {str(e)}")

    def _show_popup_reminder(self, course):
        """显示弹窗提醒"""
        root = tk.Tk()
        root.withdraw()  # 隐藏主窗口
        messagebox.showinfo(
            "课程提醒",
            f"即将开始上课:\n\n"
            f"课程: {course[1]}\n"
            f"老师: {course[2]}\n"
            f"地点: {course[3]}\n"
            f"时间: {course[7]}-{course[8]}"
        )
        root.destroy()

    def _play_sound_reminder(self):
        """播放声音提醒"""
        try:
            # Windows系统使用系统默认提示音
            winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
        except Exception as e:
            logger.error(f"播放声音提醒失败: {str(e)}")

    def _get_current_week(self):
        """获取当前周数"""
        current_semester = self.course_manager.get_current_semester()
        if not current_semester:
            return 1
            
        today = datetime.now()
        start_date = datetime.strptime(current_semester[2], "%Y-%m-%d")
        week_diff = (today - start_date).days // 7 + 1
        return max(1, min(week_diff, 20))