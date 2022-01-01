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
		
		item1 = types.InlineKeyboardButton('Формулы сокращенного умножения', callback_data='formula')
		item2 = types.InlineKeyboardButton('Sin', callback_data='sh_sin')
		item3 = types.InlineKeyboardButton('Cos', callback_data='sh_cos')
		item4 = types.InlineKeyboardButton('Tg', callback_data='sh_tg')
		item5 = types.InlineKeyboardButton('Ctg', callback_data='sh_ctg')

		markup.add(item1, item2, item3, item4, item5)

		bot.send_message(message.chat.id, 'Выберете шпаргалку',reply_markup = markup)

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
		if call.data == 'sh_sin':
			
			bot.edit_message_text(chat_id=call.message.chat.id, message_id= call.message.message_id, text='Выбери шпаргалку',
			reply_markup=None)
		
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

bot.polling (none_stop=True)

