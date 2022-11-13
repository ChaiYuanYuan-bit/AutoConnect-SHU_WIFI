# AutoConnect-SHU_WIFI
自动连接上海大学校园网，方便远程办公！

## 本脚本出自上海大学EIPL实验室

## AutoConnect
### 环境安装
1.在https://developer.microsoft.com/zh-cn/microsoft-edge/tools/webdriver/中安装合适自己edge版本的webdriver
2.将webdriver中的exe重命名为MicrosoftWebDriver.exe并添加到环境变量

### 添加用户名和密码
右键编辑bat文件，将用户名和密码改为自己的用户名与密码

### 参数说明
--username 用户名 defaule =''
--password 密码 defaule =''
--reconnect 是否选择断网重连 defaule=True
--time 断网重连检查时长 defaule=3600 (单位s)

### 开机自启动
win+r中输入shell:startup，将bat文件的桌面快捷方式剪切到该文件夹下

### 日志信息
在桌面logger.log中

## 源代码
main.py
