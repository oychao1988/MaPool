#coding:utf-8
import logging
import tornado


def check_params(self,*args):
    params = [self.get_argument(i,None) for i in args]
    if not all(params):
        data = {'success': -1, 'code': 400, 'msg': '缺少必要参数'}
        self.write(data)
        return
    return params


class LogFormatter(tornado.log.LogFormatter):
    def __init__(self):
        super(LogFormatter, self).__init__(
            fmt='%(color)s[%(asctime)s %(filename)s:%(funcName)s:%(lineno)d %(levelname)s]%(end_color)s %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
        )


class Logger:
    @staticmethod
    def get_logger(name, level=logging.INFO):
        # 创建一个日志器
        logger = logging.getLogger(name)
        
        # 设置日志级别
        logger.setLevel(level)

        # 创建日志格式
        formatter = LogFormatter()

        # 创建一个处理程序，将日志写入日志文件
        file_handler = logging.FileHandler('logs/mai_ticket.log')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # 创建另一个处理程序，将日志输出到控制台
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        return logger