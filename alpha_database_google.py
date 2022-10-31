import gspread
from oauth2client.service_account import ServiceAccountCredentials


#P.S. все переоменные назвываем рандомно, но чтоб было удобно, даём правильные имена
#обязательные параметры
scope = ["https://spreadsheets.google.com/feeds", #сами таблицы
         "https://www.googleapis.com/auth/spreadsheets",#АПИ для работы с таблицей
         "https://www.googleapis.com/auth/drive.file", #коннект к гугл-диску
         "https://www.googleapis.com/auth/drive"] #АПИ для авторизации к гугл диску
        
#подключаем необходимые ключи
creads = ServiceAccountCredentials.from_json_keyfile_name("alpha_hr_bot_credits.json", scope) #в скобочках указываем название файла из json

#авторизируемся под своим аккаунтом из ключа
client = gspread.authorize(creads) #к нему будем обращаться в дальнейшем, т.к. он идёт как подключение

##############
#конец основной части. буду называть её header


### ---- БЛОК РАБОТЫ С СОТРУДНИКАМИ --------####

#Подключение к таблице, которую мы сами до этого создали
table = client.open('ALPHA_data_base') # изменить название на своё
#подключили листы из таблицы
staff_list = table.worksheet('staff') # изменить название листа на своё
file_list = table.worksheet('files')

#добавление нового сотрудника в базу (админом) - имя, должность, позиция
def add_admin_staff(id, name, position, status):
    staff_list.append_row([id, '', name, '', '', position, status])

#добавление информации сотрудником
def add_info_from_staff(id, date_birth, number, telegram_id):
    cell = staff_list.find(str(id))
    staff_list.update_cell(cell.row, 2, telegram_id)
    staff_list.update_cell(cell.row, 5, date_birth) #обновление ячейки с днём рождения
    staff_list.update_cell(cell.row, 4, number) #обновление ячейки с номером
   

# изменение статуса сотрудника (сотрудник\стажер)
def change_status_staff(id, status):
    cell = staff_list.find(str(id))
    staff_list.update_cell(cell.row, 7, status)

# изменение должности сотрудника 
def change_position_staff(id, position):
    cell = staff_list.find(str(id))
    staff_list.update_cell(cell.row, 7, position)

# получение всех telegram_id для рассылок
def get_all_telegram_id():
    values= staff_list.col_values(2)
    values = values[1:]
    value_list = []
    for i in values:
        value_list.append(int(i))
    return value_list

#получение информации о всех сотрудниках
def get_all_info_staff():
    data = staff_list.get_all_values()

    id_line = ''
    name_line = ''
    number_line = ''
    position_line = ''
    birthday_line = ''
    status_line = ''
    full_line = ''

    for i in range(1,len(data)):
        id_line = f'{data[i][0]} | '
        name_line = f'{data[i][2]} | '
        number_line = f'{data[i][3]} | '
        position_line = f'{data[i][4]} |'
        birthday_line = f'{data[i][5]} |'
        status_line = f'{data[i][6]} |'


        full_line += f'{id_line} {name_line} {number_line} {position_line} {birthday_line} {status_line} \n -----------------------\n'

    return full_line


#проверка наличия id при регистрации
def check_all_id(id):
    values = staff_list.col_values(1)
    
    if str(id) in values:
        return True
    else:
        return False

#проверка наличия telegram_id в базе (во время работы)
def check_all_telegram_id(telegram_id):
    values = staff_list.col_values(2)
    
    if str(telegram_id) in values:
        return True
    else:
        return False

# получение telegram-id из id для оповещения сотрудника об измениях
def get_telegram_id(id):
    cell = staff_list.find(str(id))
    value = staff_list.cell(cell.row, 2).value
    
    return value

# удаление сотрудника из базы по id
def delete_staff(id):
    cell = staff_list.find(str(id))
    staff_list.update_cell(cell.row, cell.col, '')
    staff_list.update_cell(cell.row, cell.col+1, '')



### ------ БЛОК РАБОТЫ С ФАЙЛАМИ --------###

#добавление нового файла в таблицу
def add_new_file(id, telegram_id_file, file_name):
    file_list.append_row([id, file_name, telegram_id_file])

# получение telegram_file_id по id
def get_telegram_file_id(id):
    cell = file_list.find(str(id))
    telegram_file_id = file_list.cell(cell.row, 3).value

    return telegram_file_id

# изменение имени файла по id
def change_file_name(id, name):
    cell = file_list.find(str(id))
    file_list.update_cell(cell.row, 2, name)

# удаление файла из таблицы
def delete_file(id):
    cell = file_list.find(str(id))
    file_list.update_cell(cell.row, 1, '')
    file_list.update_cell(cell.row, 2, '')
    file_list.update_cell(cell.row, 3, '')

# получение всех данных о файлах
def get_all_info_files():
    data = file_list.get_all_values()

    id_line = ''
    name_line = ''

    full_line = ''

    for i in range(1,len(data)):
        id_line = f'{data[i][0]} | '
        name_line = f'{data[i][1]} | '

        full_line += f'{id_line} {name_line} \n'

    return full_line

# получение списка id файлов (чтоб не вводили несуществующие)
def check_file_id(id):
    id_list = file_list.col_values(0)

    if id in id_list:
        return True
    else:
        return False