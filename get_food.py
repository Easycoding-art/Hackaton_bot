import execjs  
import database

def get_js():    
    f = open("order.js", 'r', encoding='UTF-8')  
    line = f.readline()  
    htmlstr = ''  
    while line:  
        htmlstr = htmlstr + line  
        line = f.readline()  
    return htmlstr

def set_order(user) :
    user_info = database.get_user_info(user)
    adress = user_info.get('adress')
    name = user_info.get('name')
    phone = user_info.get('phone')
    order_list = database.get_order(user)
    total = database.get_total(user)
    make_order(order_list, name, phone, adress, total)

def make_order(order_list, name, phone, adress, total) :
    jsstr = get_js()  
    ctx = execjs.compile(jsstr)
    for i in range(len(order_list)) :
        ctx.call('add_to_cart', order_list[i])
    ctx.call('push', total, 'a')
    ctx.call('send_form', name, 'Имя', 'input')
    ctx.call('send_form', phone, '+7', 'input')
    ctx.call('push', 'Изменить', 'a')
    ctx.call('send_form', adress, 'Введите улицу и дом', 'input')
    ctx.call('push', 'Подтвердить адрес', 'button')
    ctx.call('check_all_in_document')
    ctx.call('push', 'Далее', 'button')
    ctx.call('push', 'Оформить заказ', 'button')


    