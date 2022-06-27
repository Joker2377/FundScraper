from Func import *

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
input(color.RED+"stop"+color.END)
