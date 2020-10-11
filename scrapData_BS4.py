from bs4 import BeautifulSoup as soup
from urllib.request import urlopen 
import csv
import re


def getDep_links(contaiter):
    links = []
    titles = []
    links_ = contaiter.findAll("a")
    for link in links_:
        titles.append(link.text)
        links.append(link.get("href"))
    return titles, links


def goToDep(dept_url):
    depClient = urlopen(dept_url)
    dept_page = depClient.read()
    depClient.close()
    dept_soup = soup(dept_page, "html.parser")
    teachers_con = dept_soup.findAll("li", {"class":"item item-designer test"})


faculty_url = "https://faculty.daffodilvarsity.edu.bd/"
uClient = urlopen(faculty_url)
page_faculty = uClient.read()
uClient.close()

faculty_soup = soup(page_faculty, "html.parser")

facultys_container = faculty_soup.findAll("div",{"class":"columns-col columns-col-6"})

container0 = facultys_container[1]
# container0_titles = facultys_container[0].text

# print(container0_titles)


titles , links = getDep_links(container0)

#goto to dep
goToDep(links)


    
