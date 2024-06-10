import requests
from bs4 import BeautifulSoup

def fetch_page_content(url):
    """Fetch the HTML content of a page."""
    response = requests.get(url)
    response.raise_for_status()  # Check if the request was successful
    return response.text

def parse_examination_data(html_content):
    """Parse the HTML content to extract examination data."""
    soup = BeautifulSoup(html_content, 'html.parser')
    rows = soup.find_all('tr')[3:]  # Skip header rows
    data = []
    
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
            data.append({
                'county': county,
                'school': school,
                'grade': grade,
                'semester': semester,
                'subject_area': subject_area,
                'file_url': file_url
            })
    return data

def get_total_pages(url):
    """Get the total number of pages."""
    html_content = fetch_page_content(url)
    soup = BeautifulSoup(html_content, 'html.parser')
    total_pages = int(soup.select_one('#total_p').get('data-val'))
    return total_pages

def format_results(results):
    """Format the results as a string."""
    formatted_result = "\n".join([
        f"{item['county']} {item['school']} {item['grade']} {item['semester']} {item['subject_area']} {item['file_url']}"
        for item in results
    ])
    return formatted_result

def main():
    base_url = 'https://exam.naer.edu.tw/searchResult.php'
    total_pages = get_total_pages(f'{base_url}?page=1&orderBy=lastest')

    all_results = []
    for i in range(total_pages):
        page_url = f'{base_url}?page={i + 1}&orderBy=lastest'
        html_content = fetch_page_content(page_url)
        page_results = parse_examination_data(html_content)
        all_results.extend(page_results)

    formatted_result = format_results(all_results)
    print(formatted_result)

if __name__ == '__main__':
    main()
