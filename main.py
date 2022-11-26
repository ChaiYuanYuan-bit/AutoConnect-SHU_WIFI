import os
import time
import datetime
import argparse
import logging
from selenium import webdriver
from selenium.webdriver import Edge, ActionChains
from selenium.webdriver.common.by import By

logging.basicConfig(filename=os.path.join(os.path.expanduser('~'), "Desktop/logger.log"), level=logging.INFO)

options = {
    "browserName": "MicrosoftEdge",
    "version": "",
    "platform": "WINDOWS",
    "ms:edgeOptions": {"extensions": [], "args": ["--headless"]}  # 无窗口运行
}


def check_input(opt):
    if opt.username == '' or opt.password == '':
        show_info(current_time() + " " + str("用户名或密码为空!"))
        return False
    else:
        return True


def is_net_ok():
    driver = Edge(capabilities=options)
    try:
        driver.get("http://10.10.9.9:8080")
        time.sleep(0.5)
        online_text = driver.find_element(By.ID, "userMessage").text
        driver.quit()
        if online_text == "您已成功连接校园网!":
            return True
        else:
            return False

    except Exception as e:
        driver.quit()
        show_info(current_time() + " " + str(e))
        show_info(current_time() + " " + str("未连接校园网..."))
        return False


def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--username', type=str, default='', help='please input username')
    parser.add_argument('--password', type=str, default='', help='please input password')
    parser.add_argument('--reconnect', type=bool, default=True, help='reconnect when offline')
    parser.add_argument('--time', type=int, default=3600, help='check time')
    opt = parser.parse_args()
    return opt


def connect(opt):
    driver = Edge(capabilities=options)
    ac = ActionChains(driver)
    show_info(current_time() + " " + "尝试连接校园网...")
    try:
        time.sleep(1)
        driver.get("http://10.10.9.9:8080")
        ac.move_to_element(driver.find_element(By.ID, "username")).perform()
        driver.find_element(By.ID, "username").send_keys(str(opt.username))
        time.sleep(1)
        driver.find_element_by_id("pwd_tip").click()
        driver.find_element_by_id("pwd").send_keys(str(opt.password))
        driver.find_element(By.ID, "loginLink_div").click()
        time.sleep(1)
        driver.quit()
    except Exception as e:
        show_info(current_time() + " " + str(e))


def disconnect():
    # 添加该函数是为了防止网页显示连接到校园网但实际需要手动断开重连的情况
    driver = Edge(capabilities=options)
    ac = ActionChains(driver)
    offline_text = ""
    show_info(current_time() + " " + "尝试与校园网断开连接...")
    try:
        driver.get("http://10.10.9.9:8080")
        ac.move_to_element(driver.find_element(By.ID, "toLogOut")).perform()
        driver.find_element(By.ID, "toLogOut").click()
        time.sleep(2)
        driver.find_element_by_id("sure").click()
        time.sleep(2)
        offline_text = driver.find_element(By.ID, "messageTip").text
        driver.quit()
        if offline_text == "您已下线, 欢迎使用网络":
            show_info(current_time() + " " + "成功与校园网断开连接！")
            return True
        else:
            return False
    except Exception as e:
        show_info(current_time() + " " + str(e))
        return True


def current_time():
    org = str(datetime.datetime.now())
    point = org.find('.')
    return org[0:point]


def show_info(info):
    print(info)
    logging.info(info)


def main(opt):
    reconnect_times = 0
    reconnect_delay = 15  # 每次重连间隔15s
    reconnect_sleep = 60 * 15  # 15分钟后重新连接
    if opt.reconnect:
        while True:
            if is_net_ok():
                show_info(current_time() + " " + str(u"您已连接登录校园网~"))
                while True:
                    show_info(current_time() + " " + str(u"检查网络连接"))
                    # 如果网络断开，推出循环重新连接网络
                    if os.system('ping www.baidu.com'):
                        if reconnect_times < 5: # 每次连续重连次数
                            reconnect_times += 1
                            show_info(current_time() + " " + str(u"网络连接异常..."))
                            show_info(current_time() + " " + str(u"第%d次重连..." % reconnect_times))
                            while True:
                                if disconnect():
                                    break
                                else:
                                    continue
                            connect(opt)
                            time.sleep(reconnect_delay)
                            break
                        else:
                            time.sleep(reconnect_sleep) # 连续重连失败可能是网络问题，等待十五分钟后继续重连
                            reconnect_times = 0
                    else:
                        reconnect_times = 0
                        show_info(current_time() + " " + str(u"网络连接正常..."))
                    time.sleep(opt.time)
            else:
                connect(opt)
            time.sleep(5)
    else:
        connect(opt)


if __name__ == "__main__":
    opt = parse_opt()
    if check_input(opt):
        main(opt)
