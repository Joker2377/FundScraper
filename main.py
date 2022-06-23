import Func as f

f1 = f.FundListScraper()
f1.setTargetUrl("https://www.fundrich.com.tw/new-theme-fund/root.HOT.hot006")
f1.start()

fundList = f1.getFundList()
f2 = f.FundDetailScraper(fundList[0].getId())
for x in fundList:
    id = x.getId()
    f2.setTargetFund(id)
    f2.start()
    infoList = f2.getInfoList()
    for info in infoList:
        x.add(info)

for x in fundList:
    print(x.show())
input(f.color.RED+"stop"+f.color.END)
