import sqlite3
from datetime import datetime


#подключаем sql
connection = sqlite3.connect('alpha_hr_test.db')
sql = connection.cursor()


##генерируем таблицы
# табилца с базовыми данными о сотруднике
sql.execute('CREATE TABLE IF NOT EXISTS staff (id INTEGER PRIMARY KEY AUTOINCREMENT, telegram_id INTEGER, name TEXT, '
            'number TEXT, position TEXT, date_birthday TEXT, status TEXT)')
# таблица с файлами (id в таблице, id файла в тг,  название файла)
sql.execute('CREATE TABLE IF NOT EXISTS files (id INTEGER PRIMARY KEY AUTOINCREMENT, id_file_message INTEGER, name TEXT)')


# дата рождения в формате "гггг-мм-дд"
# статусы /стажер/сотрудник/уволен
# номер телефона в формате 998946412299
# при удалении сотрудника из базы данных - id меняются (нужно перепроверять)



# фунции работы с таблицей

# проверка сотрудника на наличие в таблице
def check_staff(id):
    connection = sqlite3.connect('alpha_hr_test.db')
    sql = connection.cursor()

    id_check = sql.execute('SELECT name FROM staff WHERE id = ?', (id)).fetchone()

    if id_check:
        #status = sql.execute('SELECT status FROM staff WHERE id = ?', (id)).fetchone()
        return True

    else:
        return False

#проверка сотрудника на наличие в бд по телеграм id для команды /start
def check_staff_telegram_id(telegram_id):
    connection = sqlite3.connect('alpha_hr_test.db')
    sql = connection.cursor()

    id_check = sql.execute('SELECT name FROM staff WHERE telegram_id = ?', (telegram_id,)).fetchone()

    if id_check:
        status = sql.execute('SELECT status FROM staff WHERE id = ?', (telegram_id,)).fetchone()
        return True

    else:
        return False

# функция на добавление сотрудника в базу
def add_staff_admin(name, position, status):
    connection = sqlite3.connect('alpha_hr_test.db')
    sql = connection.cursor()

    sql.execute('INSERT INTO staff (name, position, status) VALUES (?,?,?)', (name, position, status))
    
    connection.commit()

# функция для регистрация сотрудника в боте (чекинг)
def add_staff_user(id, telegram_id, number, date):
    connection = sqlite3.connect('alpha_hr_test.db')
    sql = connection.cursor()
    sql.execute('UPDATE staff SET telegram_id = ? WHERE id = ?', (telegram_id, id))
    sql.execute('UPDATE staff SET number = ? WHERE id = ?', (number, id))
    sql.execute('UPDATE staff SET date_birthday = ? WHERE id = ?', (date, id))
    #sql.execute('INSERT INTO staff (telegram_id, number, date_birthday) VALUES (?,?,?) WHERE id = ?', (telegram_id, number, date, id))

    connection.commit()

# функция для изменения статуса сотрудника
def change_status_staff(id, status):
    connection = sqlite3.connect('alpha_hr_test.db')
    sql = connection.cursor()

    sql.execute('UPDATE staff SET status = ? WHERE id = ?', (status, id))

    connection.commit()

# функция для изменения позиции сотрудника
def change_position_staff(id, position):
    connection = sqlite3.connect('alpha_hr_test.db')
    sql = connection.cursor()

    sql.execute('UPDATE staff SET position = ? WHERE id = ?', (position, id))

    connection.commit()

# Удаление сотрудника из базы данных:
def delete_staff(id):
    connection = sqlite3.connect('alpha_hr_test.db')
    sql = connection.cursor()

    sql.execute('DELETE FROM staff WHERE id = ?', (id))

    connection.commit()

# Получение информации о всех сотрудниках:
def get_all_staff():
    connection = sqlite3.connect('alpha_hr_test.db')
    sql = connection.cursor()

    id_line = ''
    name_line = ''
    number_line = ''
    position_line = ''
    birthday_line = ''
    status_line = ''
    full_line = ''

    all_staff = sql.execute('SELECT * FROM staff')
    #print(all_staff.fetchall())
    for staff in all_staff:
        id_line = f'{str(staff[0])} | '
        name_line = f'{str(staff[2])} | '
        number_line = f'{str(staff[3])} | '
        position_line = f'{str(staff[4])} |'
        birthday_line = f'{str(staff[5])} |'
        status_line = f'{str(staff[6])} |'

        full_line += f'{id_line} {name_line} {number_line} {position_line} {birthday_line} {status_line} \n -----------------------\n'
                        

    return full_line


# получение telegram_id через id
def take_telegram_id(id):
    connection = sqlite3.connect('alpha_hr_test.db')
    sql = connection.cursor()

    telegram_id = sql.execute('SELECT telegram_id FROM staff WHERE id = ?', (id,)).fetchone()[0]
    #telegram_id = telegram_id[0]
    return telegram_id


# получение всех telegram_id для рассылок
def take_all_telegram_id():
    connection = sqlite3.connect('alpha_hr_test.db')
    sql = connection.cursor()

    all_telegram_id = sql.execute('SELECT telegram_id FROM staff').fetchall()

    return all_telegram_id


##--- РАБОТА С ТАБЛИЦЕЙ ФАЙЛОВ ---###

# добавление нового файла в базу
def register_new_file(name, id_file_message):
    connection = sqlite3.connect('alpha_hr_test.db')
    sql = connection.cursor()

    sql.execute('INSERT INTO files (id_file_message, name) VALUES (?,?)', (id_file_message, name,))
    
    connection.commit()

# получение telegram_id_file по id
def get_telegram_file_id(id):
    connection = sqlite3.connect('alpha_hr_test.db')
    sql = connection.cursor()

    telegram_fire_id = sql.execute('SELECT id_file_message FROM files WHERE id = ?', (id,)).fetchone()[0]

    return telegram_fire_id

# изменение имени файла
def change_file_name(id, new_name):
    connection = sqlite3.connect('alpha_hr_test.db')
    sql = connection.cursor()

    sql.execute('UPDATE files SET name = ? WHERE id = ?', (new_name, id,))

    connection.commit()

# удаление файла из таблицы
def delete_file(id):
    connection = sqlite3.connect('alpha_hr_test.db')
    sql = connection.cursor()

    sql.execute('DELETE FROM files WHERE id = ?', (id,))
    connection.commit()

# получение всех данных о файлах
def get_all_files():
    connection = sqlite3.connect('alpha_hr_test.db')
    sql = connection.cursor()

    id_line = ''
    name_line = ''

    full_line = ''

    all_staff = sql.execute('SELECT * FROM files')

    for staff in all_staff:
        id_line = f'{str(staff[0])} | '
        name_line = f'{str(staff[2])} | '

        full_line += f'{id_line} {name_line} \n'

    return full_line

# получение списка id файлов (чтоб не вводили не существующие)
def get_id_files():
    connection = sqlite3.connect('alpha_hr_test.db')
    sql = connection.cursor()

    all_id = sql.execute('SELECT id FROM files')

    return all_id

print(get_all_files())