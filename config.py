# -*- coding:utf-8 -*-
# AUTHOR: Sun

# 是否开启debug模式
debug = False

# 使用同步工作模式，内存占用最少
worker_class = "sync"

# 访问地址
bind = "0.0.0.0:80"

# 工作进程数
workers = 1

# 工作线程数
threads = 1

# 超时时间
timeout = 600

# 输出日志级别
loglevel = 'info'

# 存放日志路径
accesslog = "/app/access.txt"

# 存放日志路径
errorlog = "/app/error.txt"


if __name__ == '__main__':
    pass
