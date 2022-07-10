from FundScraper import *

f = FundScraper()
f.setTarget(1)
print('Please wait...')
f.startFundListScraping()
f.startFundDetailScraping()
