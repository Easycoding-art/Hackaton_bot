import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton,\
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.exceptions import  ChatNotFound
import food_parser
import database
import usable
import get_food

API_TOKEN = 'TOKEN'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot,  storage=storage)
button1 = KeyboardButton('Сделать заказ')
button2 = KeyboardButton('Изменить данные')
greet_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(button1, button2)
reply_markup_delete=types.ReplyKeyboardRemove()

class Form(StatesGroup):
    name = State() 
    adress = State()
    phone_number = State()

class ID(StatesGroup) :
    id = State()

def generate_markup(data): # передаём в функцию data

    markup = ReplyKeyboardMarkup(resize_keyboard=True) # создаём клавиатуру
    markup.row_width = 1 # кол-во кнопок в строке
    for i in range(len(data)): # цикл для создания кнопок
        markup.add(KeyboardButton(data[i])) #Создаём кнопки, i[1] - название, i[2] - каллбек дата
    return markup #возвращаем клавиатуру

@dp.message_handler(text=['Сделать заказ', 'Назад'])
async def buy(message: types.Message):
    data = usable.dict_to_list(food_parser.mrlim_get_categories(), 'catigory')
    await bot.send_message(message.from_user.id, 'Список:', reply_markup=generate_markup(data))

@dp.message_handler(text=['Оформить заказ'])
async def buy(message: types.Message):
    await ID.id.set()
    await message.reply('Пожалуйста, напишите usename', reply_markup=reply_markup_delete)
    '''
    if len(list(total_price)) >= 6 :
        get_food.set_order(message.from_user.username)
        await bot.send_message(message.from_user.id, 'Заказ отправлен!', reply_markup=greet_kb)
    else :
        await bot.send_message(message.from_user.id, 
                        'Заказ должен быть на сумму больше, чем 1000 рублей. У вас ' + total_price, 
                        reply_markup=greet_kb)
    '''

@dp.message_handler(state=ID.id)
async def process(message: types.Message, state: FSMContext):
    async with state.proxy() as answer:
        answer['id'] = message.text
    id = database.get_id(answer['id'])
    if id == 0 :
        await message.reply('Пользователь не зарегистрирован...', reply_markup=greet_kb)
    else :
        try :
            await bot.send_message(id, ' ')
        except ChatNotFound:
            await message.reply('Пользователь не зарегистрирован...', reply_markup=greet_kb)
        else :
            total_price = database.get_total(str(message.from_user.username))
            order_list = database.get_order(str(message.from_user.username))
            message_text = 'Пользователь ' + message.from_user.first_name + ' ' + message.from_user.last_name + 'Прислал вам свои пожелания\n'
            for i in range(len(order_list)) :
                message_text = message_text + order_list[i] + '\n'
            message_text = message_text + 'Стоимость выбранного: ' + total_price
            await bot.send_message(id, message_text)
            await message.reply('Заказ отправлен!', reply_markup=greet_kb)
    await state.finish()

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await Form.name.set()
    await message.reply("Пожалуйста, введите имя.", reply_markup=reply_markup_delete)

@dp.message_handler(text = "Изменить данные")
async def send_welcome(message: types.Message):
    await Form.name.set()
    await message.reply("Пожалуйста, введите имя.", reply_markup=reply_markup_delete)

# Сюда приходит ответ с именем

@dp.message_handler(state=Form.name)
async def process_name1(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await Form.next()
    await message.reply("Пожалуйста, введите адрес доставки.")

@dp.message_handler(state=Form.adress)
async def process_name2(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['adress'] = message.text

    await Form.next()
    await message.reply("Пожалуйста, введите номер телефона без 8.")

@dp.message_handler(state=Form.phone_number)
async def process_name3(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone_number'] = message.text

    await message.reply("Спасибо за регистрацию!", reply_markup=greet_kb)
    database.write(str(message.from_user.username), 
                message.from_user.id,
                str(data['name']), 
                str(data['adress']), 
                str(data['phone_number']))
    await state.finish()

@dp.message_handler(commands=['help'])
async def send_message(message: types.Message):
    await message.reply('Для заказа еды просто нажми кнопку "заказать"\n Потом выбери понравившееся блюдо\n Если бот сломался, пиши /feedback', reply_markup=greet_kb)

@dp.message_handler()
async def send_message(message: types.Message):
    data = usable.dict_to_list(food_parser.mrlim_get_categories(), 'catigory')
    links = usable.dict_to_list(food_parser.mrlim_get_categories(), 'link')
    all_food =[]
    for n in range(len(links)) :
        element = food_parser.mrlim_get_menu(links[n])
        food_name = usable.dict_to_list(element, 'food')
        food_price = usable.dict_to_list(element, 'price')
        for a in range(len(food_name)) :
            all_food.append(food_name[a] + ', ' + food_price[a])

    if message.text in data: 
        i = 0
        while data[i] != message.text :
            i+=1
        menu = food_parser.mrlim_get_menu(links[i])
        food = usable.dict_to_list(menu, 'food')
        price = usable.dict_to_list(menu, 'price')
        result = ['Назад', 'Оформить заказ']
        for j in range(len(food)) :
            result.append(food[j] + ', ' + price[j])
        await bot.send_message(message.from_user.id, 'Меню:', reply_markup=generate_markup(result))
    
    elif message.text in all_food :
        order = usable.delete_price(message.text)
        value = usable.delete_food_name(message.text)
        database.write_order(str(message.from_user.username), str(order))
        database.set_total(str(message.from_user.username), value)
        await message.reply('Добавлено в корзину...') 
    else:
        await message.reply("Я не понимаю тебя. Нажми на одну из кнопок или напиши /help", reply_markup=greet_kb)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)