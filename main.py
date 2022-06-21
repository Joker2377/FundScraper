from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from os import system
import time


class NetProcess:
    def __init__(self, url):
        self.url = url
        self.driver = webdriver.Edge()
        self.driver.get(self.url)
        time.sleep(10)

    def returnElements(self):
        element = self.driver.find_element(By.CLASS_NAME, 'tbody')
        return element

    def fundsList(self):
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
        for x in range(3):
            webdriver.ActionChains(self.driver).move_by_offset(0, 0).click().perform()

    def nextPage(self):
        self.driver.find_element(By.CLASS_NAME, "btn-next").click()

    def close(self):
        self.driver.close()


class Fund:
    def __init__(self, **kwargs):
        self.id = kwargs['id']
        self.name = kwargs['name']
        self.data1 = kwargs['d1']
        self.data2 = kwargs['d2']
        self.data3 = kwargs['d3']
        self.data4 = kwargs['d4']
        self.data5 = kwargs['d5']
        self.data6 = kwargs['d6']
        self.data7 = kwargs['d7']

    def show(self):
        print(self.id, self.name)


net = NetProcess("https://www.fundrich.com.tw/new-theme-fund/root.HOT.hot13")
funds = net.fundsList()
net.nextPage()

fundList = funds
start = time.time()
oldFunds = []
while funds:
    system('cls')
    print(f"time passed: {round(time.time() - start)}")
    funds = []
    funds = net.fundsList()
    if oldFunds == funds:
        break
    time.sleep(0.4)
    print("---Processing---")
    time.sleep(0.3)
    net.escape()
    oldFunds = funds
    net.nextPage()
    fundList = fundList + funds

net.close()
FundList = []
for fund in fundList:
    f = Fund(id=fund[0], name=fund[1], d1=fund[2], d2=fund[3], d3=fund[4], d4=fund[5], d5=fund[6], d6=fund[7],
             d7=fund[8])
    FundList.append(f)

for x in FundList:
    x.show()

input("Press any key to leave")
print('\n')
