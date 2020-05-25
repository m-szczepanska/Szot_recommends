from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

import re


def save_to_txt(book_in_libs):
    '''Save an information in a txt file where the book can be borrow and where
    is currently borrowed. Before saving results to a txt file parse result to
    be easier to understand.'''
    result_strip = book_in_libs.replace('\n', ' ')

    result_available = re.findall(r'\d{2}\s-\s\w+ Dostępny', result_strip)
    available_in_library = set([x.replace(' Dostępny', '') for x in result_available])

    result_not_available = re.findall(r'\d{2}\s-\s\w+ Poza biblioteką', result_strip)
    not_available_in_library = set([x.replace(' Poza biblioteką', '') for x in result_not_available])

    with open(f'{book_name}.txt', 'w+') as file:
        file.write(f'Dostępne - {available_in_library}\nWypożyczone - {not_available_in_library}')

def book_details(driver):
    '''Find the book in MBP Wrocław catalog "Primo". Save result in book_in_libs
    variable.'''
    book_or_books = driver.find_element_by_xpath('//div[3]/div/span')
    if book_or_books.text == 'WIELE WYDAŃ':
        driver.find_element_by_tag_name('prm-brief-result-container').click()
        books_editions = driver.find_elements_by_tag_name('prm-brief-result-container')
        book_in_libs = ''
        for book in range(len(books_editions)):
            books_editions[book].click()
            book_edition = driver.find_element_by_tag_name('md-list').text
            book_in_libs = book_in_libs + str(book_edition)
            driver.back()
            books_editions = driver.find_elements_by_tag_name('prm-brief-result-container')
    else:
        driver.find_element_by_tag_name('prm-brief-result-container').click()
        book_in_libs = driver.find_element_by_tag_name('md-list').text

    save_to_txt(book_in_libs)


def book_record_in_primo(book_name):
    '''Open MBP Wrocław catalog "Primo" in headless mode through
    Selenium Webdriver. Find the named book or return fixed error.'''
    # opts = Options()
    # opts.headless = True

    driver = webdriver.Chrome()
    driver.get("https://primo-48mbp.hosted.exlibrisgroup.com/primo-explore/search?vid=48MBP_VIEW&lang=pl_PL")

    find_book = driver.find_element_by_id("searchBar")
    find_book.clear()
    find_book.send_keys(book_name)
    driver.implicitly_wait(1)
    driver.find_element_by_class_name('md-button.button-confirm').click()
    driver.implicitly_wait(2)

    try:
        book_details(driver)

    except NoSuchElementException as err:
        import pdb; pdb.set_trace()
        if driver.find_element_by_tag_name('prm-no-search-result'):
            print('No books with that title available')
        else:
            print(err)

    driver.close()


book_name = input('Podaj nazwę książki >> ')
book_record_in_primo(book_name)
