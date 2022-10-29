from telebot import types

#основные кнопки админа

def main_admin_buttons():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    button_1 = types.KeyboardButton('Работа с файлами')
    button_2 = types.KeyboardButton('Работа с сотрудниками')
    button_3 = types.KeyboardButton('Подготовить рассылку')

    kb.row(button_1, button_2)
    kb.row(button_3)

    return kb



def admin_buttons_for_staff():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    button_1 = types.KeyboardButton('Получение информации о всех сотрудниках')
    button_2 = types.KeyboardButton('Добавление нового сотрудника')
    button_3 = types.KeyboardButton('Изменить статус сотрудника')
    button_4 = types.KeyboardButton('Удаление сотрудника')
    button_5 = types.KeyboardButton('Изменить позицию сотрудника')
    button_6 = types.KeyboardButton('Назад')
    ## добавить кнопку для работы с файлами

    kb.row(button_1)
    kb.row(button_2, button_3)
    kb.row(button_4, button_5)
    kb.row(button_6)
    
    return kb

def admin_buttons_for_file():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    button_1 = types.KeyboardButton('Загрузка нового файла')
    button_2 = types.KeyboardButton('Изменнеие имени файла')
    button_3 = types.KeyboardButton('Удаление файла')
    button_4 = types.KeyboardButton('Посмотреть все файлы в базе')
    button_5 = types.KeyboardButton('Назад')
    ## добавить кнопку для работы с файлами

    kb.row(button_1)
    kb.row(button_2, button_3)
    kb.row(button_4)
    kb.row(button_5)
    
    return kb

def send_number():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)

    button_1 = types.KeyboardButton('Отправить номер', request_contact=True)
    kb.add(button_1)

    return kb

## добавить кнопки для добавления файлов


def main_staff_buttons():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    button_1 = types.KeyboardButton('Получить список файлов')
    button_2 = types.KeyboardButton('Скачать файл')
    button_3 = types.KeyboardButton('Связаться с HR-менеджером')
    button_4 = types.KeyboardButton('Получить информацию о сотрудниках')

    kb.add(button_1, button_2)
    kb.row(button_4)
    kb.row(button_3)
    

    return kb

def cancel():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)

    button_1 = types.KeyboardButton('Отмена')

    kb.add(button_1)

    return kb