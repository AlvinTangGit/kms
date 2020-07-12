# 使用systemd设置gunicorn服务

1. 新建配置文件```/etc/systemd/system/gunicorn.service```

    ```bash
    [Unit]
    Description=gunicorn daemon
    After=network.target
 
    [Service]
    User=thfA
    Group=thfA
    WorkingDirectory=/home/thfA/flaskproject
    ExecStart=/home/thfA/flaskproject/venv/bin/gunicorn --chdir /home/thfA/flaskproject/ -b localhost:8000 -w 3 hello:app
    Restart=always
    
    [Install]
    WantedBy=multi-user.target
    ```

2. 启用服务

    ```bash
    systemctl enable --now gunicorn
    ```


