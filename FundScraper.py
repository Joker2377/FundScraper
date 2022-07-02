from FundDetailScraper import *
from FundListScraper import *


class FundScraper:
    def __init__(self):
        self.f1 = FundListScraper()
        self.f2 = FundDetailScraper()
        self.url1 = 'https://www.fundrich.com.tw/new-theme-fund/root.HOT.hot006'  # 單筆top20
        self.url2 = 'https://www.fundrich.com.tw/new-theme-fund/root.HOT.hot13'  # 定額top20
        self.url3 = 'https://www.fundrich.com.tw/new-theme-fund/'  # 全部
        self.url = None
        self.fundList = None

    def setTarget(self, **kwargs):
        if kwargs is None:
            num = input()
        else:
            num = kwargs['num']
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
        if self.url is None:
            print(Color.RED + 'Please set the target before scraping.' + Color.END)
            self.setTarget()
        self.f1.setTargetUrl(self.url)
        self.f1.start()
        self.fundList = self.f1.getFundList()

    def startFundDetailScraping(self):
        if not self.fundList:
            print(Color.RED + 'Get a fundList before starting \"fund detail scraping\".' + Color.END)
        for x in self.fundList:
            id = x.getId()
            self.f2.setTargetFund(id)
            self.f2.start()

            infoList = self.f2.getInfoList()
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
        input(Color.RED + "stop" + Color.END)


if __name__ == '__main__':
    f = FundScraper()
    f.setTarget(num=2)
    f.startFundListScraping()
    f.startFundDetailScraping()
