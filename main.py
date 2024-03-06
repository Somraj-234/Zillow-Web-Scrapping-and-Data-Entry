import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

response = requests.get("https://appbrewery.github.io/Zillow-Clone/")
web_html = response.text
# print(web_html)

soup = BeautifulSoup(web_html, "html.parser")
properties = soup.find_all(name="div", class_="StyledPropertyCardDataWrapper")

prop_link_tags = []
prop_price_tags = []
prop_addr_tags = []

for prop_tag in properties:
    link_tag = prop_tag.find("a") # Find the nested <a> tag within the <span>
    price_tag = prop_tag.find(name="span", class_="PropertyCardWrapper__StyledPriceLine")
    addr_tag = prop_tag.find("address")
    if link_tag or price_tag or addr_tag:
        link = link_tag.get("href")
        prop_link_tags.append(link)
        text = price_tag.getText().split("+")[0].split("/")[0]
        prop_price_tags.append(text)
        addr = addr_tag.getText().strip().replace("|", "")
        prop_addr_tags.append(addr)

# print(prop_link_tags)
# print(prop_price_tags)
# print(prop_addr_tags)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

FORM_URL ="https://docs.google.com/forms/d/e/1FAIpQLSd8cQMrScCsY17sOsh82pj2HFlBN5FcURRKlmrYVt16_Oethg/viewform?usp=sf_link"
driver = webdriver.Chrome()

for n in range(len(prop_link_tags)):
    driver.get(FORM_URL)
    time.sleep(2)

    fill_addr = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    fill_price = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    fill_link = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    submit_button = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')

    fill_addr.send_keys(prop_addr_tags[n])
    fill_price.send_keys(prop_price_tags[n])
    fill_link.send_keys(prop_link_tags[n])
    submit_button.click()



