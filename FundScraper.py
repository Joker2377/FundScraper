import json
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
                if len(fundIdList) > 1:
                    for x in fundIdList:
                        if len(x) > 6:
                            x = x[:-1:]
                        if x not in self.fundIdList and len(x) == 6:
                            self.fundIdList.append(x)
                elif len(fundIdList) == 1:
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

    def getFundList(self):
        return self.fundList

    def toJson(self, fundList):
        jsonFundList = []
        for fund in fundList:
            d1 = {'name': fund.name,
                  'id': fund.id,  # 基金代碼
                  'eng_name': fund.infoList[1],  # 英文名稱
                  'general_agent': fund.infoList[2],  # 總代理
                  'company': fund.infoList[3],  # 基金公司
                  'create_date': fund.infoList[4],  # 成立日期
                  'fund_type': fund.infoList[5],  # 基金類型
                  'register_country': fund.infoList[6],  # 基金註冊地
                  'goal': fund.infoList[7],  # 投資目標
                  'original_scale': fund.infoList[8],  # 原始可發行規模(百萬)
                  'scale': fund.infoList[9],  # 基金規模
                  'manage_institution': fund.infoList[10],  # 保管機構
                  'manage_fee': fund.infoList[11],  # 基金保管費率
                  'manage_fee_max': fund.infoList[12],  # 基金管理費率(最高)
                  'earning_distribute': fund.infoList[13],  # 收益分配方式
                  'buying_handling_fee': fund.infoList[14],  # 申購手續費
                  'company_url': fund.infoList[15],  # 公司簡介網址
                  'value_list': fund.valueList,  # 淨值表
                  'earn_list': fund.earnList,  # 績效表現
                  'configure_list': fund.confList,  # 資產配置
                  'industry_proportion': fund.dataList[0],  # 行業比重
                  'risk_evaluate': fund.dataList[1],  # 風險評估
                  'top10_shareholding': fund.dataList[2],  # 前十大持股
                  'risk': fund.risk,  # 風險評等(RR)
                  'dividend': fund.dividend  # 配息紀錄
                  }
            jsonFundList.append(d1)
        jsonStr = json.dumps(jsonFundList, ensure_ascii=False)
        return jsonStr

    def writeJsonfile(self, jsonStr):
        with open('fund_list.json', 'w', encoding='UTF-8') as jsonFile:
            jsonFile.write(str(jsonStr))


if __name__ == '__main__':
    print('---Initializing driver---')
    f = FundScraper()

    #f.startFundListScraping()
    f.startFundDetailScraping(byId=True)
    fundList = f.getFundList()
    jsonStr = f.toJson(fundList)
    f.writeJsonfile(jsonStr)
    input(Color.RED + 'stop' + Color.END)
