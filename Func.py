from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from os import system
import time


class color:
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
        self.driver = webdriver.Edge()
        self.driver.get(self.url)
        print("---Waiting---")
        time.sleep(10)

    def returnElement(self):
        element = self.driver.find_element(By.CLASS_NAME, 'tbody')
        return element

    def getFundInfo(self):
        element = self.returnElement()
        result = element.text
        str = result.split('立即結帳')
        funds = []
        for x in str:
            s = x.split('\n')
            newS = []
            for y in s:
                if y != '':
                    newS.append(y)
            funds.append(newS)
        funds = funds[:-1:]
        return funds

    def escape(self):
        for x in range(5):
            webdriver.ActionChains(self.driver).move_by_offset(0, 0).click().perform()

    def nextPage(self):
        element = self.driver.find_element(By.CLASS_NAME, "btn-next")
        element.click()
        if element.is_enabled():
            return True
        else:
            return False

    def close(self):
        self.driver.close()


class FundDetailNetProcess:
    def __init__(self, url):
        self.url = url
        self.driver = webdriver.Edge()
        self.driver.get(self.url)
        print(color.BOLD + "---Waiting---" + color.END)
        time.sleep(3)
        system('cls')

    def setTarget(self, url):
        self.url = url
        self.driver.get(url)

    def returnPage1Element(self):  # 基金資料
        element = self.driver.find_elements(By.CLASS_NAME, 'col-sm-8')
        return element

    def returnPage1Href(self):  # 公司網址
        elements = self.driver.find_elements(By.CSS_SELECTOR, 'td > a')
        href = [elem.get_attribute('href') for elem in elements]
        return href

    def returnPage2Elements(self):  # 淨值表
        element = self.driver.find_element(By.XPATH, "//span[text()='淨值走勢']")
        element.click()
        dateElements = self.driver.find_elements(By.XPATH,
                                                 "//td[@style='padding: 3px; height: 48px; text-align: center; "
                                                 "font-size: 14px; overflow: hidden; white-space: inherit; "
                                                 "text-overflow: inherit; background-color: rgb(240, 240, "
                                                 "237); word-break: break-all; font-weight: 500; line-height: "
                                                 "2.95; letter-spacing: 0.7px; color: rgb(119, 119, 119);']")
        valueElements = self.driver.find_elements(By.XPATH, "//td[@style='padding: 3px; height: 48px; text-align: "
                                                            "center; font-size: 14px; overflow: hidden; white-space: "
                                                            "inherit; text-overflow: inherit; background-color: "
                                                            "inherit; word-break: break-all; font-weight: 500; "
                                                            "line-height: 2.95; letter-spacing: 0.7px; color: rgb("
                                                            "119, 119, 119);']")
        return zip(dateElements, valueElements)

    def returnPage3Elements(self):  # 資產配置
        element = self.driver.find_element(By.XPATH, "//span[text()='資產配置']")
        element.click()
        elements1 = self.driver.find_elements(By.XPATH, "//*[@text-anchor='end']")
        elements2 = self.driver.find_elements(By.XPATH, "//*[@style='background-color: rgb(255, 255, 255); padding: "
                                                        "0px 24px; width: 100%; border-collapse: collapse; "
                                                        "border-spacing: 0px; table-layout: fixed; font-family: "
                                                        "微軟正黑體, \"Microsoft JhengHei\", SimHei, 新細明體, Arial, "
                                                        "Verdana, Helvetica, sans-serif;']")
        return [elements1, elements2]  # 資產配置(股票現金占比)/資產配置頁的其他東西

    def returnPage4Elements(self):  # 風險評等
        self.driver.find_element(By.XPATH, "//span[text()='風險評等']").click()
        element = self.driver.find_element(By.XPATH, "//*[@style='margin: 5px 0px; text-align: center; font-size: "
                                                     "18px; font-weight: 500; line-height: 1.67;']")
        return element

    def returnPage5elements(self):  # 配息紀錄
        self.driver.find_element(By.XPATH, "//span[text()='配息紀錄']").click()
        element = self.driver.find_element(By.XPATH, "//*[contains(text(), '無配息資料')]")
        return element

    def getFundDetail(self):
        elements = self.returnPage1Element()
        infoList = []
        for x in elements:
            str = x.text.split('\n')
            infoList += str
        infoList = infoList[:-7:]
        infoList += self.returnPage1Href()
        return infoList

    def getFundValueList(self):
        data = self.returnPage2Elements()
        dateList = []
        valueList = []
        for elem1, elem2 in data:
            dateList.append(str(elem1.text))
            valueList.append(str(elem2.text))
        c = list(zip(dateList, valueList))
        return c

    def getFundConfigure(self):
        data = self.returnPage3Elements()
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

    def getFundRisk(self):
        element = self.returnPage4Elements()
        return element.text

    def getFundDividend(self):
        element = self.returnPage5elements()
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

    def escape(self):
        for x in range(2):
            webdriver.ActionChains(self.driver).move_by_offset(0, 0).click().perform()

    def close(self):
        self.driver.close()


class FundInfo:
    def __init__(self, *args):
        self.id = args[0]
        self.name = args[1]
        self.info = []
        self.valueList = []
        self.confList = []
        self.dataList = []
        self.risk = None
        self.dividend = None
        for x in args:
            self.info.append(x)
        self.info = self.info[2::]

    def show(self):
        print(color.CYAN + self.id + self.name + color.END)
        print(color.PURPLE+"Info:"+color.END)
        for x in self.info:
            print(x)
        print(color.PURPLE+"Value List:"+color.END)
        for x in self.valueList:
            print(x)
        print(color.PURPLE + "Configure List:" + color.END)
        for x in self.confList:
            print(x)
        print(color.PURPLE + "Data List:" + color.END)
        for x in self.dataList:
            print(x)
        print(color.PURPLE + "Risk:" + color.END)
        print(self.risk)
        print(color.PURPLE + "Dividend:" + color.END)
        if isinstance(self.dividend, str):
            print(self.dividend)
        else:
            for x in self.dividend:
                print(x)
        print('-----------------------------------------------------------')

    def addInfo(self, *args):
        for x in args:
            self.info.append(x)

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
        net.nextPage()
        fundList = funds
        startTime = time.time()
        oldFunds = []
        for fund in funds:
            print(fund[0], fund[1])
        while funds:
            system('cls')
            print(f"time passed: {round(time.time() - startTime)}")
            funds = []
            funds = net.getFundInfo()
            if oldFunds == funds:
                continue
            for fund in funds:
                print(fund[0], fund[1])
            time.sleep(0.5)
            print(color.BOLD + "---Processing---" + color.END)
            time.sleep(0.5)
            net.escape()
            oldFunds = funds
            fundList = fundList + funds
            if not net.nextPage():
                break

        net.close()
        FundList = []
        for fund in fundList:
            f = FundInfo(fund[0], fund[1], fund[2], fund[3], fund[4], fund[5], fund[6],
                         fund[7],
                         fund[8])
            FundList.append(f)
        print(f"Total: {len(FundList)}")
        self.fundList = FundList

    def getFundList(self):
        return self.fundList


class FundDetailScraper:
    def __init__(self, id):
        self.id = id
        self.infoUrl = f"https://www.fundrich.com.tw/fund/{self.id}.html?id={self.id}#%E5%9F%BA%E9%87%91%E8%B3%87%E6%96%99"
        self.infoList = []  # 基金資料
        self.valueList = []  # 近30日淨值表
        self.confList = []  # 資產配置
        self.dataList = []  # 行業比重、風險評估、前十大持股
        self.risk = None
        self.dividend = None
        self.net = FundDetailNetProcess(self.infoUrl)

    def setTargetFund(self, id):
        self.id = id
        self.infoUrl = f"https://www.fundrich.com.tw/fund/{self.id}.html?id={self.id}#%E5%9F%BA%E9%87%91%E8%B3%87%E6%96%99"

    def start(self):
        if self.id is None:
            raise ValueError("Invalid ID")
        self.net.setTarget(self.infoUrl)
        self.net.escape()
        infoList = self.net.getFundDetail()
        self.net.escape()
        valueList = self.net.getFundValueList()
        confData = self.net.getFundConfigure()
        self.net.escape()
        risk = self.net.getFundRisk()
        dividendData = self.net.getFundDividend()
        self.net.escape()
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
