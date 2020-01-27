import requests
from bs4 import BeautifulSoup
import yaml


def scrape_page(n):
    url = f'http://hanzidb.org/character-list/by-frequency?page={n}'

    res = requests.get(url)

    soup = BeautifulSoup(res.content)

    chars = []
    rows = soup.find_all('tr')


    for row in rows:

        columns = row.find_all('td')

        if len(columns) is not 0:
            chars += columns[0].find_all("a")[0].get_text()



    if(len(chars) != 100):
        print(f"Error: page {n} expected 100 chars, but got {len(chars)}!")
        return


    return chars

#5000 total 
total = 5000
grouping = 5

charset = []
for i in range(total // 100):
    charset += scrape_page(i + 1)

with open('hanzidb.txt', 'w', encoding='utf-8') as fp:
    for i in range(total // grouping):

        category = (i) * grouping
        category = ((category // 100) + 1) * 100
        print(category)
        fp.write(f"//hanzidb/{category}/freq{(i + 1) * grouping}\n")
        for j in range(grouping):
            fp.write(f"{charset[i * grouping + j]}\n")
    

#with open('hanzidb.yaml', 'w', encoding='utf-8') as fp:
#    doc = yaml.dump(charset, fp)