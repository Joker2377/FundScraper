from FundDetailScraper import *
from FundListScraper import *


class FundScraper:
    def __init__(self):
        self.f1 = None
        self.f2 = None
        self.url1 = 'https://www.fundrich.com.tw/new-theme-fund/root.HOT.hot006'  # 單筆top20
        self.url2 = 'https://www.fundrich.com.tw/new-theme-fund/root.HOT.hot13'  # 定額top20
        self.url3 = 'https://www.fundrich.com.tw/new-theme-fund/'  # 全部
        self.url = None
        self.fundList = []
        self.fundIdList = []
        self.driverInitializeOrNot = False

    def initializeDriver(self):
        self.f1 = FundListScraper()
        self.f2 = FundDetailScraper()
        self.driverInitializeOrNot = True

    def setTarget(self):
        print('1. 單筆top20\n2. 定額top20\n3. 全部: ')
        num = int(input())
        print(Color.RED + 'Target set: ' + Color.END, end='')
        if num == 1:
            print(Color.DARKCYAN + '單筆top20' + Color.END)
            self.url = self.url1
        elif num == 2:
            print(Color.DARKCYAN + '定額top20' + Color.END)
            self.url = self.url2
        elif num == 3:
            print(Color.DARKCYAN + '全部' + Color.END)
            self.url = self.url3
        else:
            print(Color.RED + 'nothing' + Color.END)

    def startFundListScraping(self):
        if not self.driverInitializeOrNot:
            self.initializeDriver()
        self.setTarget()
        if self.url is None:
            print(Color.RED + 'Please set the target before scraping.' + Color.END)
            self.setTarget()
        self.f1.setTargetUrl(self.url)
        self.f1.start()
        self.fundList = self.f1.getFundList()
        fundIdList = []
        for x in self.fundList:
            fundIdList.append(x.getId())
        self.fundIdList = fundIdList
        self.writeFundIdList()

    def readFundIdList(self):
        try:
            with open('fund_id_list.txt', 'r', newline='') as file:
                fundIdList = file.readlines()
                if len(fundIdList) >1:
                    for x in fundIdList:
                        if len(x) > 6:
                            x = x[:-1:]
                        if x not in self.fundIdList and len(x) == 6:
                            self.fundIdList.append(x)
                else:
                    if len(fundIdList[0]) > 6:
                        fundIdList[0] = fundIdList[0][:-1:]
                    if fundIdList[0] not in self.fundIdList and len(fundIdList[0]) == 6:
                        self.fundIdList.append(fundIdList[0])
        except FileNotFoundError:
            with open('fund_id_list.txt', 'x', newline='') as file:
                pass

    def writeFundIdList(self):
        self.readFundIdList()
        with open('fund_id_list.txt', 'w', newline='') as file:
            print(self.fundIdList)
            for id in self.fundIdList:
                file.write(id)
                file.write('\n')

    def startFundDetailScraping(self, **kwargs):
        if not self.driverInitializeOrNot:
            self.initializeDriver()
        self.readFundIdList()
        if not self.fundList and not self.fundIdList:
            print(Color.RED + 'Get a fundList or fundIdList before starting \"fund detail scraping\".' + Color.END)

        if len(kwargs) < 1:
            if not self.fundList:
                print(Color.RED + 'Get a fundList before starting \"fund detail scraping by fundList\".' + Color.END)
            for x in self.fundList:
                id = x.getId()
                self.f2.setTargetFund(id)
                self.f2.start()

                infoList = self.f2.getInfoList()
                if x.name is None:
                    x.setName(infoList[0])
                x.setValueList(self.f2.getValueList())
                x.setEarnList(self.f2.getEarnList())
                x.setConfList(self.f2.getConflist())
                x.setDataList(self.f2.getDataList())
                x.setRisk(self.f2.getRisk())
                x.setDividend(self.f2.getDividend())
                for info in infoList:
                    x.addInfo(info)
            for x in self.fundList:
                x.show()

        elif kwargs['byId']:
            fundList = []
            for x in self.fundIdList:
                fundList.append(Fund(x))
            self.fundList = fundList
            self.startFundDetailScraping()

        input(Color.RED + "stop" + Color.END)

    def getFundList(self):
        return self.fundList


if __name__ == '__main__':
    f = FundScraper()
    #f.startFundListScraping()
    f.startFundDetailScraping(byId=True)
    input(Color.RED + 'stop' + Color.END)
