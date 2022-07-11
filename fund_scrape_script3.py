from FundScraper import *

f = FundScraper()
f.setTarget(2)
print('Please wait...')
f.startFundListScraping()
f.startFundDetailScraping()
f.excelOutput()
