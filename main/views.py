from django.shortcuts import render
from django.http import HttpResponse

import requests
from bs4 import BeautifulSoup


def main_page(request):
    return render(request, 'main\MainPage.html')

def model_page(request):

    # Something
    HOST = 'https://outmaxshop.ru/'
    URL =  'https://outmaxshop.ru/clothes'
    
    URL2 = 'https://outmaxshop.ru/novinki-new'
    URL3 = 'https://outmaxshop.ru/accessories'
    URL4 = 'https://outmaxshop.ru/catalog/sezon--zima'
    HEADERS = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 OPR/92.0.0.0'
    }

    # Functions
    def get_html(url, params=''):
        r = requests.get(url, headers= HEADERS,params=params)
        return r

    def get_content(html):
        soup = BeautifulSoup(html, 'html.parser')
        items = soup.find_all('a', class_ ='catalog-product__item')
        clothes = []
        for item in items:
            clothes.append(
                {
                    'name':item.find('div', class_ ='catalog-item__name catalog-item__name--catalog').get_text(strip =True),
                    #'link':item.find('a', class_='data-layer-click').get_href(),
                    'price_y_dis':item.find('div', class_ ='catalog-item__price catalog-item__price--catalog catalog-item__price--red').get_text(strip =True),
                    'dis':item.find('div', class_ ='catalog-product__label').get_text(strip =True),
                    'price_n_dis':item.find('div', class_ ='catalog-item__price catalog-item__price--catalog catalog-item__price--line').get_text(strip =True),
                    'article':item.find('div', class_ ='catalog-item__articul catalog-item__articul--catalog catalog-item__articul--with-instock').get_text(strip =True),
                    #'img': item.find('div', class_ ='catalog-item__img catalog-item__img--horizontal').get('href')
                }
            )
        return clothes
    
    def parser(url,pagination):
        

        PAGENATTION = pagination * 40
        #PAGENATTION = int(PAGENATTION.strip())
        html = get_html(url)
        if html.status_code == 200:
            cards = []
            for page in range(1,PAGENATTION,40):
                print(f'Парсим страницу:{(round(page//40))+1}')
                html = get_html(url, params = {'page': page})
                cards.extend(get_content(html.text))
            print(cards)
            return cards
        else:
            print("Сайт полёг!!!")
            return ['Problem with connet']


    answer = []
    v = False

    if request.method == 'POST':
        try:
            POSTdict = request.POST.dict()
            pag = int((POSTdict.get('count')))
            pagination = (POSTdict.get('list1'))
            print(pagination)
            print(type(pagination))
            if (pagination == 'Новинки'):
                answer = parser(URL2,pag)
                v = True
            if (pagination == 'Одежда'):
                answer = parser(URL,pag)
                v = True
            if (pagination == 'Аксессуары'):
                answer = parser(URL3,pag)
                v = True
            if (pagination == 'Зима'):
                answer = parser(URL4,pag)
                v = True

            
        except:
            answer = ['Error in processing']
            v = False

    return render(request, 'main\ModelPage.html', {'v': v, 'answer': answer})

def contacts_page(request):
    return render(request, 'main\ContactsPage.html')