from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from selenium.common.exceptions import NoSuchElementException

driver = webdriver.Chrome('/usr/bin/chromedriver')

names = []
categories = []
ratings = []
prices = []
in_stocks = []
livros =[]
driver.get("http://books.toscrape.com/")

content = driver.page_source
soup = BeautifulSoup(content, 'html.parser')
livros = driver.find_element_by_xpath("//*[@id='default']/div/div/div/aside/div[2]/ul/li/ul").text.split('\n')
livros = list(map(lambda x: x.replace(' ', '-'), livros))
livros = list(map(str.lower, livros))

cont = 2
for livro in livros:
    cont = str(cont)
    url = driver.get("http://books.toscrape.com/catalogue/category/books/" + livro + "_" + cont + "/index.html")
    npag = 1
    try:
     npag = driver.find_element_by_xpath(
         '//*[@id="default"]/div/div/div/div/section/div[2]/div/ul/li[1]').text
     npag = int(npag[10])
    except NoSuchElementException:
        npag = 1

    for item in range(1,npag+1):
        item = str(item)

        if npag < 2 :
            url = driver.get("http://books.toscrape.com/catalogue/category/books/" + livro + "_" + cont + "/index.html")
        else:
            url = driver.get("http://books.toscrape.com/catalogue/category/books/" + livro + "_" + cont + "/page-" + item +".html")

        for a in soup.findAll('article'):
            name = a.find('img')
            name = name['alt']
            names.append(name)

            rating = a.find('p')
            rating = rating['class'][1]
            ratings.append(rating)

            price = a.find('p', class_='price_color').text
            prices.append(price)

            in_stock = a.find('p', class_='instock availability').text.strip()
            in_stocks.append(in_stock)

            categories.append(livro)

    cont = int(cont)
    cont = cont + 1

#Salvando o scrapping no Daframe
data = pd.DataFrame()
data['book_name'] = names
data['star_rating'] = ratings
data['price'] = prices
data['categories'] = categories
data['stock_availability'] = in_stocks

data.to_csv('books.csv', index=True)





