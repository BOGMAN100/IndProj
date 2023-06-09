import os
import telebot
from dotenv import load_dotenv
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

load_dotenv()
# Создаем экземпляр бота
bot = telebot.TeleBot(os.getenv('TOKEN'))
page = 1
count = 3
stn = 1
# кнопки с предметами
sub_data = [InlineKeyboardButton(text='Математика', callback_data='math', ),
            InlineKeyboardButton(text='Русский', callback_data='rus'),
            InlineKeyboardButton(text='Физика', callback_data='phys'),
            InlineKeyboardButton(text='География', callback_data='geo'),
            InlineKeyboardButton(text='История', callback_data='his'),
            InlineKeyboardButton(text='Биология', callback_data='bio'),
            InlineKeyboardButton(text='Литература', callback_data='lit'),
            InlineKeyboardButton(text='Информатика', callback_data='inf'),
            InlineKeyboardButton(text='Обществознание', callback_data='ob'),
            InlineKeyboardButton(text='Химия', callback_data='him'),
            InlineKeyboardButton(text='Английский', callback_data='eng'),
            InlineKeyboardButton(text='Немецкий', callback_data='nem')]
sub_name = {'math': "математике", 'rus': "русскому", 'phys': "физике", 'geo': "географии", 'his': "истории",
            'bio': "биологии", 'lit': "литературе", 'inf': "информатике", 'ob': "обществознанию",
            'him': "химии", 'eng': "английскому", 'nem': "немецкому"}
file_name = {"kodif": "Кодификатор", "spec": "Спецификатор", "demo": "Демоверсия"}
cor = ('math', 'rus', 'phys', 'geo', 'his', 'bio', 'lit', 'inf', 'ob', 'him', 'eng', 'nem')
vector = ''


def start(m):
    global count
    global page
    global stn
    markup = InlineKeyboardMarkup()
    markup.add(sub_data[page - 1], sub_data[page])
    markup.add(sub_data[page + 1], sub_data[page + 2])
    markup.add(InlineKeyboardButton(text='Скрыть', callback_data='unseen'))
    markup.add(InlineKeyboardButton(text=f'<--- Назад', callback_data=f'back-page'),
               InlineKeyboardButton(text=f'{page}/{count}', callback_data=f' '),
               InlineKeyboardButton(text=f'Вперёд --->', callback_data=f'next-page')
               )
    if stn == 1:
        bot.send_message(m.from_user.id, f"По какому предмету нужен материал?\n            {exam_name}",
                         reply_markup=markup)  # не знаю почему наоборот, но да
        stn = 0
    elif stn == 0:
        bot.send_message(m.from_user.id, f"Готово!\nЧто-нибудь ещё?\n            {exam_name}", reply_markup=markup)
        stn = 1


# обработка действий кнопок
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    req = call.data.split('_')
    global count
    global page
    global vector
    global stn
    global sub
    global fil
    global exam_name
    global fo_func
    # Обработка кнопки - скрыть
    if req[0] == 'unseen':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        page = 1
    elif req[0] == 'exEGE':
        exam_name = "EGE"
        bot.delete_message(call.message.chat.id, call.message.message_id)
        start(fo_func)
    elif req[0] == "exOGE":
        exam_name = "OGE"
        bot.delete_message(call.message.chat.id, call.message.message_id)
        start(fo_func)

    elif any([req[0] == x for x in cor]):
        sub = req[0]  # название предмета для вывода
        vector = exam_name + '\\' + req[0] + '\\'  # в папке с каким предметом искать
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text="Демоверсия", callback_data='demo'),
                   InlineKeyboardButton(text="Спецификатор", callback_data="spec"),
                   InlineKeyboardButton(text="Кодификатор", callback_data="kodif"))
        markup.add(InlineKeyboardButton(text='Скрыть', callback_data='unseen'))
        markup.add(InlineKeyboardButton(text=f'Назад', callback_data=f'back-page'))
        bot.edit_message_text(f'Выбери тип документа: ', reply_markup=markup,
                              chat_id=call.message.chat.id,
                              message_id=call.message.message_id)
    elif any([req[0] == x for x in ['demo', 'spec', 'kodif']]):
        fil = req[0]  # тип документа для вывода
        bot.delete_message(call.message.chat.id, call.message.message_id)
        message = bot.send_message(call.message.chat.id, file_name[fil] + " " + exam_name + " по " + sub_name[sub]
                                   + " загружается...")
        # bot.send_message(call.message.chat.id, file_name[fil] + " по " + sub_name[sub] + " загружается...")
        path = vector + req[0] + ".pdf"
        path = path.replace("\\", "/")  # замена для правильной работы с докером
        bot.send_document(call.message.chat.id, open(path, 'rb'))
        page = 1
        stn = 0
        bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id,
                              text=file_name[fil] + " " + exam_name + " по " + sub_name[sub] + ".")
        start(call)

    # Обработка кнопки - вперед
    elif req[0] == 'next-page':
        if page < count:
            page = page + 1
            markup = InlineKeyboardMarkup()
            markup.add(sub_data[(1 + page * 4 - 4) - 1], sub_data[(1 + page * 4 - 4)])  # махинации с правильным
            # показом предметов
            markup.add(sub_data[(1 + page * 4 - 4) + 1], sub_data[(1 + page * 4 - 4) + 2])
            markup.add(InlineKeyboardButton(text='Скрыть', callback_data='unseen'))
            markup.add(InlineKeyboardButton(text=f'<--- Назад', callback_data=f'back-page'),
                       InlineKeyboardButton(text=f'{page}/{count}', callback_data=f' '),
                       InlineKeyboardButton(text=f'Вперёд --->', callback_data=f'next-page'))
            bot.edit_message_text(f'По какому предмету нужен материал?\n            {exam_name}', reply_markup=markup,
                                  chat_id=call.message.chat.id,
                                  message_id=call.message.message_id)


    # Обработка кнопки - назад
    elif req[0] == 'back-page':
        if page == 1:
            page += 1
        if page > 1:
            try:
                page = page - 1
                markup = InlineKeyboardMarkup()
                markup.add(sub_data[(1 + page * 4 - 4) - 1], sub_data[(1 + page * 4 - 4)])
                markup.add(sub_data[(1 + page * 4 - 4) + 1], sub_data[(1 + page * 4 - 4) + 2])
                markup.add(InlineKeyboardButton(text='Скрыть', callback_data='unseen'))
                markup.add(InlineKeyboardButton(text=f'<--- Назад', callback_data=f'back-page'),
                           InlineKeyboardButton(text=f'{page}/{count}', callback_data=f' '),
                           InlineKeyboardButton(text=f'Вперёд --->', callback_data=f'next-page'))
                bot.edit_message_text(f'По какому предмету нужен материал?\\            *{exam_name}*',
                                      reply_markup=markup,
                                      chat_id=call.message.chat.id,
                                      message_id=call.message.message_id)
            # убирает ошибку *сообщение не было изменено* ( в идеале перехватывать только ее )
            except:
                pass


# Обработчик входящих сообщений

@bot.message_handler(content_types=['text'])
def exam(ch):
    global fo_func
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text='ЕГЭ', callback_data='exEGE'))
    markup.add(InlineKeyboardButton(text='ОГЭ', callback_data='exOGE'))
    fo_func = ch
    bot.send_message(ch.from_user.id, "Привет!\nПо какому экзамену нужен материал?", reply_markup=markup)


if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True, interval=0)
        except:
            pass
