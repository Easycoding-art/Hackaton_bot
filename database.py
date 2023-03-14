import pandas as pd
def write(username, id, name, adress, phone_number) :
    data_pd = pd.read_excel('database.xlsx')
    data_pd.drop (data_pd.columns [[0]], axis= 1 , inplace= True )
    if username in data_pd["username"].unique() :
        list = data_pd.index[data_pd['username'] == username].to_list()
        data_pd.at[list[0], 'ID'] = str(id)
        data_pd.at[list[0], 'Адрес'] = adress
        data_pd.at[list[0], 'Имя'] = name
        data_pd.at[list[0], 'Телефон'] = phone_number
        data_pd.at[list[0], 'Заказ'] = ' '
        data_pd.at[list[0], 'Всего'] = '0'
    else :
        data_pd = data_pd.append({'username': username,'ID':id,'Адрес': adress, 'Имя' : name, 'Телефон' : phone_number}, ignore_index=True)
    data_pd.to_excel('database.xlsx')

def get_user_info(username) :
    data_pd = pd.read_excel('database.xlsx')
    data_pd.drop (data_pd.columns [[0]], axis= 1 , inplace= True )
    list = data_pd.index[data_pd['username'] == username].to_list()
    answer = {'adress' : data_pd.iloc[list[0], 1], 
            'name' : data_pd.iloc[list[0], 2], 
            'phone' : data_pd.iloc[list[0], 3]}
    return answer
def write_order(username, food) :
    data_pd = pd.read_excel('database.xlsx')
    data_pd.drop (data_pd.columns [[0]], axis= 1 , inplace= True )

    list = data_pd.index[data_pd['username'] == username].to_list()
    data_pd.at[list[0], 'Заказ'] = data_pd.at[list[0], 'Заказ'] + "#" + food
    data_pd.to_excel('database.xlsx')

def get_order(username) :
    data_pd = pd.read_excel('database.xlsx')
    data_pd.drop (data_pd.columns [[0]], axis= 1 , inplace= True )

    list = data_pd.index[data_pd['username'] == username].to_list()
    order = data_pd.at[list[0], 'Заказ']
    order_list = order.split('#')
    order_list.pop(0)
    return order_list

def set_total(username, value) :
    data_pd = pd.read_excel('database.xlsx')
    data_pd.drop (data_pd.columns [[0]], axis= 1 , inplace= True )

    list = data_pd.index[data_pd['username'] == username].to_list()
    data_pd.at[list[0], 'Всего'] = int(data_pd.at[list[0], 'Всего']) + value
    data_pd.to_excel('database.xlsx')

def get_total(username) :
    data_pd = pd.read_excel('database.xlsx')
    data_pd.drop (data_pd.columns [[0]], axis= 1 , inplace= True )

    list = data_pd.index[data_pd['username'] == username].to_list()
    total = str(data_pd.at[list[0], 'Всего']) + ' ₽'
    return total

def get_id(username) :
    data_pd = pd.read_excel('database.xlsx')
    data_pd.drop (data_pd.columns [[0]], axis= 1 , inplace= True )
 
    list = data_pd.index[data_pd['username'] == username].to_list()

    if len(list) == 0 :
        return 0
    else :
        total = int(data_pd.at[list[0], 'ID'])
        data_pd.at[list[0], 'Заказ'] = ' '
        data_pd.at[list[0], 'Всего'] = '0'
        data_pd.to_excel('database.xlsx')
        return total