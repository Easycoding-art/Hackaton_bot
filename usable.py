def dict_to_list(list, field) :
    arr = []
    for i in range(len(list)) :
        arr.append(list[i].get(field))
    return arr

def delete_price(text) :
    to_deleting = [',', '₽', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    arr = list(text)
    index_list = []
    for i in range(0, len(arr)) :
        if arr[i] in to_deleting :
            index_list.append(i)

    for j in range(0, len(index_list) + 1) :
        arr.pop()
    arr.pop()
    return ''.join(arr)

def delete_food_name(text) :
    to_deleting = list('ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮйцукенгшщзхъфывапролджэячсмитьбю ₽')
    arr = list(text)
    index_list = []
    for i in range(0, len(arr)) :
        if arr[i] in to_deleting :
            index_list.append(i)

    for j in range(0, len(index_list) - 1) :
        arr.pop(0)
    arr.pop()
    arr.pop()
    return int(''.join(arr))