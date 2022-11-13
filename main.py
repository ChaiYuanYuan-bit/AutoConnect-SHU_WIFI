import os
import time
import datetime
import argparse
import logging
from selenium.webdriver import Edge, ActionChains
from selenium.webdriver.common.by import By

logging.basicConfig(filename=os.path.join(os.path.expanduser('~'), "Desktop/logger.log"), level=logging.INFO)


def check_input(opt):
    if opt.username == '' or opt.password == '':
        logging.info(current_time() + " " + str("用户名或密码为空!"))
        return False
    else:
        return True


def is_net_ok():
    driver_test = Edge()
    try:
        driver_test.get("http://10.10.9.9:8080")
        online_text = driver_test.find_element(By.ID, "userMessage").text
        driver_test.quit()
    except Exception as e:
        logging.info(current_time() + " " + str("与校园网断开连接..."))
        driver_test.quit()
        return False
    if online_text == "您已成功连接校园网!":
        return True
    else:
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
    logging.info(current_time() + " " + "尝试连接校园网...")
    driver = Edge()
    ac = ActionChains(driver)
    try:
        driver.get("http://10.10.9.9:8080")
        ac.move_to_element(driver.find_element(By.ID, "username")).perform()
        driver.find_element(By.ID, "username").send_keys(str(opt.username))
        time.sleep(0.5)
        driver.find_element_by_id("pwd_tip").click()
        driver.find_element_by_id("pwd").send_keys(str(opt.password))
        driver.find_element(By.ID, "loginLink_div").click()
        time.sleep(1)
        driver.quit()
        logging.info(current_time() + " "+ str(u"成功登录校园网!"))
    except Exception as e:
        logging.info(current_time() + " " + str(e))
        driver.quit()



def current_time():
    org = str(datetime.datetime.now())
    point = org.find('.')
    return org[0:point]


def main(opt):
    if opt.reconnect:
        while True:
            if is_net_ok():
                logging.info(current_time() + " " + str(u"您已成功登录校园网!"))
                while True:
                    logging.info(current_time() + " " + str(u"检查网络连接"))
                    # 如果网络断开，推出循环重新连接网络
                    if os.system('ping www.baidu.com'):
                        logging.info(current_time() + " "+ str(u"与校园网断开连接..."))
                        break
                    else:
                        logging.info(current_time() + " "+ str(u"与校园网保持连接中"))
                    time.sleep(opt.time)
            else:
                logging.info(current_time() + " " + str(u"与校园网断开连接..."))
                connect(opt)
    else:
        connect(opt)


if __name__ == "__main__":
    opt = parse_opt()
    if check_input(opt):
        main(opt)
