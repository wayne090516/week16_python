import requests
from bs4 import BeautifulSoup
import re

def get_exam(page):
    url = f'https://exam.naer.edu.tw/searchResult.php?page={page}&orderBy=lastest&keyword=&selCountry=&selCategory=0&selTech=0&selYear=&selTerm=&selType=&selPublisher='
    res = requests.get(url)
    res.encoding = 'utf-8'
    
    soup = BeautifulSoup(res.text, 'html.parser')
    table = soup.find_all('td', {'bgcolor': '#FFFFFF', 'class': 't4'})
    
    string=""
    i=0 
    while(True):
        if len(table)<=i:
            break
        string = string + table[i+1].get_text() + " " + table[i+2].get_text() + " " + table[i+3].get_text() + " " + table[i+9].find('a').get('href') + "\n"
        i=i+12
    return string

if __name__ == '__main__':
    string=""
    for i in range(1910):
        string+=get_exam(i)
    print(string)
