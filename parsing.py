from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
import time
import csv
from bs4 import BeautifulSoup as BS

options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(options=options)

actions = ActionChains(driver) 

stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )

url = "https://www.nseindia.com"
driver.get(url)
time.sleep(5)

market_data = driver.find_element(by=By.ID, value="link_2")

actions.move_to_element(market_data) 
actions.perform()

market = driver.find_element(By.LINK_TEXT, "Pre-Open Market")
market.click()
time.sleep(3)
table = driver.find_element(by=By.ID, value="livePreTable")
html = table.get_attribute('innerHTML')

soup = BS(html, "html.parser")
tbody = soup.find(name="tbody")
trs = tbody.find_all(name="tr")

with open("output.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Name", "FINAL"])
    for tr in trs:
        tds = tr.find_all(name="td")
        if len(tds) >= 7:
            a = tds[1].find(name="a")
            if a is not None:
                name = a.text
                price = tds[6].text
                writer.writerow([name, price])
            else:
                continue