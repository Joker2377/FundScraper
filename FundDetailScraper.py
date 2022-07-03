import time
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from os import system

from Color import *


class FundDetailNetProcess:
    def __init__(self, url):
        self.url = url
        opt = webdriver.EdgeOptions()
        opt.add_argument('log-level=3')
        opt.headless = True
        self.driver = webdriver.Edge(options=opt)
        self.driver.get(self.url)
        print(Color.BOLD + "---Waiting---" + Color.END)
        time.sleep(3)
        system('cls')

    def setTarget(self, url):
        self.url = url
        self.driver.get(url)

    def getFundDetail(self):  # 基金資料
        while True:
            try:
                wait = WebDriverWait(self.driver, 5)
                wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'col-sm-8')))
                elements = self.driver.find_elements(By.CLASS_NAME, 'col-sm-8')

                infoList = []
                for x in elements:
                    str = x.text.split('\n')
                    infoList += str
                infoList = infoList[:-7:]

                elements = self.driver.find_elements(By.CSS_SELECTOR, 'td > a')  # 公司網址
                href = [elem.get_attribute('href') for elem in elements]

                infoList += href
                return infoList
            except selenium.common.exceptions.ElementClickInterceptedException:
                self.escape()
                continue
            except selenium.common.exceptions.NoSuchElementException:
                print(Color.RED + '---Waiting---' + Color.END)
                time.sleep(1)
                self.driver.refresh()
                continue
            except selenium.common.exceptions.TimeoutException:
                self.driver.refresh()
                continue

    def getFundValueList(self):  # 淨值表
        while True:
            try:
                wait = WebDriverWait(self.driver, 5)
                btn = wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()='淨值走勢']")))
                btn.click()
                dateElements = self.driver.find_elements(By.XPATH,
                                                         "//td[@style='padding: 3px; height: 48px; text-align: center; "
                                                         "font-size: 14px; overflow: hidden; white-space: inherit; "
                                                         "text-overflow: inherit; background-color: rgb(240, 240, "
                                                         "237); word-break: break-all; font-weight: 500; line-height: "
                                                         "2.95; letter-spacing: 0.7px; color: rgb(119, 119, 119);']")
                valueElements = self.driver.find_elements(By.XPATH,
                                                          "//td[@style='padding: 3px; height: 48px; text-align: "
                                                          "center; font-size: 14px; overflow: hidden; white-space: "
                                                          "inherit; text-overflow: inherit; background-color: "
                                                          "inherit; word-break: break-all; font-weight: 500; "
                                                          "line-height: 2.95; letter-spacing: 0.7px; color: rgb("
                                                          "119, 119, 119);']")
                dateList = []
                valueList = []
                for x in dateElements:
                    dateList.append(str(x.text))
                for x in valueElements:
                    valueList.append(str(x.text))
                c = list(zip(dateList, valueList))
                if not c:
                    self.driver.refresh()
                    continue
                return c
            except selenium.common.exceptions.ElementClickInterceptedException:
                self.escape()
                continue
            except selenium.common.exceptions.NoSuchElementException:
                print(Color.RED + '---Waiting---' + Color.END)
                time.sleep(1)
                self.driver.refresh()
                continue
            except selenium.common.exceptions.TimeoutException:
                self.driver.refresh()
                continue

    def getEarn(self):  # 績效表現
        wait = WebDriverWait(self.driver, 5)
        btn = wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()='績效表現']")))
        btn.click()
        element = self.driver.find_element(By.XPATH,
                                           "//div[@style='width: 100%; padding-bottom: 45px; display: "
                                           "inline-block;']//div[@class='row']")
        ls = element.text.split('\n')
        re = []
        for x in ls:
            c = x.split()
            if tuple(c) not in re:
                if len(c) == 3:
                    c = [c[0], c[1]+c[2]]
                c = tuple(c)
                re.append(c)
        return re

    def getFundConfigure(self):  # 資產配置
        while True:
            try:
                wait = WebDriverWait(self.driver, 5)
                btn = wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()='資產配置']")))
                btn.click()
                elements1 = self.driver.find_elements(By.XPATH, "//*[@text-anchor='end']")
                elements2 = self.driver.find_elements(By.XPATH,
                                                      "//*[@style='background-color: rgb(255, 255, 255); padding: "
                                                      "0px 24px; width: 100%; border-collapse: collapse; "
                                                      "border-spacing: 0px; table-layout: fixed; font-family: "
                                                      "微軟正黑體, \"Microsoft JhengHei\", SimHei, 新細明體, Arial, "
                                                      "Verdana, Helvetica, sans-serif;']")

                data = [elements1, elements2]  # 資產配置(股票現金占比)/資產配置頁的其他東西
                confList = []
                dataList = []
                for x in data[0]:
                    tmp = x.text.split()
                    c = tuple([tmp[0], tmp[1]])
                    confList.append(c)
                for x in data[1]:
                    if x.text != '':
                        s = x.text.split('\n')
                        dataList.append(s)
                newDataList = []
                lst = []
                for x in dataList[0]:
                    if dataList[0].index(x) > 0:
                        tmp = x.split()
                        value = tmp[-1]
                        tmp = tmp[:-1:]
                        str1 = ""
                        for y in tmp:
                            str1 += y + " "
                        c = tuple([str1, value])
                        lst.append(c)
                    else:
                        c = tuple(x.split())
                        lst.append(c)
                newDataList.append(lst)
                lst = []
                for x in dataList[1]:
                    if dataList[1].index(x) > 0:
                        tmp = x.split()
                        unit = tmp[0]
                        value = tmp[1::]
                        c = tuple([unit, value])
                        lst.append(c)
                    else:
                        c = tuple(x.split())
                        lst.append(c)
                newDataList.append(lst)
                lst = []
                for x in dataList[2]:
                    if dataList[2].index(x) > 0:
                        tmp = x.split()
                        value = tmp[-1]
                        tmp = tmp[:-1:]
                        str1 = ""
                        for y in tmp:
                            str1 += y + " "
                        c = tuple([str1, value])
                        lst.append(c)
                    else:
                        c = tuple(x.split())
                        lst.append(c)
                newDataList.append(lst)
                return [confList, newDataList]
            except selenium.common.exceptions.ElementClickInterceptedException:
                self.escape()
                continue
            except selenium.common.exceptions.NoSuchElementException:
                print(Color.RED + '---Waiting---' + Color.END)
                time.sleep(1)
                self.driver.refresh()
                continue
            except selenium.common.exceptions.TimeoutException:
                self.driver.refresh()
                continue

    def getFundRisk(self):  # 風險評等
        while True:
            try:
                wait = WebDriverWait(self.driver, 5)
                btn = wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()='風險評等']")))
                btn.click()
                element = self.driver.find_element(By.XPATH,
                                                   "//*[@style='margin: 5px 0px; text-align: center; font-size: "
                                                   "18px; font-weight: 500; line-height: 1.67;']")
                return element.text
            except selenium.common.exceptions.ElementClickInterceptedException:
                self.escape()
                continue
            except selenium.common.exceptions.NoSuchElementException:
                print(Color.RED + '---Waiting---' + Color.END)
                time.sleep(1)
                self.driver.refresh()
                continue
            except selenium.common.exceptions.TimeoutException:
                self.driver.refresh()
                continue

    def getFundDividend(self):  # 配息紀錄
        while True:
            try:
                wait = WebDriverWait(self.driver, 5)
                btn = wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()='配息紀錄']")))
                btn.click()
                element = self.driver.find_element(By.XPATH, "//*[contains(text(), '無配息資料')]")
                if element.get_attribute('style') == 'display: none;':
                    elements = self.driver.find_elements(By.XPATH,
                                                         "//*[@style='background-color: rgb(255, 255, 255); padding: 0px "
                                                         "24px; width: 100%; border-collapse: collapse; border-spacing: 0px; "
                                                         "table-layout: fixed; font-family: 微軟正黑體, \"Microsoft JhengHei\", "
                                                         "SimHei, 新細明體, Arial, Verdana, Helvetica, sans-serif;']")
                    b = None
                    for elem in elements:
                        a = elem.text.split('\n')
                        b = []
                        for item in a:
                            c = item.split()
                            if c:
                                c = tuple(c)
                                b.append(c)

                    return b
                else:
                    return '無配息資料'
            except selenium.common.exceptions.ElementClickInterceptedException:
                self.escape()
                continue
            except selenium.common.exceptions.NoSuchElementException:
                print(Color.RED + '---Waiting---' + Color.END)
                time.sleep(3)
                continue
            except selenium.common.exceptions.TimeoutException:
                self.driver.refresh()
                continue

    def escape(self):
        for x in range(2):
            webdriver.ActionChains(self.driver).move_by_offset(0, 0).click().perform()

    def close(self):
        self.driver.close()


class FundDetailScraper:  # earnList not added
    def __init__(self, **kwargs):
        if not kwargs:
            self.id = 'ALI006'  # 參考基金，用以建立driver instance
        else:
            self.id = kwargs['id']
        self.infoUrl = f"https://www.fundrich.com.tw/fund/{self.id}.html?id={self.id}#%E5%9F%BA%E9%87%91%E8%B3%87%E6%96%99"
        self.infoList = []  # 基金資料
        self.earnList = []  # 績效表現
        self.valueList = []  # 近30日淨值表
        self.confList = []  # 資產配置
        self.dataList = []  # 行業比重、風險評估、前十大持股
        self.risk = None  # 風險評等
        self.dividend = None  # 配息紀錄
        self.net = FundDetailNetProcess(self.infoUrl)

    def setTargetFund(self, id):
        self.id = id
        self.infoUrl = f"https://www.fundrich.com.tw/fund/{self.id}.html?id={self.id}#%E5%9F%BA%E9%87%91%E8%B3%87%E6%96%99"

    def start(self):
        if self.id is None:
            raise ValueError("Invalid ID")
        self.net.setTarget(self.infoUrl)
        self.infoList = self.net.getFundDetail()
        self.earnList = self.net.getEarn()
        self.valueList = self.net.getFundValueList()
        self.confList = self.net.getFundConfigure()[0]
        self.dataList = self.net.getFundConfigure()[1]
        self.risk = self.net.getFundRisk()
        self.dividend = self.net.getFundDividend()
        print(Color.GREEN + "---Data received---" + Color.END + self.infoList[0])

    def getInfoList(self):
        return self.infoList

    def getEarnList(self):
        return self.earnList

    def getValueList(self):
        return self.valueList

    def getConflist(self):
        return self.confList

    def getDataList(self):
        return self.dataList

    def getRisk(self):
        return self.risk

    def getDividend(self):
        return self.dividend

    def close(self):
        self.net.close()
