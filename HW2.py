from bs4 import BeautifulSoup
import requests

def get_latest_examinations(total_pages):

    result = []

    for i in range(total_pages):
        url = f'https://exam.naer.edu.tw/searchResult.php?page={i}&orderBy=lastest&keyword=&selCountry=&selCategory=0&selTech=0&selYear=&selTerm=&selType=&selPublisher='
        res = requests.get(url)

        html_content = res.text

        soup = BeautifulSoup(html_content, 'html.parser')

        rows = soup.find_all('tr')[3:] 

        for row in rows:
            cols = row.find_all('td')
            if len(cols) < 10:
                continue 

            county = cols[0].text.strip()
            school = cols[1].text.strip()
            grade = cols[2].text.strip()
            semester = cols[3].text.strip()
            subject_area = cols[4].text.strip()
            
            file_url = ''
            if cols[9].find('a'):
                file_url = cols[9].find('a')['href'].strip()

            if county and school and grade and semester and subject_area and file_url:
                output = f"{county} {school} {grade} {semester} {subject_area} {file_url}"
                result.append(output)
        
    return result

def result_to_string(result_list):

    all_info = ""

    for info in result_list:
        all_info += "".join(info+"\n")

    return all_info

def main():
    base_url = 'https://exam.naer.edu.tw/searchResult.php'
    
    params = {
        'page': 1,
        'orderBy': 'lastest'
    }

    response = requests.get(base_url, params=params)
    soup = BeautifulSoup(response.content, 'html.parser')

    total_pages = int(soup.select_one('#total_p').get('data-val'))

    result_list = get_latest_examinations(total_pages)
    all_info = result_to_string(result_list)
    print(all_info)

if __name__ == '__main__':
    main()