from tinydb import TinyDB, Query

#Очистка базы данных
db = TinyDB('DBTemplates.json')
db.truncate()
