from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import csv

browser = webdriver.Chrome()
browser.get("https://venuewest.eventsair.com/cmspreview/iabse-2019-congress/")
browser.implicitly_wait(2)
element = browser.find_element_by_class_name("desktop")

nav_tabs = []
links = []


def get_modal_content():
    WebDriverWait(browser, 10).until(lambda x: x.find_element_by_class_name('modal-content'))
    tutorial_soup = BeautifulSoup(browser.page_source, 'html.parser')
    modal_title = tutorial_soup.find("div", {"class":"modal-header"})
    modal_body = tutorial_soup.find("div", {"class": "modal-body"})
    modal_title.find('button').decompose()
    author_titles = {}
    try:
        authors = [tag.text.strip() for tag in modal_body.find_all("div", {'class': 'col-sm-3'})]
        titles = [tag.find("h5").text for tag in modal_body.find_all("div", {'class': 'col-sm-9'})]
        author_titles = dict(zip(authors, titles))
    except:
        pass
    string_rep = modal_title.prettify() + modal_body.prettify()
    return string_rep, author_titles


while len(nav_tabs) == 0:
    try:
        nav_tabs = element.find_elements_by_class_name("nav-link")
    except:
        continue

while len(links) == 0:
    try:
        links = element.find_elements_by_class_name("link")
    except:
        continue

tab_names = ['September_3_2019', 'September_4_2019', 'September_5_2019', 'September_6_2019']

master_author_titles = {}
tab_list = []
for tab in nav_tabs:
    tab.click()
    all_string = '<html>'
    for link in links:
        if link.text is not '':
            all_string = all_string + '<h2>' + link.text + '</h2>'
            link.click()
            link_string, author_titles = get_modal_content()
            master_author_titles = {**master_author_titles, **author_titles}
            all_string += link_string
            WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="Close"]'))).click()
    all_string += '</html>'
    tab_list.append(all_string)

browser.quit()

for key, value in master_author_titles.items():
    print(key, value)

for tab in tab_names:
  with open(tab + '.html', 'w') as file:
      file.write(all_string)

with open('master_author_title_list.csv', 'w') as file:
    for key in master_author_titles.keys():
        file.write("%s;%s\n"%(key, master_author_titles[key]))

