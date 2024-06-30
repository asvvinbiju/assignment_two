# #Selenium Library
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service as ChromeService
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.chrome.options import Options
# #Time
# import time

# #Selenium WebDriver for chrome
# chrome_options = Options()
# chrome_options.binary_location = "/home/asvvinbiju/chrome/linux-114.0.5735.90/chrome-linux64/chrome"
# chrome_options.headless = False
# driver = webdriver.Chrome(service=ChromeService("/usr/local/bin/chromedriver"),options=chrome_options)

# def clickload():
#     driver.get('https://www.olx.in/kozhikode_g4058877/for-rent-houses-apartments_c1723')
    
#     #Wait for the properties listing to load
    
#     WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.CLASS_NAME, 'fTZT3'))
#     )
    
#     #Waiting for "loadmore" button to load to avoide unable to find element errors
#     WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.XPATH, '//button[@data-aut-id="btnLoadMore"]'))
#     )
    
#     #Finding "loadmore" button
#     click_button = driver.find_element(By.XPATH, '//button[@data-aut-id="btnLoadMore"]')
    
#     #Waiting until it is clickable
#     WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((By.XPATH, '//button[@data-aut-id="btnLoadMore"]'))
#     )
    
#     #scrolling to button
#     driver.execute_script("arguments[0].scrollIntoView(true);", click_button)
    
#     time.sleep(2)
    
#     click_button.click()
    
#     #Wait for newly loaded properties listing to load
    
#     WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.CLASS_NAME, 'fTZT3'))
#     )
    
#     time.sleep(5)
    
#     driver.quit()
    
    
# clickload()