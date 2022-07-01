import time
from os import system

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class color:  # text colors
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


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
                print(color.RED + '---Waiting---' + color.END)
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
                print(color.RED + '---Waiting---' + color.END)
                times += 1
                if times > 5:
                    self.escape()
                continue
            except selenium.common.exceptions.TimeoutException:
                self.driver.refresh()
                print(color.RED + '---Waiting---' + color.END)
                time.sleep(3)
                continue

    def close(self):  # 關閉瀏覽器視窗
        self.driver.close()


class FundDetailNetProcess:
    def __init__(self, url):
        self.url = url
        opt = webdriver.EdgeOptions()
        opt.add_argument('log-level=3')
        opt.headless = True
        self.driver = webdriver.Edge(options=opt)
        self.driver.get(self.url)
        print(color.BOLD + "---Waiting---" + color.END)
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
                print(color.RED + '---Waiting---' + color.END)
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
                print(color.RED + '---Waiting---' + color.END)
                time.sleep(1)
                self.driver.refresh()
                continue
            except selenium.common.exceptions.TimeoutException:
                self.driver.refresh()
                continue

    def getEarn(self):  # 績效表現 developing...
        wait = WebDriverWait(self.driver, 5)
        btn = wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()='績效表現']")))
        btn.click()
        element = self.driver.find_element(By.XPATH,
                                           "//div[@style='width: 100%; padding-bottom: 45px; display: inline-block;']//div[@class='row']")
        print(element.text)

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
                print(color.RED + '---Waiting---' + color.END)
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
                print(color.RED + '---Waiting---' + color.END)
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
                print(color.RED + '---Waiting---' + color.END)
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


class FundInfo:
    def __init__(self, *args):
        self.id = args[0]
        self.name = args[1]
        self.infoList = []
        self.valueList = []
        self.confList = []
        self.dataList = []
        self.earnList = []
        self.risk = None
        self.dividend = None

    def show(self):
        print(color.CYAN + self.id + ' ' + self.name + color.END)
        print(color.PURPLE + "Info:" + color.END)
        for x in self.infoList:
            print(x)
        print('\n\n')
        print(color.PURPLE + "Value List:" + color.END)
        for x in self.valueList:
            print(x)
        print('\n\n')
        print(color.PURPLE + "Configure List:" + color.END)
        for x in self.confList:
            print(x)
        print('\n\n')
        print(color.PURPLE + "Data List:" + color.END)
        for x in self.dataList:
            print(x)
        print('\n\n')
        print(color.PURPLE + "Risk:" + color.END)
        print(self.risk)
        print('\n\n')
        print(color.PURPLE + "Dividend:" + color.END)
        if isinstance(self.dividend, str):
            print(self.dividend)
        else:
            for x in self.dividend:
                print(x)
        print('-----------------------------------------------------------')

    def addInfo(self, *args):
        for x in args:
            self.infoList.append(x)

    def setValueList(self, listOfValue: list):
        self.valueList = listOfValue

    def setConfList(self, confList):
        self.confList = confList

    def setDataList(self, dataList):
        self.dataList = dataList

    def setRisk(self, risk):
        self.risk = risk

    def setDividend(self, dividend):
        self.dividend = dividend

    def setEarnList(self, earnList):
        self.earnList = earnList

    def getId(self):
        return self.id


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
            f = FundInfo(x[0], x[1])
            fundList.append(f)
        net.nextPage()
        startTime = time.time()
        oldFunds = []
        while funds:
            system('cls')
            print(f"time passed: {round(time.time() - startTime)}")
            funds = []
            funds = net.getFundInfo()
            if oldFunds == funds:
                continue
            oldFunds = funds
            for fund in funds:
                print(f"{funds.index(fund) + 1}. {fund[0]} {fund[1]}")
            print(color.BOLD + "---Processing---" + color.END)
            newFunds = []
            for x in funds:
                f = FundInfo(x[0], x[1])
                newFunds.append(f)
            fundList = fundList + newFunds
            if not net.nextPage():
                break

        net.close()
        print(f"Total: {len(fundList)}")
        self.fundList = fundList
        return

    def getFundList(self):
        return self.fundList


class FundDetailScraper: # earnList not added
    def __init__(self, id):
        self.id = id
        self.infoUrl = f"https://www.fundrich.com.tw/fund/{self.id}.html?id={self.id}#%E5%9F%BA%E9%87%91%E8%B3%87%E6%96%99"
        self.infoList = []  # 基金資料
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
        infoList = self.net.getFundDetail()
        valueList = self.net.getFundValueList()
        confData = self.net.getFundConfigure()
        risk = self.net.getFundRisk()
        dividendData = self.net.getFundDividend()
        self.infoList = infoList
        self.valueList = valueList
        self.confList = confData[0]
        self.dataList = confData[1]
        self.risk = risk
        self.dividend = dividendData
        print(color.GREEN + "---Data received---" + color.END + infoList[0])

    def getInfoList(self):
        return self.infoList

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


class FundScraper:
    def __init__(self):
        self.f1 = FundListScraper()
        self.url1 = 'https://www.fundrich.com.tw/new-theme-fund/root.HOT.hot006'  # 單筆top20
        self.url2 = 'https://www.fundrich.com.tw/new-theme-fund/root.HOT.hot13'  # 定額top20
        self.url3 = 'https://www.fundrich.com.tw/new-theme-fund/'  # 全部
        self.url = None

    def setTarget(self, num: int):
        print(color.RED + 'Target set: ' + color.END, end='')
        if num == 1:
            print(color.DARKCYAN + '單筆top20' + color.END)
            self.url = self.url1
        elif num == 2:
            print(color.DARKCYAN + '定額top20' + color.END)
            self.url = self.url2
        elif num == 3:
            print(color.DARKCYAN + '全部' + color.END)
            self.url = self.url3
        else:
            print(color.RED + 'nothing' + color.END)

    def getListOfFunds(self):
        if self.url is None:
            print(color.RED + 'Please set the target before scraping.' + color.END)
        self.f1.start()


if __name__ == '__main__':
    f1 = FundListScraper()
    f1.setTargetUrl("https://www.fundrich.com.tw/new-theme-fund/root.HOT.hot006")
    f1.start()

    fundList = f1.getFundList()
    f2 = FundDetailScraper(fundList[0].getId())
    for x in fundList:
        id = x.getId()
        f2.setTargetFund(id)
        f2.start()

        infoList = f2.getInfoList()
        valueList = f2.getValueList()
        confList = f2.getConflist()
        dataList = f2.getDataList()
        risk = f2.getRisk()
        dividend = f2.getDividend()

        x.setValueList(valueList)
        x.setConfList(confList)
        x.setDataList(dataList)
        x.setRisk(risk)
        x.setDividend(dividend)
        for info in infoList:
            x.addInfo(info)

    for x in fundList:
        print(x.show())
    input(color.RED + "stop" + color.END)
