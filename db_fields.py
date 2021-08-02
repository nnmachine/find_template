from tinydb import TinyDB, Query

#Поля базы данных
db = TinyDB('DBTemplates.json')
print(db.all())
