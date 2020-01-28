from operator import itemgetter

import pandas as pd
from bs4 import BeautifulSoup as soup
import csv
import requests

def csv_write(i, file_list):
    select = True
    global file_name
    global objDF
    if i==0:
        file_name = 'itune_scrap.csv'
        objDF = pd.DataFrame(column=['Lst1','lst2','lst3'])
        objDF.to_csv(file_name)

    objDF = objDF.append(
        {'select': select,'Lst1':1}),
    objDF.to_csv(file_name)

def html_parser(i, url):
    item_list = []
    global li
    req = requests.get(url)
    _page_soup = soup(req.content, 'html.parser')
    if i == 0:
        ur = _page_soup.find('ul', {'class': 'list column first'}).find('a')['href']
        html_parser(1, ur)
    elif i == 1:
        list_1 = _page_soup.find('ul', attrs={'class': 'list column first'}).findAll('li')
        list_2 = _page_soup.find('ul', attrs={'class': 'list top-level-subgenres'}).findAll('li')
        li = [i for i in list_1 + list_2 if i not in list_1 or i not in list_2]

    elif i == 3:
        li = _page_soup.find('ul', attrs={'class' : 'list top-level-subgenres'}).findAll('li')

    elif i == 4:
        li = _page_soup.find('div', attrs={'id': 'selectedcontent'}).findAll('li')
    else:
        li = _page_soup

    item_list = li
    return item_list

def main():
    main_url = 'https://podcasts.apple.com/us/genre/podcasts/id26'
    cat_01_list = html_parser(0, main_url)

    for inex1, item1 in enumerate(cat_01_list):
        cat_1 = item1.find('a').text
        cat_1_url = item1.find('a')['href']

        cat_2_list = html_parser(3, cat_1_url)
        #for Loop

        cat_2 = cat_2_list[0].find('a').text
        cat_2_url = cat_2_list[0].find('a')['href']

        cat_3_list = html_parser(4, cat_2_url)
        # for Loop

        cat_3 = cat_3_list[0].find('a').text
        cat_3_url = cat_3_list[0].find('a')['href']

        cat_4_list = html_parser(5, cat_3_url)

        id=''
        postCard_name = cat_3
        postcard_host = cat_4_list.find('span', attrs={'class': 'product-header__identity podcast-header__identity'}).find('a').text.strip()
        postcard_Description = cat_4_list.findAll('p')[1].text
        category = cat_1
        no_of_epsiode = cat_4_list.find('div', attrs={'class': 'product-artwork__caption small-hide medium-show'}).text.strip()
        start_date = ''
        ArtWork = ''
        website = ''
        email = ''
        rss_Feed = ''
        language = ''
        latest_publish_Epsiode_Date = cat_4_list.find('ol', attrs={'class': 'tracks tracks--linear-show'}).find('time').text
        itune_link = cat_3_url
        latest_publish_Epsiode_Title = cat_4_list.find('ol', attrs={'class': 'tracks tracks--linear-show'}).find('a').text.strip()
        recent_pupliched_on_Last_6_weeks = ''            # (Calculate :----  from ' latest_publish_Epsiode_Date ' in rarge : Y/N )
        rating = cat_4_list.find('span', attrs={'class': 'we-star-rating-stars we-star-rating-stars-5'}).text.strip()

###          write_to_csv(    ---- ---- --- -- --- -- --- -- -)

if __name__ == '__main__':
    main()
