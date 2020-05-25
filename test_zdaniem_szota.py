import re

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException


'''First part of the project. From "Zdaniem Szota" website the recent book
review is downloaded, parsed and saved in txt file to the further evaluation.'''

opts = Options()
opts.headless = True

driver = webdriver.Chrome()
driver.get("https://zdaniemszota.pl/zrecenzowalismy/2020")

revied_book = driver.find_element_by_xpath('//div[2]/div/a/img').click()
driver.implicitly_wait(1)
book_title_author = driver.find_element_by_xpath('//h1/a').text
review_body = driver.find_element_by_xpath('//article/div[2]/div/div').text


book_title_author = book_title_author.replace('[RECENZJA] ', '')
book_title = re.search(r'\"[\w ]+\"', book_title_author).group()
book_author = book_title_author.replace(f', {book_title}', '')
book_title = book_title[1:-1]

with open(f'{book_title}, {book_author}.txt', 'w+') as file:
    file.write(review_body)


driver.close()
