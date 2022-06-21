from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

driver = webdriver.Edge()
driver.get("https://www.fundrich.com.tw/new-theme-fund/root.HOT.hot13")
element = driver.find_element(By.CLASS_NAME, 'tbody')
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
print(funds)
driver.close()
