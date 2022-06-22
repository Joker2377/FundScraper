from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from os import system
import time


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
        print("---Waiting---")
        time.sleep(5)

    def returnElements(self):
        element = self.driver.find_elements(By.CLASS_NAME, 'col-sm-8')
        return element

    def getFundDetail(self):
        elements = self.returnElements()
        infoList = []
        for x in elements:
            str = x.text.split('\n')
            infoList += str
        infoList = infoList[:-7:]
        return infoList

    def escape(self):
        for x in range(5):
            webdriver.ActionChains(self.driver).move_by_offset(0, 0).click().perform()

    def close(self):
        self.driver.close()


class FundInfo:
    def __init__(self, **kwargs):
        self.id = kwargs['id']
        self.name = kwargs['name']
        self.data1 = kwargs['d1']  # 3months
        self.data2 = kwargs['d2']  # 6months
        self.data3 = kwargs['d3']  # 1year
        self.data4 = kwargs['d4']  # 2years
        self.data5 = kwargs['d5']  # 3years
        self.data6 = kwargs['d6']  # 5years
        self.data7 = kwargs['d7']  # untilNow

    def show(self):
        print(self.id, self.name)


class FundListScraper:
    def __init__(self, url):
        self.fundList = []
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
            print("---Processing---")
            time.sleep(0.5)
            net.escape()
            oldFunds = funds
            fundList = fundList + funds
            if not net.nextPage():
                break

        net.close()
        FundList = []
        for fund in fundList:
            f = FundInfo(id=fund[0], name=fund[1], d1=fund[2], d2=fund[3], d3=fund[4], d4=fund[5], d5=fund[6],
                         d6=fund[7],
                         d7=fund[8])
            FundList.append(f)
        print(f"Total: {len(FundList)}")
        input("---Scrape Finished---")
        self.fundList = FundList

    def getFundList(self):
        return self.fundList


class FundDetailScraper:
    def __init__(self):
        self.id = None
        self.infoUrl = None

    def setTargetFund(self, id):
        self.id = id
        self.infoUrl = f"https://www.fundrich.com.tw/fund/{self.id}.html?id={self.id}#%E5%9F%BA%E9%87%91%E8%B3%87%E6%96%99"

    def getFundDetail(self):
        if self.id is None:
            raise ValueError("Invalid ID")
        net = FundDetailNetProcess(self.infoUrl)
        net.getFundDetail()
        net.close()



