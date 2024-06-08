import requests
 
# for i in range(1910):
for i in range(1):
    url = f'https://exam.naer.edu.tw/searchResult.php?page={i}&orderBy=lastest&keyword=&selCountry=&selCategory=0&selTech=0&selYear=&selTerm=&selType=&selPublisher='
    res = requests.get(url)
    print(res.text)
