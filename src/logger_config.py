import logging

def setup_logger():
    """配置日志系统"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            logging.StreamHandler(),  # 控制台输出
            logging.FileHandler('app.log', encoding='utf-8')  # 文件输出
        ]
    )
    return logging.getLogger('CourseSchedule')

# 创建全局logger实例
logger = setup_logger()