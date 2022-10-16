# from django import template
# from task_manager.statuses.models import Status
# 
# 
# register = template.Library()
# 
# 
# @register.simple_tag()
# def get_statuses():
#     return Status.objects.all()


import sqlite3

def delete_record():
    try:
        sqlite_connection = sqlite3.connect('/home/victor/python/python-project-52/db.sqlite3')
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")

        sql_delete_query = """SELECT * FROM TABLE user_user"""
        
        cursor.execute(sql_delete_query)
        sqlite_connection.commit()
        print("Запись успешно удалена")
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")

#delete_record()

