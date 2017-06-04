# NKUWLAN
南开网关登录脚本 [![Build Status](https://travis-ci.org/NewFuture/NKUWLAN.svg?branch=master)](https://travis-ci.org/NewFuture/NKUWLAN)

## 加入系统命令(NKUWLAN一键登录)
[build 分支](https://github.com/NewFuture/NKUWLAN/tree/build)会根据maste分支的提交自动编译单文件版本和[压缩版](https://github.com/NewFuture/NKUWLAN/blob/build/min.py)可以直接下载使用

* 下载[此链接支持ipv6下载]完整版(兼容python2和**python3**)

```bash
sudo curl https://newfuture.github.io/NKUWLAN/code/nkuwlan.py -#Lo /usr/local/bin/nkuwlan && sudo chmod +x /usr/local/bin/nkuwlan
```

* 下载[此链接支持ipv6下载]压缩版(仅支持python2)

```bash
sudo curl https://newfuture.github.io/NKUWLAN/code/min.py -#Lo /usr/local/bin/nkuwlan && sudo chmod +x /usr/local/bin/nkuwlan
```

```bash
#添加或者更换登录账号(密码会特殊加密保存),多用户之间不共享
nkuwlan -s
#登录(以后输入这个命令自动登录)或者将 /usr/bin/nkuwlan加入启动项开机自动登录
nkuwlan
#注销网关
nkuwlan logout
#显示版本
nkuwlan -v
#仅登录内网
nkuwlan nei
#登录外网
nkuwlan wai
```
## 临时使用

```bash
wget https://newfuture.github.io/NKUWLAN/code/nkuwlan.py

#或者下载min版(不适合修改)
#或者wget https://newfuture.github.io/NKUWLAN/code/min.py

python nkuwlan.py
```


## 其他图形化版本
* Android 版 [https://github.com/NKMSC/NKUWLAN-Android](https://github.com/NKMSC/NKUWLAN-Android)
* Windows GUI [https://github.com/NKMSC/NKUWLAN-Desktop](https://github.com/NKMSC/NKUWLAN-Desktop)


## 多文件【将账号密码编译成二进制】

核心库：(支持 Python2 和 Python3)
* 网关[nkuwlan/gateway.py](https://github.com/NewFuture/NKUWLAN/blob/master/nkuwlan/gateway.py) 对网关登录查询注销操作封装(可以单独使用)
* 配置[nkuwlan/config.py](https://github.com/NewFuture/NKUWLAN/blob/master/nkuwlan/config.py) 对配置读取加密存储进行封装

可以调用gateway.py实现其他功能
* 修改[`autologin.py`](https://github.com/NewFuture/NKUWLAN/blob/master/autologin.py#L8)第8行9行的账号和密码
* 自动登录(掉线重连)

```
python autologin.py
```
* 注销
```
python logout.py
```
