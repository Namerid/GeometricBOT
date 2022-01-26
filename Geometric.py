import telebot
from telebot import REPLY_MARKUP_TYPES, types
import config 
import math
import re
import requests

bot = telebot.TeleBot(config.TOKEN)

def form(string):
	massiv = list(string)
	while True:
		if string == '0.0000':
			massiv = '0'
			break	
		if massiv[-1] == '0' or massiv[-1] == '.':
			massiv.pop(-1)
		else:
			break
	return ''.join(massiv)

def check(text):
	massiv = list(text)
	check_massiv = ['y', 'x', '=', '(', ')', '*','/', '-', '+', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '^']
	for i in massiv:
		if i in check_massiv:
			ans = True
		else:
			ans = False
	return ans

def googleSearch(query):
    with requests.session() as c:
        url = 'https://www.google.com/search'
        query = {'q': query}
        urllink = requests.get(url, params=query)
    return urllink.url

def func1(string):
	if len(re.findall('y',string)) <= 1 and len(re.findall('=',string)) <= 1 and check(string) == True and len(string)>=3:	
		if len(re.findall('x',string)) > 0 or len(re.findall('y',string)) > 0:
			answer = True
		else:
			answer = False
	else:
		answer = False
	return answer



@bot.message_handler(commands = ['start'])
def start(message):

	sti = open('st/sticker.tgs','rb')
	bot.send_sticker(message.chat.id,sti)
	
	journal = open('journal.txt', 'r')
	dictionary = eval(journal.read())
	journal.close()
	dictionary['{.id}'.format(message.from_user)] = ''
	journal = open('journal.txt', 'w')
	journal.write(str(dictionary))
	journal.close()

	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	item1 = types.KeyboardButton('Преобразование ед.')
	item2 = types.KeyboardButton('Построение графика функции')
	item3 = types.KeyboardButton('Шпаргалка')
	item4 = types.KeyboardButton('Тригонометрические функции')
	markup.add(item1, item2, item3, item4)

	bot.send_message(message.chat.id, 'Привет, {.first_name}, я геометрический бот, что делать?'.format(message.from_user) , reply_markup=markup)

@bot.message_handler(content_types=['text'])
def lalala(message):
	check_massiv = ['Тригонометрические функции', 'Преобразование ед.', 'Шпаргалка', 'Построение графика функции']
	journal = open('journal.txt', 'r')
	dictionary = eval(journal.read())
	journal.close()
	
	if dictionary['{.id}'.format(message.from_user)] == 'sin' and message.text not in check_massiv:
		try:
			text = form('{:.4f}'.format( math.sin(math.radians(float(re.sub(',','.',message.text))))))
		except ValueError:
			text = 'Ошибка, это не число⚠️❗️'
		bot.send_message(message.chat.id, text)

	if dictionary['{.id}'.format(message.from_user)] == 'cos' and message.text not in check_massiv:
		try:
			text = form('{:.4f}'.format( math.cos(math.radians(float(re.sub(',','.',message.text))))))
		except ValueError:
			text = 'Ошибка, это не число⚠️❗️'
		bot.send_message(message.chat.id, text)

	if dictionary['{.id}'.format(message.from_user)] == 'tg' and message.text not in check_massiv:
		try:
			text = form('{:.4f}'.format( math.tan(math.radians(float(re.sub(',','.',message.text))))))
		except ValueError:
			text = 'Ошибка, это не число⚠️❗️'
		bot.send_message(message.chat.id, text)

	if dictionary['{.id}'.format(message.from_user)] == 'ctg' and message.text not in check_massiv:
		try:
			text = form('{:.4f}'.format(math.cos(math.radians(float(re.sub(',','.',message.text)))) / math.sin(math.radians(float(re.sub(',','.',message.text))))))
		except ValueError:
			text = 'Ошибка, это не число⚠️❗️'
		bot.send_message(message.chat.id, text)

	if dictionary['{.id}'.format(message.from_user)] == 'dtr' and message.text not in check_massiv:
		try:
			text = form('{:.4f}'.format(math.radians(float(re.sub(',','.',message.text)))))
		except ValueError:
			text = 'Ошибка, это не число⚠️❗️'
		bot.send_message(message.chat.id, text)

	if dictionary['{.id}'.format(message.from_user)] == 'rtd' and message.text not in check_massiv:
		try:
			text = form('{:.4f}'.format(math.degrees(float(re.sub(',','.',message.text)))))
		except ValueError:
			text = 'Ошибка, это не число⚠️❗️'
		bot.send_message(message.chat.id, text)

	if dictionary['{.id}'.format(message.from_user)] == 'graph' and message.text not in check_massiv: 
		if func1(message.text) == True and len(message.text)<=32:
			text = googleSearch(re.sub(',','.',message.text))
		else:
			text = 'Ошибка⚠️❗️'
		bot.send_message(message.chat.id, text)

	if message.text == 'Тригонометрические функции':
		markup = types.InlineKeyboardMarkup(row_width=1)
		
		item1 = types.InlineKeyboardButton('sin', callback_data='r_sin')
		item2 = types.InlineKeyboardButton('cos', callback_data='r_cos')
		item3 = types.InlineKeyboardButton('tg', callback_data='r_tg')
		item4 = types.InlineKeyboardButton('ctg', callback_data='r_ctg')
		markup.add(item1, item2, item3, item4)

		bot.send_message(message.chat.id, 'Выберете функцию', reply_markup = markup)
				
	if message.text == 'Преобразование ед.':
		markup = types.InlineKeyboardMarkup(row_width=1)
		
		item1 = types.InlineKeyboardButton('Радианы в градусы', callback_data='rtd')
		item2 = types.InlineKeyboardButton('Градусы в радианы', callback_data='dtr')
		markup.add(item1, item2)

		bot.send_message(message.chat.id, 'Выберете единицы измерения', reply_markup = markup)

	if message.text == 'Шпаргалка':
		markup = types.InlineKeyboardMarkup(row_width=1)
		
		item1 = types.InlineKeyboardButton('Алгебра', callback_data='алгебра')
		item2 = types.InlineKeyboardButton('Геометрия', callback_data='геометрия')
	
		markup.add(item1, item2)

		bot.send_message(message.chat.id, 'Выберете шпаргалку:',reply_markup = markup)

		journal = open('journal.txt', 'r')
		dictionary = eval(journal.read())
		journal.close()
		dictionary['{.id}'.format(message.from_user)] = ''
		journal = open('journal.txt', 'w')
		journal.write(str(dictionary))
		journal.close()

	if message.text == 'Построение графика функции':
		bot.send_message(message.chat.id, 'Введите функцию (пример: y=x^2):')
		journal = open('journal.txt', 'r')
		dictionary = eval(journal.read())
		journal.close()
		dictionary['{.id}'.format(message.from_user)] = 'graph'
		journal = open('journal.txt', 'w')
		journal.write(str(dictionary))
		journal.close()

	if dictionary['{.id}'.format(message.from_user)] == '' and message.text not in check_massiv:
		bot.send_message(message.chat.id, 'Я не знаю, что делать🤷‍♂️?')

@bot.callback_query_handler(func=lambda call: True)
def choose(call):
	if call.message:
		
		if call.data == 'pr_back':
			bot.edit_message_text(chat_id=call.message.chat.id, message_id= call.message.message_id, text='Введите значение:',
			reply_markup=None)

			markup = types.InlineKeyboardMarkup(row_width=1)
		
			item1 = types.InlineKeyboardButton('Радианы в градусы', callback_data='rtd')
			item2 = types.InlineKeyboardButton('Градусы в радианы', callback_data='dtr')
			markup.add(item1, item2)

			bot.send_message(call.message.chat.id, 'Выберете единицы измерения', reply_markup = markup)

			journal = open('journal.txt', 'r')
			dictionary = eval(journal.read())
			journal.close()
			dictionary['{.id}'.format(call.from_user)] = ''
			journal = open('journal.txt', 'w')
			journal.write(str(dictionary))
			journal.close()

		if call.data == 'trig_back':
			bot.edit_message_text(chat_id=call.message.chat.id, message_id= call.message.message_id, text='Введите значение(градусы):',
			reply_markup=None)

			markup = types.InlineKeyboardMarkup(row_width=1)
			
			item1 = types.InlineKeyboardButton('sin', callback_data='r_sin')
			item2 = types.InlineKeyboardButton('cos', callback_data='r_cos')
			item3 = types.InlineKeyboardButton('tg', callback_data='r_tg')
			item4 = types.InlineKeyboardButton('ctg', callback_data='r_ctg')
			markup.add(item1, item2, item3, item4)

			bot.send_message(call.message.chat.id, 'Выберете функцию', reply_markup = markup)

			journal = open('journal.txt', 'r')
			dictionary = eval(journal.read())
			journal.close()
			dictionary['{.id}'.format(call.from_user)] = ''
			journal = open('journal.txt', 'w')
			journal.write(str(dictionary))
			journal.close()

		if call.data == 'r_sin':
			markup = types.InlineKeyboardMarkup(row_width=1)
			item1 = types.InlineKeyboardButton('назад', callback_data='trig_back')
			markup.add(item1)

			bot.send_message(call.message.chat.id, 'Введите значение(градусы):',reply_markup = markup)
			
			journal = open('journal.txt', 'r')
			dictionary = eval(journal.read())
			journal.close()
			dictionary['{.id}'.format(call.from_user)] = 'sin'
			journal = open('journal.txt', 'w')
			journal.write(str(dictionary))
			journal.close()

			bot.edit_message_text(chat_id=call.message.chat.id, message_id= call.message.message_id, text='Выберете функцию',
			reply_markup=None)
		
		if call.data == 'r_cos':
			markup = types.InlineKeyboardMarkup(row_width=1)
			item1 = types.InlineKeyboardButton('назад', callback_data='trig_back')
			markup.add(item1)

			bot.send_message(call.message.chat.id, 'Введите значение(градусы):',reply_markup = markup)
			
			journal = open('journal.txt', 'r')
			dictionary = eval(journal.read())
			journal.close()
			dictionary['{.id}'.format(call.from_user)] = 'cos'
			journal = open('journal.txt', 'w')
			journal.write(str(dictionary))
			journal.close()

			bot.edit_message_text(chat_id=call.message.chat.id, message_id= call.message.message_id, text='Выберете функцию',
			reply_markup=None)

		if call.data == 'r_tg':
			markup = types.InlineKeyboardMarkup(row_width=1)
			item1 = types.InlineKeyboardButton('назад', callback_data='trig_back')
			markup.add(item1)

			bot.send_message(call.message.chat.id, 'Введите значение(градусы):',reply_markup = markup)

			journal = open('journal.txt', 'r')
			dictionary = eval(journal.read())
			journal.close()
			dictionary['{.id}'.format(call.from_user)] = 'tg'
			journal = open('journal.txt', 'w')
			journal.write(str(dictionary))
			journal.close()

			bot.edit_message_text(chat_id=call.message.chat.id, message_id= call.message.message_id, text='Выберете функцию',
			reply_markup=None)

		if call.data == 'r_ctg':
			markup = types.InlineKeyboardMarkup(row_width=1)
			item1 = types.InlineKeyboardButton('назад', callback_data='trig_back')
			markup.add(item1)

			bot.send_message(call.message.chat.id, 'Введите значение(градусы):',reply_markup = markup)

			journal = open('journal.txt', 'r')
			dictionary = eval(journal.read())
			journal.close()
			dictionary['{.id}'.format(call.from_user)] = 'ctg'
			journal = open('journal.txt', 'w')
			journal.write(str(dictionary))
			journal.close()

			bot.edit_message_text(chat_id=call.message.chat.id, message_id= call.message.message_id, text='Выберете функцию',
			reply_markup=None)

		if call.data == 'rtd':
			markup = types.InlineKeyboardMarkup(row_width=1)
			item1 = types.InlineKeyboardButton('назад', callback_data='pr_back')
			markup.add(item1)

			bot.send_message(call.message.chat.id, 'Введите значение:',reply_markup = markup)

			journal = open('journal.txt', 'r')
			dictionary = eval(journal.read())
			journal.close()
			dictionary['{.id}'.format(call.from_user)] = 'rtd'
			journal = open('journal.txt', 'w')
			journal.write(str(dictionary))
			journal.close()

			bot.edit_message_text(chat_id=call.message.chat.id, message_id= call.message.message_id, text='Выберете единицы измерения',
			reply_markup=None)

		if call.data == 'dtr':
			markup = types.InlineKeyboardMarkup(row_width=1)
			item1 = types.InlineKeyboardButton('назад', callback_data='pr_back')
			markup.add(item1)

			bot.send_message(call.message.chat.id, 'Введите значение:',reply_markup = markup)

			journal = open('journal.txt', 'r')
			dictionary = eval(journal.read())
			journal.close()
			dictionary['{.id}'.format(call.from_user)] = 'dtr'
			journal = open('journal.txt', 'w')
			journal.write(str(dictionary))
			journal.close()

			bot.edit_message_text(chat_id=call.message.chat.id, message_id= call.message.message_id, text='Выберете единицы измерения',
			reply_markup=None)
		

		if call.data == 'алгебра':

			markup = types.InlineKeyboardMarkup(row_width=1)
		
			item1 = types.InlineKeyboardButton('Основные формулы', callback_data='основные формулы')
			item2 = types.InlineKeyboardButton('Уравнения', callback_data='уравнения')
			item3 = types.InlineKeyboardButton('Неравенства', callback_data='неравенства')
			item4 = types.InlineKeyboardButton('Функции', callback_data='функции')
			item5 = types.InlineKeyboardButton('Прогрессия', callback_data='прогрессия')
			item6 = types.InlineKeyboardButton('Производная', callback_data='производная')
			item7 = types.InlineKeyboardButton('Первообразная Интеграл', callback_data='первообразная интеграл')
			item8 = types.InlineKeyboardButton('Комбинаторика', callback_data='комбинаторика')
	
			markup.add(item1, item2, item3, item4, item5, item6, item7, item8)

			
			bot.edit_message_text(chat_id=call.message.chat.id, message_id = call.message.message_id, text='Выберете шпаргалку:',
			reply_markup=markup)


		if call.data == 'основные формулы':

			markup = types.InlineKeyboardMarkup(row_width=1)
		
			item1 = types.InlineKeyboardButton('Формулы сокращенного умножения', callback_data='формулы сокращенного умножения')
			item2 = types.InlineKeyboardButton('Дискриминант', callback_data='дискриминант')
			item3 = types.InlineKeyboardButton('т. Виета', callback_data='т. Виета')
			item4 = types.InlineKeyboardButton('Тригонометрические функции', callback_data='тригонометрические функции')
	
			markup.add(item1, item2, item3, item4)

			
			bot.edit_message_text(chat_id=call.message.chat.id, message_id = call.message.message_id, text='Выберете шпаргалку:',
			reply_markup=markup)
		
			
		if call.data == 'формулы сокращенного умножения':
			
			bot.send_photo(call.message.chat.id, open('photo/formula.png','rb'))
			
			bot.edit_message_text(chat_id=call.message.chat.id, message_id = call.message.message_id, text='Выберете шпаргалку:',
			reply_markup=None)

		if call.data == 'дискриминант':
		
			bot.send_photo(call.message.chat.id, open('photo/Дискриминант.png','rb'))
			
			bot.edit_message_text(chat_id=call.message.chat.id, message_id = call.message.message_id, text='Выберете шпаргалку:',
			reply_markup=None)

		if call.data == 'т. Виета':

			bot.send_photo(call.message.chat.id, open('photo/т. Виета.png','rb'))
			
			bot.edit_message_text(chat_id=call.message.chat.id, message_id = call.message.message_id, text='Выберете шпаргалку:',
			reply_markup=None)

		if call.data == 'тригонометрические функции':
			
			bot.send_photo(call.message.chat.id, open('photo/треугольник.png', 'rb'))
			bot.send_photo(call.message.chat.id, open('photo/табл. треугольник.png', 'rb'))
			bot.send_photo(call.message.chat.id, open('photo/табл. тригонометрические функции.png', 'rb'))
			bot.send_photo(call.message.chat.id, open('photo/тригонометрические формулы.png', 'rb'))
			bot.send_photo(call.message.chat.id, open('photo/тригонометрические формулы2.png', 'rb'))

			bot.edit_message_text(chat_id=call.message.chat.id, message_id= call.message.message_id, text='Выбери шпаргалку',
			reply_markup=None)

		
		if call.data == 'уравнения':
			
			markup = types.InlineKeyboardMarkup(row_width=1)
		
			item1 = types.InlineKeyboardButton('Кв. уравнение', callback_data='кв. уравнение')
			
	
			markup.add(item1)

			
			bot.edit_message_text(chat_id=call.message.chat.id, message_id = call.message.message_id, text='Выберете шпаргалку:',
			reply_markup=markup)

		

		if call.data == 'кв. уравнение':
			
			bot.send_photo(call.message.chat.id, open('photo/кв. уравнение.png','rb'))
			
			bot.edit_message_text(chat_id=call.message.chat.id, message_id = call.message.message_id, text='Выберете шпаргалку:',
			reply_markup=None)



		if call.data == 'геометрия':
			
			markup = types.InlineKeyboardMarkup(row_width=1)
		
			item1 = types.InlineKeyboardButton('Планиметрия', callback_data='планиметрия')
			item2 = types.InlineKeyboardButton('Стереометрия', callback_data='стереометрия')
		
	
			markup.add(item1, item2)

			
			bot.edit_message_text(chat_id=call.message.chat.id, message_id = call.message.message_id, text='Выберете шпаргалку:',
			reply_markup=markup)


		if call.data == 'планиметрия':
			
			markup = types.InlineKeyboardMarkup(row_width=1)
		
			item1 = types.InlineKeyboardButton('Простые фигуры на плоскости', callback_data='простые фигуры на плоскости')
			item2 = types.InlineKeyboardButton('Треугольники', callback_data='треугольники')
			item3 = types.InlineKeyboardButton('Четырехугольники', callback_data='четырехугольники')
			item4 = types.InlineKeyboardButton('Окружность и круг', callback_data='окружность и круг')
			item5 = types.InlineKeyboardButton('Площади фигур', callback_data='площади фигур')
			item6 = types.InlineKeyboardButton('Векторы', callback_data='векторы')
			item7 = types.InlineKeyboardButton('Геометрические преобразования на плоскости', callback_data='геом. преобразования на плоскости')
	
			markup.add(item1, item2, item3, item4, item5, item6, item7)

			
			bot.edit_message_text(chat_id=call.message.chat.id, message_id = call.message.message_id, text='Выберете шпаргалку:',
			reply_markup=markup)


		if call.data == 'стереометрия':

			markup = types.InlineKeyboardMarkup(row_width=1)
		
			item1 = types.InlineKeyboardButton('Многогранники', callback_data='многогранники')
			item2 = types.InlineKeyboardButton('Тела вращения', callback_data='тела вращения')
		
	
			markup.add(item1, item2)

			
			bot.edit_message_text(chat_id=call.message.chat.id, message_id = call.message.message_id, text='Выберете шпаргалку:',
			reply_markup=markup)


		if call.data == 'многогранники':

			markup = types.InlineKeyboardMarkup(row_width=1)
		
			item1 = types.InlineKeyboardButton('Призма', callback_data='призма')
			item2 = types.InlineKeyboardButton('Пирамида', callback_data='пирамида')
		
	
			markup.add(item1, item2)

			
			bot.edit_message_text(chat_id=call.message.chat.id, message_id = call.message.message_id, text='Выберете шпаргалку:',
			reply_markup=markup)


		if call.data == 'тела вращения':

			markup = types.InlineKeyboardMarkup(row_width=1)
		
			item1 = types.InlineKeyboardButton('Цилиндр', callback_data='цилиндр')
			item2 = types.InlineKeyboardButton('Конус', callback_data='конус')
			item3 = types.InlineKeyboardButton('Шар', callback_data='шар')
		
	
			markup.add(item1, item2, item3)

			
			bot.edit_message_text(chat_id=call.message.chat.id, message_id = call.message.message_id, text='Выберете шпаргалку:',
			reply_markup=markup)


bot.polling (none_stop=True)

