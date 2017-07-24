#!/usr/bin/env python
# -*- coding: utf-8 -*-

import telebot
import telebot.types as types

import re
import cash
import botan
import config
import chisla_fun

#import configTest as config
bot = telebot.TeleBot(config.token)

# Инлайн-режим с непустым запросом
@bot.inline_handler(lambda query: len(query.query) > 0)
def query_text(query):
    #botan.track(config.botan_key, query.from_user.id, {}, 'inline запрос')
    kb = types.InlineKeyboardMarkup()
    # Добавляем колбэк-кнопку с содержимым "test"
    kb.add(types.InlineKeyboardButton(text="Нажми меня", callback_data="test"))
    results = []
    single_msg = types.InlineQueryResultArticle(
        id="1", title="Press me",
        input_message_content=types.InputTextMessageContent(message_text="Решил проверить, что я умею?)"),
        reply_markup=kb
    )
    results.append(single_msg)
    bot.answer_inline_query(query.id, results)

#Если сообщение на которое тыкнули из инлайн-режима
@bot.callback_query_handler(lambda call: call.inline_message_id)
def callback_inline(call):
    if call.inline_message_id:
        if call.data == "test":
            bot.edit_message_text(inline_message_id=call.inline_message_id, text="Бдыщь")

# Если сообщение из чата с ботом
@bot.callback_query_handler(lambda call: call.message)
def callback_inline(call):
    if call.data == "test":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=call.message.text)
        text = 'Добро пожаловать!\nВыберите интересующий вас раздел:'
        keyboardStart = telebot.types.InlineKeyboardMarkup()
        callback_button0 = telebot.types.InlineKeyboardButton(text="Клиент", callback_data="cl")
        callback_button1 = telebot.types.InlineKeyboardButton(text="Гость", callback_data="g")
        keyboardStart.add(callback_button0,callback_button1)
        bot.send_message(call.message.chat.id, text,reply_markup=keyboardStart)
    if call.data == "cl":
        text = "Для записи на консультацию *позвоните* по номеру:\n\n[+79165127377](tel:+79165127377)"
        # bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=call.message.text)
        bot.send_message(call.message.chat.id, text, parse_mode='Markdown')
    if call.data == "g":
        text = "Для посчёта вашего числа введите полностью *ФИО* или *дату рождения*.\nДата рождения в формате:\n*ГГГГ ММ ДД* или *ДД ММ ГГГГ*"
        # bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=call.message.text)
        bot.send_message(call.message.chat.id, text, parse_mode='Markdown')
    if call.data == "sll":
        keyboard = telebot.types.InlineKeyboardMarkup()
        for text in cash.keyb["students"]:
            callback_button = telebot.types.InlineKeyboardButton(text=text, callback_data=cash.keyb["students"][text])
            keyboard.add(callback_button)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=call.message.text)
        bot.send_message(call.message.chat.id, text='Вы Выбрали раздел Студент.', reply_markup=keyboard)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    botan.track(config.botan_key, message.chat.id, message, '/start')
    text = 'Добро пожаловать!\nЯ помогу тебе разобраться с числами!\nВыберите интересующий вас раздел:'
    keyboardStart = telebot.types.InlineKeyboardMarkup()
    callback_button0 = telebot.types.InlineKeyboardButton(text="Посчитать моё число", callback_data="g")
    callback_button1 = telebot.types.InlineKeyboardButton(text="Записаться на консультацию", callback_data="cl")
    keyboardStart.add(callback_button0)
    keyboardStart.add(callback_button1)
    bot.send_message(message.chat.id, text, reply_markup=keyboardStart)

@bot.message_handler(commands=['help'])
def send_help(message):
    botan.track(config.botan_key, message.chat.id, message, '/help')
    text = 'Помошь:\n/help - это сообещние\n/about - о боте\n\nДля содсчёт "собственного числа имени" введите ФИО полностью.\nДля подсчёта "собственного числа даты вождения" введите дату рождения в формате ДД ММ ГГГГ или ГГГГ ММ ДД.'
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['about'])
def send_about(message):
    botan.track(config.botan_key, message.chat.id, message, '/about')
    text = 'Бот предназначен для помощи в посчёте "своих чисел".\nОбратная связь/разработчик: @pa_antya'
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['test'])
def send_help(message):
    #botan.track(config.botan_key, message.chat.id, message, '/test')
    text = "Бот работает"
    keyboardTest = telebot.types.InlineKeyboardMarkup()
    callback_button_test = telebot.types.InlineKeyboardButton(text="ok!", callback_data="ok")
    keyboardTest.add(callback_button_test)
    bot.send_message(message.chat.id, text, reply_markup=keyboardTest)

# Обычный режим
@bot.message_handler(content_types=["text"])
def any_msg(message):
    print(message.text)
    pdate = re.compile(r'(\d{1,4})[\-_:;\\\|\/ ,.]{0,}(\d{1,2})[\-_:;\\\|\/ ,.]{0,}(\d{1,4})')
    pfio = re.compile(r'([a-zA-ZА-Яа-яёЁ\-\s]{2,})')

    mfio = pfio.match(message.text)
    mdate = pdate.match(message.text)

    print(mfio)
    print(mdate)
    if (mfio or mdate):
        if mdate:
            print('Match found: "{}"'.format(mdate.group()))
            chislo = chisla_fun.date(message)
        if mfio:
            print('Match found: "{}"'.format(mfio.group()))
            chislo = chisla_fun.fio(message)
        text = 'Вы ввели: *{}*\nВыше число: *{}*'.format(message.text, chislo)
        bot.send_message(message.chat.id, text, parse_mode='Markdown')
    else:
        text = 'Введены *не верные* данные.\nПерепроверьте, пожалуйста:\n{}\n*Если* данные *верные* - свяжитесь с разработчиком в раздете /about.'.format(message.text)
        bot.send_message(message.chat.id, text,parse_mode='Markdown')

    text = 'Выберите интересующий вас раздел:'
'''keyboardText = telebot.types.InlineKeyboardMarkup()
    callback_button0 = telebot.types.InlineKeyboardButton(text="Клиент", callback_data="cl")
    callback_button1 = telebot.types.InlineKeyboardButton(text="Гость", callback_data="g")
    keyboardText.add(callback_button0, callback_button1)
    bot.send_message(message.chat.id, text, reply_markup=keyboardText)
'''
if __name__ == '__main__':
    #try:
    bot.polling(none_stop=True)
    #except Exception:
    #    print('error Exception')

#YandexMetrica.setCustomAppVersion("1.13.2");
