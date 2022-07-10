import time
from os import system

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from Fund import *


class FundListNetProcess:
    def __init__(self, url):
        self.url = url
        opt = webdriver.EdgeOptions()
        opt.add_argument('log-level=3')
        self.driver = webdriver.Edge(options=opt)
        self.driver.get(self.url)

    def getFundInfo(self):  # 取得清單上的基金資料(代碼、基金名稱)
        while True:
            try:
                wait = WebDriverWait(self.driver, 5)
                wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'tbody')))
                element = self.driver.find_element(By.CLASS_NAME, 'tbody')
                result = element.text
                str = result.split('立即結帳')
                funds = []
                for x in str:
                    s = x.split('\n')
                    newS = []
                    for y in s:
                        if y != '':
                            newS.append(y)
                    if newS:
                        funds.append([newS[0], newS[1]])
                if not funds:
                    continue
                return funds
            except selenium.common.exceptions.NoSuchElementException:
                self.escape()  # 關閉廣告
                print('---Waiting---')
                time.sleep(1)
                self.driver.refresh()
                continue
            except selenium.common.exceptions.TimeoutException:
                self.escape()
                self.driver.refresh()
                continue

    def escape(self):  # 避免廣告視窗干擾運作
        for x in range(3):
            webdriver.ActionChains(self.driver).move_by_offset(0, 0).click().perform()

    def nextPage(self):  # 下一頁
        times = 0
        while True:
            try:
                time.sleep(1)
                wait = WebDriverWait(self.driver, 5)
                btn = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "btn-next")))
                btn.click()
                element = self.driver.find_element(By.CLASS_NAME, "btn-next")
                times = 0
                if element.is_enabled():
                    return True
                else:
                    return False
            except selenium.common.exceptions.ElementClickInterceptedException:
                print('---Waiting---')
                times += 1
                if times > 5:
                    self.escape()
                continue
            except selenium.common.exceptions.TimeoutException:
                self.driver.refresh()
                print('---Waiting---')
                time.sleep(3)
                continue

    def close(self):  # 關閉瀏覽器視窗
        self.driver.close()


class FundListScraper:
    def __init__(self):
        self.fundList = []
        self.url = None

    def setTargetUrl(self, url):
        self.url = url

    def start(self):
        if self.url is None:
            raise ValueError("Url invalid!")
        net = FundListNetProcess(self.url)
        funds = net.getFundInfo()
        fundList = []
        for x in funds:
            f = Fund(x[0], x[1])
            fundList.append(f)
        net.nextPage()
        startTime = time.time()
        oldFunds = []
        while funds:
            system('cls')
            funds = []
            funds = net.getFundInfo()
            if oldFunds == funds:
                continue
            oldFunds = funds
            print("---Processing---")
            newFunds = []
            for x in funds:
                f = Fund(x[0], x[1])
                newFunds.append(f)
            fundList = fundList + newFunds
            if not net.nextPage():
                break

        net.close()
        print(f"Total: {len(fundList)}")
        self.fundList = fundList
        system('cls')
        return

    def getFundList(self):
        return self.fundList
