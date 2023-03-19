import os
import telebot
from dotenv import load_dotenv
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# import PyPDF2

load_dotenv()
# Создаем экземпляр бота
bot = telebot.TeleBot(os.getenv('TOKEN'))
page = 1
count = 3
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
cor = ('math', 'rus', 'phys', 'geo', 'his', 'bio', 'lit', 'inf', 'ob', 'him', 'eng', 'nem')
vector = ''


# обработка действий кнопок
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    req = call.data.split('_')
    global count
    global page
    global vector
    # Обработка кнопки - скрыть
    if req[0] == 'unseen':
        bot.delete_message(call.message.chat.id, call.message.message_id)

    elif any([req[0] == x for x in cor]):
        vector = 'OGE\\' + req[0] + '\\'  # в папке с каким предметом искать
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text="Демоверсия", callback_data='demo'),
                   InlineKeyboardButton(text="Спецификатор", callback_data="spec"),
                   InlineKeyboardButton(text="Кодификатор", callback_data="kodif"))
        markup.add(InlineKeyboardButton(text='Скрыть', callback_data='unseen'))
        bot.edit_message_text(f'Выбери тип документа: ', reply_markup=markup,
                              chat_id=call.message.chat.id,
                              message_id=call.message.message_id)
    elif any([req[0] == x for x in ['demo', 'spec', 'kodif']]):
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "Документ загружается...")
        path = vector + req[0] + ".pdf"
        path = path.replace("\\", "/")
        bot.send_document(call.message.chat.id, open(path, 'rb'))

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
            bot.edit_message_text(f'По какому предмету нужен материал?', reply_markup=markup,
                                  chat_id=call.message.chat.id,
                                  message_id=call.message.message_id)

    # Обработка кнопки - назад
    elif req[0] == 'back-page':
        if page > 1:
            page = page - 1
            markup = InlineKeyboardMarkup()
            markup.add(sub_data[(1 + page * 4 - 4) - 1], sub_data[(1 + page * 4 - 4)])
            markup.add(sub_data[(1 + page * 4 - 4) + 1], sub_data[(1 + page * 4 - 4) + 2])
            markup.add(InlineKeyboardButton(text='Скрыть', callback_data='unseen'))
            markup.add(InlineKeyboardButton(text=f'<--- Назад', callback_data=f'back-page'),
                       InlineKeyboardButton(text=f'{page}/{count}', callback_data=f' '),
                       InlineKeyboardButton(text=f'Вперёд --->', callback_data=f'next-page'))
            bot.edit_message_text(f'По какому предмету нужен материал?', reply_markup=markup,
                                  chat_id=call.message.chat.id,
                                  message_id=call.message.message_id)


# Обработчик входящих сообщений
@bot.message_handler(content_types=['text'])
def start(m):
    global count
    global page
    markup = InlineKeyboardMarkup()
    markup.add(sub_data[page - 1], sub_data[page])
    markup.add(sub_data[page + 1], sub_data[page + 2])
    markup.add(InlineKeyboardButton(text='Скрыть', callback_data='unseen'))
    markup.add(InlineKeyboardButton(text=f'<--- Назад', callback_data=f'back-page'),
               InlineKeyboardButton(text=f'{page}/{count}', callback_data=f' '),
               InlineKeyboardButton(text=f'Вперёд --->', callback_data=f'next-page')
               )
    bot.send_message(m.from_user.id, "Привет!\nПо какому предмету нужен материал?", reply_markup=markup)


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)