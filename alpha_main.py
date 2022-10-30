from sunau import AUDIO_FILE_ENCODING_ADPCM_G723_5
import telebot

import alpha_button
import alpha_database
import time

####---- подключение бота ----####

bot = telebot.TeleBot('5362600863:AAF3trI8XAgxWRklTWkTI6r8-DXoZDBQSZc')


####---- блок работы admin-панели ----####
@bot.message_handler(commands=['admin', 'hr'])
def start_message_admin(message):
    admin_id = 82798286

    if message.from_user.id == admin_id:
        bot.send_message(admin_id, 'Выберите команду: ', reply_markup=alpha_button.main_admin_buttons())
        bot.register_next_step_handler(message, get_main_admin_command)
    else:
        pass


def get_main_admin_command(message):
    command = message.text

    list_of_commands = ['Работа с файлами', 'Работа с сотрудниками', 'Подготовить рассылку']

    if command == list_of_commands:

        if command == 'Работа с файлами':
            bot.send_message(message.from_user.id, 'Что будем делать с фалами?', reply_markup=alpha_button.admin_buttons_for_file())
            bot.register_next_step_handler(message, get_file_admin_command)

        elif command == 'Работа с сотрудниками':
            bot.send_message(message.from_user.id, 'Выберите действие с сотрудниками', reply_markup=alpha_button.admin_buttons_for_staff())
            bot.register_next_step_handler(message, get_staff_admin_command)

        elif command == 'Подготовить рассылку':
            bot.send_message(message.from_user.id, 'Отправьте текст для рассылки всем сотрудникам')
            bot.register_next_step_handler(message, get_message_for_flood)

    else:
        bot.send_message(message.from_user.id, 'Введена неизвестная команда. Попробуйте снова или обратитесь к разработчику:\n\n @lagutinmichael')
        bot.register_next_step_handler(message, get_main_admin_command)

#обработчик админ-команд для сотрудников
def get_staff_admin_command(message):
    command = message.text

    list_of_command_for_files = ['Получение информации о всех сотрудниках', 'Добавление нового сотрудника', 'Изменить статус сотрудника', 'Удаление сотрудника', 'Изменить позицию сотрудника', 'Назад' ]
    
    if command in list_of_command_for_files:
        if command == 'Получение информации о всех сотрудниках':
            data = alpha_database.get_all_staff()
            bot.send_message(message.from_user.id, f'Данные о всех сотрудниках:\n\n {data}', reply_markup=alpha_button.main_admin_buttons())
            bot.register_next_step_handler(message, get_main_admin_command)

        elif command == 'Добавление нового сотрудника':
            bot.send_message(message.from_user.id, 'Введите Имя и Фамилию')
            bot.register_next_step_handler(message, get_new_name)

        elif command == 'Изменить статус сотрудника':
            bot.send_message(message.from_user.id, 'Отправьте id сотрудника, кому хотите изменить статус')
            bot.register_next_step_handler(message, get_id_for_change)

        elif command == 'Изменить позицию сотрудника':
            bot.send_message(message.from_user.id, 'Отправьте id сотрудика, чью позицию хотите изменить')
            bot.register_next_step_handler(message, get_id_for_change_position)

        elif command == 'Подготовить рассылку':
            bot.send_message(message.from_user.id, 'Отправьте единое сообщение с рассылкой')
            bot.register_next_step_handler(message, get_message_for_flood)

        elif command == 'Удаление сотрудника':
            bot.send_message(message.from_user.id, 'Введите id сотрудника, которого удалить из базы', reply_markup=alpha_button.cancel())
            bot.register_next_step_handler(message, get_id_for_delete)

        elif command == 'Назад':
            bot.send_message(message.from_user.id, 'Выберите действие', reply_markup=alpha_button.main_admin_buttons())
            bot.register_next_step_handler(message, get_main_admin_command)
    
    else:
        bot.send_message(message.from_user.id, 'Вы ввели несуществующую команду.\n\n Попробуйте воспользоваться кнопками')
        bot.register_next_step_handler(message, get_staff_admin_command)

####---- блок регистрации нового сотрудника ----####
#получение имя нового сотрудника
def get_new_name(message):
    name_staff = message.text

    bot.send_message(message.from_user.id, 'Введите должность/позицию')
    bot.register_next_step_handler(message, get_position, name_staff)

#получение позиции нового сотрудника
def get_position(message, name_staff):
    new_position = message.text

    bot.send_message(message.from_user.id, 'Введите статус сотрудинка (стажер, сотрудник, уволен)')
    bot.register_next_step_handler(message, get_status, name_staff, new_position)

#получение статуса и регистрация сотрудника в базе данных
def get_status(message, name_staff, new_position):
    new_status = message.text

    alpha_database.add_staff_admin(name_staff, new_position, new_status)
    bot.send_message(message.from_user.id, 'Сотрудник успешно добавлен в базу.\nОжидайте регистрации сотрудником ;)', reply_markup = alpha_button.main_admin_buttons())
    bot.register_next_step_handler(message, get_main_admin_command)



####----- блок изменения статуса сотрудника ----#####

#получить id сотрудника для команды (изменить статус сотрудника)
def get_id_for_change(message):
    staff_id = int(message.text)

    bot.send_message(message.from_user.id, 'Отправьте новый статус сотрудника')
    bot.register_next_step_handler(message, get_new_status, staff_id)

#получение нового статуса для команды (изменить статус сотрудника)
def get_new_status(message, staff_id):
    new_status = message.text
    telegram_id_staff = alpha_database.take_telegram_id(staff_id)
    
    alpha_database.change_status_staff(staff_id, new_status)
    bot.send_message(message.from_user.id, 'Статус успешно обновлен\n\nВыберите действие', reply_markup=alpha_button.main_admin_buttons())
    bot.send_message(telegram_id_staff, f'Ваш статус изменён.\nНовый статус: {new_status}')
    bot.register_next_step_handler(message, get_main_admin_command)


####---- блок измениния позиции сотрудника ----####

# получение id сотрудника
def get_id_for_change_position(message):
    staff_id_position = int(message.text)

    bot.send_message(message.from_user.id, 'Отправьте новый позицию сотрудника')
    bot.register_next_step_handler(message, get_new_position, staff_id_position)


# получение новой позиции для команды (изменить позицию сотрудника)
def get_new_position(message, staff_id_position):
    new_position = message.text

    telegram_id_staff = alpha_database.take_telegram_id(staff_id_position)

    alpha_database.change_position_staff(staff_id_position, new_position)
    bot.send_message(message.from_user.id, 'Статус сотрудника успешно изменён', reply_markup=alpha_button.main_admin_buttons())
    bot.send_message(telegram_id_staff, f'У вас новая позиция: {new_position}. Успехов!')
    bot.register_next_step_handler(message, get_main_admin_command)


####---- Блок удаления сотрудника из базы ----####
def get_id_for_delete(message):


    if message.text == 'Отмена':
        bot.send_message(message.from_user.id, 'Выберите действие', reply_markup=alpha_button.admin_buttons_for_staff())
        bot.register_next_step_handler(message, get_staff_admin_command)

    else:
        id = int(message.text)

        alpha_database.delete_staff(id)
        bot.send_message(message.from_user.id, 'Сотрудник удалён из базы\nВыберите следующее действие:',
                        reply_markup=alpha_button.main_admin_buttons())
        bot.register_next_step_handler(message, get_main_admin_command)

####---- Блок подготовки рассылок ----####
def get_message_for_flood(message):
    text = message.text

    all_telegram_id = alpha_database.take_all_telegram_id()

    for i in all_telegram_id:
        bot.send_message(i[0], f'Вам рассылка от HR {text}')
        time.sleep(0.5)
    
    bot.register_next_step_handler(message, get_main_admin_command)




##### ---- БЛОК РАБОТЫ ФАЙЛОВОЙ СИСТЕМЫ --- ####


# обработка команд с файлами 
def get_file_admin_command(message):
    command = message.text
    list_of_command_for_files = ['Загрузка нового файла', 'Изменнеие имени файла', 'Удаление файла', 'Посмотреть все файлы в базе', 'Назад']

    if command in list_of_command_for_files:

        if command == 'Загрузка нового файла':
            bot.send_message(message.from_user.id, 'Отправьте файл')
            bot.register_next_step_handler(message, get_telegram_id_file, command)

        elif command == 'Изменнеие имени файла':
            bot.send_message(message.form_user.id, 'Отправьте id файла')
            bot.register_next_step_handler(message, get_telegram_id_file, command)

        elif command == 'Удаление файла':
            bot.send_message(message.from_user.id, 'Введите id файла для удаления')
            bot.register_next_step_handler(message, get_id_file_to_delete)

        elif command == 'Посмотреть все файлы в базе':
            data = alpha_database.get_all_files()
            bot.send_message(message.from_user.id, f'Данные о файлах:\n\n {data}')
            bot.register_next_step_handler(message, get_file_admin_command)

        elif command == 'Назад':
            bot.send_message(message.from_user.id, 'Выберите действие', reply_markup=alpha_button.main_admin_buttons())
            bot.register_next_step_handler(message, get_main_admin_command)

    else:
        bot.send_message(message.from_user.id, 'Вы ввели несуществующую команду, попробуйте еще раз'
                                                '\n\n\nПопробуйте воспользоваться кнопками')
        bot.register_next_step_handler(message, get_file_admin_command)

# - получение  - #
#получение id файла
def get_telegram_id_file(message, command):
    if command == 'Загрузка нового файла':
        tg_id_file = message.document.file_id
        bot.send_message(message.from_user.id, 'Отправьте название файла')
        bot.register_next_step_handler(message, get_name_file, tg_id_file)

    elif command == 'Изменнеие имени файла':
        tg_id_file = int(message.text)
        bot.send_message(message.from_user.id, 'Отправьте новое имя файла')
        bot.register_next_step_handler(message, get_new_file_name, tg_id_file)

#получение имени файла при первом добавлении файла в базу
def get_name_file(message, tg_id_file):
    file_name = message.text

    alpha_database.register_new_file(file_name, tg_id_file)
    bot.send_message(message.from_user.id, 'Файл успешно зарегестрирван в базе.\nВыберите следующее действие')
    bot.register_next_step_handler(message, get_main_admin_command)


#получение нового имени файла для изменения его в базе
def get_new_file_name(message, tg_id_file):
    new_name = message.text

    alpha_database.change_file_name(tg_id_file, new_name)
    bot.send_message(message.from_user.id, 'Выберите следующее действие', reply_markup=alpha_button.main_admin_buttons())
    bot.register_next_step_handler(message, get_main_admin_command)

#удаление файла из базы по id
def get_id_file_to_delete(message):
    file_id = int(message.text)

    alpha_database.delete_file(file_id)
    bot.send_message(message.from_user.id, 'Выберите следующее действие', reply_markup=alpha_button.main_admin_buttons())
    bot.register_next_step_handler(message, get_main_admin_command)


####################################
#----------------------------------#
#----------------------------------#
####################################



##### ---- БЛОК РАБОТЫ КЛИЕНТСКОЙ СТОРОНЫ --- ####


@bot.message_handler(commands=['start'])
def start_message_staff(message):
    
    checker_telegram_id = alpha_database.check_staff_telegram_id(message.from_user.id)
    if checker_telegram_id:
        bot.send_message(message.from_user.id, 
                         text = 'Выбереите нужный для вас пункт', 
                         reply_markup=alpha_button.main_staff_buttons())
        bot.register_next_step_handler(message, get_main_staff_command)

    else: 
        bot.send_message(message.from_user.id, 'Отправьте свой ID для проверки')
        bot.register_next_step_handler(message, check_data)

# провека пользователя на присутсвие в базе данных 
def check_data(message):
    id_check = int(message.text)
    checker = alpha_database.check_staff(message.text)
    
    if alpha_database.take_telegram_id(id_check) != 'NULL':
        bot.send_message(message.from_user.id, 'Этот id пользователя занят. Cвяжитесь с HR')
        bot.register_next_step_handler(message, start_message_staff)
    elif checker:
        bot.send_message(message.from_user.id, 'Добро пожаловать в HR-бот ALPHA\n \nОтправьте свой номер для регистрации в базе',
                                                        reply_markup=alpha_button.send_number())
        bot.register_next_step_handler(message, get_number, id_check)
    else:
        bot.send_message(bot.from_user.id, 'Вас нет в базе сотрудников. Свяжитесь с HR-ALPHA')


## блок первой регистрации сотрудника после добавления его в базу HR-орм
# получение имени пользователя
def get_number(message, id_check):
    phone_number = message.contact.phone_number

    bot.send_message(message.from_user.id, 'Отправьте дату своего рождения в формате "гггг-мм-дд"')
    bot.register_next_step_handler(message, get_data_birth, id_check, phone_number)

#получения даты рождения и регистрация нового сотрудника в базе
def get_data_birth(message, id_check, phone_number):
    data_bitrh = message.text

    alpha_database.add_staff_user(id_check, message.from_user.id, phone_number, data_bitrh)
    bot.send_message(message.from_user.id, 'Вы успешно добавлены зарегестрировались\nВвыберите действие', reply_markup=alpha_button.main_staff_buttons())
    bot.register_next_step_handler(message, get_main_staff_command)

# обработчик команд пользователя
def get_main_staff_command(message):
    command = message.text

    list_of_commands = ['Скачать файл', 'Получить список файлов', 'Связаться с HR-менеджером', 'Получить информацию о сотрудниках']

    if command == list_of_commands:

        if command == 'Скачать файл':
            bot.send_message(message.from_user.id, 'Отпавьте id файла')
            bot.register_next_step_handler(message, get_file)

        elif command == 'Получить список файлов':
            data = alpha_database.get_all_files()
            bot.send_message(message.from_user.id, data)
            bot.register_next_step_handler(message, get_main_admin_command)

        elif command == 'Связаться с HR-менеджером':
            bot.send_message(message.from_user.id, 'Контактные данные HR-менеджмера:\nUsername: @hr_alphaedu')
            bot.register_next_step_handler(message.from_user.id, get_main_staff_command)

        elif command == 'Получить информацию о сотрудниках':
            data = alpha_database.get_all_staff()

            bot.send_message(message.from_user.id, data)
            bot.register_next_step_handler(message, get_main_admin_command)

    else:
        bot.send_message(message.from_user.id, 'Неизвестный запрос. Воспользуйтесь кнопкой', reply_markup=alpha_button.main_staff_buttons())
        bot.register_next_step_handler(message, get_main_staff_command)
        

def get_file(message):
    id = int(message.text)

    tg_file_id = alpha_database.get_telegram_file_id(id)

    bot.send_document(message.from_user.id, tg_file_id)
    bot.register_next_step_handler(message, get_main_staff_command)

bot.polling()

