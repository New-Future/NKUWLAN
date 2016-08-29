# NKUWLAN
南开网关登录脚本

此`build`分支是根据`master`分支自动构建的分支
---------------

## 临时使用
- *nix使用

```bash
curl -#L https://raw.githubusercontent.com/NewFuture/NKUWLAN/build/nkuwlan.py && chmod +x nkuwlan.py

./nkuwlan.py
```

## 用法

* 登录
```
python nkuwlan.py
```

* 注销
```
python nkuwlan.py logout
```
* 循环登录【断网重连】
```
python nkuwlan.py loop
```


## 多文件【会改代码的用这个】

* 修改`autologin.py`第七行八行的账号和密码
* 自动登录(掉线重连)
```
python autologin.py
```
* 注销
```
python logout.py
```

- windows

## 其他图形化版本
* Android 版 [https://github.com/NKMSC/NKUWLAN-Android](https://github.com/NKMSC/NKUWLAN-Android)
* Windows GUI [https://github.com/NKMSC/NKUWLAN-Desktop](https://github.com/NKMSC/NKUWLAN-Desktop)
