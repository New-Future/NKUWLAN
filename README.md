# NKUWLAN
南开网关登录脚本


## 加入系统命令使用

```bash
sudo curl https://raw.githubusercontent.com/NewFuture/NKUWLAN/build/nkuwlan.py -#Lo /usr/bin/nkuwlan && sudo chmod +x /usr/bin/nkuwlan
```
```bash
# 添加登录账号
nkuwlan -s
#自动登录
nkuwlan
#注销
nkuwlan logout

```
## 临时使用
```bash
curl https://raw.githubusercontent.com/NewFuture/NKUWLAN/build/nkuwlan.py -#Lo nkuwlan.py
python nkuwlan.py
```


## 其他图形化版本
* Android 版 [https://github.com/NKMSC/NKUWLAN-Android](https://github.com/NKMSC/NKUWLAN-Android)
* Windows GUI [https://github.com/NKMSC/NKUWLAN-Desktop](https://github.com/NKMSC/NKUWLAN-Desktop)



## 多文件【将账号密码编译成二进制】

* 修改`autologin.py`第七行八行的账号和密码
* 自动登录(掉线重连)
```
python autologin.py
```
* 注销
```
python logout.py
```
