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

    def returnElements(self):
        element = self.driver.find_element(By.CLASS_NAME, 'tbody')
        return element

    def getFundInfo(self):
        element = self.returnElements()
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

    def returnPage1Element(self):
        element = self.driver.find_elements(By.CLASS_NAME, 'col-sm-8')
        return element

    def returnPage1Href(self):
        elements = self.driver.find_elements(By.CSS_SELECTOR, 'td > a')
        href = [elem.get_attribute('href') for elem in elements]
        return href

    def getFundDetail(self):
        elements = self.returnPage1Element()
        infoList = []
        for x in elements:
            str = x.text.split('\n')
            infoList += str
        infoList = infoList[:-7:]
        print(color.GREEN + "---Data received---" + color.END + infoList[0])
        infoList += self.returnPage1Href()
        return infoList

    def escape(self):
        for x in range(5):
            webdriver.ActionChains(self.driver).move_by_offset(0, 0).click().perform()

    def close(self):
        self.driver.close()


class FundInfo:
    def __init__(self, *args):
        self.id = args[0]
        self.name = args[1]
        self.info = []
        for x in args:
            self.info.append(x)
        self.info = self.info[2::]

    def show(self):
        print(self.id, self.name, self.info)

    def add(self, *args):
        for x in args:
            self.info.append(x)

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
        self.infoList = []
        self.net = FundDetailNetProcess(self.infoUrl)

    def setTargetFund(self, id):
        self.id = id
        self.infoUrl = f"https://www.fundrich.com.tw/fund/{self.id}.html?id={self.id}#%E5%9F%BA%E9%87%91%E8%B3%87%E6%96%99"

    def start(self):
        if self.id is None:
            raise ValueError("Invalid ID")
        self.net.setTarget(self.infoUrl)
        infoList = self.net.getFundDetail()
        self.net.escape()
        self.infoList = infoList

    def getInfoList(self):
        return self.infoList

    def close(self):
        self.net.close()
