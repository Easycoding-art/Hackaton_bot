from os import link
import requests
import bs4
def delete(text) :
    text = str(text)
    res = text.replace('\n', '')
    return res.replace('  ', '')
def mrlim_get_categories() :
    cafe_mrlim_url = 'https://mrlim.ru'
    cafe_mrlim = requests.get(cafe_mrlim_url)
    cafe_mrlim_text = bs4.BeautifulSoup(cafe_mrlim.text, 'lxml')
    categories = cafe_mrlim_text.find_all('a')
    i=1
    categories_list = []
    for category in categories :
        if category != None and i > 1 and i < 13 and category.text != "Завтраки":
            categories_list.append({'catigory' : category.text, 
            'link' : cafe_mrlim_url + category.get('href')})
        i+=1
    return categories_list

def mrlim_get_menu(category_url) :
    cafe_mrlim = requests.get(category_url)
    cafe_mrlim_text = bs4.BeautifulSoup(cafe_mrlim.text, 'lxml')
    categories = cafe_mrlim_text.find_all('span')
    i=1
    categories_list = []
    food_price = [0]*2
    for category in categories :
        if category != None and i > 6 and i < (len(categories))*2 - 3 :
            if (i) % 2 == 0 :
                if list(delete(category.text))[-1] == '₽' :
                    food_price[1] = category.text
                    categories_list.append({'food' : delete(food_price[0]), 
                    'price' : delete(food_price[1])})
                elif delete(category.text) == 'Доступно на альтернативном молоке' :
                    pass
                elif delete(category.text) == 'Обрати ВНИМАНИЕ:' :
                    i+=1
                    pass
                else :
                    food_price[0] = category.text
                    i+=1
            elif (i) % 2 != 0 :
                if list(delete(category.text))[-1] != '₽' and delete(category.text) != 'Доступно на альтернативном молоке' and delete(category.text) != 'Обрати ВНИМАНИЕ:':
                    food_price[0] = category.text
                elif delete(category.text) == 'Доступно на альтернативном молоке' :
                    pass
                elif delete(category.text) == 'Обрати ВНИМАНИЕ:' :
                    pass
        i+=1
    return categories_list