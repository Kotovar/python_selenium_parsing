from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
import time
from selenium.webdriver.support.ui import Select

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

nifty_bank = driver.find_element(by=By.ID, value="tabList_NIFTYBANK")
nifty_bank.click()
time.sleep(2)

element = driver.find_element(by=By.CSS_SELECTOR, value="a[href='/market-data/live-equity-market?symbol=NIFTY BANK']")
actions.move_to_element(element)
banner = driver.find_element(by=By.CSS_SELECTOR, value="a[onclick='getNifty50Data()']")
actions.move_to_element(banner)
banner.click()
time.sleep(2)

actions.move_to_element(element)
element.click()
time.sleep(2)

list = driver.find_element(by=By.ID, value="equitieStockSelect")
select = Select(list)
select.select_by_visible_text("NIFTY ALPHA 50")
time.sleep(2)

driver.execute_script("window.scrollBy(0, 1000);")
time.sleep(5)


