# -*- coding:utf-8 -*-
# AUTHOR: Sun

# 是否开启debug模式
debug = False

# 使用异步工作模式提高性能
worker_class = "gevent"

# 访问地址
bind = "0.0.0.0:80"

# 工作进程数，设置为CPU核心数
workers = 1

# 工作线程数，增加并发处理能力
threads = 2

# 超时时间
timeout = 300

# 输出日志级别
loglevel = 'info'

# 存放日志路径
accesslog = "/app/access.txt"

# 存放日志路径
errorlog = "/app/error.txt"


if __name__ == '__main__':
    pass
