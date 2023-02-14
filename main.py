import time

from selenium import webdriver
from selenium.webdriver.firefox.options import Options as firefoxOption
from sys import platform
from selenium.webdriver.common.by import By
import loguru
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
from datetime import datetime

card_scrty_code = "your_code"
CellPhone = "your_number"
CheckInDate = "2023/08/13"
MyMail = "your_email"
MyPW = "your_password"
logger = loguru.logger
LoginPage = "https://www.toyoko-inn.com/login/"

headless = True

preferences = {
    "download.prompt_for_download": False,
    "directory_upgrade": True,
    "safebrowsing.enabled": True}


def login():
    options = firefoxOption()
    options.set_preference("browser.download.folderList", 2)
    options.set_preference("browser.download.manager.showWhenStarting", False)
    options.set_preference("browser.helperApps.neverAsk.saveToDisk",
                           "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    # 打開表示背景運作  不開啟瀏覽器
    if headless:
        options.add_argument('--headless')
    options.add_argument("--window-size=1920x1080")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Firefox(executable_path="./geckodriver", options=options)

    ################
    # 有房源後登入訂房
    ################
    driver.get(LoginPage)
    element = driver.find_element(by=By.NAME, value="mail")
    element.send_keys(MyMail)
    element = driver.find_element(by=By.NAME, value="password")
    element.send_keys(MyPW)
    element = driver.find_element(by=By.ID, value="linkLogin")
    driver.execute_script("arguments[0].click();", element)
    logger.info("login successful")
    # time.sleep(3)

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "slct_area")))
    # select area
    select = Select(driver.find_element(by=By.ID, value="slct_area"))
    # select by visible text
    select.select_by_visible_text("Asakusa and Ueno Area")
    # select hotel
    select = Select(driver.find_element(by=By.ID, value="sel_htl"))
    # select by visible text
    select.select_by_visible_text("Toyoko Inn Tokyo Akiba Asakusabashi-eki Higashi-guchi")

    # driver.find_element(by=By.PARTIAL_LINK_TEXT, value="btnLink03").click()
    driver.find_element(by=By.CLASS_NAME, value="btnLink03").click()

    element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "datepicker")))
    element.click()
    js = 'document.getElementById("datepicker").removeAttribute("readonly");'  # js去掉readonly属性
    driver.execute_script(js)
    js_value = 'document.getElementById("datepicker").value="%s"' % CheckInDate  # js添加时间
    driver.execute_script(js_value)
    logger.info(element.get_attribute('value'))
    logger.info("sent date")

    element = driver.find_element(by=By.ID, value="srch_dtl")
    driver.execute_script("arguments[0].click();", element)

    try:
        element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.XPATH, "//a[contains(@onclick, \"submitReserve('%s,00243,1,0,30,DT\")]" % CheckInDate)))
        element.click()

    except Exception as e:
        logger.info(e)
        return False

    # 修改入住者資料
    check = driver.find_element(by=By.NAME, value="reserve_user_same")
    check.click()
    # name
    element = driver.find_element(by=By.NAME, value="room[0][ldgr_fmly_name]")
    element.send_keys("HSU")
    element = driver.find_element(by=By.NAME, value="room[0][ldgr_frst_name]")
    element.send_keys("YILENG")

    # select 人數
    select = Select(driver.find_element(by=By.CLASS_NAME, value="jsSelectPrsnNum"))
    select.select_by_visible_text("2")

    #  加電話
    element = driver.find_element(by=By.NAME, value="room[0][tlpn]")
    element.send_keys(CellPhone)

    # 選check in 時間
    select = Select(driver.find_element(by=By.CLASS_NAME, value="jsCheckinTimes"))
    select.select_by_visible_text("16:00～17:00")

    #  加信用卡驗證碼
    element = driver.find_element(by=By.NAME, value="card_scrty_code")
    element.send_keys(card_scrty_code)

    # confirm
    element = driver.find_element(by=By.CLASS_NAME, value="jsBtnCnfrm")
    element.click()

    # confirm
    element = driver.find_element(by=By.CLASS_NAME, value="jsBtnCnfrm")
    element.click()

    # confirm page的checkbox
    element = driver.find_element(by=By.CLASS_NAME, value="jsCheckboxAgree")
    element.click()  # click Reserve

    # click Reserve
    element = driver.find_element(by=By.ID, value="entry")
    element.click()

    return True


if __name__ == '__main__':
    random.seed(datetime.now().timestamp())
    while True:
        qk = random.randint(600, 900)
        result = login()
        if not result:
            logger.info("沒釋出房源")
            time.sleep(qk)
        else:
            break
