## 简介

无需使用浏览器进行网页登录，直接在终端执行脚本即可。

配合系统定时任务，如linux上的crontab等，可实现永不掉线功能

## 使用方式

#### 下载代码

```shell
git clone --recursive https://github.com/YanzheL/schoolnet.git
```

注意加上`--recursive`选项

#### 登录校园网

```shell
python3 main.py -u 你的校园网学号 -p 你的校园网密码 -m login
```

注: 此命令可以重复执行，若已登录则不会重复登录

#### 退出校园网

```shell
python3 main.py -u 你的校园网学号 -p 你的校园网密码 -m logout
```

#### 永不掉线功能

只举例linux下设置，其他系统需自行上网查找资料

1. 打开定时任务编辑

   ```shell
   crontab -e
   ```

2. 添加定时任务

   ```shell
   */5 * * * * python3 main.py -u 你的校园网学号 -p 你的校园网密码 -m login
   ```

   此处的作用是每隔5分钟检查一下登录状态，如果掉线就重新登录