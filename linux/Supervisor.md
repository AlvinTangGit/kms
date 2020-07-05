*# Supervisor

## 简介
Supervisor是一个C/S系统，用于在类Unix系统上控制进程，可自动重启崩溃的进程

## 安装(in venv)
    pip install supervisor

### 创建配置文件
    echo_supervisord_conf > /etc/supervisord.conf

### 修改配置文件(Gunicorn)

    [program:gunicorn]
    command=/path/to/gunicorn main:application -c /path/to/gunicorn.conf.py
    directory=/path/to/project
    user=nobody
    autostart=true
    autorestart=true
    redirect_stderr=true

gunicorn.conf.py内容如下：

```py
import multiprocessing

bind = "127.0.0.1:8000"
workers = multiprocessing.cpu_count() * 2 + 1
```

