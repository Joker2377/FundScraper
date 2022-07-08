from FundScraper import *
from openpyxl import *

# class outputFormat:

if __name__ == '__main__':
    wb = load_workbook('test.xlsx')
    f = FundScraper()
    f.startFundDetailScraping(byId=True)
    d1 = f.readData()
    print(d1)
    if len(d1) == 1:
        d1 = d1[0]
    sheet = wb.create_sheet(d1['name'])
    for key, value in d1.items():
        if type(value) is not list:
            tmp = [key, value]
            sheet.append(tmp)

    wb.save('test.xlsx')
