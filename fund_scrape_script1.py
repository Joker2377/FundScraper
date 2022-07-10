from FundScraper import *

f = FundScraper()
f.setTarget(3)
print('Please wait...')
f.startFundListScraping()
f.startFundDetailScraping()
f.excelOutput()
